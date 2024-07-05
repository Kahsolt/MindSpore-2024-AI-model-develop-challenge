# Finetue

----

### baseline finetune lora setting

```python
Param_groups = {
  "decay": {
    "weight_decay": 0.0,
    "params": [
      "model.layers.0.attention.wq.mindpet_delta_lora_a",
      "model.layers.0.attention.wq.mindpet_delta_lora_b",
      "model.layers.0.attention.wv.mindpet_delta_lora_a",
      "model.layers.0.attention.wv.mindpet_delta_lora_b",
      "model.layers.1.attention.wq.mindpet_delta_lora_a",
      "model.layers.1.attention.wq.mindpet_delta_lora_b",
      "model.layers.1.attention.wv.mindpet_delta_lora_a",
      "model.layers.1.attention.wv.mindpet_delta_lora_b",
      "model.layers.2.attention.wq.mindpet_delta_lora_a",
      "model.layers.2.attention.wq.mindpet_delta_lora_b",
      "model.layers.2.attention.wv.mindpet_delta_lora_a",
      "model.layers.2.attention.wv.mindpet_delta_lora_b",
      "model.layers.3.attention.wq.mindpet_delta_lora_a",
      "model.layers.3.attention.wq.mindpet_delta_lora_b",
      "model.layers.3.attention.wv.mindpet_delta_lora_a",
      "model.layers.3.attention.wv.mindpet_delta_lora_b",
      "model.layers.4.attention.wq.mindpet_delta_lora_a",
      "model.layers.4.attention.wq.mindpet_delta_lora_b",
      "model.layers.4.attention.wv.mindpet_delta_lora_a",
      "model.layers.4.attention.wv.mindpet_delta_lora_b",
      "model.layers.5.attention.wq.mindpet_delta_lora_a",
      "model.layers.5.attention.wq.mindpet_delta_lora_b",
      "model.layers.5.attention.wv.mindpet_delta_lora_a",
      "model.layers.5.attention.wv.mindpet_delta_lora_b",
      "model.layers.6.attention.wq.mindpet_delta_lora_a",
      "model.layers.6.attention.wq.mindpet_delta_lora_b",
      "model.layers.6.attention.wv.mindpet_delta_lora_a",
      "model.layers.6.attention.wv.mindpet_delta_lora_b",
      "model.layers.7.attention.wq.mindpet_delta_lora_a",
      "model.layers.7.attention.wq.mindpet_delta_lora_b",
      "model.layers.7.attention.wv.mindpet_delta_lora_a",
      "model.layers.7.attention.wv.mindpet_delta_lora_b",
      "model.layers.8.attention.wq.mindpet_delta_lora_a",
      "model.layers.8.attention.wq.mindpet_delta_lora_b",
      "model.layers.8.attention.wv.mindpet_delta_lora_a",
      "model.layers.8.attention.wv.mindpet_delta_lora_b",
      "model.layers.9.attention.wq.mindpet_delta_lora_a",
      "model.layers.9.attention.wq.mindpet_delta_lora_b",
      "model.layers.9.attention.wv.mindpet_delta_lora_a",
      "model.layers.9.attention.wv.mindpet_delta_lora_b",
      "model.layers.10.attention.wq.mindpet_delta_lora_a",
      "model.layers.10.attention.wq.mindpet_delta_lora_b",
      "model.layers.10.attention.wv.mindpet_delta_lora_a",
      "model.layers.10.attention.wv.mindpet_delta_lora_b",
      "model.layers.11.attention.wq.mindpet_delta_lora_a",
      "model.layers.11.attention.wq.mindpet_delta_lora_b",
      "model.layers.11.attention.wv.mindpet_delta_lora_a",
      "model.layers.11.attention.wv.mindpet_delta_lora_b",
      "model.layers.12.attention.wq.mindpet_delta_lora_a",
      "model.layers.12.attention.wq.mindpet_delta_lora_b",
      "model.layers.12.attention.wv.mindpet_delta_lora_a",
      "model.layers.12.attention.wv.mindpet_delta_lora_b",
      "model.layers.13.attention.wq.mindpet_delta_lora_a",
      "model.layers.13.attention.wq.mindpet_delta_lora_b",
      "model.layers.13.attention.wv.mindpet_delta_lora_a",
      "model.layers.13.attention.wv.mindpet_delta_lora_b",
      "model.layers.14.attention.wq.mindpet_delta_lora_a",
      "model.layers.14.attention.wq.mindpet_delta_lora_b",
      "model.layers.14.attention.wv.mindpet_delta_lora_a",
      "model.layers.14.attention.wv.mindpet_delta_lora_b",
      "model.layers.15.attention.wq.mindpet_delta_lora_a",
      "model.layers.15.attention.wq.mindpet_delta_lora_b",
      "model.layers.15.attention.wv.mindpet_delta_lora_a",
      "model.layers.15.attention.wv.mindpet_delta_lora_b",
      "model.layers.16.attention.wq.mindpet_delta_lora_a",
      "model.layers.16.attention.wq.mindpet_delta_lora_b",
      "model.layers.16.attention.wv.mindpet_delta_lora_a",
      "model.layers.16.attention.wv.mindpet_delta_lora_b",
      "model.layers.17.attention.wq.mindpet_delta_lora_a",
      "model.layers.17.attention.wq.mindpet_delta_lora_b",
      "model.layers.17.attention.wv.mindpet_delta_lora_a",
      "model.layers.17.attention.wv.mindpet_delta_lora_b",
      "model.layers.18.attention.wq.mindpet_delta_lora_a",
      "model.layers.18.attention.wq.mindpet_delta_lora_b",
      "model.layers.18.attention.wv.mindpet_delta_lora_a",
      "model.layers.18.attention.wv.mindpet_delta_lora_b",
      "model.layers.19.attention.wq.mindpet_delta_lora_a",
      "model.layers.19.attention.wq.mindpet_delta_lora_b",
      "model.layers.19.attention.wv.mindpet_delta_lora_a",
      "model.layers.19.attention.wv.mindpet_delta_lora_b",
      "model.layers.20.attention.wq.mindpet_delta_lora_a",
      "model.layers.20.attention.wq.mindpet_delta_lora_b",
      "model.layers.20.attention.wv.mindpet_delta_lora_a",
      "model.layers.20.attention.wv.mindpet_delta_lora_b",
      "model.layers.21.attention.wq.mindpet_delta_lora_a",
      "model.layers.21.attention.wq.mindpet_delta_lora_b",
      "model.layers.21.attention.wv.mindpet_delta_lora_a",
      "model.layers.21.attention.wv.mindpet_delta_lora_b",
      "model.layers.22.attention.wq.mindpet_delta_lora_a",
      "model.layers.22.attention.wq.mindpet_delta_lora_b",
      "model.layers.22.attention.wv.mindpet_delta_lora_a",
      "model.layers.22.attention.wv.mindpet_delta_lora_b",
      "model.layers.23.attention.wq.mindpet_delta_lora_a",
      "model.layers.23.attention.wq.mindpet_delta_lora_b",
      "model.layers.23.attention.wv.mindpet_delta_lora_a",
      "model.layers.23.attention.wv.mindpet_delta_lora_b",
      "model.layers.24.attention.wq.mindpet_delta_lora_a",
      "model.layers.24.attention.wq.mindpet_delta_lora_b",
      "model.layers.24.attention.wv.mindpet_delta_lora_a",
      "model.layers.24.attention.wv.mindpet_delta_lora_b",
      "model.layers.25.attention.wq.mindpet_delta_lora_a",
      "model.layers.25.attention.wq.mindpet_delta_lora_b",
      "model.layers.25.attention.wv.mindpet_delta_lora_a",
      "model.layers.25.attention.wv.mindpet_delta_lora_b",
      "model.layers.26.attention.wq.mindpet_delta_lora_a",
      "model.layers.26.attention.wq.mindpet_delta_lora_b",
      "model.layers.26.attention.wv.mindpet_delta_lora_a",
      "model.layers.26.attention.wv.mindpet_delta_lora_b",
      "model.layers.27.attention.wq.mindpet_delta_lora_a",
      "model.layers.27.attention.wq.mindpet_delta_lora_b",
      "model.layers.27.attention.wv.mindpet_delta_lora_a",
      "model.layers.27.attention.wv.mindpet_delta_lora_b",
      "model.layers.28.attention.wq.mindpet_delta_lora_a",
      "model.layers.28.attention.wq.mindpet_delta_lora_b",
      "model.layers.28.attention.wv.mindpet_delta_lora_a",
      "model.layers.28.attention.wv.mindpet_delta_lora_b",
      "model.layers.29.attention.wq.mindpet_delta_lora_a",
      "model.layers.29.attention.wq.mindpet_delta_lora_b",
      "model.layers.29.attention.wv.mindpet_delta_lora_a",
      "model.layers.29.attention.wv.mindpet_delta_lora_b",
      "model.layers.30.attention.wq.mindpet_delta_lora_a",
      "model.layers.30.attention.wq.mindpet_delta_lora_b",
      "model.layers.30.attention.wv.mindpet_delta_lora_a",
      "model.layers.30.attention.wv.mindpet_delta_lora_b",
      "model.layers.31.attention.wq.mindpet_delta_lora_a",
      "model.layers.31.attention.wq.mindpet_delta_lora_b",
      "model.layers.31.attention.wv.mindpet_delta_lora_a",
      "model.layers.31.attention.wv.mindpet_delta_lora_b"
    ]
  }
}
```


### our finetune

⚪ run-0

⚠ runtime   
ℹ train speed: 5.66398 samples/s/p on NPU*4(32G)  

```
data: uniform_pick_17145
epoch: 5
bs: 32
lr: 1e-5
n_param: 3407872

samples_count: 200
  match rate: 0.00% (0)
  correct rate: 20.00% (40)
bingo_cnt:
{0: [39, 137], 1: [0, 17], 2: [0, 12], 4: [0, 7], 5: [0, 13], 6: [0, 3], 7: [0, 4], 8: [1, 1], 9: [0, 5], 10: [0, 1]}
```
