import bs4 as bs
import requests

def get_and_write(url,f_path):
    r= requests.get(url)
    with open(f_path,'w', encoding='utf-8') as f:
        f.write(r.text)

url  =  'https://onlinecourses.nptel.ac.in/noc25_cs20/unit?unit=21&lesson=27'

get_and_write(url,'nptel.html')