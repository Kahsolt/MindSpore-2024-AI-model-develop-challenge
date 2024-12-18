# Copyright 2023 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""LLaMA Model Layers' APIs."""

import sys
from enum import Enum
import numpy as np

from mindspore.common.tensor import Tensor
from mindspore.common.parameter import Parameter
from mindspore import nn
import mindspore.common.dtype as mstype
from mindspore.ops import operations as P
from mindspore.ops import functional as F
from mindspore.nn.cell import Cell

try:
    from mindspore._checkparam import Validator
except ImportError:
    import mindspore._checkparam as Validator
from mindspore import log as logger
from mindspore.common.initializer import initializer
from mindspore.parallel._utils import _get_parallel_mode
from mindspore.context import ParallelMode
from mindformers.version_control import check_valid_big_kernel
from mindformers.modules.transformer.op_parallel_config import default_dpmp_config
from mindformers.modules.layers import Linear, _check_input_dtype, _args_type_validator_check, \
    _valid_value_checks
from mindformers.tools.logger import _LogActionOnce
from mindformers.version_control import check_rmsnorm_big_kernel_valid

IS_WIN = sys.platform == 'win32'


class SeqExtendMethod(Enum):
    """Stores the acceptable string identifiers for seq length extend method"""
    PI = "PI"
    NTK = "NTK"
    NONE = "None"


class LlamaSiLU(Cell):
    r"""
    A self-defined SwiGlu.

        Inputs:
            - **x** (Tensor) - Tensor.

        Outputs:
            Tensor. x = silu(x).
    """

    def __init__(self):
        super().__init__()
        if check_valid_big_kernel():
            # pylint: disable=W0212
            self.silu = P._inner_ops.SiLU()
            self.self_define = False
        else:
            self.sigmoid = P.Sigmoid()
            self.mul = P.Mul()
            self.silu = self._self_silu
            self.self_define = True

    def _self_silu(self, x):
        return self.mul(x, self.sigmoid(x))

    def construct(self, x):
        return self.silu(x)

    def shard(self, strategy):
        if self.self_define:
            self.sigmoid.shard(strategy)
            self.mul.shard((strategy[0], strategy[0]))
        else:
            self.silu.shard(strategy)

    def activation_shard(self, strategy):
        # activation_shard is the api called by moe [dp_group, expert_dim, capacity, ffn_hidden]
        if hasattr(strategy, "expert_parallel"):
            moe_strategy = ((strategy.data_parallel, strategy.expert_parallel, 1, strategy.model_parallel),)
            self.shard(moe_strategy)


class FreqsMgr(Cell):
    r"""freqs_cis manager."""

    def __init__(self,
                 head_dim,
                 seq_length=None,
                 max_position_embedding=4096,
                 rotary_dtype=mstype.float16,
                 theta=10000,
                 scaling_factor=1.0,
                 extend_method=SeqExtendMethod.NONE.value):
        super().__init__()
        if seq_length is not None and seq_length > max_position_embedding:
            max_position_embedding = seq_length
        if extend_method == SeqExtendMethod.NTK.value:
            theta *= scaling_factor
        freqs_base = np.arange(0, head_dim, 2)[: (head_dim // 2)].astype(np.float32)  # (head_dim // 2, )
        freqs = 1.0 / (theta ** (freqs_base / head_dim))  # (head_dim // 2, )
        if extend_method == SeqExtendMethod.PI.value:
            t = np.arange(0, max_position_embedding / scaling_factor, 1 / scaling_factor).astype(np.float32)
        else:
            t = np.arange(0, max_position_embedding, 1).astype(np.float32)
        freqs = np.outer(t, freqs)  # (max_position_embedding, head_dim // 2)
        emb = np.concatenate((freqs, freqs), axis=-1)
        freqs_cos = np.cos(emb)  # (seq_len, head_dim)
        freqs_sin = np.sin(emb)  # (seq_len, head_dim)
        swap_mask = FreqsMgr.get_swap_mask(head_dim)

        self.head_dim = head_dim
        self.freqs_cos = Tensor(freqs_cos, dtype=rotary_dtype)
        self.freqs_sin = Tensor(freqs_sin, dtype=rotary_dtype)
        self.swap_mask = Tensor(swap_mask, dtype=rotary_dtype)

        self.slice = P.StridedSlice().shard(((1, 1),))
        self.gather = P.Gather().shard(((1, 1), (1,)))
        self.tile = P.Tile().shard(((1, 1),))

    def construct(self, seq_length):
        freqs_cos = self.slice(self.freqs_cos, (0, 0), (seq_length, self.head_dim), (1, 1))
        freqs_sin = self.slice(self.freqs_sin, (0, 0), (seq_length, self.head_dim), (1, 1))
        return freqs_cos, freqs_sin, self.swap_mask

    def prefill(self, batch_size, seq_length):
        freqs_cos = self.tile(self.slice(self.freqs_cos, (0, 0), (seq_length, self.head_dim), (1, 1)), (batch_size, 1))
        freqs_sin = self.tile(self.slice(self.freqs_sin, (0, 0), (seq_length, self.head_dim), (1, 1)), (batch_size, 1))
        return freqs_cos, freqs_sin, self.swap_mask

    def increment(self, batch_valid_length):
        freqs_cos = self.gather(self.freqs_cos, batch_valid_length, 0)
        freqs_sin = self.gather(self.freqs_sin, batch_valid_length, 0)
        return freqs_cos, freqs_sin, self.swap_mask

    @staticmethod
    def get_swap_mask(head_dim):
        """Swap matrix"""
        zero_block = np.zeros((head_dim // 2, head_dim // 2), dtype=np.float32)
        id_block = np.identity(head_dim // 2, dtype=np.float32)
        return np.block([[zero_block, id_block], [-id_block, zero_block]])


class LlamaRotaryEmbedding(Cell):
    r"""
    Rotary Position Embedding.

    Args:
            - **head_dim** (int): The dim of multi head attention.
            - **compute_dtype** (mstype): The compute type, default mstype.float16.
            - **parallel_config** (dict): - Parallel Config.
    Inputs:
            - **x** (Tensor) - Tensor of shape :math:`(batch, seq\_length, hidden\_size)`.

    Outputs:
            Tensor of shape :math:`(batch, seq_length, hidden_size)`.
    """

    def __init__(self, head_dim=128, compute_dtype=mstype.float32, use_rope_slice=False):
        super().__init__(auto_prefix=False)
        self.half_head_dim = head_dim // 2
        self.head_dim = head_dim
        self.dtype = compute_dtype
        self.use_rope_slice = use_rope_slice
        self.is_first_iteration = True

        self.add = P.Add()
        self.bmm_swap = P.BatchMatMul()
        self.mul = P.Mul()
        self.mul_inc = P.Mul()
        self.neg = P.Neg()
        self.slice = P.StridedSlice()
        self.concat = P.Concat(axis=-1)
        self.shape = P.Shape()

    def rotate_half(self, x, swap_mask):
        # [bs, n_head/n_kv_head, seq/1, head_dim], [head_dim, head_dim]
        if IS_WIN:
            B, H, S, D = x.shape
            x = x.reshape([B * H * S, D])
            x = self.bmm_swap(x, swap_mask)
            x = x.reshape([B, H, S, D])
        else:
            x = self.bmm_swap(x, swap_mask)
        return x

    def slice_half(self, x):
        bs, n_head, seq, _ = self.shape(x)
        x1 = self.slice(x, (0, 0, 0, 0), (bs, n_head, seq, self.half_head_dim), (1, 1, 1, 1))
        x2 = self.slice(x, (0, 0, 0, self.half_head_dim), (bs, n_head, seq, self.head_dim), (1, 1, 1, 1))
        x = self.concat((self.neg(x2), x1))
        return x

    #@profile
    def construct(self, xq: Tensor, xk: Tensor, freqs_cis):
        """Forward of rotary position embedding."""
        original_type = xq.dtype
        # TIMEIT: 1.3% (CPU)
        xq = self.cast(xq, self.dtype)
        # TIMEIT: 1.1% (CPU)
        xk = self.cast(xk, self.dtype)
        # xq, xk: [bs, n_head/n_kv_head, seq/1, head_dim]
        freqs_cos, freqs_sin, swap_mask = freqs_cis
        mul = self.mul if self.is_first_iteration else self.mul_inc
        if self.use_rope_slice:
            xq_out = self.add(mul(xq, freqs_cos), mul(self.slice_half(xq), freqs_sin))
            xk_out = self.add(mul(xk, freqs_cos), mul(self.slice_half(xk), freqs_sin))
        else:       # <- this way
            # TIMEIT: 53.3% (CPU)
            xq_out = self.add(mul(xq, freqs_cos), mul(self.rotate_half(xq, swap_mask), freqs_sin))
            # TIMEIT: 40.7% (CPU)
            xk_out = self.add(mul(xk, freqs_cos), mul(self.rotate_half(xk, swap_mask), freqs_sin))

        # TIMEIT: 2.0% (CPU)
        xq_out = self.cast(xq_out, original_type)
        # TIMEIT: 1.6% (CPU)
        xk_out = self.cast(xk_out, original_type)
        return xq_out, xk_out

    def shard(self, strategy_in):
        self.add.shard((strategy_in, strategy_in))
        self.bmm_swap.shard((strategy_in, (1, 1)))
        self.mul.shard((strategy_in, (1, 1)))
        self.mul_inc.shard((strategy_in, (strategy_in[0], 1, 1, 1)))
        self.neg.shard((strategy_in,))
        self.slice.shard((strategy_in,))
        self.concat.shard((strategy_in, strategy_in))


class LlamaEmbedding(Cell):
    """
    Embedding Layer.

    Args:
            - **vocab_size** (int): Size of the dictionary of embeddings.
            - **embedding_size** (int): The size of each embedding vector.
            - **param_init_type** (mstype): The param init type, default mstype.float32.
            - **parallel_config** (TransformerOpParallelConfig): The parallel config of network. Default
                `default_embedding_parallel_config`, an instance of `EmbeddingOpParallelConfig` with default args.
            - **param_init** (Union[Tensor, str, Initializer, numbers.Number]): Initializer for the embedding_table.
                Refer to class `initializer` for the values of string when a string
                is specified. Default: 'normal'.
    Inputs:
            - **input_ids** (Tensor) - The tokenized inputs with datatype int32 with shape (batch_size, seq_length)

    Outputs:
            - **output** (Tensor) - The embedding vector for the input with shape (batch_size,
              seq_length, embedding_size).
    """

    @_LogActionOnce(m_logger=logger, key='Embedding',
                    no_warning=_get_parallel_mode() in (ParallelMode.STAND_ALONE,))
    @_args_type_validator_check(vocab_table_size=Validator.check_positive_int,
                                embedding_size=Validator.check_positive_int)
    def __init__(self, vocab_table_size, embedding_size, param_init_type=mstype.float32, param_init='normal',
                 parallel_optimizer=False):
        super().__init__()
        self.vocab_table_size = vocab_table_size
        self.embedding_size = embedding_size
        self.embedding_weight = Parameter(
            initializer(param_init, [self.vocab_table_size, self.embedding_size], dtype=param_init_type),
            name='embedding_weight', parallel_optimizer=parallel_optimizer)
        self.gather = P.Gather()

    def construct(self, input_ids):
        """Forward of vocab embedding."""
        _check_input_dtype(F.dtype(input_ids), "input_ids", [mstype.int32, mstype.int64], self.cls_name)
        output = self.gather(self.embedding_weight, input_ids, 0)
        return output

    def shard(self, parallel_config):
        """sharding for embedding"""
        dp = parallel_config.data_parallel
        mp = parallel_config.model_parallel
        if parallel_config.vocab_emb_dp:
            self.gather.shard(((1, 1), (dp, 1)))
            logger.info(f"Using {dp} data parallel for the embedding lookup.")
        else:
            if self.vocab_table_size % mp != 0:
                logger.warning("The vocab size of Loss is: %s, it is not divide by model_parallel: %s",
                               self.vocab_table_size, mp)
                logger.warning("Now, the model_parallel num of Loss will be changed: mp = 1")
                self.gather.shard(((1, 1), (dp, 1)))
            else:
                self.gather.shard(((mp, 1), (dp, 1)))
                logger.info(f"Using {dp} data parallel and {mp} "
                            f"model parallel for the embedding lookup.")


class LlamaRMSNorm(nn.Cell):
    r"""
    A self-defined RMSNorm operation using reduce mean.

        Args:
            dim (tuple): The shape of the input tensor
            eps (float): The epsilon value of the denominator. Default 1e-5.
            compute_type: The compute type.
        Inputs:
            - **x** (Tensor) - Tensor of shape :math:`(batch, seq\_length, hidden\_size)`.

        Outputs:
            Tensor of shape :math:`(batch, seq_length, hidden_size)`.
    """

    def __init__(self, dim, eps=1e-6, compute_type=mstype.float32):
        super(LlamaRMSNorm, self).__init__()
        self.eps = eps
        self.compute_type = compute_type
        self.weight = Parameter(initializer('ones', (dim,), dtype=mstype.float32), parallel_optimizer=False)

        if check_rmsnorm_big_kernel_valid() and not IS_WIN:
            self.norm = P.RmsNorm(eps)
            self.rms_norm = self._rms_norm
            self.self_define = False
            self.cast = P.Cast()
            self.rcast = P.Cast()
            self.cast.recompute()
        else:
            self.cast = P.Cast()
            self.mul = P.Mul()
            self.mul2 = P.Mul()
            self.square = P.Square()
            self.mean = P.ReduceMean(keep_dims=True)
            self.add = P.Add()
            self.rsqrt = P.Rsqrt()
            self.rms_norm = self._self_norm
            self.self_define = True

    def _self_norm(self, x):
        original_type = x.dtype
        norm_factor = self.square(self.cast(x, self.compute_type))
        norm_factor = self.mean(norm_factor, -1)
        norm_factor = self.add(norm_factor, self.eps)
        norm_factor = self.rsqrt(norm_factor)
        output = self.mul(x, self.cast(norm_factor, original_type))
        output = self.mul2(output, self.cast(self.weight, original_type))
        return output

    def _rms_norm(self, x):
        original_type = x.dtype
        output = self.norm(self.cast(x, self.compute_type), self.cast(self.weight, self.compute_type))[0]
        return self.rcast(output, original_type)

    def construct(self, x):
        """Forward of RMSNorm."""
        return self.rms_norm(x)

    def shard(self, strategy_in):
        """Parallel strategy configuratiuon interface."""
        if self.self_define:
            self.square.shard((strategy_in,))
            self.mean.shard((strategy_in,))
            self.rsqrt.shard((strategy_in,))
            self.add.shard((strategy_in, ()))
            self.mul.shard((strategy_in, strategy_in))
            self.mul2.shard((strategy_in, (1,)))
        else:
            self.norm.shard((strategy_in, (1,)))


class LlamaFeedForward(Cell):
    r"""
    LLaMA FeedForward.

    .. math::
            (xW_1 * xW_3)W_2

        Inputs:
            - **x** (Tensor) - should be `[batch, seq_length, hidden_size] or [batch * seq_length, hidden_size]`.
              Float tensor.

        Outputs:
            Tensor, the output of this layer after mapping. The shape is `[batch, seq_length, hidden_size] or
            [batch * seq_length, hidden_size]`.

        Raises:
            ValueError: `hidden_dim` is not a multiple of the model parallel way.
            ValueError: `dim` is not a multiple of the model parallel way.
    """

    @_LogActionOnce(m_logger=logger, key='FeedForward',
                    no_warning=_get_parallel_mode() in (ParallelMode.STAND_ALONE,))
    @_args_type_validator_check(dim=Validator.check_positive_int,
                                hidden_dim=Validator.check_positive_int,
                                multiple_of=Validator.check_positive_int,
                                compute_dtype=_valid_value_checks([mstype.float32, mstype.float16, mstype.bfloat16],
                                                                  "FeedForward"),
                                param_init_type=_valid_value_checks([mstype.float32, mstype.float16, mstype.bfloat16],
                                                                    "FeedForward"))
    def __init__(self, dim,
                 intermediate_size=None,
                 hidden_dim=None,
                 expert_num=1,
                 multiple_of=256,
                 hidden_act=LlamaSiLU,
                 ffn_dim_multiplier=None,
                 compute_dtype=mstype.float16,
                 param_init_type=mstype.float32,
                 is_dynamic=False,
                 parallel_config=default_dpmp_config):
        super().__init__()

        if hidden_act is None or not (isinstance(hidden_act, str) or issubclass(hidden_act, nn.Cell)):
            raise TypeError(f"For FeedForward cell, the hidden_act should str type or nn.Cell type, "
                            f"but got {hidden_act}.")

        if intermediate_size is not None:
            hidden_dim = intermediate_size
        else:
            if ffn_dim_multiplier is not None:
                hidden_dim = int((ffn_dim_multiplier + 0.01) * hidden_dim)
            hidden_dim = int(2 * hidden_dim / 3)
            hidden_dim = multiple_of * \
                         ((hidden_dim + multiple_of - 1) // multiple_of)

        if expert_num > 1:
            ep = parallel_config.expert_parallel
            dp_moe = parallel_config.data_parallel // ep
        else:
            dp_moe = 1
        self.dtype = compute_dtype
        self.hidden_act = hidden_act
        self.dim = dim
        self.hidden_dim = hidden_dim
        self.expert_num = expert_num

        self.mul = P.Mul()
        self.cast = P.Cast()
        self.w1 = Linear(in_channels=dim,
                         out_channels=hidden_dim,
                         expert_num=expert_num,
                         outer_batch=dp_moe,
                         activation=hidden_act,
                         has_bias=False,
                         compute_dtype=compute_dtype,
                         param_init_type=param_init_type,
                         skip_redistribution=is_dynamic)

        self.w2 = Linear(in_channels=hidden_dim,
                         out_channels=dim,
                         expert_num=expert_num,
                         outer_batch=dp_moe,
                         has_bias=False,
                         compute_dtype=compute_dtype,
                         param_init_type=param_init_type,
                         skip_redistribution=is_dynamic)

        self.w3 = Linear(in_channels=dim,
                         out_channels=hidden_dim,
                         expert_num=expert_num,
                         outer_batch=dp_moe,
                         has_bias=False,
                         compute_dtype=compute_dtype,
                         param_init_type=param_init_type,
                         skip_redistribution=is_dynamic)

    #@profile
    def construct(self, x):
        """Forward process of the FeedForward"""
        _check_input_dtype(F.dtype(x), "x", [mstype.float32, mstype.float16, mstype.bfloat16], self.cls_name)
        x = self.cast(x, self.dtype)
        # [bs, seq, hidden_dim] or [bs * seq, hidden_dim]
        # TIMEIT: 33.8% (CPU)
        gate = self.w1(x)  # dp,1 -> dp, mp
        # TIMEIT: 32.6% (CPU)
        hidden = self.w3(x)  # dp,1 -> dp, mp
        # TIMEIT: 0.3% (CPU)
        hidden = self.mul(hidden, gate)  # dp,mp -> dp, mp
        # TIMEIT: 33.4% (CPU)
        output = self.w2(hidden)  # dp,mp -> dp, 1
        return output

    def shard(self, parallel_config):
        """sharding for feedforward"""
        dp = parallel_config.data_parallel
        mp = parallel_config.model_parallel
        if self.hidden_dim % mp != 0:
            raise ValueError("For 'FeedForward', the class variable 'hidden_dim' must be a multiple of the"
                             "num of model parallel, but got the hidden_dim is {} and the num of model "
                             "parallel is {}.".format(self.hidden_dim, mp))
        if self.dim % mp != 0:
            raise ValueError("For 'FeedForward', the class variable 'dim' must be a multiple of the num of "
                             "model parallel, but got the dim is {} and the num of model parallel is {}."
                             .format(self.dim, mp))
        if self.expert_num == 1:
            self.w1.shard(((dp, 1), (mp, 1)), strategy_activation=((dp, mp),))
            self.w1.activation.shard(((dp, mp),))
            self.w2.shard(((dp, mp), (1, mp)))
            self.w3.shard(((dp, 1), (mp, 1)))
            self.mul.shard(((dp, mp), (dp, mp)))
        else:
            logger.info("shard ffn with MoE")
            ep = parallel_config.expert_parallel
            dp = parallel_config.data_parallel // ep
            self.w1.shard(strategy_matmul=((dp, ep, 1, 1), (ep, mp, 1)),
                          strategy_activation=((dp, ep, mp, 1),))
            self.w2.shard(strategy_matmul=((dp, ep, 1, mp), (ep, 1, mp)))
            self.w3.shard(strategy_matmul=((dp, ep, 1, 1), (ep, mp, 1)))
            self.mul.shard(((dp * ep, mp), (dp * ep, mp)))
