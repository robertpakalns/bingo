
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

@app.route('/pirmais')
def hello_world():
    return 'Hello from Flask!'

@app.route('/teksts')
def teksts():
    return "teksts"

@app.route('/skaitlis')
def skaitlis():
    return str(random.randint(0, 10))

@app.route('/ntais/<int:n>')
def ntais(n):
    return str(random.randint(n, n+10))

@app.route('/vards/<string:v>')
def vards(v):
    if(v[-1] == "s"):
        return render_template("temp_page.html", comment = v[:-1])
    return render_template("temp_page.html", comment = v)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("web_game.html")

     

@app.route('/romusk/<string:st>')
def rom(st):
    try:
        sk = int(st)
        if sk > 0 and sk < 11:
            print('yes')
            f=open('/home/Kruman/mysite/templates/skaitli.txt', 'r')
            skaitli = f.read().splitlines()
            f.close()
            return skaitli[sk-1]
        else:
            return "\"XX\""
    except:
        return "\"XX\""

@app.route('/main')
def spelet1():
    return render_template("web_game.html")

@app.route('/noteikumi')
def lasit():
    return render_template("noteikumi.html")

@app.route('/game')
def game():
    return render_template('index.html')

@app.route('/leaderboard.html')
def leaderboard_page():
    return render_template('leaderboard.html')

@app.route('/get_leaderboard/<game_type>', methods=['GET'])
def get_leaderboard(game_type):
    table_mapping = {
        "30": "leaderboard_5x6",
        "24": "leaderboard_4x6",
        "20": "leaderboard_4x5",
        "16": "leaderboard_4x4",
        "12": "leaderboard_3x4",
        "8": "leaderboard_2x4",
        "6": "leaderboard_2x3",
        "4": "leaderboard_2x2"
    }
    table_name = table_mapping.get(game_type)

    if not table_name:
        return jsonify({"error": "Invalid game type"}), 400

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT name, score FROM {table_name} ORDER BY score ASC LIMIT 10"
        cursor.execute(query)
        leaderboard = cursor.fetchall()

        return jsonify(leaderboard), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    print("Received data: ", data)
    name = data.get('name')
    score = data.get('score') / (data.get('acc')/100)
    game_type = data.get('game_type')

    if not name or not score or not game_type:
        return jsonify({"error": "Missing required fields"}), 400

    table_mapping = {
        "30": "leaderboard_5x6",
        "24": "leaderboard_4x6",
        "20": "leaderboard_4x5",
        "16": "leaderboard_4x4",
        "12": "leaderboard_3x4",
        "8": "leaderboard_2x4",
        "6": "leaderboard_2x3",
        "4": "leaderboard_2x2"
    }
    table_name = table_mapping.get(game_type)

    if not table_name:
        return jsonify({"error": "Invalid game type"}), 400
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = f"INSERT INTO {table_name} (name, score) VALUES (%s, %s)"
        cursor.execute(query, (name, score))
        connection.commit()

        return jsonify({"message": "Score submitted successfully"}), 200
    except mysql.connector.Error as err:
        print(err)
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()

@app.route('/lvbingo')
def lvBingo():
    return render_template('lvbingo.html');

@app.route('/fullbingo')
def fullBingo():
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








