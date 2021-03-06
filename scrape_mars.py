from bs4 import BeautifulSoup
import os
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_mars():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup1 = BeautifulSoup(html, 'html.parser')

    title = soup1.find_all('div', class_='content_title')[1].text
    p = soup1.find_all('div', class_='article_teaser_body')[0].text

    print(title)
    print("----------------------------------")
    print(p)

    tables = pd.read_html('https://space-facts.com/mars/')

    mars_facts = tables[0]
    mars_facts.columns = ['Fact','Answer']
    mars_html_table = mars_facts.to_html()
    mars_html_table = mars_html_table.replace('\n', '')

    main_usgs = 'https://astrogeology.usgs.gov'
    mars_usgs = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(mars_usgs)

    hemispheres_html = browser.html

    soup3 = BeautifulSoup(hemispheres_html, 'html.parser')

    mars_hemispheres = soup3.find_all('div', class_='item')

    hemisphere_image_urls = []

    for i in mars_hemispheres:
        hemisphere = i.find('div', class_="description")
        title2 = hemisphere.h3.text
            
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(main_usgs + hemisphere_link)
            
        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')
            
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        image_dict = {}
        image_dict['title'] = title2
        image_dict['img_url'] = image_url
            
        hemisphere_image_urls.append(image_dict)

    mars_dict = {
        "news_title": title, 
        "news_p": p, "fact_table": 
        str(mars_html_table), 
        "hemisphere_images": hemisphere_image_urls
        }
    
    browser.quit()

    return mars_dict

    

