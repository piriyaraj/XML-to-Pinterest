"""
This module provides a Browser class that can be used to automate pin creation on Pinterest. 

It requires the selenium package and a ChromeDriverManager to be installed.

Example usage:

    browser = Browser(username='myusername', password='mypassword')
    browser.start()
    browser.createPin(image='path/to/image.jpg', title='My Pin', 
    description='A description of my pin', destinationLink='https://example.com')
"""

import json
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

pinterest_home = "https://www.pinterest.com/"
pre_login_button = '/html/body/div[1]/div/div[1]/div/div/div/div/div/div[1]/div/div/div[1]/div/div[2]/div[2]/button/div/div'
login_button = "//button[@type='submit']"
pin_builder = "https://www.pinterest.com/pin-builder/"
pin_name = "//*[starts-with(@id, 'pin-draft-title-')]"
pin_description = "//*[starts-with(@id, 'pin-draft-description-')]/div/div/div/div/div/div/div/div/span/br"
image_input = "//*[starts-with(@id, 'media-upload-input-')]"
pin_link = "//*[starts-with(@id, 'pin-draft-link-')]"
drop_down_menu = "//button[@data-test-id='board-dropdown-select-button']"
publish_button = "//button[@data-test-id='board-dropdown-save-button']"


class Autoposter:

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def __login(self):
        # Open Pinterest on Chrome Driver
        self.driver.get(pinterest_home)
        time.sleep(30)

        # Click log in link
        self.driver.find_element(By.XPATH, pre_login_button).click()
        time.sleep(3)

        # Log in
        user = self.driver.find_element(By.NAME, "id")
        user.send_keys(self.username)
        time.sleep(3)
        pas = self.driver.find_element(By.NAME, "password")
        pas.send_keys(self.password)
        time.sleep(3)
        self.driver.find_element(By.XPATH, login_button).click()
        time.sleep(3)

    def start(self):

        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        # maximize browser
        self.driver.maximize_window()
        self.__login()

    def createPin(self, image: str, title: str, description: str, destinationLink: str, imageAlt: str, boardName: str):
        """
        Creates a new pin on Pinterest using the provided image, title, description, destination link,
        image alt text, and board name.

        Args:
            image (str): The file path to the image to use for the pin.
            title (str): The title to use for the pin.
            description (str): The description to use for the pin.
            destinationLink (str): The destination link to use for the pin.
            imageAlt (str): The alt text to use for the pin image.
            boardName (str): The name of the board to save the pin to.

        Returns:
            None: This method does not return anything, but creates a new pin on the Pinterest account.
        """
        # Navigate to the pin builder page
        self.driver.get(pin_builder)
        time.sleep(10)
        if (self.driver.current_url != pin_builder):
            self.driver.get(pin_builder)
            time.sleep(10)

        # Upload the image
        imgUpload = self.driver.find_element(By.XPATH, '//input[@type="file"]')
        time.sleep(1)
        imgUpload.send_keys(image)
        time.sleep(10)
        print("=====> image uploaded")
        # Enter the pin title
        pinTitleTag = self.driver.find_element(By.XPATH, pin_name)
        pinTitleTag.send_keys(title[:40])
        time.sleep(10)
        print("=====> title posted")

        # Enter the pin description
        pinDescriptionTag = self.driver.find_element(By.XPATH, pin_description)
        actions = ActionChains(self.driver)
        # pinDescriptionTag.send_keys(description)
        actions.move_to_element(pinDescriptionTag).click().send_keys(description[:500]).perform()
        print("=====> description posted")

        # Add alt
        pinAltTag = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/div[4]/div/button/div/div")
        print(pinAltTag.get_attribute('class'))
        pinAltTag.click()
        time.sleep(10)
        # pinAltTag1 = self.driver.find_element(By.XPATH, '//*[@id="pin-draft-alttext-26ef1a63-cc14-4f7b-96bf-aaeeb9d1f2ae"]')
        pinAltTag1 = self.driver.find_element(By.XPATH, "//*[starts-with(@id, 'pin-draft-alttext-')]")
        print(pinAltTag1.get_attribute('placeholder'))
        pinAltTag1.send_keys(imageAlt[:500])
        time.sleep(10)

        # Select a board to save the pin to
        # dropdown_menu = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/button[1]')
        dropdown_menu = self.driver.find_element(By.XPATH, '//button[@data-test-id="board-dropdown-select-button"]')
        dropdown_menu.click()
        print("=====> Dropdown clicked")
        time.sleep(10)
        option = self.driver.find_element(By.XPATH, '//div[contains(text(), "'+boardName+'")]')
        option.click()
        print("=====> Board selected")

        time.sleep(10)

        # Enter the pin destination link
        pinLinkTag = self.driver.find_element(By.XPATH, pin_link)
        pinLinkTag.send_keys(destinationLink)
        time.sleep(10)
        print("=====> Link posted")

        # Publish the pin
        pinPublishTag = self.driver.find_element(By.XPATH, publish_button)
        print(pinPublishTag.get_attribute('class'))
        pinPublishTag.click()
        time.sleep(10)


# test code
if __name__ == "__main__":
    username = ""
    password = ""
    autoposter = Autoposter(username, password)
    autoposter.start()
    autoposter.createPin(
        "D:\Bots\XML to pintrest\media\images\Adiva-VX-1-2021-0-motozbike.jpg",
        "test title",
        "test description",
        "https://www.google.com",
        "test alt",
        "MotoZbike"
    )