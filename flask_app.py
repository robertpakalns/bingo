
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, redirect, request, url_for, jsonify
import mysql.connector
import os
import random
import json
app = Flask(__name__)
comments = []

db_config = {
    'host': '',
    'user': '',
    'password': '',
    'database': ''
}
@app.route('/lvbingo')
def lvBingo():
    return render_template('bingo.html');

@app.route('/new_bingo/<string:category>', methods=['GET'])
def newBingo(category):
    f=open('/home/Kruman/mysite/templates/assets/' + category + 'Prompts.txt', 'r')
    prompts = f.read().splitlines()
    f.close()
    random.shuffle(prompts)
    temp = prompts[0]
    for x in range(24):
        temp += " "+prompts[x+1]
    return jsonify(temp), 200








