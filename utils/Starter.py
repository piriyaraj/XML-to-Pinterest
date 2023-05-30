import os
import json
from utils.Autoposter import Autoposter
from utils.Database import Database

from utils.Scrapper import downloadImg, getAllLinksFromXML, postScraper

class Starter:
    def __init__(self) -> None:
        self.sitemap = ""
    def getSitemap(self):
        config_file = "src/config.json"

        if not os.path.exists(config_file):
            self.getData()
            config_data = {
                "sitemap": self.sitemap,
                "username": self.username,
                "password": self.password
            }
            with open(config_file, 'w') as file:
                json.dump(config_data, file, indent=4)
            print(f"The '{config_file}' file has been created.")
            return self.sitemap, self.username, self.password
        else:
            self.readConfig(config_file)
            print(f"The '{config_file}' file already exists.")
            return self.sitemap, self.username, self.password

    def getData(self):
        sitemap = input("Enter the XML: ")
        self.sitemap = sitemap
        self.username = input("Enter the username:")
        self.password = input("Enter the password:")

    def readConfig(self, config_file):
        with open(config_file, 'r') as file:
            config_data = json.load(file)
            self.sitemap = config_data.get("sitemap")
            self.username = config_data.get("username")
            self.password = config_data.get("password")
            if(self.sitemap is None):
                self.getData()
                config_data = {
                    "sitemap": self.sitemap,
                    "username": self.username,
                    "password": self.password
                }
                with open(config_file, 'w') as file:
                    json.dump(config_data, file, indent=4)

def main(noOfPost: int):
    # get sitemap data from config file / set sitemap
    starter = Starter()
    sitemap, username, password = starter.getSitemap()
    # extract sitemap and get post links
    urls = getAllLinksFromXML(sitemap)
    # save links in database
    database = Database()
    database.setUrls(urls)
    
    # initiate autoposter
    autoPost = Autoposter(username,password)
    autoPost.start()
    for i in range(noOfPost):
        # get a post link from database
        post_link = database.getALink()
        
        # extract the post link data
        title, imgUrl, description = postScraper(post_link)
        
        # download the image
        path = downloadImg(imgUrl)
    
        autoPost.createPin(os.path.abspath(path),title,description,post_link,title,"MotoZbike")
        
        # set post as posted
        database.setALink(post_link)


if __name__ == "__main__":
    starter = Starter()
    starter.createConfig()
    # https://groupsor.link/seo/sitemap.xml