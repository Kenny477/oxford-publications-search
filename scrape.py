from bs4 import BeautifulSoup
import requests
import re
import wget
import os

page = requests.get("https://www.oxford-man.ox.ac.uk/publications/")
soup = BeautifulSoup(page.text, 'html.parser')

search = "Mixture Density"

search_results = soup.find_all(text=re.compile(search))
for result in search_results:
    container = result.parent.parent.parent.parent
    download_button = container.find(text=re.compile('Download PDF')).parent
    link = download_button.attrs['href']

    parts = link.split('/')
    title = parts[-1]

    if(not os.path.exists('./data/' + title)):
        wget.download(link, './data/' + title)
    else:
        print("File exists")
