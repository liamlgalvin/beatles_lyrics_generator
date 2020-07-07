# beatles_lyrics_generator

A silly little project that generates beatles style lyrics, with an ABCB rhyming pattern using deep learning.
The results are far from perfect but it is an interesting little project and it is funny to see the resulting songs.

## Getting Started

- song lyrics to train the model are scraped by running data_collection.py 
- to build the model run beatles.py
- to make a song using model use make_song.py

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

uses code following code for the model generation
https://github.com/jeffheaton/t81_558_deep_learning/blob/master/t81_558_class_10_3_text_generation.ipynb

uses big phoney to analyze the phonetics and syllables of the lyrics
https://github.com/repp/big-phoney
