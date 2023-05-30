import re
import shutil
from bs4 import BeautifulSoup
import requests

def getAllLinksFromXML(sitemapUrl):
    reqs = requests.get(sitemapUrl)
    soup = BeautifulSoup(reqs.text, features='xml')
    links = re.findall(r'<loc>(.+?)</loc>',soup.prettify().replace("\n","").replace(" ",""))
    return links

def downloadImg(imgurl):
    # download image from url and save it to folder media/images
    r = requests.get(imgurl, stream=True)
    if r.status_code == 200:
        with open('media/images/' + imgurl.split('/')[-1], 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    # return image absolute path
    return 'media/images/' + imgurl.split('/')[-1]
            
def postScraper(url):
    # scrape post title, img link, description
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, features='html.parser')
    title = soup.title.text
    img = soup.find_all('img')[1]['src']
    # get the post description from meta tags
    meta_tags = soup.find_all('meta')
    # print(meta_tags)
    description = None
    for meta_tag in meta_tags:
        if 'property' in meta_tag.attrs and meta_tag.attrs['property'].lower() == 'og:description':
            description =  meta_tag.attrs.get('content')
            
    return title, img, description

if __name__ == "__main__":
    result = downloadImg('https://motozbike.com/wp-content/uploads/2023/05/Adiva-VX-1-2021-0-motozbike.jpg')