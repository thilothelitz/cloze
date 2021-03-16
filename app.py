#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
Basic code explained here: https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application
"""
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/gaps')
def gaps():
    return render_template("gaps.html")