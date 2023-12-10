from flask import Flask ,jsonify ,request, render_template
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app = Flask(__name__, template_folder='templates')
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://tpofinalcrystalz:t12345678@tpofinalcrystalzen.mysql.pythonanywhere-services.com/tpofinalcrystalz$default'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

# defino la tabla
class Producto(db.Model):   # la clase Producto hereda de db.Model    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    imagen=db.Column(db.String(400))
    titulo=db.Column(db.String(100))
    descripcion=db.Column(db.String(200))
    descuento=db.Column(db.Integer)
    precio=db.Column(db.Integer)
   
    
    def __init__(self, imagen, titulo, descripcion, descuento, precio):   #crea el  constructor de la clase
        self.imagen=imagen   
        self.titulo=titulo
        self.descripcion=descripcion
        self.descuento=descuento
        self.precio=precio


class Contactos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    correo = db.Column(db.String(255))
    mensaje = db.Column(db.Text)
    def __init__(self,nombre,correo,mensaje):   
        self.nombre=nombre   
        self.correo=correo
        self.mensaje=mensaje

with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','imagen','titulo','descripcion','descuento','precio')


producto_schema=ProductoSchema()            # El objeto producto_schema es para traer un producto
productos_schema=ProductoSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto

class ContactoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'correo', 'mensaje')

contacto_schema = ContactoSchema()
contactos_schema = ContactoSchema(many=True)

# crea los endpoint o rutas (json)
@app.route('/')
def inicio():
    ultimos_productos = Producto.query.order_by(Producto.id.desc()).limit(8).all()
    homeproductos = productos_schema.dump(ultimos_productos)
    return render_template('index.html', homeproductos=homeproductos)

@app.route('/quienes-somos')
def quienes_somos():
    return render_template('quienes-somos.html')

@app.route('/guia-cristales')
def guiacristale():
    return render_template('guia-cristales.html')

@app.route('/mercado')
def mercado():
    todos_productos=Producto.query.all() 
    todosproductos=productos_schema.dump(todos_productos)
    return render_template('mercado.html', todosproductos=todosproductos)

from flask import render_template, request

@app.route('/saber-mas/<int:id>', methods=['GET'])
def sabermas(id):
    detalleproducto = Producto.query.get(id)
    return render_template('saber-mas.html', detalleproducto=detalleproducto)


@app.route('/section-explorar')
def sectionexplorar():
    return render_template('section-explorar.html')

@app.route('/guia-cristales')
def guiacristales():
    return render_template('guia-cristales.html')

@app.route('/herramientas-sanacion')
def herramientassanacion():
    return render_template('herramientas-sanacion.html')

@app.route('/cuidado')
def cuidados():
    return render_template('cuidado.html')

@app.route('/cristaloterapia')
def cristaloterapias():
    return render_template('cristaloterapia.html')

@app.route('/yoga')
def yogas():
    return render_template('yoga.html')

@app.route('/gemoterapia')
def gemoterapias():
    return render_template('gemoterapia.html')

@app.route('/contacto')
def contactos():
    return render_template('contacto.html')

@app.route('/productos',methods=['GET'])
def get_Productos():
    all_productos=Producto.query.all()         # el metodo query.all() lo hereda de db.Model
    result=productos_schema.dump(all_productos)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
  
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla

@app.route('/', methods=['POST'])
def enviar_formulario():
    nombre=request.json['nombre']
    correo=request.json['correo']
    mensaje=request.json['mensaje']
    new_producto=Contactos(nombre,correo,mensaje)
    db.session.add(new_producto)
    db.session.commit()
    return contacto_schema.jsonify(new_producto)


@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    producto=Producto.query.get(id)
    return producto_schema.jsonify(producto)   # retorna el JSON de un producto recibido como parametro


@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    producto=Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)   # me devuelve un json con el registro eliminado

@app.route('/productos', methods=['POST']) # crea ruta o endpoint
def create_producto():
    #print(request.json)  # request.json contiene el json que envio el cliente
    imagen=request.json['imagen']
    titulo=request.json['titulo']
    descripcion=request.json['descripcion']
    descuento=request.json['descuento']
    precio=request.json['precio']
    new_producto=Producto(imagen,titulo,descripcion,descuento,precio)
    db.session.add(new_producto)
    db.session.commit()
    return producto_schema.jsonify(new_producto)

@app.route('/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    producto=Producto.query.get(id)
 
    producto.imagen=request.json['imagen']
    producto.titulo=request.json['titulo']
    producto.descripcion=request.json['descripcion']
    producto.descuento=request.json['descuento']
    producto.precio=request.json['precio']

    db.session.commit()
    return producto_schema.jsonify(producto)
 

# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000
