from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enternew')
def food():
    return render_template('food.html')

@app.route('/addfood', methods = ['POST'])
def addfood():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    try:
        name = request.form['name']
        calories = request.form['calories']
        cuisine = request.form['cuisine']
        is_vegetarian = request.form['is_vegetarian']
        is_gluten_free = request.form['is_gluten_free']
        cursor.execute('INSERT INTO foods (name,calories,cuisine,is_vegetarian,is_gluten_free) VALUES (?,?,?,?,?)', (name,calories,cuisine,is_vegetarian,is_gluten_free))
        connection.commit()
        message = 'success'
    except:
        connection.rollback()
        message = 'error'
    finally:
        return render_template('result.html', message = message)
        connection.close()

#extra credit 1
@app.route('/favorite', methods = ['GET'])
def favorite():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute ('SELECT * FROM foods WHERE name = "spam and eggs"')
    data = cursor.fetchall()
    return jsonify(data)
    connection.close()

#extra credit 2
@app.route('/search', methods = ['GET'])
def search():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    try:
        name = (request.args.get('name'),)
        cursor.execute('SELECT * FROM foods WHERE name = ?', name)
        data = cursor.fetchall()
        return jsonify(data)
    except:
        return "Invalid search"
        connection.close()

#extra credit 3
@app.route('/drop')
def drop():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    try:
        cursor.execute('DROP TABLE foods')
        return "successfully dropped"
    except:
        return "failed to drop"
        connection.close()
