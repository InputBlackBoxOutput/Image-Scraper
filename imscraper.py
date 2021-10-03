import os, platform, sys, argparse
import time
import base64
import hashlib
from io import BytesIO
from html.parser import HTMLParser
from urllib.parse import quote, unquote

from selenium import webdriver
from tqdm import tqdm
import urllib3
import PIL.Image as Image

parser = argparse.ArgumentParser(description="Scrape images from the web")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-k', type=str, help="Keyword to search")
group.add_argument('-f', type=str, help="File with list of keywords")
parser.add_argument('-se', type=str, help="Search engine [google, bing, yahoo, duckduckgo, all] (default=all)", default="all")
parser.add_argument('-n', type=int, help="Number of images per keyword. Downloads all images by default", default=None)
parser.add_argument('-p', type=str, help="Keyword prefix", default=None)
parser.add_argument('-s', type=str, help="Keyword suffix", default=None)
parser.add_argument('-o', type=str, help="Output directory", default=None)
args = parser.parse_args()

# Get the SHA-256 hash of a file
def sha256(fname, size=4096):
 
	sha256_hash = hashlib.sha256()
	with open(fname, 'rb') as f:
		for byte_block in iter(lambda: f.read(4096), b""):
			sha256_hash.update(byte_block)
		
	return sha256_hash.hexdigest()

# Find difference between files using SHA-256 and remove duplicates
def remove_duplicate_images(dir):
	print("\nChecking for duplicate images by comparing SHA-256 hash")
	flag = False

	fileList = list(os.walk(dir))[0][-1]

	unique = []
	for file in fileList:
		filepath = os.path.join(dir, file)
		filehash = sha256(filepath)

		if filehash not in unique:
			unique.append(filehash)
		else:
			print(f"Removing duplicate image: {filepath}")
			os.remove(filepath)	
			flag = True
			
	if flag == False:
		print("No duplicate images found")	

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
	try:
		if out_dir == None:
			os.mkdir(keyword)		
		else:
			# If output directory does not exist create it
			try:
				os.mkdir(out_dir)
			except:
				pass

			os.mkdir(f"{out_dir}/{keyword}")

	except FileExistsError:
		pass

def add_prefix_suffix(keyword, prefix=None, suffix=None):
	if prefix != None:
		keyword = prefix + " " + keyword

	if suffix != None:
		keyword = keyword + " " + suffix
	
	return keyword

# Search for the specified keyword using the specified search engine, load the url on chrome using chromedriver, extract certain attribute values and then collect the images
def scrape_images(keyword, search_engine, output_directory, num_images=None):		
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
	browser.get_log('browser')
	time.sleep(1)

	extractor.src = []

	if search_engine == "google":
		extractor.tag_attr = "data-src"
		extractor.feed(browser.page_source)
		
		extractor.tag_attr = "src"
		extractor.feed(browser.page_source)

	elif search_engine == "bing":
		extractor.tag_attr = "src2"
		extractor.feed(browser.page_source)

		extractor.src = list(map(lambda x: x.split('&')[0], extractor.src))
		extractor.src = list(set(extractor.src))

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
			if "https://" in each_src:
				response = http.request('GET', each_src)
				img_data = BytesIO(response.data)
			else:
				img_data = base64.b64decode(each_src.split(',')[-1])
				img_data = BytesIO(img_data)

			image = Image.open(img_data).convert("RGBA")
			image.save(f"{output_directory}/{search_engine[0]}-{count+1}.png")
			
		except:
			pass

		count+=1

	print(f"Downloaded {count}/{num_images} images")


def main(keyword, search_engine, out_dir, num_images):
	print('\n' + '-' * 100)
	print(f"Keyword: {keyword}")

	create_output_directory(keyword, out_dir)
	output_directory = keyword if out_dir == None else f"{out_dir}/{keyword}"

	if search_engine != "all":
		scrape_images(keyword=keyword, search_engine=search_engine, output_directory=output_directory, num_images=num_images)
	else:
		for each_se in ['google', 'bing', 'yahoo', 'duckduckgo']:
			scrape_images(keyword=keyword, search_engine=each_se, output_directory=output_directory, num_images=num_images)
		
	remove_duplicate_images(output_directory)
	print('-' * 100)

if __name__ == "__main__":
	browser = setup_browser()
	extractor = Extractor()
	http = urllib3.PoolManager()

	if args.se not in ['google', 'bing', 'yahoo', 'duckduckgo', 'all']:
		print("Search engine needs to be one of the following: google, bing, yahoo, duckduckgo or all")
		sys.exit()

	if args.f == None:
		keyword = add_prefix_suffix(args.k, prefix=args.p, suffix=args.s)
		main(keyword, args.se, args.o, args.n)
		
	else:
		try:
			with open(args.f, 'r') as infile:
				keywords = infile.read().splitlines()

				for each in keywords:
					if each != "":
						keyword = add_prefix_suffix(each, prefix=args.p, suffix=args.s)
						main(keyword, args.se, args.o, args.n)

		except FileNotFoundError:
			print(f"\nFile not found: {args.f}")
			sys.exit()
		except:
			print("\nSomething went wrong!")
			sys.exit()

	browser.quit()
