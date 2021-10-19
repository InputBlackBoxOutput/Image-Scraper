# Image-Scraper

![](demo.gif)

## Salient features
- Images are searched on the web using the following search engines: Google, Bing, Yahoo and DuckDuckGo
- A file containing a list of keywords can be passed to the program when multiple keywords need to be scraped
- Images from a custom URL can be scraped
- A new directory is created for every keyword
- A prefix and/or a suffix can be added to all the keywords passed to the program via a file
- Duplicate images are found by comparison of SHA-256 hash and then removed
- Similar images are found using perceptual hashing and then removed


## How to use the scraper?
```text
usage: imscraper.py [-h] (-k K | -f F | -c C) [-se SE] [-n N] [-p P] [-s S] [-st ST] [-o O]

-h, --help  show this help message and exit
-k K        Keyword to search
-f F        File with list of keywords
-c C        Custom URL
-se SE      Search engine [google, bing, yahoo, duckduckgo, all] (default=all)
-n N        Number of images per keyword. Downloads all images by default
-p P        Keyword prefix
-s S        Keyword suffix
-st ST      Similarity threshold (default = 98 percent)
-o O        Output directory
```

[Read a detailed manual](https://rutuparn.medium.com/9cf9a5950594?source=friends_link&sk=7e353dd0ffe00a765d97fd508656fc61)

## Run the scraper on the cloud
|Platform|Notebook link|
|--|--|
|Google Colab|https://colab.research.google.com/drive/1ZnuGgv5KI5-EXaAnpXHB7q--osSOQWER?usp=sharing|
|Kaggle|https://www.kaggle.com/inputblackboxoutput/image-scraper|

### Disclaimer
It is advised to use this image scraper for academic or research purposes only.


Under no circumstances will the creator/s of this application be held responsible or liable in any way for any claims, damages, losses, expenses, costs or liabilities whatsoever (including, without limitation, any direct or indirect damages for loss of profits, business interruption or loss of information) resulting or arising directly or indirectly from your use of or inability to use this application even if the creator/s of this application have been advised of the possibility of such damages in advance.

### Made with lots of ⏱️, 📚 and ☕ by InputBlackBoxOutput

