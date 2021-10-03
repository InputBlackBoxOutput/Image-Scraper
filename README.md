## Features
1. Images are searched on the web using the following search engines: Google, Bing, Yahoo and DuckDuckGo
1. A file containing a list of keywords can be passed to the program when multiple keywords need to be scraped
1. A new directory is created for every keyword
1. A prefix and/or a suffix can be added to all the keywords passed to the program via a file
1. Duplicate images are found by comparison of SHA-256 hash and removed

## How to use the scraper?
```
usage: imscraper.py [-h] (-k K | -f F) [-se SE] [-n N] [-p P] [-s S] [-o O]

-k K        Keyword to search
-f F        File with list of keywords
-se SE      Search engine [google, bing, yahoo, duckduckgo, all] (default=all)
-n N        Number of images per keyword. Downloads all images by default
-p P        Keyword prefix
-s S        Keyword suffix
-o O        Output directory
-h, --help  Show help message and exit
```

[Read a detailed manual](https://rutuparn.medium.com/9cf9a5950594?source=friends_link&sk=7e353dd0ffe00a765d97fd508656fc61)

## Run the scraper on the cloud
|Platform|Notebook link|
|--|--|
|Google Colab|https://colab.research.google.com/drive/1ZnuGgv5KI5-EXaAnpXHB7q--osSOQWER?usp=sharing|
|Kaggle|https://www.kaggle.com/inputblackboxoutput/image-scraper|

### Disclaimer
It is advised to use this image scraper for learning/research purposes only.

Under no circumstances will the creator/s of this application be held responsible or liable in any way for any claims, damages, losses, expenses, costs or liabilities whatsoever (including, without limitation, any direct or indirect damages for loss of profits, business interruption or loss of information) resulting or arising directly or indirectly from your use of or inability to use this application even if the creator/s of this application have been advised of the possibility of such damages in advance.

### Made with lots of ⏱️, 📚 and ☕ by InputBlackBoxOutput

