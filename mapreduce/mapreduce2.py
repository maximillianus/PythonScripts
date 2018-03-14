"""
Sample implementation of map reduce algorithm in python.
MapReduce is an algorithm (or more correctly defined as programming model)
which implements both map and reduce functions to do distributed data
processing.
We will tokenize and count words
"""


text1 = ['I love computer, but computer does not love me.']
text2 = ['I like margarita.', 'He does not like Gin.']

print(" ** Method 1: Using list of implement MapReduce.")
# Map
# Map is a processing task that takes in certain input and turn it into
# a key-value pair as an output. In this example we will take in a sentence
# as an input and turn it into a key-value word-count pair

def mapping(text):
    # In context of text analysis, mapping is done by first tokenizing
    # words in a sentence.

    # Before everything else, cleaning has to be done
    # lowercasing
    text = [s.lower() for s in text]
    # remove punctuation
    punct = set(['.'])
    # text = ''.join([s for s in text if s not in punct])
    text = [s.replace('.','').replace(',','') for s in text]

    # now tokenizing. turn a sentence into list of words
    text = [t.split(' ') for t in text]

    # flatten it
    text = [item for sublist in text for item in sublist]
    return text

# Reduce
# Reduce is a processing task that takes in key-value pairs input and 
# reducing the number of the pairs by aggregating them. The output is the
# list of sum of values.

def reducing(wordlist):
    # now that we got list of words, we count the overall occurences
    wordlist = [[word, wordlist.count(word)] for word in set(wordlist)]
    return wordlist


# words = mapping(text2)
# print(words)
# wordcount = reducing(words)
# print(wordcount)


print(" ** Method 2: Using dict of implement MapReduce.")

def mapping2(text):
    # In context of text analysis, mapping is done by first tokenizing
    # words in a sentence.

    # Before everything else, cleaning has to be done
    # lowercasing
    text = [s.lower() for s in text]
    # remove punctuation
    punct = set(['.'])
    # text = ''.join([s for s in text if s not in punct])
    text = [s.replace('.','').replace(',','') for s in text]

    # now tokenizing. turn a sentence into list of words
    text = [t.split(' ') for t in text]

    # flatten it
    text = [[item,1] for sublist in text for item in sublist]

    # add count:
    return text


def reducing2(keyvalue):
    # now that we got list of words, we count the overall occurences
    wordcount = {}
    for item in keyvalue:
        # add key to dict if it's not already there
        # if it's there, add 1
        wordcount[item[0]] = wordcount.get(item[0], 0) + 1
        
    return wordcount

words = mapping2(text1)
print(words)
wordcount = reducing2(words)
print(wordcount)
