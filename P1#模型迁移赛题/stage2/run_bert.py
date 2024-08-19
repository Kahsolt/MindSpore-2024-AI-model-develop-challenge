#!/usr/bin/env python3
# Author: Armit
# Create Time: 2024/08/19 

import os
os.environ['MINDNLP_CACHE'] = './mindnlp/.mindnlp'
from time import time

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.optimize import curve_fit
import mindspore as ms
from mindspore import ops
from mindnlp.transformers import *

model: BertModel = BertModel.from_pretrained('google-bert/bert-base-uncased')
tokenizer: BertTokenizer = BertTokenizer.from_pretrained('google-bert/bert-base-uncased')

TEXT = '''
In Buddhism, the Four Noble Truths are "the truths of the Noble Ones", the truths or realities for the "spiritually worthy ones".[1][web 1][2] The truths are: 
dukkha ("not being at ease", "suffering",[note 1] unsatisfactory unstableness; from dush-stha, "standing unstable,"[3][4][5][6]) is an innate characteristic of samsara, (lit. 'wandering'), existence:[web 2][7][8] nothing is forever, this hurts; 
samudaya (origin, arising, combination; "cause"): together with dukkha (unease, disbalance) there is taṇhā (lit. 'thirst'), "craving," "desire" for or "attachment" to (upādāna) this transient, unsatisfactory existence;[web 3][9][10][note 2][12] 
nirodha (cessation, ending, confinement): the attachment to dukkha can be severed or contained by the confinement[11][12] or letting go of this taṇhā;[13][14][15][16] 
marga (path, Noble Eightfold Path) is the path leading to the confinement of tanha and the release (vimutti) from dukkha.[17][18][19] 
The eight Buddhist practices in the Noble Eightfold Path are: 
Right View: our actions have consequences, death is not the end, and our actions and beliefs have consequences after death. The Buddha followed and taught a successful path out of this world and the other world (heaven and underworld/hell).[33][34][35][web 1] Later on, right view came to explicitly include karma and rebirth, and the importance of the Four Noble Truths, when "insight" became central to Buddhist soteriology, especially in Theravada Buddhism.[36][37] 
Right Resolve (samyaka-saṃkalpa/sammā-saṅkappa) can also be known as "right thought", "right aspiration", or "right motivation".[38] In this factor, the practitioner resolves to strive toward non-violence (ahimsa) and avoid violent and hateful conduct.[37] It also includes the resolve to leave home, renounce the worldly life and follow the Buddhist path.[39] 
Right Speech: no lying, no rude speech, no telling one person what another says about him to cause discord or harm their relationship, no idle chatter.[40][41] 
Right Conduct or Action: no killing or injuring, no taking what is not given, no sexual misconduct, no material desires. 
Right Livelihood: no trading in weapons, living beings, meat, liquor, or poisons. 
Right Effort: preventing the arising of unwholesome states, and generating wholesome states, the bojjhagā (Seven Factors of Awakening). This includes indriya-samvara, "guarding the sense-doors", restraint of the sense faculties.[42][43] 
Right Mindfulness (sati; Satipatthana; Sampajañña): a quality that guards or watches over the mind;[44] the stronger it becomes, the weaker unwholesome states of mind become, weakening their power "to take over and dominate thought, word and deed."[45][note 2] In the vipassana movement, sati is interpreted as "bare attention": never be absent minded, being conscious of what one is doing; this encourages the awareness of the impermanence of body, feeling and mind, as well as to experience the five aggregates (skandhas), the five hindrances, the four True Realities and seven factors of awakening.[43] 
Right samadhi (passaddhi; ekaggata; sampasadana): practicing four stages of dhyāna ("meditation"), which includes samadhi proper in the second stage, and reinforces the development of the bojjhagā, culminating into upekkhā (equanimity) and mindfulness.[47] In the Theravada tradition and the vipassana movement, this is interpreted as ekaggata, concentration or one-pointedness of the mind, and supplemented with vipassana meditation, which aims at insight. 
'''.strip()

input_ids = tokenizer.encode(TEXT, return_tensors='ms')
nlen = input_ids.shape[-1]
print('nlen:', nlen)


# infer max-length
'''
>> infer-512: 0.9963772296905518
>> infer-512: 0.7094094753265381
>> infer-512: 0.6394333839416504
>> infer-512: 0.6423554420471191
>> infer-512: 0.6430082321166992
>> infer-512: 0.6563448905944824
>> infer-512: 0.6365606784820557
>> infer-512: 0.6430091857910156
>> infer-512: 0.6498172283172607
>> infer-512: 0.6407642364501953
'''
for _ in range(10):
  ids = input_ids[:, :512]   # max_len=512
  attention_mask = ops.zeros_like(ids)
  ts_start = time()
  output = model(ids, attention_mask)[0][0]
  ts_end = time()
  output_ids = output.argmax(-1)
  output_text = tokenizer.decode(output_ids)
  print(f'>> infer-512: {ts_end - ts_start}')


# infer multi-lengths
'''
>> infer-10: 0.06621363162994384
>> infer-20: 0.07598776817321777
>> infer-30: 0.08096997737884522
>> infer-40: 0.08958468437194825
>> infer-50: 0.10130910873413086
>> infer-60: 0.11085288524627686
>> infer-70: 0.1176417350769043
>> infer-80: 0.12713706493377686
>> infer-90: 0.12751359939575196
>> infer-100: 0.14202992916107177
>> infer-110: 0.14286632537841798
>> infer-120: 0.15183534622192382
>> infer-130: 0.16358323097229005
>> infer-140: 0.1791896104812622
>> infer-150: 0.1861947298049927
>> infer-160: 0.19524815082550048
>> infer-170: 0.21330766677856444
>> infer-180: 0.2123154878616333
>> infer-190: 0.23489420413970946
>> infer-200: 0.24950873851776123
>> infer-210: 0.25798892974853516
>> infer-220: 0.24933414459228515
>> infer-230: 0.2813833475112915
>> infer-240: 0.29076266288757324
>> infer-250: 0.2898708343505859
>> infer-260: 0.3235267877578735
>> infer-270: 0.34158480167388916
>> infer-280: 0.3426505565643311
>> infer-290: 0.36318325996398926
>> infer-300: 0.36487910747528074
>> infer-310: 0.3903172492980957
>> infer-320: 0.405916690826416
>> infer-330: 0.42217140197753905
>> infer-340: 0.4356399059295654
>> infer-350: 0.4488281488418579
>> infer-360: 0.4486760854721069
>> infer-370: 0.46639385223388674
>> infer-380: 0.48669278621673584
>> infer-390: 0.5222228288650512
>> infer-400: 0.5376412153244019
>> infer-410: 0.5451196193695068
>> infer-420: 0.5572662353515625
>> infer-430: 0.5647869110107422
>> infer-440: 0.5765958547592163
>> infer-450: 0.6127312898635864
>> infer-460: 0.6289200782775879
>> infer-470: 0.6247688055038452
>> infer-480: 0.6831738710403442
>> infer-490: 0.7286645174026489
>> infer-500: 0.6886951684951782
>> infer-510: 0.6996675968170166
'''
n_repeat = 10
len_list = np.linspace(10, 510, 51, dtype=np.int32)
ts_list = []
for xlen in tqdm(len_list):
  ts_acc = 0.0
  for _ in range(n_repeat):
    cp = int(np.random.randint(nlen - xlen))
    ids = input_ids[..., cp:cp+int(xlen)]
    attention_mask = ops.zeros_like(ids)
    ts_start = time()
    model(ids, attention_mask)
    ts_end = time()
    ts_acc += ts_end - ts_start
  ts_list.append(ts_acc / n_repeat)
  print(f'>> infer-{xlen}: {ts_list[-1]}')

# y = 1.239742694772917e-06 * x^2 + 0.0006631159757477782 * x + 0.06100525471682994
f = lambda x, a, b, c: a * x**2 + b * x + c
popt, pcov = curve_fit(f, len_list, ts_list)
a, b, c = popt
print(f'y = {a} * x^2 + {b} * x + {c}')

plt.plot(len_list, ts_list, 'b', label='truth')
plt.plot(len_list, f(len_list, *popt), 'r', label='regression')
plt.suptitle('bert: input length - infer time')
plt.legend()
plt.savefig('list_models.png', dpi=400)
