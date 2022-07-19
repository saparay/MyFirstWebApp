from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
import os
app=Flask(__name__)
app.secret_key=os.urandom(24)
conn = mysql.connector.connect(host="localhost", user="root", password="root", database="learningflask")

cursor = conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'uid' in session:
        cursor.execute("""SELECT * FROM `logininfo`""")
        data = cursor.fetchall()
        return render_template('home.html', logininfo=data)
    else:
        return redirect('/')

@app.route('/login_validation', methods=['GET', 'POST'])
def login_validation():
    if 'uid' in session:
        return redirect('/home')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        cursor.execute(
            """SELECT * FROM `logininfo` WHERE `email` LIKE '{}'
             AND `password` LIKE '{}'""".format(username, password))
        users = cursor.fetchall()
        if len(users) > 0:
            session['uid'] = users[0][0]
            return redirect('/home')
        else:
            if 'uid' in session:
                return redirect('/home')
            else:
                return redirect('/')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    cursor.execute("""INSERT INTO `logininfo` (`uid`, `name`, `email`, `password`)
     VALUES (null, '{}', '{}', '{}')""".format(name, email, password))
    conn.commit()
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('uid')
    return redirect('/')

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        cursor.execute("""INSERT INTO `logininfo` (`uid`, `name`, `email`, `password`) 
        VALUES (Null, '{}', '{}', '{}')""".format(name, email, password))
        conn.commit()
        return redirect('/home')


@app.route('/delete/<string:id>', methods=['GET'])
def delete(id):
    cursor.execute("""DELETE FROM `logininfo` WHERE uid = '{}'""".format(id))
    conn.commit()
    return redirect('/home')

@app.route('/update/<string:id>', methods=['POST', 'GET'])
def update(id):
       if request.method == 'POST':
           name = request.form['name']
           email = request.form['email']
           password = request.form['password']
           cursor.execute("""UPDATE `logininfo` SET name='{}', email='{}',
            password='{}' WHERE uid='{}'""".format(name, email, password, id))
           conn.commit()
           return redirect('/home')
       cursor.execute("""SELECT * FROM `logininfo` WHERE uid='{}'""".format(id))
       data = cursor.fetchone()
       return render_template('update.html', data=data)



@app.route('/add_data')
def add_data():
    return render_template('insert.html')
if __name__ == "__main__":
    app.run(debug=True)