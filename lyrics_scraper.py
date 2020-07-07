import time
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.select import Select
import pandas as pd
from pandas import DataFrame
import string
import random
import shutil



def azlyrics_scraper(band):
    folder = "lyrics"
    if not os.path.exists(folder):
        os.makedirs(folder)

    first_letter = band[0:1].lower()

    url = str("https://www.azlyrics.com/%s/%s.html" %(first_letter, band.lower()))
    source = requests.get(url).text

    soup = BeautifulSoup(source, 'lxml')

    album_div = soup.find('div',{'id': 'listAlbum'})
    albums = album_div.find_all('div',{'class': 'listalbum-item'})
    for track in albums:
        track_url = 'https://www.azlyrics.com/' + track.find('a').get('href')[3:] # removes the ../ from the url
        track_title = track.find('a').text
        track_title = track_title.translate(str.maketrans('', '', string.punctuation))
        #make a new bs item for each song
        songbs = BeautifulSoup(requests.get(track_url).text, 'lxml')
        song_main = songbs.find('div', {'class':"col-xs-12 col-lg-8 text-center"}) # this gets the main div 
        song_main_divs = song_main.find_all('div') # makes a list of all divs inside the main div
        song_lyrics = (song_main_divs[5].text) # 5 is the song div
        file_name = 'lyrics/' + track_title + '.txt'
        file = open(file_name ,'w') 
        file.write(song_lyrics.strip()) 
        file.close() 
        print(file_name + "done")
        time.sleep(random.randint(5,30)) # to not look like a robot


def combine_lyrics(name):
    folder = "lyrics"
    temp = ""
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        file = open(path, 'r')
        temp = temp + file.read() + "\n\n"

    newfile = open(str("%s.txt" %(name)) ,'w') 
    newfile.write(temp) 
    newfile.close() 

def delete_lyrics():
    shutil.rmtree('lyrics')

        
