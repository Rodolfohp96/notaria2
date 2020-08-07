from flask import Flask
from flask_mysqldb import MySQL

from random import randint

# Global variables
HOST_NAME = 'localhost'
USER_NAME = 'admin'
USER_PASS = 'adminpass'
DB_NAME = 'notaria2'

setup_app = Flask(__name__)
setup_app.config['MYSQL_HOST'] = HOST_NAME
setup_app.config['MYSQL_USER'] = USER_NAME
setup_app.config['MYSQL_PASSWORD'] = USER_PASS
setup_app.config['MYSQL_DB'] = DB_NAME

mysql = MySQL(setup_app)



@setup_app.route('/setup')
def setup_db():
    db = mysql.connection.cursor()

    # Drop all tables
    db.execute('SET FOREIGN_KEY_CHECKS = 0')
    db.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = \'{}\''.format(DB_NAME))
    all_tables = db.fetchall()
    print(all_tables)
    for tables in all_tables:
        for table in tables:
            print('Deleting table: {}'.format(table))
            db.execute('DROP TABLE IF EXISTS {}'.format(table))
    db.execute('SET FOREIGN_KEY_CHECKS = 0')
    # Show empty
    db.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = \'{}\''.format(DB_NAME))
    data = db.fetchall()
    print(data)

    #RecibosProv
    db.execute("""CREATE TABLE Recibos(
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            nombreSolicitante VARCHAR(50) NOT NULL,
            cantidadRecibo FLOAT NOT NULL,
            concepto VARCHAR(300) NOT NULL,
            escrituraNum INT NOT NULL,
            avaluo FLOAT NOT NULL,
            fechaRecibo DATE NOT NULL,
            nombreCreador VARCHAR(50) NOT NULL,
            folio INT 
        )""")

    

    db.connection.commit()
    # Terminar la conexion
    return 'success'

if __name__ == '__main__':
    setup_app.run(port = 3000, debug = True)
