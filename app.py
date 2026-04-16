from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_mysqldb import MySQL
from functools import wraps


app = Flask(__name__)
app.secret_key = '123456'

# Configuración MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestor_reservas'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/habitaciones')
def habitaciones():
    return render_template('habitaciones.html')

@app.route('/detalle_estandar')
def detalle_estandar():
    return render_template('detalle-estandar.html')

@app.route('/detalle_deluxe')
def detalle_deluxe():
    return render_template('detalle-deluxe.html')

@app.route('/detalle_suite')
def detalle_suite():
    return render_template('detalle-suite.html')

@app.route('/detalle_presidencial')
def detalle_presidencial():
    return render_template('detalle-presidencial.html')

@app.route('/confirmar-reserva', methods=['POST'])
def confirmar_reserva():
    if request.method == 'POST':
        
        #trae los datos del formulario
        id_cedula = request.form['id']
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        f_entrada = request.form['entrada']
        f_salida = request.form['salida']
        huespedes = request.form['huespedes']
        habitacion = request.form['habitacion']

        cur = mysql.connection.cursor()

        try:
            
            cur.execute("""
                INSERT INTO reservas (id, nombre, email, telefono, fecha_entrada, fecha_salida, huespedes, habitacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_cedula, nombre, email, telefono, f_entrada, f_salida, huespedes, habitacion))
            
            cur.execute("""
                INSERT IGNORE INTO usuarios (id, email, password) 
                VALUES (%s, %s, %s)
            """, (id_cedula, email, id_cedula))

            mysql.connection.commit()

            session['usuario_id']=id_cedula
            session['usuario_email']=email
            
            flash('Reserva confirmada')

        except Exception as e:
            print(f"Error: {e}")
            mysql.connection.rollback()
        finally:
            cur.close()

        return redirect(url_for('reservas'))

@app.route('/reservas')
def reservas():

    if 'usuario_id' not in session:

        flash("Por favor inicia sesión para ver tus reservas")
        return redirect(url_for('index')) 

    cedula = session['usuario_id']
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM reservas WHERE id = %s', [cedula])
    
    mis_reservas = cur.fetchall()
    cur.close()

    return render_template('reservas.html', lista_reservas=mis_reservas)

@app.route('/eliminar_reserva/<int:id>')
def eliminar_reserva(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM reservas WHERE id=%s', [id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('reservas'))


@app.route('/login-huesped', methods=['POST'])
def login_huesped():
    email = request.form['email']
    cedula = request.form['cedula'] # La usamos como password

    cur = mysql.connection.cursor()
    # Buscamos que coincida el email y la cédula en la tabla usuarios
    cur.execute("SELECT id, email FROM usuarios WHERE email = %s AND id = %s", (email, cedula))
    usuario = cur.fetchone()
    cur.close()

    if usuario:
        session['usuario_id'] = usuario[0]
        session['usuario_email'] = usuario[1]
        return redirect(url_for('reservas'))
    else:
        flash("Datos incorrectos, verifica tu correo y cédula.")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)