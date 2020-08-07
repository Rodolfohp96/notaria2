from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mysqldb import MySQL

from utils import *
from setup import HOST_NAME, USER_NAME, USER_PASS, DB_NAME

app = Flask(__name__)
app.config['MYSQL_HOST'] = HOST_NAME 
app.config["MYSQL_USER"] = USER_NAME
app.config['MYSQL_PASSWORD'] = USER_PASS
app.config['MYSQL_DB'] = DB_NAME
app.secret_key = 'MYSECRET_KEY'
mysql = MySQL(app)

 
@app.route('/')
def Index():
    
    return render_template('index.html')

@app.route('/add_recive', methods=['POST'])
def add_recive():
    msg = ""
    if request.method =='POST':
        try:
            nombreSolicitante = request.form['nombreSolicitante']
            cantidadRecibo = float(request.form['cantidadRecibo'])
            concepto = request.form['concepto']
            escrituraNum = int(request.form['escrituraNum'])
            avaluo = float(request.form['avaluo'])
            fechaRecibo = request.form['fechaRecibo']
            nombreCreador = request.form['nombreCreador']
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO recibos (nombreSolicitante, cantidadRecibo, concepto, escrituraNum, avaluo, fechaRecibo, nombreCreador) VALUES (%s, %s, %s, %s, %s, %s,%s)',(nombreSolicitante, cantidadRecibo, concepto, escrituraNum, avaluo, fechaRecibo, nombreCreador))
            mysql.connection.commit()
            flash('Recibo creado')
        except ValueError:
            msg = "Ocurrió un error al agregar la información"
        
    return redirect(url_for('Index'))

@app.route('/recibos_prov')
def recibos_prov():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM recibos')
    data = cur.fetchall()
    cur.execute('SELECT count(id) FROM recibos')
    numrecibos = cur.fetchall()[0][0]
    cur.execute('SELECT sum(cantidadRecibo) FROM recibos')
    anticipo = cur.fetchall()[0][0]
    cur.execute('SELECT sum(avaluo) FROM recibos')
    avaluo = cur.fetchall()[0][0]
    

    return render_template('recibosProv.html',recibosProv = data, numrecibost = numrecibos, anticipot = anticipo, avaluot = avaluo)

@app.route('/reciboMenu')
def reciboMenu():
    return render_template('newReciboProvisional.html')

@app.route('/tiposbusqueda')
def tiposbusqueda():
    return render_template('tiposbusqueda.html')


@app.route('/busquedaFol', methods=['POST'])
def busquedaFol():
    if request.method == 'POST':
        qu = request.form['queryFol']
        db = mysql.connection.cursor()
        db.execute('SELECT * FROM recibos WHERE id =  %s', (qu))
        data = db.fetchall()
        print(data)
        return render_template('tiposbusqueda.html', datos = data)

@app.route('/busquedaName', methods=['POST'])
def busquedaName():
    if request.method == 'POST':
        qu = request.form['queryName']
        db = mysql.connection.cursor()
        db.execute('SELECT * FROM recibos WHERE nombreSolicitante LIKE \'%{}%\''.format(qu))
        data = db.fetchall()
        print(data)
        return render_template('tiposbusqueda.html', datos = data)

@app.route('/busquedaConc', methods=['POST'])
def busquedaConc():
    if request.method == 'POST':
        qu = request.form['queryConc']
        db = mysql.connection.cursor()
        db.execute('SELECT * FROM recibos WHERE concepto LIKE \'%{}%\''.format(qu))
        data = db.fetchall()
        print(data)
        return render_template('tiposbusqueda.html', datos = data)

@app.route('/busquedaEsc', methods=['POST'])
def busquedaEsc():
    if request.method == 'POST':
        qu = request.form['queryEsc']
        db = mysql.connection.cursor()
        db.execute('SELECT * FROM recibos WHERE escrituraNum LIKE \'%{}%\''.format(qu))
        data = db.fetchall()
        print(data)
        return render_template('tiposbusqueda.html', datos = data)

@app.route('/busquedaFech', methods=['POST'])
def busquedaFech():
    if request.method == 'POST':
        qu = request.form['queryFe']
        db = mysql.connection.cursor()
        db.execute('SELECT * FROM recibos WHERE fechaRecibo LIKE \'%{}%\''.format(qu))
        data = db.fetchall()
        print(data)
        return render_template('tiposbusqueda.html', datos = data)

@app.route('/busquedaCread', methods=['POST'])
def busquedaCread():
    if request.method == 'POST':
        qu = request.form['queryCr']
        db = mysql.connection.cursor()
        db.execute('SELECT * FROM recibos WHERE nombreCreador LIKE \'%{}%\''.format(qu))
        data = db.fetchall()
        print(data)
        return render_template('tiposbusqueda.html', datos = data)
    
@app.route('/print/<string:id>')
def printr(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM recibos WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('imprimirRecibo.html',recibo = data[0])

@app.route('/delete/<string:id>')
def delete_reciboProv(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM recibos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Recibo eliminado correctamente')
    return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True) 