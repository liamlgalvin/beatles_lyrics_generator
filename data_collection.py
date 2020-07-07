import lyrics_scraper as ls

# scrape azlyrics for beatles
ls.azlyrics_scraper("beatles")
# combine all the lyrics in one text file
ls.combine_lyrics()
# uncomment if you want to delete lyrics files
# ls.delete_lyrics()
