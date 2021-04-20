#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
Basic code explained here: 
https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application
Use terminal command "flask run" for dev server
"""
from flask import Flask, render_template, request
import json
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/gaps")
def gaps():
    return render_template("gaps.html")

@app.route("/bundle", methods=["GET"])
def bundle():
    bundle = test_bundle
    return json.dumps(bundle)

test_bundle = {"target": "fish",
               "sent_1_left": "Andrea got up early in the morning to",
               "sent_1_right": ".",
               "sent_2_left": "If you can see this, you're a good programmer and not a",
               "sent_2_right": ".",
               "sent_3_left": "Andrea got up early in the morning to",
               "sent_3_right": ".",
               "sent_4_left": "Andrea got up early in the morning to",
               "sent_4_right": "."}