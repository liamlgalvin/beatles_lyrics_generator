import tensorflow as tf
import numpy as np
import os
import sys
import time
import re
import random
from big_phoney import BigPhoney


phoney = BigPhoney()

pre_text = open("lyrics.txt" ,'r') 
text = pre_text.read().lower()

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])

vocab = sorted(list(set(text)))

print('total chars:', len(vocab))
char_index = dict((c, i) for i, c in enumerate(vocab))
index_char = dict((i, c) for i, c in enumerate(vocab))

# load model
model = tf.keras.models.load_model('model.h5')
# summarize model.
model.summary()

def sample(preds, temperature):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)
song = ""
start_index = random.randint(0, len(text) - maxlen - 1)
#sentence = input("enter: ").strip()[:40]
for temperature in [1.0]:#[0.2, 0.5, 1.0, 1.2]:
    print('----- temperature:', temperature)
    generated = ""
    sentence = text[start_index: start_index + maxlen]
    generated += sentence
    print('----- Generating with seed: "' + sentence + '"')
    sys.stdout.write(generated)

    for i in range(5000):
        x_pred = np.zeros((1, maxlen, len(vocab)))
        for t, char in enumerate(sentence):
            x_pred[0, t, char_index[char]] = 1.

        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, temperature)
        next_char = index_char[next_index]

        generated += next_char
        sentence = sentence[1:] + next_char
        
        song = song + next_char
        
        # sys.stdout.write(next_char)
        # sys.stdout.flush()
    print()

#print('song = ' , song)

song_list = song.split("\n")
syls=[]

print("----------making song----------")
for i in song_list:
    if i != "":
        if (phoney.count_syllables(i)) in range (6,9):
          syls.append(i) #append line to syls if it has 6-8 syllables
        # print(phoney.phonize(i))

print('length = ' , len(song))

print("sum:", len(song_list))

print("total:",  len(syls))


syl_list_dict = {} # for every line that i 6 - 8 syllables group by last sound phonetically

for line in syls: 
# goes through lines with 6-8 sylables (syls) and adds them to dictionary based on
# last syllable. i.e. do they rhyme  
    num_syls = phoney.count_syllables(line)
    line_list = line.split()
    last_word = line_list[len(line_list)-1]
    last_word_phon = phoney.phonize(last_word) 
    last_word_phon = last_word_phon.split()
    last_word_last_syl = last_word_phon[len(last_word_phon)-1]
    if last_word_last_syl in syl_list_dict:
        syl_list_dict[last_word_last_syl].append(line)
    else:
        syl_list_dict[last_word_last_syl] = [line]

#print(syl_list_dict)
sort_dict = sorted(syl_list_dict.items(), key=lambda x: len(x[1]), reverse=True)
more_syls = []
one_syls = []
for key in sort_dict:
    print(key[0], ": ", len(key[1]), " rhyming words" )
    print(key[1])
    if len(key[1]) > 1:
        more_syls.append(key)
    else:
        one_syls.append(key)
        

def write_verse(num):
    verse = ""
    verse += (get_random_lyric(more_syls)) + "\n"
    verse += (more_syls[num][1][0]) + "\n"
    verse += (get_random_lyric(more_syls)) + "\n"
    if len(more_syls[num][0])!= 1:
        verse += (more_syls[num][1][1]) + "\n"
    else:
        verse += (get_random_lyric(one_syls)) + "\n"
    return verse

def get_chorus():
    chorus = ""
    chorus += (get_random_lyric(one_syls)) + "\n"
    chorus += (more_syls[0][1][0]) + "\n"
    chorus += (get_random_lyric(one_syls)) + "\n"
    if len(more_syls[0][1])!= 1:
        chorus += (more_syls[0][1][1]) + "\n"
    else:
        chorus += (get_random_lyric(one_syls)) + "\n"
    
    return chorus

def get_random_lyric(lyric_list):
    # pulls a random lyric from list
    # @ param lyric list: list of lists
    rand = random.randint(0, len(lyric_list)-1)
    rand_list = lyric_list[rand][1]
    rand = random.randint(0, len(rand_list)-1)
    rand_lyric = rand_list[rand]
    return rand_lyric

num_sets = [i for i in range(0,len(sort_dict))]
print (len(sort_dict))

print (num_sets)
print ('-------- Verse 1 ---------')
print(write_verse(1))

print ('-------- Chorus ---------')
chorus = get_chorus()
print(chorus)

print ('-------- Verse 2 ---------')
print(write_verse(2))
print ('-------- Chorus ---------')
print(chorus)

print ('-------- Bridge ---------')

bridge = get_random_lyric(sort_dict)
print(bridge)
print(bridge)

print ('-------- Chorus ---------')
print(chorus)



