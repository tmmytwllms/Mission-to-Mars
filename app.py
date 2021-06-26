from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping
import numpy as np

app=Flask(__name__)

#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"]='mongodb://localhost:27017/mars_app'
mongo=PyMongo(app)

#Set up the home route
@app.route("/")
def index():
    #Finds the mars collection in our database, created by the scraping code
    mars=mongo.db.mars.find_one()
    #Return an HTML template using an index.html file; use mars collection in mongodb
    return render_template("index.html",mars=mars)

#Set up the scraping route
@app.route('/scrape')
def scrape():
    #access database
    mars=mongo.db.mars
    #scrape new data with our scraping script (scrape_all is a function of the scraping.py file)
    mars_data=scraping.scrape_all()
    #update the database with a empty dictionary
    #updating the database is a function that takes a query_parameter, data, and options)
    mars.update({},mars_data,upsert=True) #upsert creates a new document, and saves data
    #redirects us to the homepage, which is now updated with the scraped data
    return redirect('/',code=302)

#Run flask
if __name__ == "__main__":
    app.run()