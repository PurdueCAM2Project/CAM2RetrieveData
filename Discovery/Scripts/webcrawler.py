"""
--------------------------------------------------------------------------------
Descriptive Name     : webcrawler.py
Author               : Kyle Martin
Contact Info         : marti716@purdue.edu
Date Written         : 06/05/17
Description          : Crawls through every link with a domain
Command to run script: python3 webcrawler.py <domain-link>
Usage                : No extra requirements
Output               : N/A
Note                 : 
Other files required by : N/A
this script and where 
located

"""

import sys
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request as urllib2
import re

def crawl_soup(address, domain):
    soup = BS(urllib2.urlopen(address).read(), "lxml")
    a_list = soup.find_all("a")
    link_dict = {}
    link_dict[address] = 0
    cur_list = []
    fin_list = [address]
    for a in a_list:
        link = a.get("href")
        if (link is not None and domain in link):
            link_dict[link] = 0
            cur_list.append(link)
    while (len(cur_list) > 0):
        this_link = cur_list.pop()
        fin_list.append(this_link)
        try:
            soup = BS(urllib2.urlopen(this_link).read(), "lxml")
        except:
            continue
        # do something here to check for a stream
        a_list = soup.find_all("a")
        for a in a_list:
            link = a.get("href")
            if (link is not None and link not in link_dict and domain in link): 
                link_dict[link] = 0
                cur_list.append(link)
        print_progress(len(fin_list), len(cur_list))

                
def crawl_selenium(address, domain):
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(10)
    try:
        driver.get(address)
    except e:
        raise e
    a_list = driver.find_elements_by_tag_name("a")
    link_dict = {} # a dictionary containing all links that have been found
    link_dict[address] = 0 # value doesn't matter for this dictionary
    cur_list = [] # a list with all the links yet to be analyzed
    fin_list = [address] # a list with all the links that have been analyzed
    # do something here to check for a stream
    for a in a_list:
        link = a.get_attribute("href")
        if (link is not None and domain in link):
            link_dict[link] = 0 # the value doesn't matter, just providing 0
            cur_list.append(link)

    while (len(cur_list) > 0):
        this_link = cur_list.pop()
        fin_list.append(this_link)
        try:
            driver.get(this_link)
        except:
            continue
        # do something here to check for a stream
        a_list = driver.find_elements_by_tag_name("a")
        for a in a_list:
            link = a.get_attribute("href")
            if (link is not None and link not in link_dict and domain in link):
                link_dict[link] = 0
                cur_list.append(link)
        print_progress(len(fin_list), len(cur_list))

def get_domain(address):
    m = re.search(r"https?:\/\/([\w\.\-]+)(\/|$)", address)
    if m:
        return m.group(1)
    else:
        return None

def print_progress(num_analyzed, num_remaining):
    print("\r{0:d} links analyzed; {1:d} additional links found" + " "*10
          .format(num_analyzed, num_remaining), end="\r")

if __name__ == '__main__':
    address = sys.argv[1]
    domain = get_domain(address)
    if (domain is None):
        raise ValueError("The passed web address has no domain")
    crawl_selenium(address, domain)
    print() # account for the print_progress command
