from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import os
import scrape_mars

app = Flask(__name__)

# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_info = mongo.db.collection.find_one()
    # mars_info = "hello"

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger scrape functionç
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    mars_info = mongo.db.mars_info

    mars_data = scrape_mars.scrape()

    mars_info.update({}, mars_data, upsert=True)


    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)

