# %% Import
import bs4 as bs
import urllib.request
import re
import pandas as pd
import os
from urllib.parse import urljoin

# %% Scrap from BOM
base = 'https://www.boxofficemojo.com/brand/'
source = urllib.request.\
          urlopen(base).\
          read()
soup = bs.BeautifulSoup(source,'lxml')

trs = soup.find_all("tr")

col_names = ["Release",
              "Brand"]
df = pd.DataFrame(columns=col_names)

df_rank = pd.DataFrame(columns = ["Rank","Brand"])

rank = 1
for tr in trs[1:]:
  td = tr.contents[0]
  brand = td.text
  href = td.a["href"]
  join = urljoin(base,href)
  print(brand)
  print(join)

  source_brand = urllib.request.\
                 urlopen(join).\
                 read()
  soup_brand = bs.BeautifulSoup(source_brand,'lxml')

  for tr_brand in soup_brand.find_all("tr")[1:]:
    release = tr_brand.contents[1].text
    df.loc[len(df)] = [release, brand]

  df_rank.loc[len(df_rank)] = [rank, brand]

# %% Write to csv
path = os.getcwd() + "/raw_data/bom_brands.tsv"
df.to_csv(path, sep='\t',index=False)

path = os.getcwd() + "/raw_data/bom_brands_ranks.tsv"
df_rank.to_csv(path, sep='\t',index=False)
