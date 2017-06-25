#!/usr/bin/python3
# -*- coding: latin-1 -*-
import os
import sys
# import psycopg2
import json
from bson import json_util
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

# REPLACE WITH YOUR DATABASE NAME
MONGODATABASE = "dbEscuchas"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
mongodb = client[MONGODATABASE]

''' # Uncomment for postgres connection
# REPLACE WITH YOUR DATABASE NAME, USER AND PASS
POSTGRESDATABASE = "mydatabase"
POSTGRESUSER = "myuser"
POSTGRESPASS = "mypass"
postgresdb = psycopg2.connect(
    database=POSTGRESDATABASE,
    user=POSTGRESUSER,
    password=POSTGRESPASS)
'''

#Cambiar por Path Absoluto en el servidor
QUERIES_FILENAME = '/var/www/FlaskApp/queries'


@app.route("/")
def home():
    with open(QUERIES_FILENAME, 'r', encoding='utf-8') as queries_file:
        json_file = json.load(queries_file)
        pairs = [(x["name"],
                  x["database"],
                  x["description"],
                  x["query"]) for x in json_file]
        return render_template('file.html', results=pairs)


@app.route("/mongo")
def mongo():
    query = request.args.get("query")
    if query is None and "find" in query:
        return "no query"
    
    results = eval('mongodb.'+query)
    results = json_util.dumps(results, sort_keys=True, indent=4)
    return render_template('mongo.html', results=results)


def wrap_quotes(word):
    """Return a word wrapped in quotation marks"""
    return "\'" + str(word) + "\'"


@app.route("/word")
def search_by_word():
    """Provide a url to search word in 'contenido'"""
    word = request.args.get("word")
    if word is None:
        return "[]" # No query

    results = mongodb.colEscuchas.find({"$text":{"$search": wrap_quotes(word)}})
    results = json_util.dumps(results, sort_keys=True, indent=4)
    return str(results) # return plain string


@app.route("/fecha")
def search_by_date():
    """Provide a url to search phone numbers by date"""
    date = request.args.get("date")
    if date is None:
        return "[]" # No query

    results = mongodb.colEscuchas.find({"fecha": date}, {"_id":0, "numero":1})
    results = json_util.dumps(results, sort_keys=True, indent=4)
    return str(results) # return plain string


@app.route("/postgres")
def postgres():
    return "Postgres API is not available"
    query = request.args.get("query")
    if not query is None:
        cursor = postgresdb.cursor()
        cursor.execute(query)
        results = [[a for a in result] for result in cursor]
        print(results)
        return render_template('postgres.html', results=results)
    else:
        return "no query"


@app.route("/example")
def example():
    return render_template('example.html')


if __name__ == "__main__":
    app.run()
