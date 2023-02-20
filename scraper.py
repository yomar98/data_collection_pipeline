from select import select
from unicodedata import name
from urllib import request
from warnings import filters 
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from typing import List
import pandas as pd
import urllib
import os  
import json

class Scraper: 
    """
    A web scraper class that navigates to a given URL and performs a search on the page.

    Attributes:
        driver (webdriver): An instance of the Chrome webdriver.
        url (str): The URL to navigate to. Default is 'https://www.prodirectsport.com/rugby/'.
    """

    def __init__(self, url: str = 'https://www.prodirectsport.com/rugby/' ):
        """
        Initializes the Scraper class by launching a Chrome browser and navigating to the given URL.

        Args:
            url (str): The URL to navigate to. Default is 'https://www.prodirectsport.com/rugby/'.
        """
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get(url)
        time.sleep(10)

    def search_boots(self):
        """
        Performs a search for 'boots' on the website by finding the search bar, inputting the word 'boots', and clicking the return button to get the search results.
        """
        search = self.driver.find_element_by_xpath('/html/body/header/div[1]/div/div/div[1]/div[2]/input') 
        search.send_keys('boots') 
        search.send_keys(Keys.RETURN) 
        time.sleep(3)
    
    def open_all_boots_page(self):
        """
        Opens the page for all boots by selecting the 'boots' tab in the filters section and getting the href.
        """
        all_boots = self.driver.find_element(by=By.XPATH, value='/html/body/main/section[2]/section/div[2]/ul/li[1]/div/ul/li[1]/a')
        boots_link = all_boots.get_attribute('href')
        self.driver.get(boots_link)

    def get_boots_links(self):
        """
        Retrieves the links for all boots on the page.

        The function first selects the container where all the boots are located. Within that container, it selects the grid where the boots are located. Then, it creates an empty list to store the list of links for each boot, without pressing into them individually.

        Returns:
            list: A list of links to all boots on the page.
        """
        container = self.driver.find_element_by_xpath('/html/body/main/section[2]/section/div[3]/div[1]')
        boots_list = container.find_elements_by_xpath('//div[contains(@class, "lister-grid__item")]')
        links = []
        for boots in boots_list:
            a_tag = boots.find_element_by_tag_name('a')
            boots_link = a_tag.get_attribute('href')
            links.append(boots_link)

        return links

    def next_page(self):
        """
        Navigates to the next page of results.

        The function finds the container where the 'next' button is located. Within the container, it selects the 'next' button by xpath and retrieves the link for the next page. The function then navigates to the next page using the retrieved link.

        Returns:
            None
        """
        container = self.driver.find_element_by_xpath('/html/body/main/section[2]/section/div[3]/div[1]')
        next_page_button = container.find_element(by=By.XPATH, value='//a[contains(@class, "pagination__next")]')
        next_page_link = next_page_button.get_attribute('href')
        self.driver.get(next_page_link)
    
    def get_all_links(self):
        """
        Get all the boots links from the website by iterating through all the pages.

        Returns:
        List: A list of all the boots links on the website.
        """
        self.all_links = []
        self.all_links.extend(self.get_boots_links())
        for x in range(0, 2):
            self.next_page()
            self.all_links.extend(self.get_boots_links())
        
        return self.all_links

    def details_of_boots_from_links(self):
        """
        This function scrapes the details of the boots from the links obtained by the `get_all_links` function.
        It iterates through each link, retrieves the boot details (name, colour, price and images), and appends it to a list.
        The lists are then used to create a pandas dataframe and the dataframe is saved to a csv file.
    
        Returns:
        boot_info_df (DataFrame): A pandas dataframe containing the details of the boots.
        """
        names = []
        colours = []
        prices = []
        images = []

        for link in self.all_links[0:2]:
            self.driver.get(link)
            container_containing_description = self.driver.find_element_by_xpath('/html/body/main')
            try: 
                boots_details_container = container_containing_description.find_element(by=By.XPATH, value='/html/body/main/div[1]/div[1]') 
                boot_name = boots_details_container.find_element(by=By.XPATH, value='//h1[@class="ml-meta__title"]').text
            except:
                print('error name')
            
            try:
                boot_colour = boots_details_container.find_element(by=By.XPATH, value='//div[@class="ml-meta__colourway"]').text
            except:
                print('error colour')

            try:
                boot_price = boots_details_container.find_element(by=By.XPATH, value='//div[@class="ml-prices__price"]').text
            except:
                print('error price')

            try:
                boot_images = boots_details_container.find_element(by=By.XPATH, value='//div[@class="ml-gallery__image ml-gallery__image--main lazyloaded"]')
            except:
                print('error images')
            
            names.append(boot_name)
            colours.append(boot_colour)
            prices.append(boot_price)
            images.append(boot_images)

        boot_info_df = pd.DataFrame( {
            'boot_name': names,
            'boot_colour': colours,
            'boot_price': prices,
            'boot_images': images
            })

        boot_info_df.to_csv

        print(boot_info_df)

        

if __name__ == '__main__':
    prodirect_rugby = Scraper() 
    prodirect_rugby.search_boots()
    prodirect_rugby.open_all_boots_page()
    prodirect_rugby.get_boots_links()
    prodirect_rugby.get_all_links()
    prodirect_rugby.details_of_boots_from_links()
    prodirect_rugby.driver.quit()

    """
    Main function to run the Scraper class

    Instantiates an object of the Scraper class as prodirect_rugby
    Calls the search_boots method to initiate a search for rugby boots on the website
    Calls the open_all_boots_page method to open the page containing all the boots
    Calls the get_boots_links method to get the links for all the boots on the current page
    Calls the get_all_links method to get the links for all the boots for all pages
    Calls the details_of_boots_from_links method to scrape the details of each boots including name, colour, price and images
    Calls the quit method on the driver to close the web browser.
    """