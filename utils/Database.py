import os
import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.db_file = "src/urls.sqlite"
        self.createDatabase()

    def createDatabase(self):
        if not os.path.exists(self.db_file):
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute('''CREATE TABLE urls
                         (url TEXT UNIQUE, posted BOOLEAN DEFAULT 0, date_time DATETIME DEFAULT NULL)''')
            conn.commit()
            conn.close()
            print(f"The '{self.db_file}' database has been created.")
        else:
            print(f"The '{self.db_file}' database already exists.")

    def setUrls(self, urlList):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        for url in urlList:
            c.execute("INSERT OR IGNORE INTO urls (url) VALUES (?)", (url,))
        conn.commit()
        conn.close()
        print("URLs have been added to the database.")

    def getALink(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT url FROM urls WHERE posted = 0 LIMIT 1")
        link = c.fetchone()
        if link:
            return link[0]
        else:
            return None

    def setALink(self, link):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("UPDATE urls SET posted = 1, date_time = ? WHERE url = ?", (datetime.now(), link))
        conn.commit()
        conn.close()
        print(f"The link '{link}' has been updated.")

if __name__ == "__main__":
    # Create an instance of the Database class
    db = Database()

    db.setALink("https://motozbike.com/")