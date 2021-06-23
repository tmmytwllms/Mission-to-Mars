#!/usr/bin/env python
# coding: utf-8

#Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#Set up the browser
executable_path={'executable_path':ChromeDriverManager().install()}
browser=Browser('chrome',**executable_path,headless=False)

#Visit the mars nasa news site
url='https://redplanetscience.com'
browser.visit(url)
#Optional delay for loading the page
browser.is_element_present_by_css('div.list_text',wait_time=1)

html=browser.html
news_soup=soup(html,'html.parser')
slide_elem=news_soup.select_one('div.list_text')

#Find the news title in the new link
news_title=slide_elem.find('div',class_='content_title').get_text()
news_title

#Find the article summary
news_p=slide_elem.find('div',class_='article_teaser_body').get_text()
news_p

#Visit URL
url='https://spaceimages-mars.com'
browser.visit(url)

#Find full image and click button
full_image_elem=browser.find_by_tag('button')[1]
full_image_elem.click()

#Parse the resulting html with soup
html=browser.html
img_soup=soup(html,'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

#Use the base URL to create a full URL
img_url=f'https://spaceimages-mars.com/{img_url_rel}'
img_url

#Visit another site
url="https://galaxyfacts-mars.com/"
browser.visit(url)

#Convert the 'mars facts' to a dataframe using pandas
df=pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description','Mars','Earth']
df.set_index('description',inplace=True)
df

#Convert the dataframe into HTML
df.to_html()

#End the browser
browser.quit()