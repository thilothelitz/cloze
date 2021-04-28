#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic code explained here: 
https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application
Use terminal command "flask run" for dev server
"""
import random
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

DATA_PATH = Path(__file__).resolve().parent / "data"


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/gaps")
def gaps():
    return render_template("gaps.html")


@app.route("/bundle", methods=["GET"])
def bundle():
    level = request.args["level"]
    with open(DATA_PATH / "bundles" / f"{level}.jsonl") as bundles:
        jsons = bundles.readlines()
    return random.choice(jsons)
