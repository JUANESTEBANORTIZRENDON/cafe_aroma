"""
Café Aroma - Flask Application
==============================
Una aplicación web simple que permite a los usuarios enviar emails
a través de un formulario web usando SMTP de Gmail.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, flash, redirect, url_for

# Cargar variables de entorno solo en desarrollo local
if os.path.exists('.env'):
    from dotenv import load_dotenv
    load_dotenv()

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configuración de la aplicación
# SECRET_KEY es necesario para usar flash messages y sesiones
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# Configuración SMTP desde variables de entorno
SMTP_CONFIG = {
    'host': os.getenv('SMTP_HOST', 'smtp.gmail.com'),
    'port': int(os.getenv('SMTP_PORT', '465')),
    'user': os.getenv('SMTP_USER'),
    'password': os.getenv('SMTP_PASS'),
    'from_email': os.getenv('SMTP_FROM')
}


def send_email(to_email, subject, message):
    """
    Envía un email usando SMTP_SSL de Gmail
    
    Args:
        to_email (str): Dirección de email del destinatario
        subject (str): Asunto del email
        message (str): Contenido del mensaje
    
    Returns:
        bool: True si el email se envió correctamente, False en caso contrario
    """
    try:
        # Crear el mensaje MIME
        msg = MIMEMultipart()
        msg['From'] = SMTP_CONFIG['from_email']
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Agregar el cuerpo del mensaje
        msg.attach(MIMEText(message, 'plain', 'utf-8'))
        
        # Establecer conexión SMTP_SSL (puerto 465)
        with smtplib.SMTP_SSL(SMTP_CONFIG['host'], SMTP_CONFIG['port']) as server:
            # Autenticarse con las credenciales
            server.login(SMTP_CONFIG['user'], SMTP_CONFIG['password'])
            
            # Enviar el email
            text = msg.as_string()
            server.sendmail(SMTP_CONFIG['from_email'], to_email, text)
            
        return True
        
    except Exception as e:
        print(f"Error al enviar email: {str(e)}")
        return False


@app.route('/')
def index():
    """
    Ruta principal que muestra la página de inicio con el formulario
    
    Returns:
        str: Template HTML renderizado
    """
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send():
    """
    Ruta que procesa el formulario y envía el email
    Acepta solo métodos POST
    
    Returns:
        str: Redirección a la página principal con mensaje de estado
    """
    # Obtener el email del formulario
    email = request.form.get('email')
    
    # Validar que se proporcionó un email
    if not email:
        flash('Por favor, ingresa una dirección de email válida.', 'error')
        return redirect(url_for('index'))
    
    # Verificar que las variables SMTP estén configuradas
    if not all([SMTP_CONFIG['user'], SMTP_CONFIG['password'], SMTP_CONFIG['from_email']]):
        flash('Error de configuración del servidor. Contacta al administrador.', 'error')
        return redirect(url_for('index'))
    
    # Preparar el contenido del email
    subject = "¡Bienvenido a Café Aroma!"
    message = f"""
    ¡Hola!
    
    Gracias por tu interés en Café Aroma. 
    Hemos recibido tu solicitud desde nuestra página web.
    
    Tu email registrado: {email}
    
    ¡Esperamos verte pronto en nuestro café!
    
    Saludos cordiales,
    El equipo de Café Aroma
    """
    
    # Intentar enviar el email
    if send_email(email, subject, message):
        flash('¡Email enviado correctamente! Revisa tu bandeja de entrada.', 'success')
    else:
        flash('Error al enviar el email. Por favor, inténtalo más tarde.', 'error')
    
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    """
    Manejador de errores 404 (página no encontrada)
    
    Args:
        error: Objeto de error de Flask
        
    Returns:
        tuple: Template HTML y código de estado HTTP
    """
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Manejador de errores 500 (error interno del servidor)
    
    Args:
        error: Objeto de error de Flask
        
    Returns:
        tuple: Template HTML y código de estado HTTP
    """
    flash('Error interno del servidor. Por favor, inténtalo más tarde.', 'error')
    return render_template('index.html'), 500


if __name__ == '__main__':
    """
    Punto de entrada principal de la aplicación
    Configura el servidor para ejecutarse en todas las interfaces (0.0.0.0)
    en el puerto 5000 con modo debug activado
    """
    print("🚀 Iniciando Café Aroma...")
    print(f"📧 SMTP configurado para: {SMTP_CONFIG['host']}:{SMTP_CONFIG['port']}")
    print("🌐 Servidor disponible en: http://localhost:5000")
    
    # Ejecutar la aplicación Flask
    app.run(
        host="0.0.0.0",  # Permite conexiones desde cualquier IP
        port=5000,       # Puerto de la aplicación
        debug=True       # Modo debug para desarrollo
    )
