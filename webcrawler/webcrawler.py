import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

class Snail():
    """
    Snail that crawls KUSSS and collects data
    """
    base_url = "https://www.kusss.jku.at/kusss/"
    def __init__(self):
        pass
    
    ####### Basic Methods #######
    def crawl_and_extract(self, url):
        """
        Crawls the given URL and extracts the data
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    
    def search_html(self, soup, tag, attributes=None, all=True):
        """
        Searches the given soup for the given tag and class_name
        """
        if all:
            return soup.find_all(tag, attrs=attributes)
        else:
            return soup.find(tag, attrs=attributes)


    ######### Methods for KUSSS #########
    #https://www.kusss.jku.at/kusss/coursecatalogue-start.action
    def get_course_catalogue(self):
        """
        Returns the course catalog
        """
        url = self.base_url + "coursecatalogue-start.action"
        soup = self.crawl_and_extract(url)
        return soup   
    
    def get_detailed_course_catalogue(self):
        """
        Returns the detailed course catalog
        """
        #coursecatalogue-start.action?advanced=true
        url = self.base_url + "coursecatalogue-start.action" + "?advanced=true"
        soup = self.crawl_and_extract(url)
        return soup
    
    
    
    