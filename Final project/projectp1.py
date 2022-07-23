#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 20:14:01 2022

@author: olgavyrvich
"""

from flask import Flask, render_template, request 

from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'Project1'

mysql = MySQL(app)

@app.route('/rank', methods = ['POST'])
def Universit1():
     if request.method == "POST":
         cur = mysql.connection.cursor()
         uni = request.form['uni']
         select_stmt = """ SELECT r.rank, u.name, l.location, r.national_rank, r.quality_of_education, r.alumni_employment, r.quality_of_faculty,
                r.research_performance, r.score 
                from ranks r, list_of_universities u, location l
                where r.name = u.id and r.location = l.id and u.name = %(name)s"""
         cur.execute(select_stmt,{ 'name': uni })
         data = cur.fetchall()
         cur.close()
         
         cur = mysql.connection.cursor()
         select_stmt = """SELECT r.name_user, r.review 
                from reviews r, list_of_universities u
                where r.name_university = u.id  and u.name = %(name)s;"""
         cur.execute(select_stmt,{ 'name': uni })       
         rev = cur.fetchall()
         cur.close()
         return render_template("rank.html", universities=data, reviews = rev) 
 
@app.route('/', methods = ['POST','GET'])
def insert():
    if request.method == "POST":
        name_user = request.form['name_user']
        name_university = request.form['name_university']
        review = request.form['review']
        cur = mysql.connection.cursor()
        select_stmt = """select id from list_of_universities where name = %(name1)s"""
        cur.execute(select_stmt,{ 'name1': name_university })
        name_university = cur.fetchone()
        cur.execute("INSERT INTO reviews (name_user, name_university ,review) VALUES (%s, %s, %s)", (name_user,name_university[0],review))
        mysql.connection.commit()
        cur.close()
        
    cur = mysql.connection.cursor()
    cur.execute("""
            SELECT r.rank, l.name,l.domain, r.score
            FROM list_of_universities l INNER JOIN ranks r ON l.id=r.name;
        """)
    data = cur.fetchall()
    cur.close()
    return render_template("index.html", ranks=data)

@app.route('/about')
def information():
     return render_template("about.html")



    
if __name__=="__main__":
    app.run(port=5000, debug=True)
    
