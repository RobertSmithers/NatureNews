from content import content
import torch
from tqdm import tqdm
import fairseq

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", category=UserWarning) 

bart = torch.hub.load('pytorch/fairseq', 'bart.large.cnn')
bart.eval()  # disable dropout (or leave in train mode to finetune)

max_len = 800
min_len = 400
chunks = 3
DEBUG = False
with open('input_news_3.txt', encoding='utf8') as source, open('output.txt', 'w') as fout:
    sline = source.readline().strip()
    slines = [sline]
    slines = []
      
    for it, sline in enumerate(source):
      if len(sline) < 10:
        continue

      try:
        line = sline.strip()
      except:
        print("*** Error: Bad line -", sline)
        continue
      
      slines.append(line)
    
    # Separate into "chunks" chunks
    chunk_sz = len(slines)//chunks
    input_sz = 0
    for i in tqdm(range(chunks), desc="Batches"):
      chunk = ""
      for ct, line in enumerate(slines[chunk_sz*i:chunk_sz*(i+1)]):
        chunk += line
        input_sz += len(line)
        # if len(slines) // (ct // chunks) == 0:
          
      with torch.no_grad():
        if DEBUG:
          tqdm.print("Min =", min_len // chunks)
          tqdm.print("Max =", max_len // chunks)
  
        # https://github.com/facebookresearch/fairseq/blob/b5a039c292facba9c73f59ff34621ec131d82341/fairseq/search.py
        # https://github.com/facebookresearch/fairseq/blob/d9c661bf4fad170a1c66a7abd9f433a848d0d26a/fairseq/sequence_generator.py
        # min_lens = self.min_len_a * self.src_lengths + self.min_len_b
        # max_lens = self.max_len_a * self.src_lengths + self.max_len_b
        
        hypotheses_batch = bart.sample([chunk], beam=10, lenpen=1.0, max_len_a=0.0, max_len_b=max_len // chunks, min_len_a=0.0, min_len_b=min_len // chunks)#, no_repeat_ngram_size=3) #max_len_a=0.2, max_len_b=200,)

        for hypothesis in hypotheses_batch:
          if DEBUG:
            tqdm.print(f"Input ({input_sz}) Output ({len(hypothesis)})")
          fout.write(hypothesis + '\n')
          fout.flush()
            
print("Finished")