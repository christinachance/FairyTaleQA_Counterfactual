# IMPORTS NECESSARY:

# !pip install openai
# !pip install stanza
# !pip install -q transformers accelerate sentencepiece gradio
# !pip install sentencepiece
# !pip install backoff


import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import nltk
from nltk.tokenize import RegexpTokenizer
import os
import openai


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')



default_prompt = """
Providing a pair of words, if the first word is gendered, the paired word is the opposite gender of the original word, if the first word is gender neutral, the paired word is the same word as the first word. Provide the word to complete the pair.

prince -> princess
daughter -> son
bus -> bus
person -> person
teacher -> teacher
"""
