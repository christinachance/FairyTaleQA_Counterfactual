# IMPORTS NECESSARY:

# !pip install stanza

import stanza
import copy
import csv
import re 
import sys
import os


# uses https://github.com/uclanlp/corefBias/blob/master/WinoBias/wino/word_swapper.py
# assumes generalized_swaps.txt and extra_gendered_words.txt are in directoy
 

nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos')

def word_swapper(stdin, stdout):
  swaps = open("./gender_swap/generalized_swaps.txt").readlines()
  swap_dict = {}
  for line in swaps:
    tabs = line.split("\t")
    swap_dict[tabs[-2].strip()] = tabs[-1].strip()

  swaps = open("./gender_swap/extra_gendered_words.txt").readlines()
  for line in swaps:
    tabs = line.split("\t")
    swap_dict[tabs[-2].strip()] = tabs[-1].strip()
    swap_dict[tabs[-1].strip()] = tabs[-2].strip()

  print(swap_dict)
    
  lines = open(stdin).readlines()
  
  swapped_doc = ""

  for line in lines:
    doc = nlp(line)
    swapped_line = ""
    for sentence in doc.sentences:
      for word in sentence.words:
        q = word.text.lower()
        swap = None

        if q in swap_dict:
          swap = swap_dict[q]
        if q == "her":
          if word.xpos == "PRP": 
            swap = "him"
          else: swap = "his"
        if swap is not None and q.isupper(): 
          swap = swap[0].upper()+swap[1:]
        if swap is None:
          swapped_line += q + " "
        else:
          swapped_line += swap + " "
    
    swapped_doc += swapped_line[:-1] + "\n"

  translation_table = str.maketrans({
    "< /s >": "</s>",
    "</s >": "</s>",
    "< /s>": "</s>",
    "< sep >": "<SEP>",
    "< sep>": "<SEP>",
    "<sep>>": "<SEP>"})
    
  with open(stdout, 'w') as outfile:
    swapped_doc = swapped_doc.translate(translation_table)
    outfile.write(swapped_doc)

