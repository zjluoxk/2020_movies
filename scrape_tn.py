# %% Import
import bs4 as bs
import urllib.request
import re
import pandas as pd
import os
from urllib.parse import urljoin

# %% Scrap from BOM
base = 'https://www.the-numbers.com/movie/budgets/all'

rank = 1

col_names = ["Date","Movie", "Budget", "Domestic", "Worldwide"]
df = pd.DataFrame(columns=col_names)

while(True):
  print(rank)
  if rank == 1:
    addon = ""
  else:
    addon = "/" + str(rank)
  url = base + addon
  req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  source = urllib.request.urlopen(req).read()
  soup = bs.BeautifulSoup(source,'lxml')
    
  trs = soup.find_all("tr")

  if len(trs) < 2: break

  for tr in trs[1:]:
    date = tr.contents[2].text
    movie = tr.contents[4].text
    budget = tr.contents[6].text
    domestic = tr.contents[8].text
    worldwide = tr.contents[10].text
    df.loc[len(df)] = [date, movie, budget, domestic, worldwide]

  rank += 100

# %% Write to csv
path = os.getcwd() + "/raw_data/tn_movie_budgets.tsv"
df.to_csv(path, sep='\t',index=False)
