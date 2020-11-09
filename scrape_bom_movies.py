# %% Import
import bs4 as bs
import urllib.request
import re
import pandas as pd
import os

# %% Setup DataFrame
years = range(1977,2020+1)
col_names = ["Year",
             "Rank",
             "Release_Group",
             "Worldwide",
             "Domestic",
             "Domestic_Percent",
             "Foreign",
             "Foreign_Percent"]

df = pd.DataFrame(columns=col_names)

# %% Scrap from BOM

for year in years:
  print(year)

  source = urllib.request.\
            urlopen('https://www.boxofficemojo.com/year/world/' + str(year) + '/').\
            read()
  soup = bs.BeautifulSoup(source,'lxml')

  trs = soup.find_all("tr")

  for tr in trs:
    if tr.contents[0].name == "td":
      row_data = [year]
      for td in tr.contents:
        row_data.append(td.text)
      df.loc[len(df)] = row_data

# %% Write to csv
path = os.getcwd() + "/raw_data/bom_movies.tsv"
df.to_csv(path, sep='\t',index=False)
