# Import Dependencies 
from flask import Flask, render_template, redirect, url_for
import pymongo
import os

# Create MongoDB connection; Create database and collection if it does not exist.
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client["marsDB"]
collection = db["mars"]

# Create an instance of Flask app
app = Flask(__name__)

@app.route("/scrape")
def import_scrape():
    # Import scrape_mars python file that will web scrapping using beautiful soup and return the data in dictionary.
    import scrape_mars
    if len(db.list_collection_names()) != 0:
        db.mars.drop()
    collection.insert_one(scrape_mars.scrape())
    # return "Data was successfully scrapped."
    return redirect(url_for('show_scraped_data'))


@app.route("/")
def show_scraped_data():
    # Query the Mongo database and pass the mars data into an HTML template to display the data.
    mars_dic = None
    if len(db.list_collection_names()) == 0:
        return render_template("scrape.html")
    else:
        for field in collection.find():
            mars_dic = field
            break
        return render_template("index.html", dic=mars_dic)


if __name__ == "__main__":
    app.run()
