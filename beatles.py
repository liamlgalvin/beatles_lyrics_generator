
"""
Created on Wed Jul  1 10:06:23 2020
based on the code by
@author: Jeff Heaton
https://github.com/jeffheaton/t81_558_deep_learning/blob/master/t81_558_class_10_3_text_generation.ipynb
"""

import tensorflow as tf
import numpy as np
import os
import time
import re
import sys
import random

pre_text = open("lyrics.txt" ,'r') 
text = pre_text.read().lower()

print('corpus length:', len(text))
vocab = sorted(list(set(text)))

print('total chars:', len(vocab))
char_index = dict((c, i) for i, c in enumerate(vocab))
index_char = dict((i, c) for i, c in enumerate(vocab))

# Convert text to integers
text_as_int = np.array([char_index[c] for c in text])

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
x = np.zeros((len(sentences), maxlen, len(vocab)), dtype=np.bool)
y = np.zeros((len(sentences), len(vocab)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_index[char]] = 1
    y[i, char_index[next_chars[i]]] = 1

#build the model: a single LSTM
print('Build model...')
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.LSTM(128, input_shape=(maxlen, len(vocab))))
model.add(tf.keras.layers.Dense(len(vocab), activation='softmax'))

optimizer = tf.keras.optimizers.RMSprop(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

model.summary()

model.fit(x, y,
          batch_size=128,
          epochs=60)

model.save("model.h5")
print("Model saved to disk")

# # load model
# model = tf.keras.models.load_model('model.h5')
# # summarize model.
# model.summary()

# def sample(preds, temperature):
#     # helper function to sample an index from a probability array
#     preds = np.asarray(preds).astype('float64')
#     preds = np.log(preds) / temperature
#     exp_preds = np.exp(preds)
#     preds = exp_preds / np.sum(exp_preds)
#     probas = np.random.multinomial(1, preds, 1)
#     return np.argmax(probas)

# start_index = random.randint(0, len(text) - maxlen - 1)

# for temperature in [0.2, 0.5, 1.0, 1.2]:
#     print('----- temperature:', temperature)
#     generated = ""
#     sentence = text[start_index: start_index + maxlen]
#     generated += sentence
#     print('----- Generating with seed: "' + sentence + '"')
#     sys.stdout.write(generated)

#     for i in range(400):
#         x_pred = np.zeros((1, maxlen, len(vocab)))
#         for t, char in enumerate(sentence):
#             x_pred[0, t, char_index[char]] = 1.

#         preds = model.predict(x_pred, verbose=0)[0]
#         next_index = sample(preds, temperature)
#         next_char = index_char[next_index]

#         generated += next_char
#         sentence = sentence[1:] + next_char

#         sys.stdout.write(next_char)
#         sys.stdout.flush()
#     print()
