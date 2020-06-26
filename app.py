from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#MySQL Connection
app.config['MYSQL_HOST'] = 'beuaofgulns1vqjmklcj-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'ubfvkejo67xxdzw0'
app.config['MYSQL_PASSWORD'] = 'yOizmLIEJb488a8dtlEi'
app.config['MYSQL_DB'] = 'beuaofgulns1vqjmklcj'
mysql = MySQL(app)

#Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
        mysql.connection.commit()
        flash('Integrante Agregado Satisfactoriamente')
        return redirect(url_for('index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', [id])
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Integrante Eliminado Satisfactoriamente')
    return redirect(url_for('index'))

@app.route('/update/<id>',methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE contacts SET fullname = %s, phone = %s, email = %s WHERE contacts.id = %s', (fullname, phone, email, id))
        mysql.connection.commit()
        flash('Integrante Actualizado Satisfactoriamente')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port = 3000, debug = False)