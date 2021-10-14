import os, platform, sys, argparse
import time
import base64
from io import BytesIO
from html.parser import HTMLParser
from urllib.parse import quote, unquote, urlparse

from selenium import webdriver
from tqdm import tqdm
import urllib3
import PIL.Image as Image

import duplicate

# Instantiate and connect to the chrome driver 
def setup_browser():
	operating_system = platform.system()

	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument("--log-level=3")

	if operating_system == 'Linux':
		browser = webdriver.Chrome("./chrome-driver/chrome-driver-linux64", options=options)
	elif operating_system == 'Windows':
		browser = webdriver.Chrome("./chrome-driver/chrome-driver-win32.exe", options=options)
	elif  operating_system == 'Darwin':
		browser = webdriver.Chrome("./chrome-driver/chrome-driver-mac64", options=options)
	else:
		raise Exception("The operating system could not be determined")

	return browser

# Class to extract the value of specific HTML tag attribute
class Extractor(HTMLParser):
  src = []
  tag_attr = None
  def handle_starttag(self, tag, attrs):
    if tag == "img":
      for each in attrs:
        if each[0] == self.tag_attr:
          self.src.append(each[1])

# Create output directory if it does not exist
def create_output_directory(keyword, out_dir=None):
	if out_dir == None:
		os.makedirs(keyword, exist_ok=True)		
	else:
		os.makedirs(out_dir, exist_ok=True)
		os.makedirs(f"{out_dir}/{keyword}", exist_ok=True)

def add_prefix_suffix(keyword, prefix=None, suffix=None):
	if prefix != None:
		keyword = prefix + " " + keyword

	if suffix != None:
		keyword = keyword + " " + suffix
	
	return keyword

def filter_src_format(src_list):
	filtered = []

	for each_src in src_list:
		if ".png" in each_src or ".jpg" in each_src or ".jpeg" in each_src:
			filtered.append(each_src)
		elif "/png" in each_src or "/jpg" in each_src or "/jpeg" in each_src:
			filtered.append(each_src)
		elif "https:" in each_src:
			filtered.append(each_src)
		else:
			continue

	return filtered


def get_img_data(url, src):
	if "https:" in src or "www." in src:
		response = http.request('GET', src)
		img_data = BytesIO(response.data)

	elif src.endswith(".png") or src.endswith(".jpg"):
		base_url = urlparse(url).netloc
		src = base_url + src

		response = http.request('GET', src)
		img_data = BytesIO(response.data)

	else:
		src = src.split(',')[-1]
		img_data = base64.b64decode(src)
		img_data = BytesIO(img_data)

	return img_data

# Search for the specified keyword using the specified search engine, load the url on chrome 
# using chromedriver, extract certain attribute values and then collect the images
def scrape_images_search_engine(keyword, search_engine, output_directory, num_images=None):		
	print(f"\nSearch engine: {search_engine}")

	search_engine_urls = {
		"google" : f"https://www.google.com/search?tbm=isch&q={quote(keyword)}",
		"bing" : f"https://www.bing.com/images/search?q={quote(keyword)}",
		"yahoo" : f"https://images.search.yahoo.com/search/images?p={quote(keyword)}",
		"duckduckgo": f"https://duckduckgo.com/?q={quote(keyword)}&iax=images&ia=images"
	}
	url = search_engine_urls[search_engine]
	print(f"URL: {url}")

	browser.get(url)
	time.sleep(2)

	scroll_count = {"google": 3, "bing": 3, "yahoo": 1, "duckduckgo": 5}
	for _ in range(scroll_count[search_engine]):
		browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
		browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
		time.sleep(2)

	extractor.src = []

	if search_engine == "google":
		extractor.tag_attr = "data-src"
		extractor.feed(browser.page_source)
		
		extractor.tag_attr = "src"
		extractor.feed(browser.page_source)

	elif search_engine == "bing":
		extractor.tag_attr = "src"
		extractor.feed(browser.page_source)

		extractor.src = list(map(lambda x: x.split('?w')[0], extractor.src))
		extractor.src = list(set(extractor.src))

		extractor.src = filter_src_format(extractor.src)

		filtered = []
		for each in extractor.src:
			if "OIP" in each:
				filtered.append(each)

		extractor.src = filtered	
		
	elif search_engine == "yahoo":
		extractor.tag_attr = "src"
		extractor.feed(browser.page_source)

		extractor.src = list(map(lambda x: x.split('&')[0], extractor.src))
		extractor.src = list(set(extractor.src))

	elif search_engine == "duckduckgo":
		extractor.tag_attr = "src"
		extractor.feed(browser.page_source)

		extractor.src = list(map(lambda x: unquote(x.split('?')[-1][2:]), extractor.src))

	len_src = len(extractor.src)
	print(f"Number of images found: {len_src}")

	if num_images != None:
		src_list = extractor.src[:num_images]
	else:
		src_list = extractor.src

	count = 0
	for each_src in tqdm(src_list):
		try:
			img_data = get_img_data(url, each_src)

			image = Image.open(img_data).convert("RGBA")
			image.save(f"{output_directory}/{search_engine[0]}-{count+1}.png")
				
			count+=1

		except:
			print(f"Something went wrong while scraping the image at URL:\n{each_src}")

	if num_images != None:
		print(f"Downloaded {count}/{num_images} images")
	else:
		print(f"Downloaded {count}/{len_src} images")


def search_scrape(keyword, search_engine, out_dir, num_images):
	print('\n' + '-' * 80)
	print(f"Keyword: {keyword}")

	create_output_directory(keyword, out_dir)
	output_directory = keyword if out_dir == None else f"{out_dir}/{keyword}"

	if search_engine != "all":
		scrape_images_search_engine(keyword=keyword, search_engine=search_engine, output_directory=output_directory, num_images=num_images)
	else:
		if num_images != None:
			num_images = [num_images // 4 + (1 if x < num_images % 4 else 0)  for x in range (4)]
			for i, each_se in enumerate(['google', 'bing', 'yahoo', 'duckduckgo']):
				scrape_images_search_engine(keyword=keyword, search_engine=each_se, output_directory=output_directory, num_images=num_images[i])
		else:
			for each_se in ['google', 'bing', 'yahoo', 'duckduckgo']:
				scrape_images_search_engine(keyword=keyword, search_engine=each_se, output_directory=output_directory, num_images=num_images)
		
	duplicate.remove_duplicate_images(output_directory)
	duplicate.remove_similar_images(output_directory, similarity_threshold=0.90)

	print(f"\nImages saved in directory: {output_directory} ")
	print('-' * 80)


def scrape_images_custom(url, output_directory, num_images=None):	
	os.makedirs(output_directory, exist_ok=True)

	browser.get(url)
	time.sleep(2)
	
	extractor.tag_attr = "src"
	extractor.feed(browser.page_source)

	len_src = len(extractor.src)
	print(f"Number of images found: {len_src}")

	if num_images != None:
		src_list = extractor.src[:num_images]
	else:
		src_list = extractor.src

	src_list = filter_src_format(src_list)

	count = 0
	for each_src in tqdm(src_list):
		try:
			img_data = get_img_data(url, each_src)

			image = Image.open(img_data).convert("RGBA")
			image.save(f"{output_directory}/{count+1}.png")

			count+=1
		except:
			print(f"Something went wrong while scraping the image at URL:\n{each_src}")

	if num_images != None:
		print(f"Downloaded {count}/{num_images} images")
	else:
		print(f"Downloaded {count}/{len_src} images")

if __name__ == "__main__":
	browser = setup_browser()
	extractor = Extractor()
	http = urllib3.PoolManager()

	parser = argparse.ArgumentParser(description="Scrape images from the web")
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument('-k', type=str, help="Keyword to search")
	group.add_argument('-f', type=str, help="File with list of keywords")
	group.add_argument('-c', type=str, help="Custom URL")
	parser.add_argument('-se', type=str, help="Search engine [google, bing, yahoo, duckduckgo, all] (default=all)", default="all")
	parser.add_argument('-n', type=int, help="Number of images per keyword. Downloads all images by default", default=None)
	parser.add_argument('-p', type=str, help="Keyword prefix", default=None)
	parser.add_argument('-s', type=str, help="Keyword suffix", default=None)
	parser.add_argument('-o', type=str, help="Output directory", default=None)
	args = parser.parse_args()	

	if args.c:
		if args.o == None:
			args.o = "custom"
		
		scrape_images_custom(args.c, args.o, args.n)
		print(f"\nImages saved in directory: {args.o}")

		sys.exit()

	if args.se not in ['google', 'bing', 'yahoo', 'duckduckgo', 'all']:
		print("Search engine needs to be one of the following: google, bing, yahoo, duckduckgo or all")
		sys.exit()

	if args.f == None:
		try:
			keyword = add_prefix_suffix(args.k, prefix=args.p, suffix=args.s)
			search_scrape(keyword, args.se, args.o, args.n)
		except:
			print("Something went wrong!")
			sys.exit()
	else:
		try:
			with open(args.f, 'r') as infile:
				keywords = infile.read().splitlines()

				for each in keywords:
					if each != "":
						keyword = add_prefix_suffix(each, prefix=args.p, suffix=args.s).strip()
						search_scrape(keyword, args.se, args.o, args.n)

		except FileNotFoundError:
			print(f"\nFile not found: {args.f}")
			sys.exit()
		except:
			print("\nSomething went wrong!")
			sys.exit()

	browser.quit()
