import os
import re
from time import sleep
from tqdm import tqdm
import pandas as pd
from gptconsole import Batch


############################################################
# read the records and parse them to prepare prompt inputs #
############################################################

with open('records.txt', 'r', encoding='utf-8') as f:
    contents = f.read()

record_bodies = []
records = re.split(r"<RECORD \d+>\n\n", contents)[1::]

# limit records for illustration
records = records[:3]


def get_element(element_str, record):
    out = re.findall(element_str + r":(.*)\n.*:", record)
    assert len(out) == 1
    return out[0].replace(element_str+":", "").strip()


for record in records:
    title = get_element('Title', record)
    abstract = get_element('Abstract', record)
    record_body = f'Title: {title}\nAbstract: {abstract}'
    record_bodies.append(record_body)


prompt_list = []
with open('prompt_template.txt', 'r', encoding='utf-8') as f:
    prompt_template = f.read()
for record_body in record_bodies:
    prompt_list.append(prompt_template.replace('======', record_body))


###################
# get the results #
###################

gptbatch = Batch(api_key="that's a secret")
# gptbatch.api_interface.set_model__gpt3p5()  # dumber but cheaper.

# Limit output to (0-10).
gptbatch.api_interface.set_max_tokens(25)
gptbatch.api_interface.set_system_message(
    "Answer with a number between 0 and 10, "
    "0 meaning unlikely and 10 highly likely")


# if it gets interrupted, just re-run. It caches the results to the
# output_directory so that you can keep going with the rest.

output_df = gptbatch.get_responses(prompt_list=prompt_list, output_directory="/tmp/test", sleep_seconds=10)


###############################
# post-processing the results #
###############################

# verify that we got answers we expect (0-10). Manually fix issues here.
output_df['response'].value_counts()

# convert to numeric and sort by relevance
output_df['response'] = output_df['response'].astype(int)
output_df.sort_values(by='response', ascending=False, inplace=True)

# print and review the sorted records
for resp in output_df.iterrows():
    print(resp[1]['input'])
    print('Answer:', resp[1]['response'])
    print()
