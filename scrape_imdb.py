# %% Import
import bs4 as bs
import urllib.request
import re
import gzip

# %% Find links
source = urllib.request.urlopen('https://datasets.imdbws.com/').read()
soup = bs.BeautifulSoup(source,'lxml')

file_links = []

for url in soup.find_all('a'):
    link = url.get('href')
    if re.search("\.gz$",link) is not None:
      file_links.append(link)

print(file_links)

# %% Download files from links
file_full_paths = []
for link in file_links:
  file_name = re.search(r"[^/]*\.gz$",link)[0]
  file_full_path = os.getcwd() + "/raw_data/" + file_name
  urllib.request.urlretrieve(link, file_full_path)
  file_full_paths.append(file_full_path)
  print(file_full_path)

# %% Extract gz
print(file_full_paths)
extracted_paths = []
for compressed_path in file_full_paths:
  extracted_path = compressed_path[:-3]
  print(extracted_path)
  extracted_paths.append(extracted_path) 
  with gzip.open(compressed_path,"rb") as compressed:
    bindata = compressed.read()
    with open(extracted_path,"wb") as extracted:
      extracted.write(bindata)