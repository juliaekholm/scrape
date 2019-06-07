

import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape(url, cols):

    # Create an empty dataframe to store the result.
    res = pd.DataFrame(columns=cols)


    def scrape_page(url):

        # Parse web page and store it as text.
        page=requests.get(url)
        soup=BeautifulSoup(page.text,'html.parser')

        # Specify the attribute and the class of the container that 
        # holds the data.
        content = soup.find('ul', class_='search-results__list blurb')       

        # Specify the attribute and the class of the containers that
        # hold the data for each item.
        items = content.findAll('div', class_='search-results__item__text')

        # Create an empty dataframe to store the scraped data.
        res = pd.DataFrame(columns=cols)

        # Loop through all item containers and scrape the specified data.
        # Specify the attribute tree structure for each item to retrieve 
        # the text value for that item.
        for i in items:

            #foo = i.header.h2.a.text.strip()
            foo=i.find('header').find('h2').find('a').text.strip()

            #bar = i.dl.dd.text.strip()
            bar=i.find('dl').find('dd').text.strip()

            tmp = pd.DataFrame([[foo,bar]],columns=cols)
            res = res.append(tmp, ignore_index=True)
            
        return res

    scrape_page.__doc__ = "This function accepts a URL as input and returns scraped data as a Python dataframe."

    
    # Scrape the first page of the specified URL.
    base_url=url
    res = scrape_page(url=base_url)
    
    # Retrieve all pages of the specified URL that should be scraped.
    page=requests.get(base_url)
    soup=BeautifulSoup(page.text,'html.parser')
    all_pages = soup.find_all('a')
    links = set()
    for page in all_pages:
        if page["href"].startswith(base_url):
            links.add(page["href"])

    # Scrape the remaining pages of the specified URL.
    for next_page in links:
        tmp = scrape_page(next_page)
        res = res.append(tmp, ignore_index=True)

    return res

scrape.__doc__ = "This function accepts a URL as input, scrapes all pages of the specified URL and returns the scraped data as a Python dataframe."


# Scrape data from URL.
data = pd.DataFrame()
data = scrape(url='https://', cols=['foo','bar'])

# Export data.
data.to_csv('data.csv', index=False)