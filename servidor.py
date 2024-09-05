from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

#instancia de la clase Flask de la biblioteca flask
app = Flask(__name__)

#Configurar la DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Inicializar la BD
db = SQLAlchemy(app)

#Crear modelo BD
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    nombre_servicio = db.Column(db.String(50), nullable=False)
    nivel_severidad = db.Column(db.String(20), nullable=False)
    mensaje = db.Column(db.String(200), nullable=False)
    fecha_recepcion =db.Column(db.DateTime, default = datetime.utcnow)

#pagina de inicio
#Endpoint para recibir logs
@app.route('/logs',methods=['POST'])
def recibir_log():
    data = request.json
    token = request.headers.get('Authorization')

    #Validar Token
    if not validar_token(token):
        return jsonify({'error': 'Token no valido'}), 403 # El código de estado HTTP 403 o 403 Forbidden indica que el servidor ha recibido una petición, pero no permite el acceso al recurso solicitado
    
    
    #Crear un nuevo log
    nuevo_log = Log(
        fecha_evento = datetime.fromisoformat(data['timestamp']),
        nombre_servicio = data['service_name'],
        nivel_severidad = data['log_level'],
        mensaje = data['message']
    )

    #Guardamos los nuevos logs en la db
    db.session.add(nuevo_log)
    db.session.commit()

    return jsonify ({'mensaje' : 'Log recibido correctamente'}), 201 #El código de estado HTTP 201 "Creado" indica que una solicitud HTTP se realizó correctamente y que se creó un nuevo recurso
    
#@Endpoint para vizualizar los logs en el navegador
@app.route('/', methods = ['GET'])
def ver_logs():
    logs = Log.query.order_by(Log.fecha_evento.desc()).all()
    zona_horaria_local = pytz.timezone('America/Asuncion')
    logs_convertidos = []
    for log in logs:
        log_dict = log.__dict__.copy()
        log_dict['fecha_evento'] = log.fecha_evento.replace(tzinfo=pytz.utc).astimezone(zona_horaria_local)
        log_dict['fecha_recepcion'] = log.fecha_evento.replace(tzinfo=pytz.utc).astimezone(zona_horaria_local)
        logs_convertidos.append(log_dict)
    return render_template('ver_logs.html', logs= logs_convertidos)

#Definir Validar Tokens
def validar_token(token):
    tokens_validos = ['token_servicio1', 'token_servicio2', 'token_servicio3']
    return token.split()[-1] in tokens_validos #Compruba si el token esta en la lista de token validos

# Inicializar la base de datos

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(port=5001)





    








