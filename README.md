# ☕ Café Aroma - Experiencia Artesanal de Café

Una aplicación web Flask moderna con diseño hipster que ofrece una experiencia única de café artesanal. Los usuarios pueden suscribirse a nuestra newsletter y recibir emails reales usando SMTP de Gmail.

## ✨ Características Principales

### 🎨 **Diseño Moderno e Hipster**
- **Interfaz contemporánea** con animaciones CSS avanzadas
- **Tipografía Google Fonts** (Poppins + Dancing Script)
- **Efectos visuales** con glassmorphism y gradientes
- **Animaciones fluidas** con transiciones suaves
- **Responsive design** optimizado para todos los dispositivos

### 🚀 **Funcionalidades Técnicas**
- **Envío de emails reales** usando SMTP_SSL de Gmail (puerto 465)
- **Validación en tiempo real** del formulario con JavaScript
- **Configuración segura** por variables de entorno
- **Dockerizado** para despliegue fácil y escalable
- **Manejo robusto de errores** con mensajes flash elegantes

### 🎯 **Experiencia de Usuario**
- **Efectos de parallax** suaves al hacer scroll
- **Animaciones de entrada** para elementos
- **Feedback visual** en formularios
- **Mensajes de estado** con iconos y colores

## 📁 Estructura del Proyecto

```
cafe_aroma/
├── app.py                 # 🐍 Aplicación Flask principal con SMTP
├── requirements.txt       # 📦 Dependencias (Flask + python-dotenv)
├── Dockerfile            # 🐳 Configuración Docker (Python 3.11-slim)
├── docker-compose.yml    # 🚀 Orquestación con variables de entorno
├── .dockerignore         # 🚫 Optimización del build Docker
├── .gitignore           # 🔒 Archivos a ignorar en Git
├── .env                 # 🔐 Variables de entorno (SMTP, SECRET_KEY)
├── README.md            # 📖 Documentación completa
├── templates/
│   └── index.html       # 🎨 Landing page moderna con JavaScript
└── static/
    └── style.css        # ✨ Estilos CSS hipster con animaciones
```

## 🎨 **Nuevas Características de Diseño**

### **Paleta de Colores Moderna**
- **Primary:** `#2c1810` (Café oscuro profundo)
- **Secondary:** `#8b4513` (Café medio)
- **Accent:** `#d4a574` (Dorado café)
- **Gradientes:** Múltiples combinaciones para efectos visuales

### **Animaciones CSS Avanzadas**
- ✨ **Shimmer effect** en el contenedor principal
- 🌊 **Float animation** en el background
- 📈 **Slide-in animations** para secciones
- 🔄 **Rotate effects** en elementos hero
- 💫 **Hover transformations** en tarjetas

### **Efectos Visuales Modernos**
- 🔍 **Glassmorphism** con backdrop-filter
- 🎭 **3D transforms** en hover states
- 🌈 **Gradient overlays** dinámicos
- 💎 **Box shadows** suaves y profundas

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

## 🆕 **Últimas Actualizaciones**

### **v2.0 - Diseño Hipster Moderno** *(Actualización Reciente)*

#### **🎨 Mejoras Visuales**
- ✅ **Rediseño completo** con estética hipster contemporánea
- ✅ **Nuevas animaciones CSS** con efectos avanzados
- ✅ **Tipografía moderna** Google Fonts (Poppins + Dancing Script)
- ✅ **Paleta de colores** inspirada en café artesanal
- ✅ **Efectos glassmorphism** y gradientes dinámicos

#### **⚡ Mejoras de Interactividad**
- ✅ **JavaScript mejorado** con validación en tiempo real
- ✅ **Efectos de parallax** suaves al hacer scroll
- ✅ **Animaciones de entrada** con Intersection Observer
- ✅ **Feedback visual** mejorado en formularios
- ✅ **Estados de hover** con transformaciones 3D

#### **🔧 Optimizaciones Técnicas**
- ✅ **Variables CSS** para mantenimiento fácil
- ✅ **Responsive design** mejorado para móviles
- ✅ **Performance optimizada** con animaciones eficientes
- ✅ **Accesibilidad mejorada** con ARIA labels
- ✅ **SEO optimizado** con meta tags actualizados

## 🚀 **Roadmap Futuro**

### **v2.1 - Próximas Mejoras**
- 🔄 **Modo oscuro/claro** toggle
- 📱 **PWA support** para instalación móvil
- 🌐 **Internacionalización** (ES/EN)
- 📊 **Analytics dashboard** para administradores
- 🔔 **Notificaciones push** para suscriptores

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autor

Desarrollado con ❤️ y mucho ☕ por artesanos del código

---

**¡Disfruta tu café y tu código con estilo hipster!** ☕✨🎨
