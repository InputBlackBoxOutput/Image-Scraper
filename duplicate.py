import os 
import glob
import hashlib
import imagehash
import numpy as np
import PIL

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


# Get a combined perceptual hashs of a image
def get_perceptual_hash(img_path):
	img = PIL.Image.open(img_path)

	hashes = [
		imagehash.average_hash,
		imagehash.phash,
		imagehash.dhash,
		imagehash.whash,
	]

	combined_hash = np.array([h(img).hash for h in hashes]).flatten()
	combined_hash = np.where(combined_hash==True, 1, 0)

	return combined_hash

# Compare combined perceptual hashs of two images
def compare_hash(hash1, hash2):
	assert len(hash1) == len(hash2)

	count = 0
	for i in range(len(hash1)):
		if hash1[i] == hash2[i]:
			count +=1

	return count/len(hash1)

# Remove similar images using perceptual hashs
def remove_similar_images(directory, similarity_threshold=0.98):
	print("\nChecking for similar images")
	file_list = glob.glob(f"{directory}/*.png")

	found = False
	unique = []
	for file in file_list:
		filehash = get_perceptual_hash(file)

		flag = False
		for each in unique:
			similarity = compare_hash(each, filehash)

			if similarity >= similarity_threshold:
				flag = True
				found = True
				break

		if flag:
			print(f"Removing similar image: {file}")
			os.remove(file)
		else:
			unique.append(filehash)

	if not found:
		print("No similar images found")