# IMPORTS NECESSARY:

# !pip install --upgrade openai
# !pip install --upgrade pip

import openai

#
# TO RUN THE CODE:
#   llm_rewrite(input_file_path, output_file_path)
#


# This backoff function allows for the code to handle error handling and rate limit errors without erroring out

openai.api_key = # <OPENAI.API_KEY HERE>
@backoff.on_exception(backoff.expo, (openai.error.RateLimitError, openai.error.ServiceUnavailableError, openai.error.APIError))

def chat_completions_with_backoff(**kwargs):
  return openai.ChatCompletion.create(**kwargs)

default_prompt = """
rewrite the original text changing all gendered pronouns and nouns referencing people to the opposite gender and maintain the format of the text:
[Original]: there once lived a poor widow who supported herself and her only son by gleaning in the fields the stalks of grain that had been missed by the reapers . he had big blue eyes , and fair golden curls , and he loved his good mother very dearly , and was never more pleased than when she allowed him to help her with her work . <SEP> how did the poor widow support herself and her son ? <SEP> gleaning in the fields the stalks of grain that had been missed by the reapers . </s> by gleaning in the fields the stalks of grain that had been missed by the reapers . <SEP> action <SEP> explicit
[Rewritten]: there once lived a poor widower who supported himself and his only daughter by gleaning in the fields the stalks of grain that had been missed by the reapers . she had big blue eyes , and fair golden curls , and she loved her good father very dearly , and was never more pleased than when he allowed her to help him with his work . <SEP> how did the poor widower support himself and his daughter? <SEP> gleaning in the fields the stalks of grain that had been missed by the reapers . </s> by gleaning in the fields the stalks of grain that had been missed by the reapers . <SEP> action <SEP> explicit

[Original]: it so happened that the great man was walking in his garden with his daughter madge that morning , so that when he suddenly looked up and saw a little boy before him , he said , kindly , " well , my child , what can i do for you ? " " if you please , sir , " said the boy , bravely , although he was frightened at meeting the squire face to face , " i want you to give me some work to do , so that i can earn money . " " to buy food for my mother , sir . we are very poor , and since she is no longer able to work for me i wish to work for her . " <SEP> what was the name of the man's daughter ? <SEP> madge . </s> madge . <SEP> character <SEP> explicit
[Rewritten]: it so happened that the great woman was walking in her garden with her son madge that morning , so that when she suddenly looked up and saw a little girl before her , she said , kindly , " well , my child , what can i do for you ? " " if you please , ma'am , " said the girl , bravely , although she was frightened at meeting the squire face to face , " i want you to give me some work to do , so that i can earn money . " " to buy food for my father , ma'am . we are very poor , and since he is no longer able to work for me i wish to work for him . " <SEP> what was the name of the woman's son ? <SEP> madge . </s> madge . <SEP> character <SEP> explicit

[Original]:
"""


def llm_rewrite(stdin, stdout):

  completion = ""
  with open(stdin) as fp:
      Lines = fp.readlines()
      for line in Lines:
        prompt_line = default_prompt + line + "\n [Rewritten]:"
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo", 
          messages=[{"role": "user", "content": input_text}]
        )      
        completion += response.choices[0].message.content + "\n"
  
  with open(stdout, 'w') as outfile:
        outfile.write(completion)
