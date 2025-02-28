#go with <div id="video-transcript-div"> and then follow up with the tiuimestamp based scraping
#single transcript file for each lecture

from bs4 import BeautifulSoup
import requests
#update the file name as and when required.
with open ('lecture-11.html','r',encoding='utf-8') as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')
#print(soup.prettify()) --> no need to print the soup contents 

transcript_divs = soup.select("#video-transcript-div div")

transcript_text = "\n".join(div.get_text(" ", strip=True) for div in transcript_divs)

with open ("response_files/script.txt",'w',encoding = 'utf-8') as f:
    f.write(transcript_text)