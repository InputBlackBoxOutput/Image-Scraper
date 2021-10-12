import os 
import glob
import hashlib

# Get the SHA-256 hash of a file
def sha256(fname, size=4096):
 
	sha256_hash = hashlib.sha256()
	with open(fname, 'rb') as f:
		for byte_block in iter(lambda: f.read(4096), b""):
			sha256_hash.update(byte_block)
		
	return sha256_hash.hexdigest()

# Find difference between files using SHA-256 and remove duplicates
def remove_duplicate_images(directory):
	print("\nChecking for duplicate images by comparing SHA-256 hash")
	flag = False

	file_list = glob.glob(f"{directory}/*.png")

	unique = []
	for file in file_list:
		filehash = sha256(file)

		if filehash not in unique:
			unique.append(filehash)
		else:
			print(f"Removing duplicate image: {file}")
			os.remove(file)	
			flag = True
			
	if flag == False:
		print("No duplicate images found")