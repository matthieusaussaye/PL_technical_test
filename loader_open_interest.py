from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import pandas as pd

url = "https://www.cftc.gov/dea/futures/electricity_sf.htm"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out
# get text
text = soup.get_text()
# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

with open('html_text.txt', 'w') as f:
    for line in text:
        f.write(line)

with open('html_text.txt', 'r') as fi, open('filtered_text.txt', 'w') as new_file :
    copy_bool = False

    for line in fi:
        
        if ': Positions' in line :
            copy_bool = False

        if copy_bool and '----' not in line and 'CFTC Code' not in line and 'Open Interest is' not in line : 
            new_file.write(line.strip())

        elif ':Spreading :' in line :
            copy_bool = True
    
            
    new_file.close()
    fi.close()

with open('filtered_text.txt', 'r') as f1 :
    items=f1.readlines()[0][:-1].split(':') # remove the last blank line
    f1.close()

os.remove('filtered_text.txt')
os.remove('html_text.txt')


dict_CFTC = {'contract' : [items[k] for k in range(len(items)) if k%2==0], 
             'open_interest' : [int(items[k].replace(',','',1)) for k in range(len(items)) if k%2==1]}

#Save as csv
pd.DataFrame.from_dict(dict_CFTC).to_csv('CFTC.csv',index=False)

with open('CFTC.csv', 'r') as f2 :
    for line in f2 :
        print(line.replace('"',''))
