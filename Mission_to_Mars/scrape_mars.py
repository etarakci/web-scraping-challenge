# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os
import requests
import pandas as pd
import time
import numpy as np 
# import warnings
# warnings.filterwarnings('ignore')

def init_browser():
    import os
    if os.name=="nt":
        executable_path = {'executable_path': './chromedriver.exe'}
    else:
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_news():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    news_soup = bs(html, 'html.parser')
    # Retrieve all elements that contain book information
    articles = news_soup.find_all('div', class_='list_text')
    article = articles[0]
    # Use Beautiful Soup's find() method to navigate and retrieve attributes
    news_title = article.find('a').contents[0]
    news_p = article.find_all('div', class_='article_teaser_body')[0].contents[0]
    browser.quit()
    return [news_title,news_p]
    

def scrape_image():
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url) 
    html = browser.html
    # Parse HTML with Beautiful Soup
    image_soup = bs(html, 'html.parser')
    # Retrieve all elements that contain book information
    image = image_soup.find('div', class_='image_and_description_container')
    # Use Beautiful Soup's find() method to navigate and retrieve attributes
    featured_image_url  = 'https://www.jpl.nasa.gov' + image.find_all('div',class_='img')[0].contents[1]['src']
    browser.quit()
    return featured_image_url

def scrape_weather():
    browser = init_browser()
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    # Parse HTML with Beautiful Soup
    weather_soup = bs(html, 'html.parser')
    all_tweets = weather_soup.find_all('div', attrs={"lang": "en"})
    tweet = all_tweets[0]
    mars_weather = tweet.text
    browser.quit()
    return mars_weather
    
def scrape_facts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_df = tables[0]
    mars_df = mars_df.rename(columns={0:'Description',1:'Measurement'})
    mars_df.set_index('Description',inplace=True)
    mars_html_table = mars_df.to_html()
    return mars_html_table

def scrape_hemispheres():
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Iterate through all pages
    hemisphere_image_urls = []
    img_page_urls = []

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    hemi_soup = bs(html, 'html.parser')
    # Retrieve all elements that contain book information
    hemispheres = hemi_soup.find_all('div', class_='item')

    # Iterate through each book
    for hemisphere in hemispheres:
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        description = hemisphere.find_all('div', class_='description')[0].contents[0]
        title = description.find('h3').contents[0]
        img_page_url = 'https://astrogeology.usgs.gov' + description['href']
        
        hemisphere_image_urls.append({"title":title})
        img_page_urls.append(img_page_url)

    i = 0
    for url in img_page_urls:
        
        browser.visit(url)
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')
        download = soup.find_all('div', class_='downloads')[0]
        img_url = download.find_all('li')[0].contents[0]['href']

        hemisphere_image_urls[i]['img_url'] = img_url
        i += 1   
    browser.quit()
    return hemisphere_image_urls


def scrape():
    mars_data = {}
    news_title,news_p = scrape_news()
    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p
    mars_data['featured_image_url'] = scrape_image()
    mars_data['mars_weather'] = scrape_weather()
    mars_data['mars_html_table'] = scrape_facts()
    mars_data['hemisphere_image_urls'] = scrape_hemispheres()

    return mars_data




