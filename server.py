from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector 
import re,os 

app = Flask(__name__)
mysql = MySQLConnector(app,'letsDoThis')
app.secret_key = 'os.urandom(24)'
print app.secret_key 

@app.route('/', methods=['GET'])
def index():
	query="SELECT * FROM  friends"
	x=mysql.query_db(query)
	print x
	return render_template('index.html', friends=x)


@app.route('/friends', methods=['POST'])
def create():
	first_name=request.form['f_name']
	last_name=request.form['l_name']
	email=request.form['email']
	query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (:f_name, :l_name, :email, NOW(), NOW())"
	data = {
			'f_name': first_name, 
			'l_name':  last_name,
			'email': email
				}

	mysql.query_db(query, data)
	return redirect('/')



@app.route('/friends/<y>/edit')
def edit(y):
	return render_template('edit.html',friend_id=y)



@app.route('/friends/<id>', methods=['POST'])
def update(id):
    query = "UPDATE friends SET first_name = :f_name, last_name = :l_name, email = :email WHERE id = :friend_id"
    data = {
             'f_name': request.form['f_name'], 
             'l_name':  request.form['l_name'],
             'email': request.form['email'],
             'friend_id': id
           }
    mysql.query_db(query, data)
    return redirect('/')
    




@app.route('/friends/<friend_id>/delete', methods=['POST'])
def delete(friend_id):

	query = "DELETE FROM friends WHERE id = :id"
	data = {'id': friend_id}
	mysql.query_db(query, data)
	return redirect('/')

app.run(debug=True)



