import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from big_phoney import BigPhoney
import pickle
import matplotlib.pyplot as plt

# we will use this to analyse the sylables and the phonetics of the sentences.
phoney = BigPhoney()

# load in lyrics
pre_text = open("lyrics.txt" ,'r') 
text = pre_text.read().lower()

# Create and generate a word cloud image with most popular words:
wordcloud = WordCloud(stopwords=STOPWORDS, collocations=False)
wordcloud.generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

if ((path.isfile('filename.pickle')) != True):
    stats = {}
    y = 0
    for line in text.split():
        if line != " ":
            i = phoney.count_syllables(line)
            if i in stats:
                stats[i] += 1
            else:
                stats[i] = 1
                y+=1
            if (y%10 == 0):
                print(y)


    with open('filename.pickle', 'wb') as handle:
        pickle.dump(stats, handle, protocol=pickle.HIGHEST_PROTOCOL)
else:
    # open a file, where you stored the pickled data
    file = open('filename.pickle', 'rb')

    # get information from that file
    stats = pickle.load(file)

    # close the file
    file.close()



# # print out syllable numbers of rows in order 
for i in sorted(stats, key=stats.get, reverse=True):
    if i != 0:
        print("syllables: %s appears:'%d'" %(i, stats[i]))


