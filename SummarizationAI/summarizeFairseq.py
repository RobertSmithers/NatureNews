from content import content
import torch
import fairseq

bart = torch.hub.load('pytorch/fairseq', 'bart.large')
bart.eval()  # disable dropout (or leave in train mode to finetune)

# https://fairseq.readthedocs.io/en/latest/getting_started.html

'''
Usage 
python fairseq/examples/bart/summarize.py \
  --model-dir ~/bart/bart.large.cnn \
  --model-file model.pt \
  --src ~/bart/cnn_dm/ceshi.source \
  --out ~/bart/cnn_dm/ceshi.hypo
'''

print('Original Content:')
print(content)
print("=============== End content")
tokens = bart.encode('Hello world!')
print(bart.predict('new_task', tokens))


