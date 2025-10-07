# ☕ Café Aroma

Una aplicación web Flask que permite a los usuarios registrarse para recibir newsletters por email usando SMTP de Gmail.

## 🚀 Características

- **Landing page atractiva** con formulario de suscripción
- **Envío de emails reales** usando SMTP_SSL de Gmail (puerto 465)
- **Configuración por variables de entorno** (no hardcodeadas)
- **Dockerizado** para fácil despliegue
- **Responsive design** con estilos CSS modernos
- **Manejo de errores** y mensajes flash para el usuario

## 📁 Estructura del Proyecto

```
cafe_aroma/
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias de Python
├── Dockerfile            # Configuración de Docker
├── docker-compose.yml    # Orquestación de contenedores
├── .gitignore           # Archivos a ignorar en Git
├── README.md            # Este archivo
├── templates/
│   └── index.html       # Página principal con formulario
└── static/
    └── style.css        # Estilos CSS
```

## 🔧 Configuración de Variables de Entorno

### Variables Requeridas

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Configuración SMTP de Gmail
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=tu-email@gmail.com
SMTP_PASS=tu-app-password
SMTP_FROM=tu-email@gmail.com

# Clave secreta para Flask
SECRET_KEY=tu-clave-secreta-muy-segura
```

### 📧 Configuración de Gmail App Password

1. Ve a tu [cuenta de Google](https://myaccount.google.com/)
2. Selecciona **Seguridad** > **Verificación en 2 pasos**
3. En la parte inferior, selecciona **Contraseñas de aplicaciones**
4. Selecciona la aplicación y el dispositivo
5. Copia la contraseña generada y úsala como `SMTP_PASS`

## 🏃‍♂️ Ejecución Local

### Opción 1: Entorno Virtual Python

1. **Clonar el repositorio**
   ```bash
   git clone <tu-repositorio>
   cd cafe_aroma
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   - Crea el archivo `.env` con las variables mencionadas arriba

5. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

6. **Abrir en el navegador**
   - Ve a: http://localhost:5000

### Opción 2: Docker

1. **Configurar variables de entorno**
   - Crea el archivo `.env` con las variables requeridas

2. **Construir y ejecutar con Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Abrir en el navegador**
   - Ve a: http://localhost:5000

### Opción 3: Docker Manual

1. **Construir la imagen**
   ```bash
   docker build -t cafe-aroma .
   ```

2. **Ejecutar el contenedor**
   ```bash
   docker run -p 5000:5000 \
     -e SMTP_HOST=smtp.gmail.com \
     -e SMTP_PORT=465 \
     -e SMTP_USER=tu-email@gmail.com \
     -e SMTP_PASS=tu-app-password \
     -e SMTP_FROM=tu-email@gmail.com \
     -e SECRET_KEY=tu-clave-secreta \
     cafe-aroma
   ```

## 🔒 Seguridad

- **Nunca hardcodees credenciales** en el código
- **Usa App Passwords** de Gmail en lugar de tu contraseña principal
- **Cambia SECRET_KEY** en producción
- **Mantén el archivo .env** fuera del control de versiones

## 🐛 Solución de Problemas

### Error: "Error de configuración del servidor"
- Verifica que todas las variables SMTP estén configuradas en `.env`
- Asegúrate de usar un App Password válido de Gmail

### Error: "Authentication failed"
- Verifica que el App Password sea correcto
- Confirma que la verificación en 2 pasos esté habilitada en Gmail

### Error: "Connection refused"
- Verifica la configuración de red
- Asegúrate de que el puerto 5000 esté disponible

## 📝 Desarrollo

### Estructura del Código

- **`app.py`**: Aplicación Flask principal con rutas y lógica de email
- **`templates/index.html`**: Interfaz de usuario con formulario
- **`static/style.css`**: Estilos CSS responsivos
- **`requirements.txt`**: Dependencias del proyecto

### Agregar Nuevas Funcionalidades

1. **Nuevas rutas**: Agrégalas en `app.py`
2. **Nuevos templates**: Créalos en `templates/`
3. **Nuevos estilos**: Modifica `static/style.css`
4. **Nuevas dependencias**: Agrégalas a `requirements.txt`

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autor

Desarrollado con ❤️ y mucho ☕

---

**¡Disfruta tu café y tu código!** ☕✨
