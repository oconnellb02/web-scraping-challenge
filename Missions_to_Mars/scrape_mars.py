import pandas as pd
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # NASA Mars News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    news_soup = bs(html, "html.parser")

    results = news_soup.find('div', class_='slide')
    news_title = results.find('div', class_="content_title").text        
    news_p = results.find('div', class_="rollover_description_inner").text
    # print(news_title)
    # print(news_p)

    # JPL Mars Space Images
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    time.sleep(1)

    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    html = browser.html
    image_soup = bs(html, 'html.parser')

    image_link = image_soup.find('figure', class_="lede").a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{image_link}'
    # print(featured_image_url)

    # Mars Weather
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tweet_url)

    time.sleep(1)

    html = browser.html
    weather_soup = bs(html, 'html.parser')

    tweets = weather_soup.find('article', role="article")                       

    for tweet in tweets:
        try:
            mars_weather = tweets.find('div', lang="en").text
            
            if(mars_weather):
                # print(mars_weather)
                break
        except AttributeError as e:
            # print(e)
            pass

    # Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    time.sleep(1)

    html = browser.html

    tables = pd.read_html(facts_url)

    mars_facts = tables[0]
    mars_facts.columns = ["Description", "Value"]
    mars_facts.set_index("Description", inplace=True)
    mars_facts = mars_facts.to_html(classes="table table-striped")

    # Mars Hemispheres
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemisphere_image_urls = []

    results = soup.find('div', class_="collapsible results")
    hemispheres = results.find_all('div', class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find('h3').text
        title = title.replace("Enhanced", "")
        
        image_link = hemisphere.find('a')['href']    
        hemisphere_image = "https://astrogeology.usgs.gov/" + image_link
        
        browser.visit(hemisphere_image)
        html = browser.html
        soup = bs(html, "html.parser")
        
        hem_images = soup.find("div", class_="downloads")
        image_url = hem_images.find('a')['href']    
        
        hemisphere_image_urls.append({"title": title, "img_url": image_url})
        
    # print(hemisphere_image_urls)

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return mars_data




        
    

















