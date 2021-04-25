#!/bin/bash

import language_tool_python
import boto3
import json

# mention the language keyword
tool = language_tool_python.LanguageTool('en-US')

# set counts of variables to 0
num_mistakes_native = 0
word_count_native = 0
num_mistakes_learner = 0
word_count_learner = 0

# pulling files from s3 bucket for native speaker
s3 = boto3.resource('s3')
content_object = s3.Object('trans-native', 't_n_ital1.json')
file_content = content_object.get()['Body'].read().decode('utf-8')
json_content = json.loads(file_content)

# reading .json as string
text = json_content['TranslatedText']

# for loop for word count
for i in range(len(text)):
    if(text[i] == ' ' or text == '\n' or text == '\t'):
        word_count_native = word_count_native + 1
        
# for loop for checking how many grammar mistakes
for i in range(len(text)):
    matches = tool.check(text[i])
    num_mistakes_native = num_mistakes_native + len(matches)
    
# repeat process for the non-native speaker    
# pulling files from s3 bucket for non-native "learner" speaker
content_object = s3.Object('trans-learner', 't_l_ital1.json')
file_content = content_object.get()['Body'].read().decode('utf-8')
json_content = json.loads(file_content)

# reading .json as string
text = json_content['TranslatedText']

# for loop for word count
for i in range(len(text)):
    if(text[i] == ' ' or text == '\n' or text == '\t'):
        word_count_learner = word_count_learner + 1
        
# for loop for checking how many grammar mistakes
for i in range(len(text)):
    matches = tool.check(text[i])
    num_mistakes_learner = num_mistakes_learner + len(matches)


print("The number of words in the native speaker document is", word_count_native)
print("The number of mistakes in the native speaker document is", num_mistakes_native)
print("The number of words in the non-native speaker document is", word_count_learner)
print("The number of mistakes in the non-native speaker document is", num_mistakes_learner)

print("For the native speaker the grammar mistake rate is", num_mistakes_native*100/word_count_native, "%")
print("For the non-native speaker the grammar mistake rate is", num_mistakes_learner*100/word_count_learner, "%")