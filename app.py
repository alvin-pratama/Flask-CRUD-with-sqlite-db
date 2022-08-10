from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
import sqlite3

# koneksi serta membuat database
conn = sqlite3.connect('test.db')

# membuat tabel didatabase
conn.execute(''' CREATE TABLE IF NOT EXISTS data
	(
		id		INTEGER 	PRIMARY KEY		AUTOINCREMENT,
		name	TEXT	NOT NULL,
		email	INT		NOT NULL,
		phone	BIGINT
	);
	''')

conn.close()

# flask name
app = Flask(__name__)
app.secret_key = "Secret Key"

# rooute untuk index (show)
@app.route('/')
def index():
	# return "Hello...!"
	con = sqlite3.connect("test.db")
	con.row_factory = sqlite3.Row

	cur = con.cursor()
	cur.execute("SELECT * FROM data")

	rows = cur.fetchall();
	return render_template('index.html', rows=rows)

# route untuk input
@app.route('/insert',methods = ['POST'])
def insert():
	if request.method == 'POST':
		try:
			name = request.form['name']
			email = request.form['email']
			phone = request.form['phone']

			# conn.execute("INSERT INTO data (name, email, phone) VALUES (name, email, phone)");
			with sqlite3.connect("test.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO data (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
				con.commit()
				msg = "Record successfully added"
		except:
			con.rollback()
			msg = "error in insert operation"
		finally:

			flash("Employee Inserted Successfuly")
			return redirect(url_for('index'))
			con.close()

# route untuk update get data kemudian post
@app.route('/update',methods = ['GET', 'POST'])
def update():
	if request.method == 'POST':
		try:
			conn = sqlite3.connect('test.db')

			ide = request.form.get('id')
			print(ide)
			name = request.form.get('name')
			print(name)
			email = request.form.get('email')
			print(email)
			phone = request.form.get('phone')
			print(phone)

			conn.commit()

			with sqlite3.connect("test.db") as con:
				# cur = con.cursor()
				con.execute("UPDATE data set name=?, email=?, phone=? WHERE id=?", (name, email, phone, ide))
				con.commit()
				msg = "Record successfully updated"
		except:
			con.rollback()
			msg = "error in update operation"
		finally:

			flash("Employee Updated Successfuly")
			return redirect(url_for('index'))
			con.close()

# route untuk delete data, get before post
@app.route('/delete/<id>/',methods = ['GET', 'POST'])
def delete(id):
		# conn = sqlite3.connect('test.db')

		ide = id
		# ide = request.args.get('<id>') # ini bukan mengambil dari route url, malah dari form
		print(ide)
		# conn.commit()

		with sqlite3.connect("test.db") as con:
			cur = con.cursor()
			cur.execute("DELETE from data WHERE id=?", (ide,))
			
			# sql_update_query = """DELETE from data where id = ?"""
        	# cur.execute("DELETE from data where id = ?",ide)

			con.commit()

		flash("Employee Delete Successfuly")
		return redirect(url_for('index'))
		con.close()

# function run/ debug
if __name__ == "__main__":
	app.run(debug=True)