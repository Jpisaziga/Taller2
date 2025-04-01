import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


app = Flask(_name_)
database_url = os.environ.get('DATABASE_URL', 'postgresql://concesionario_kro8_user:sDgbPHOLp8b6nKrAPlZ9kOIcmF5jy38I@dpg-cvlg2g56ubrc73cgd5ag-a.oregon-postgres.render.com/concesionario_kro8')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url.replace('postgres://', 'postgresql://')
db = SQLAlchemy(app)

# Modelo de Producto
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.Text)

    def __repr__(self):
        return f'<Producto {self.nombre}>'

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        descripcion = request.form['descripcion']
        
        nuevo_producto = Producto(
            nombre=nombre, 
            precio=precio, 
            stock=stock, 
            descripcion=descripcion
        )
        
        db.session.add(nuevo_producto)
        db.session.commit()
        
        flash('Producto agregado correctamente', 'success')
        return redirect(url_for('ver_productos'))
    
    return render_template('agregar_producto.html')

@app.route('/productos')
def ver_productos():
    productos = Producto.query.all()
    return render_template('ver_productos.html', productos=productos)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = float(request.form['precio'])
        producto.stock = int(request.form['stock'])
        producto.descripcion = request.form['descripcion']
        
        db.session.commit()
        
        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('ver_productos'))
    
    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    
    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('ver_productos'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear tablas si no existen
    app.run(debug=True)
