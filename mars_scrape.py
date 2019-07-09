# Declare Dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
from sqlalchemy import create_engine

def scrape():
    scrape_dic = {}

    # # NASA Mars News
    # set up path to chrome driver
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    # Visit Nasa news url through splinter module
    base_url = 'https://mars.nasa.gov/news/'
    browser.visit(base_url)
    # HTML Object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve the latest element that contains news title and news_paragraph
    articles_dic = {"Title" : [], "Paragraph": []}
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text
    articles_dic["Title"].append(news_title)
    articles_dic["Paragraph"].append(news_p)
    # Display scrapped data 
    # print(news_title)
    # print(news_p)
    # print(articles_dic)

    # Load data to Scrape dictionary
    scrape_dic["Mars_News"] = articles_dic

    # # JPL Mars Space Images - Featured Image
    # Visit Mars Space Images through splinter module
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    # HTML Object 
    html_image = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, 'html.parser')
    # Retrieve background-image url from style tag 
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    # Website Url 
    main_url = 'https://www.jpl.nasa.gov'
    # Concatenate website url with scrapped route
    featured_image_url = main_url + featured_image_url
    # Display full link to featured image
    featured_image_url
    # Load data to Scrape dictionary
    scrape_dic["Featured_Image"] = featured_image_url

    # # Mars Weather
    # Visit Mars Weather Twitter through splinter module
    base_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(base_url)

    # HTML Object 
    html_weather = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_weather, 'html.parser')
    # Find all elements that contain tweets
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')
    mars_weather = latest_tweets[0].text
    print(mars_weather)
    # Load data to Scrape dictionary
    scrape_dic["Weather"] = mars_weather

    # # Mars Facts
    # Visit Mars facts url 
    facts_url = "http://space-facts.com/mars/"

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)
    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]
    # mars_df
    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']
    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)
    # Save html code to folder Assets
    # mars_df.to_html()
    # Display mars_df
    mars_df
    # print(data)
    # Load data to Scrape dictionary
    scrape_dic["Mars_Facts"] = mars_df.to_html()

    # # Mars Hemispheres
    # Visit hemispheres website through splinter module 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')
    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')
    # print(items)
    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []
    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
    #     print(title)
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    #     print(partial_img_url)
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        # HTML Object of individual hemisphere information website 
        img_html = browser.html
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup(img_html, 'html.parser')
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    #     print(img_url)
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    # Display hemisphere_image_urls
    hemisphere_image_urls
    # Load data to Scrape dictionary
    scrape_dic["Hemisphere"] = hemisphere_image_urls
    # Close Chromedriver and return content
    browser.quit()
    return scrape_dic

    # # MongoDB and Flask Application
    import pymongo
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client["marsDB"]
    mars_data = db.list_collection_names()

    # display content in MongoDB
    mars_data