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


def send_email(to_email, subject, html_message, text_message):
    """
    Envía un email con HTML y texto plano usando SMTP_SSL de Gmail
    
    Args:
        to_email (str): Dirección de email del destinatario
        subject (str): Asunto del email
        html_message (str): Contenido HTML del mensaje
        text_message (str): Contenido de texto plano como fallback
    
    Returns:
        bool: True si el email se envió correctamente, False en caso contrario
    """
    try:
        # Crear el mensaje MIME multipart
        msg = MIMEMultipart('alternative')
        msg['From'] = SMTP_CONFIG['from_email']
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Crear las partes del mensaje
        text_part = MIMEText(text_message, 'plain', 'utf-8')
        html_part = MIMEText(html_message, 'html', 'utf-8')
        
        # Agregar las partes al mensaje (texto primero, HTML después)
        msg.attach(text_part)
        msg.attach(html_part)
        
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
    
    # Preparar el contenido del email con HTML moderno
    subject = "🚀 ¡Bienvenido a la Experiencia Café Aroma! ☕✨"
    
    # Email HTML con diseño moderno y atractivo
    html_message = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bienvenido a Café Aroma</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Dancing+Script:wght@400;600;700&display=swap');
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Poppins', sans-serif;
                line-height: 1.6;
                color: #2c1810;
                background: linear-gradient(135deg, #f5deb3 0%, #deb887 100%);
                padding: 20px;
            }}
            
            .email-container {{
                max-width: 600px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(44, 24, 16, 0.2);
                border: 1px solid rgba(212, 165, 116, 0.3);
            }}
            
            .header {{
                background: linear-gradient(135deg, #2c1810 0%, #8b4513 50%, #d4a574 100%);
                padding: 40px 30px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            
            .header::before {{
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
                animation: rotate 20s linear infinite;
            }}
            
            @keyframes rotate {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}
            
            .logo {{
                font-family: 'Dancing Script', cursive;
                font-size: 3em;
                font-weight: 700;
                color: white;
                margin-bottom: 10px;
                text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
                position: relative;
                z-index: 2;
            }}
            
            .tagline {{
                color: #f5deb3;
                font-size: 1.1em;
                font-weight: 300;
                letter-spacing: 1px;
                text-transform: uppercase;
                position: relative;
                z-index: 2;
            }}
            
            .content {{
                padding: 40px 30px;
            }}
            
            .welcome-title {{
                font-size: 2em;
                font-weight: 600;
                color: #2c1810;
                margin-bottom: 20px;
                text-align: center;
            }}
            
            .welcome-text {{
                font-size: 1.1em;
                color: #8b4513;
                margin-bottom: 30px;
                text-align: center;
                line-height: 1.8;
            }}
            
            .user-info {{
                background: linear-gradient(135deg, rgba(245, 222, 179, 0.3) 0%, rgba(222, 184, 135, 0.3) 100%);
                padding: 20px;
                border-radius: 15px;
                margin: 30px 0;
                border-left: 4px solid #d4a574;
            }}
            
            .features {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            
            .feature {{
                text-align: center;
                padding: 20px;
                background: rgba(245, 222, 179, 0.2);
                border-radius: 15px;
                border: 1px solid rgba(212, 165, 116, 0.3);
            }}
            
            .feature-icon {{
                font-size: 2em;
                margin-bottom: 10px;
                display: block;
            }}
            
            .feature-title {{
                font-weight: 600;
                color: #2c1810;
                margin-bottom: 5px;
            }}
            
            .feature-text {{
                font-size: 0.9em;
                color: #8b4513;
            }}
            
            .cta-section {{
                background: linear-gradient(45deg, #ff6b35, #f7931e, #ffcd3c);
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                margin: 30px 0;
                color: white;
            }}
            
            .cta-title {{
                font-size: 1.5em;
                font-weight: 600;
                margin-bottom: 15px;
            }}
            
            .cta-button {{
                display: inline-block;
                background: white;
                color: #ff6b35;
                padding: 15px 30px;
                border-radius: 50px;
                text-decoration: none;
                font-weight: 600;
                font-size: 1.1em;
                margin-top: 15px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
            }}
            
            .footer {{
                background: #2c1810;
                color: #f5deb3;
                padding: 30px;
                text-align: center;
            }}
            
            .footer-text {{
                margin-bottom: 10px;
            }}
            
            .social-links {{
                margin-top: 20px;
            }}
            
            .social-links span {{
                font-size: 1.5em;
                margin: 0 10px;
            }}
            
            @media (max-width: 600px) {{
                .email-container {{
                    margin: 10px;
                    border-radius: 15px;
                }}
                
                .header, .content, .footer {{
                    padding: 20px;
                }}
                
                .logo {{
                    font-size: 2.5em;
                }}
                
                .features {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="logo">☕ Café Aroma</div>
                <div class="tagline">Experiencia Artesanal de Café</div>
            </div>
            
            <div class="content">
                <h1 class="welcome-title">🌟 ¡Bienvenido a Nuestra Familia Cafetera!</h1>
                
                <p class="welcome-text">
                    ¡Hola! Nos emociona muchísimo que te hayas unido a la experiencia Café Aroma. 
                    Acabas de dar el primer paso hacia un mundo lleno de sabores únicos, 
                    aromas extraordinarios y momentos inolvidables. ✨
                </p>
                
                <div class="user-info">
                    <strong>📧 Tu email registrado:</strong> {email}<br>
                    <strong>📅 Fecha de registro:</strong> Hoy<br>
                    <strong>🎯 Estado:</strong> ¡Activo y listo para la aventura!
                </div>
                
                <div class="features">
                    <div class="feature">
                        <span class="feature-icon">🌱</span>
                        <div class="feature-title">Granos Premium</div>
                        <div class="feature-text">Origen sostenible y ético</div>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">👨‍🍳</span>
                        <div class="feature-title">Baristas Expertos</div>
                        <div class="feature-text">Maestros del café artesanal</div>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">🎨</span>
                        <div class="feature-title">Ambiente Único</div>
                        <div class="feature-text">Espacio hipster moderno</div>
                    </div>
                </div>
                
                <div class="cta-section">
                    <div class="cta-title">🚀 ¿Listo para tu primera experiencia?</div>
                    <p>Visítanos y descubre por qué somos el café favorito de los verdaderos conocedores.</p>
                    <a href="#" class="cta-button">🗺️ Encontrar Ubicación</a>
                </div>
                
                <p style="text-align: center; color: #8b4513; font-style: italic; margin-top: 30px;">
                    "Cada taza cuenta una historia, cada sorbo es una aventura." 💫
                </p>
            </div>
            
            <div class="footer">
                <div class="footer-text">
                    <strong>Café Aroma</strong> - Experiencia Artesanal de Café
                </div>
                <div class="footer-text">
                    Hecho con ❤️ y mucho ☕ por artesanos del código
                </div>
                <div class="social-links">
                    <span>📱</span> <span>🌐</span> <span>📧</span> <span>📍</span>
                </div>
                <div style="margin-top: 15px; font-size: 0.9em; opacity: 0.8;">
                    © 2024 Café Aroma. Todos los derechos reservados.
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Mensaje de texto plano como fallback
    text_message = f"""
    🚀 ¡Bienvenido a Café Aroma! ☕✨
    
    ¡Hola! Nos emociona que te hayas unido a nuestra familia cafetera.
    
    📧 Tu email registrado: {email}
    🎯 Estado: ¡Activo y listo para la aventura!
    
    🌟 Lo que te espera:
    🌱 Granos premium de origen sostenible
    👨‍🍳 Baristas expertos y apasionados  
    🎨 Ambiente hipster único y moderno
    
    ¡Esperamos verte pronto en nuestro café!
    
    Con amor y mucho café ☕,
    El equipo de Café Aroma
    """
    
    # Intentar enviar el email con HTML y texto plano
    if send_email(email, subject, html_message, text_message):
        flash('🎉 ¡Email enviado correctamente! Revisa tu bandeja de entrada y prepárate para una experiencia increíble. ✨', 'success')
    else:
        flash('😔 Error al enviar el email. Por favor, inténtalo más tarde o contacta a nuestro equipo.', 'error')
    
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
