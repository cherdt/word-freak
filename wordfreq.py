# Given a text corpus of ASCII, generate
# a random sentence based on an order n
# Markov process.
#
# Ex: python wordfreq.py ch15-chowder 2

import pickle
import os
import random
import re
import sys
from collections import deque

class Markov:
    def __init__(self, n):
        self.n = n

    def get_random_sentence(self, dict):
        prevwords = deque([], self.n)
        for i in range(0,self.n):
            prevwords.append('NULL')
        initword = join_list(list(prevwords))
        word = 'NULL'
        sentence = ''

        while sentence == '' or join_list(list(prevwords)) != initword:
            word = random.choice(dict[join_list(list(prevwords))])
            sentence = sentence + word + ' '
            prevwords.popleft()
            prevwords.append(word)
            if contains_terminator(prevwords):
                for i in range(0,self.n):
                    prevwords.popleft()
                    prevwords.append('NULL')
        return sentence



def contains_terminator(words):
    word = list(words).pop()
    if '.' in word or '?' in word or '!' in word:
        return True
    return False

def join_list(list):
    joined = ""
    list.reverse()
    while len(list) > 0:
        joined += list.pop()
    return joined

def reinit_queue(queue):
    for i in range(0, len(queue)):
        queue.popleft()
        queue.append("NULL")

def build_dict_from_file(filename, n):
    # Read the input file specified on the command line
    with open(filename, 'r') as myfile:
        sample=myfile.read().replace('\n', ' ')
    
    # Remove double-quotes and parentheses, a pain to try to balance
    sample = re.sub(r'["\(\)]', '', sample)

    dict = {}    
    prevwords = deque([], n)
    for i in range(0, n):
        prevwords.append("NULL")
    
    # Initialize frequency table
    for word in sample.split():
        if contains_terminator(prevwords):
            reinit_queue(prevwords)
        dict[join_list(list(prevwords))] = []
        prevwords.popleft()
        prevwords.append(word)
    
    # Populate frequency table
    prevwords = deque([], n)
    for i in range(0, n):
        prevwords.append("NULL")
    
    for word in sample.split():
        if contains_terminator(prevwords):
            reinit_queue(prevwords)
        dict[join_list(list(prevwords))].append(word)
        prevwords.popleft()
        prevwords.append(word)

    return dict

def main():
    # Make sure we received an input file
    if len(sys.argv) < 2:
            print "usage: python wordfreq.py input.txt [1]"
            sys.exit()
    
    # What order Markov chains are we using? Default to 1
    if len(sys.argv) == 3:
        n = int(sys.argv[2])
    else:
        n = 1
    
    # source file + markov order + file extension
    cache_filename = sys.argv[1] + '.' + str(n) + '.pkl'
    
    # If we already have a cached version of the dictionary, use that
    if os.path.exists(cache_filename):
        pkl_file = open(cache_filename, 'rb')
        dict = pickle.load(pkl_file)
        pkl_file.close()
    
    # Otherwise, build from the file
    else:
        dict = build_dict_from_file(sys.argv[1], n)
        pkl_file = open(cache_filename, 'wb')
        pickle.dump(dict, pkl_file)
        pkl_file.close()
    
    markov = Markov(n)
    print markov.get_random_sentence(dict)

if __name__ == '__main__':
    main()
