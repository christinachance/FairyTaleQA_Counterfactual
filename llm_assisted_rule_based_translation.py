# IMPORTS NECESSARY:

# !pip install openai
# !pip install stanza
# !pip install -q transformers accelerate sentencepiece gradio
# !pip install sentencepiece
# !pip install backoff

#
# TO RUN THE CODE:
#   word_swapper(input_file_path, output_file_path)
#

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import nltk
from nltk.tokenize import RegexpTokenizer
import os
import openai
import backoff
import copy
import csv
import re
import sys
import json


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')



# This backoff function allows for the code to handle error handling and rate limit errors without erroring out

openai.api_key = # <OPENAI.API_KEY HERE>
@backoff.on_exception(backoff.expo, (openai.error.RateLimitError, openai.error.ServiceUnavailableError, openai.error.APIError))

def chat_completions_with_backoff(**kwargs):
  return openai.ChatCompletion.create(**kwargs)


# this prompt is tailored to gender perturbations but can be used for different perturbations
default_prompt = """
Providing a pair of words, if the first word is gendered, the paired word is the opposite gender of the original word, if the first word is gender neutral, the paired word is the same word as the first word. Provide the word to complete the pair.

prince -> princess
daughter -> son
bus -> bus
person -> person
teacher -> teacher
"""



# uses https://github.com/uclanlp/corefBias/blob/master/WinoBias/wino/word_swapper.py
# assumes generalized_swaps.txt and extra_gendered_words.txt are in directoy


# This tokenizer supports special characters such as '<' and '>'

tokenizer = RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')

def word_swapper(stdin, stdout):
  lines = open(stdin).readlines()
  with open("./swap_dicts/llm_generated_dict.txt") as f:
    swap_dict = f.read()

  swap_dict = json.loads(swap_dict)

  swapped_doc = ""
  for line in lines:
    swapped_line = ""
    for sentence in line.split("\n"):
      tokens = tokenizer.tokenize(sentence.lower())
      tags = pos_tag(tokens)
      for word in tags:
        q = word[0]
        pos = word[1]
        swap = None
        # handles our special characters and can be removed if there aren't special characters that confused POS tagging methods
        if q in ["</s>", "<sep>", '"']: 
          swap = None
        elif pos in ["NN", "NNS", "PRP", "PRP$"	]:
          if q in swap_dict:
            swap = swap_dict[q]
          else:
            prompt = default_prompt + q + "-> "
            
            response = chat_completions_with_backoff(model="gpt-3.5-turbo", messages=[{"role": "user", "content":prompt}])
            swap = response.choices[0].message.content

            swap = swap.split()[0]

            swap_dict[q] = swap
            swap_dict[swap] = q
          if q == "her":
            if pos == "PRP":
              swap = "him"
            else: swap = "his"
          if swap is not None and q.isupper():
            swap = swap[0].upper()+swap[1:]

        if swap is None:
          swapped_line += q + " "
        else:
          swapped_line += swap + " "

    swapped_doc += swapped_line[:-1] + "\n"


  
  with open(stdout, 'w') as outfile:
    swapped_doc = swapped_doc.replace("<sep>", "<SEP>")
    outfile.write(swapped_doc)

  with open("./swap_dicts/llm_generated_dict.txt", 'w') as outfile:
    outfile.write(json.dumps(swap_dict))




