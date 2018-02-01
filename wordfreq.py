# Given a text corpus of ASCII, generate
# a random sentence based on an order 1
# Markov process.
#
# Ex: python wordfreq.py ch15-chowder

import random
import re
import sys

def contains_terminator(word):
    if '.' in word or '?' in word or '!' in word:
        return True
    return False

def get_random_sentence(dict):
    word = 'NULL'
    sentence = ''
    while sentence == '' or word != 'NULL':
        word = random.choice(dict[word])
        sentence = sentence + word + ' '
        if contains_terminator(word):
            word = 'NULL'
    return sentence

# Make sure we received an input file
if len(sys.argv) != 2:
	print "usage: python wordfreq.py input.txt"
	sys.exit()

# Read the input file specified on the command line
with open(sys.argv[1], 'r') as myfile:
    sample=myfile.read().replace('\n', ' ')

# Remove double-quotes and parentheses, a pain to try to balance
sample = re.sub(r'["\(\)]', '', sample)

dict = {}
prevword = 'NULL'

# Initialize frequency table
for word in sample.split():
    dict[prevword] = []
    prevword = word

# Populate frequency table
prevword = 'NULL'
for word in sample.split():
    if contains_terminator(prevword):
        prevword = 'NULL'
    dict[prevword].append(word)
    prevword = word

sentence = get_random_sentence(dict)
print sentence
