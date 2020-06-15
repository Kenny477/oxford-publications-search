from bs4 import BeautifulSoup
import requests
import re
import wget
import os
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

gauth = GoogleAuth()

gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

folder = ''
file_list = drive.ListFile(
    {'q': "'root' in parents and trashed=false"}).GetList()
for file in file_list:
    if file['title'] == 'oxford-data':
        folder = file['id']

path = "./data/"

page = requests.get("https://www.oxford-man.ox.ac.uk/publications/")
soup = BeautifulSoup(page.text, 'html.parser')

# Query here ("All" for every publication)
search = "All"


def download(link):
    parts = link.split('/')
    title = parts[-1]

    if(not os.path.exists('./data/' + title)):
        wget.download(link, './data/' + title)
        f = drive.CreateFile(
            {'parents': [{"kind": "drive#fileLink", 'id': folder}], 'title': title})
        f.SetContentFile(os.path.join(path, title))
        f.Upload()
        f = None
        os.remove('./data/' + title)
    else:
        print("File exists")


if search == 'All':
    publication_list = soup.find_all(text=re.compile('Download PDF'))
    for pub in publication_list:
        url = pub.parent.attrs['href']
        download(url)
else:
    search_results = soup.find_all(text=re.compile(search))
    for result in search_results:
        container = result.parent.parent.parent.parent
        download_button = container.find(
            text=re.compile('Download PDF')).parent
        url = download_button.attrs['href']
        download(url)
