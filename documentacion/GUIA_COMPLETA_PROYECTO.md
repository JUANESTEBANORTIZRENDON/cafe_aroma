# ☕ GUÍA COMPLETA DEL PROYECTO CAFÉ AROMA
## Explicación Simple y Detallada

---

## 📚 ÍNDICE

1. [¿Qué es este proyecto?](#qué-es-este-proyecto)
2. [¿Cómo funciona?](#cómo-funciona)
3. [Componentes del proyecto](#componentes-del-proyecto)
4. [Software necesario](#software-necesario)
5. [Arquitectura completa](#arquitectura-completa)
6. [Flujo de trabajo CI/CD](#flujo-de-trabajo-cicd)
7. [Estado actual del proyecto](#estado-actual-del-proyecto)
8. [Cómo usar cada componente](#cómo-usar-cada-componente)

---

## 🎯 ¿QUÉ ES ESTE PROYECTO?

**Café Aroma** es una aplicación web completa que simula una cafetería moderna. Su objetivo principal es:

✅ **Permitir que usuarios se suscriban** a un newsletter  
✅ **Enviar emails reales** cuando alguien se suscribe  
✅ **Demostrar un flujo CI/CD profesional** (desarrollo → construcción → despliegue)  

### 🎨 Desde el punto de vista del usuario:
- Ves una página web bonita con diseño hipster moderno
- Ingresas tu email
- Recibes un correo de bienvenida en tu bandeja
- ¡Eso es todo! Simple y efectivo

### 🛠️ Desde el punto de vista técnico:
Es un **proyecto completo de DevOps** que incluye:
- Aplicación web (Flask + Python)
- Contenerización (Docker)
- Automatización (Jenkins)
- Gestión de artefactos (Artifactory)
- Base de datos (PostgreSQL)

---

## 🔄 ¿CÓMO FUNCIONA?

### Flujo Simple (Usuario Normal):

```
1. Usuario abre → http://localhost:5000
2. Ve formulario bonito
3. Ingresa su email: "juan@gmail.com"
4. Click en "Comenzar Mi Experiencia"
5. ¡Recibe email de bienvenida!
```

### Flujo Técnico (Por Detrás):

```
1. Navegador envía el email al servidor Flask
2. Flask recibe la petición en la ruta /send
3. Flask conecta con Gmail usando SMTP
4. Gmail envía el correo
5. Usuario recibe el email
6. Flask muestra mensaje: "¡Email enviado!"
```

---

## 🧩 COMPONENTES DEL PROYECTO

### 1️⃣ **APLICACIÓN WEB (Flask)**

**¿Qué es?**  
Flask es un framework de Python para crear aplicaciones web.

**Archivos principales:**
```
app.py              → Cerebro de la aplicación (lógica)
templates/          → Páginas HTML (lo que ves)
static/             → Estilos CSS (cómo se ve)
requirements.txt    → Lista de dependencias Python
```

**¿Qué hace app.py?**
```python
# Cuando alguien visita http://localhost:5000
@app.route('/')
def index():
    return render_template('index.html')  # Muestra la página

# Cuando alguien envía el formulario
@app.route('/send', methods=['POST'])
def send():
    email = request.form.get('email')  # Obtiene el email
    send_email(email, ...)             # Envía el correo
    return redirect('/')               # Vuelve a la página
```

**Variables de entorno (.env):**
```env
SMTP_HOST=smtp.gmail.com       # Servidor de Gmail
SMTP_PORT=465                  # Puerto seguro
SMTP_USER=tu_email@gmail.com   # Tu Gmail
SMTP_PASS=abcd1234efgh5678     # App Password de Gmail (NO tu contraseña)
SECRET_KEY=clave-segura         # Para proteger la sesión
```

---

### 2️⃣ **DOCKER (Contenerización)**

**¿Qué es Docker?**  
Docker empaqueta tu aplicación en un "contenedor" que funciona igual en cualquier computadora.

**Analogía:**  
Imagina que tu aplicación es una planta 🌱. Docker es como una maceta 🪴 que incluye:
- La tierra (sistema operativo)
- El agua (dependencias)
- La planta (tu código)

Puedes mover la maceta a cualquier lugar y la planta sigue funcionando igual.

**Archivos:**

**Dockerfile:**
```dockerfile
FROM python:3.11-slim           # Usa Python 3.11
WORKDIR /app                    # Carpeta de trabajo
COPY requirements.txt .         # Copia lista de dependencias
RUN pip install -r requirements.txt  # Instala dependencias
COPY . .                        # Copia todo el código
EXPOSE 5000                     # Puerto 5000
CMD ["python", "app.py"]        # Ejecuta la app
```

**docker-compose.yml:**
```yaml
services:
  cafe-aroma:
    build: .                    # Construye desde Dockerfile
    ports:
      - "5000:5000"            # Mapea puerto 5000
    env_file:
      - .env                   # Carga variables de entorno
```

**Comandos Docker:**
```bash
# Construir y ejecutar
docker compose up --build

# Ver contenedores corriendo
docker ps

# Ver logs
docker logs cafe-aroma-app

# Detener
docker compose down
```

---

### 3️⃣ **JENKINS (CI/CD - Automatización)**

**¿Qué es Jenkins?**  
Jenkins es un "robot" que automatiza tareas repetitivas:
- Construye tu aplicación
- Ejecuta pruebas
- Empaqueta todo
- Sube artefactos
- Despliega automáticamente

**Analogía:**  
Imagina que cada vez que escribes código, un asistente:
1. ✅ Verifica que funcione
2. 📦 Lo empaqueta
3. 🚀 Lo publica
4. 🎉 Lo pone en producción

¡Eso es Jenkins!

**¿Cómo funciona nuestro Jenkinsfile?**

```groovy
// Pipeline = Tubería con 6 pasos (stages)

Stage 1: Prepare Workspace
  └─ Lista archivos del proyecto

Stage 2: Package ZIP
  └─ Crea un archivo ZIP con todo el código

Stage 3: Upload ZIP to Artifactory
  └─ Sube el ZIP a Artifactory para guardarlo

Stage 4: Docker Build & Push (opcional)
  └─ Construye imagen Docker
  └─ La sube a Artifactory

Stage 5: Deploy Locally
  └─ Toma las credenciales SMTP de Jenkins
  └─ Ejecuta el contenedor con esas credenciales
  └─ ¡La app queda funcionando!

Stage 6: Health Check
  └─ Verifica que http://localhost:5000 responda
  └─ Si falla, detiene el pipeline
```

**Variables importantes:**
```groovy
ART_URL = 'http://host.docker.internal:8082/artifactory'  // URL de Artifactory
ART_GEN = 'generic-local'                                  // Repo para ZIPs
ART_DOCK = 'docker-local'                                  // Repo para imágenes
IMG_NAME = 'cafe_aroma'                                    // Nombre de la imagen
DOCKER_HOST = 'tcp://host.docker.internal:2375'           // Docker desde Jenkins
```

---

### 4️⃣ **ARTIFACTORY (Almacén de Artefactos)**

**¿Qué es Artifactory?**  
Es un "almacén" donde guardas versiones de tu aplicación.

**Analogía:**  
Como Dropbox o Google Drive, pero para software:
- Guardas ZIPs de tu código
- Guardas imágenes Docker
- Versionas todo (v1.0, v1.1, v2.0...)
- Puedes descargarlo después

**Estructura en Artifactory:**
```
artifactory/
├── generic-local/              # Repositorio genérico
│   └── cafe-aroma/
│       ├── cafe_aroma-1.zip   # Build 1
│       ├── cafe_aroma-2.zip   # Build 2
│       └── cafe_aroma-3.zip   # Build 3
│
└── docker-local/               # Repositorio Docker
    └── cafe_aroma:
        ├── latest             # Última versión
        ├── 1                  # Build 1
        ├── 2                  # Build 2
        └── 3                  # Build 3
```

---

### 5️⃣ **POSTGRESQL (Base de Datos)**

**¿Para qué?**  
Artifactory necesita una base de datos para guardar:
- Configuración
- Usuarios
- Permisos
- Metadatos de artefactos

**No almacena tus emails ni datos de la app**, solo configuración de Artifactory.

---

## 💻 SOFTWARE NECESARIO

### ✅ **LO QUE YA TIENES INSTALADO:**

1. **Windows 10/11** ✅
2. **Docker Desktop** ✅ (ya lo usamos)
3. **Python 3.11** ✅ (para desarrollo local)
4. **Git** ✅ (para control de versiones)
5. **PowerShell** ✅ (terminal de Windows)

### 📦 **LO QUE SE INSTALA AUTOMÁTICAMENTE:**

Cuando ejecutas los comandos, Docker descarga automáticamente:

1. **Python 3.11-slim** (imagen base para la app)
2. **Jenkins LTS** (servidor de automatización)
3. **Artifactory OSS** (almacén de artefactos)
4. **PostgreSQL 13** (base de datos)

### 🔑 **LO QUE NECESITAS CONFIGURAR:**

1. **Gmail App Password:**
   - Ve a: https://myaccount.google.com/security
   - Activa verificación en 2 pasos
   - Crea un "App Password"
   - Cópialo en tu archivo `.env`

2. **Archivo .env:**
   ```bash
   copy .env.example .env
   # Luego editar con tus datos reales
   ```

---

## 🏗️ ARQUITECTURA COMPLETA

```
┌─────────────────────────────────────────────────────────────────┐
│                         TU COMPUTADORA                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────┐                                             │
│  │   NAVEGADOR   │ http://localhost:5000                       │
│  └───────┬───────┘                                             │
│          │                                                      │
│          ↓                                                      │
│  ┌───────────────────────────────────────────────────────┐    │
│  │              DOCKER DESKTOP                            │    │
│  │                                                        │    │
│  │  ┌─────────────────────────────────────────────────┐ │    │
│  │  │  CONTENEDOR: cafe-aroma-app                     │ │    │
│  │  │  Puerto: 5000                                   │ │    │
│  │  │  ┌─────────────────────────────────────────┐   │ │    │
│  │  │  │  Flask App (Python)                     │   │ │    │
│  │  │  │  - Recibe peticiones web                │   │ │    │
│  │  │  │  - Renderiza HTML                        │   │ │    │
│  │  │  │  - Envía emails por SMTP ──────────┐   │   │ │    │
│  │  │  └─────────────────────────────────────┘   │   │ │    │
│  │  └─────────────────────────────────────────────────┘ │    │
│  │                                                        │    │
│  │  ┌─────────────────────────────────────────────────┐ │    │
│  │  │  CONTENEDOR: jenkins                            │ │    │
│  │  │  Puerto: 8080, 50000                           │ │    │
│  │  │  ┌─────────────────────────────────────────┐   │ │    │
│  │  │  │  Jenkins Server                         │   │ │    │
│  │  │  │  - Lee Jenkinsfile                      │   │ │    │
│  │  │  │  - Ejecuta pipeline                     │   │ │    │
│  │  │  │  - Construye, empaqueta, despliega     │   │ │    │
│  │  │  └─────────────────────────────────────────┘   │ │    │
│  │  └─────────────────────────────────────────────────┘ │    │
│  │                                                        │    │
│  │  ┌─────────────────────────────────────────────────┐ │    │
│  │  │  CONTENEDOR: artifactory-oss                    │ │    │
│  │  │  Puerto: 8081, 8082                            │ │    │
│  │  │  ┌─────────────────────────────────────────┐   │ │    │
│  │  │  │  Artifactory Server                     │   │ │    │
│  │  │  │  - Almacena ZIPs                        │   │ │    │
│  │  │  │  - Almacena imágenes Docker            │   │ │    │
│  │  │  │  - Versiona artefactos                 │   │ │    │
│  │  │  └─────────────────────────────────────────┘   │ │    │
│  │  └─────────────────────────────────────────────────┘ │    │
│  │                                                        │    │
│  │  ┌─────────────────────────────────────────────────┐ │    │
│  │  │  CONTENEDOR: artifactory-postgres               │ │    │
│  │  │  Puerto: 5432                                   │ │    │
│  │  │  ┌─────────────────────────────────────────┐   │ │    │
│  │  │  │  PostgreSQL Database                    │   │ │    │
│  │  │  │  - Guarda config de Artifactory         │   │ │    │
│  │  │  └─────────────────────────────────────────┘   │ │    │
│  │  └─────────────────────────────────────────────────┘ │    │
│  │                                                        │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │ SMTP (smtp.gmail.com:465)
                          ↓
                    ┌─────────────┐
                    │   GMAIL     │
                    │   SERVERS   │
                    └─────────────┘
                          │
                          ↓
                    ┌─────────────┐
                    │  Usuario    │
                    │  Bandeja    │
                    └─────────────┘
```

---

## 🔄 FLUJO DE TRABAJO CI/CD

### **Escenario: Haces un cambio en el código**

```
1. DESARROLLO (Tu PC)
   ├─ Editas app.py
   ├─ Agregas nueva funcionalidad
   └─ Haces commit: git commit -m "Nueva función"

2. JENKINS (Automatización)
   ├─ Stage 1: Prepare Workspace
   │   └─ Lista archivos, verifica que todo esté
   │
   ├─ Stage 2: Package ZIP
   │   └─ Crea: cafe_aroma-BUILD_5.zip
   │
   ├─ Stage 3: Upload ZIP
   │   └─ Sube a: artifactory/generic-local/cafe-aroma/
   │
   ├─ Stage 4: Docker Build & Push
   │   ├─ Construye imagen: cafe_aroma:5
   │   └─ Sube a: artifactory/docker-local/
   │
   ├─ Stage 5: Deploy Locally
   │   ├─ Detiene contenedor viejo
   │   ├─ Ejecuta nuevo contenedor
   │   └─ Con credenciales SMTP de Jenkins
   │
   └─ Stage 6: Health Check
       ├─ Intenta: curl http://localhost:5000
       └─ ✅ OK → Pipeline exitoso
           ❌ FAIL → Revierte cambios

3. PRODUCCIÓN
   └─ Tu app está corriendo con la nueva versión
```

---

## 📊 ESTADO ACTUAL DEL PROYECTO

### ✅ **SERVICIOS CORRIENDO:**

| Servicio | Puerto | Estado | URL |
|----------|--------|--------|-----|
| **Café Aroma App** | 5000 | ✅ UP | http://localhost:5000 |
| **Jenkins** | 8080 | ✅ UP | http://localhost:8080 |
| **Artifactory** | 8082 | ✅ UP | http://localhost:8082/ui |
| **PostgreSQL** | 5432 | ✅ UP | (interno) |

### 🔑 **CREDENCIALES:**

**Jenkins:**
- URL: http://localhost:8080
- Password inicial: `958f7c349b8c4362bd898cd98481c1fe`
- (Cambiar en primer login)

**Artifactory:**
- URL: http://localhost:8082/ui
- Usuario: `admin`
- Password: `admin123456789.`
- (Cambiar en primer login)

---

## 🎮 CÓMO USAR CADA COMPONENTE

### 1️⃣ **USAR LA APLICACIÓN WEB**

```bash
# Método 1: Docker (recomendado)
docker compose up -d
# Abrir: http://localhost:5000

# Método 2: Local (desarrollo)
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python app.py
# Abrir: http://localhost:5000
```

**Probar el envío de email:**
1. Abre http://localhost:5000
2. Ingresa tu email real
3. Click en "Comenzar Mi Experiencia"
4. Revisa tu bandeja (puede ir a spam)

---

### 2️⃣ **CONFIGURAR JENKINS**

```bash
# 1. Abrir Jenkins
http://localhost:8080

# 2. Password inicial
958f7c349b8c4362bd898cd98481c1fe

# 3. Install suggested plugins → Esperar

# 4. Crear usuario admin
Usuario: admin
Password: admin123
Email: admin@localhost

# 5. Configurar credenciales
Manage Jenkins → Credentials → System → Global credentials

# Credencial 1: smtp-gmail
- Kind: Username with password
- ID: smtp-gmail
- Username: juanestebanortizrendon24072004@gmail.com
- Password: kjhdtevybncwbxfe
- Description: Gmail SMTP

# Credencial 2: artifactory-creds
- Kind: Username with password
- ID: artifactory-creds
- Username: admin
- Password: admin123456789. (o tu password de Artifactory)
- Description: Artifactory Admin

# 6. Crear Pipeline Job
New Item → Pipeline → cafe-aroma

# 7. En Pipeline section:
Definition: Pipeline script
Script: [Pegar contenido completo de Jenkinsfile]

# 8. Save → Build Now
```

**Verificar pipeline:**
```
✅ Stage 1: Prepare Workspace → Lista archivos
✅ Stage 2: Package ZIP → Crea ZIP
✅ Stage 3: Upload → Sube a Artifactory
✅ Stage 4: Docker Build → Construye imagen
✅ Stage 5: Deploy → Ejecuta contenedor
✅ Stage 6: Health Check → Verifica app
```

---

### 3️⃣ **USAR ARTIFACTORY**

```bash
# 1. Abrir Artifactory
http://localhost:8082/ui

# 2. Login inicial
Usuario: admin
Password: password

# 3. Cambiar password
Welcome → Set Me Up → Change Password

# 4. Crear repositorios
Administration → Repositories → Local

# Repositorio 1: generic-local
- Type: Generic
- Repository Key: generic-local
- Description: Generic repository for ZIPs
- Save

# Repositorio 2: docker-local
- Type: Docker
- Repository Key: docker-local
- Description: Docker images repository
- Save

# 5. Verificar artefactos
Artifacts → generic-local → cafe-aroma
(Verás los ZIPs de cada build)

Artifacts → docker-local → cafe_aroma
(Verás las imágenes Docker)
```

---

### 4️⃣ **COMANDOS ÚTILES**

**Ver todos los contenedores:**
```powershell
docker ps
```

**Ver logs:**
```powershell
docker logs -f cafe-aroma-app     # App Flask
docker logs -f jenkins             # Jenkins
docker logs -f artifactory-oss     # Artifactory
```

**Reiniciar servicios:**
```powershell
docker restart cafe-aroma-app
docker restart jenkins
docker restart artifactory-oss
```

**Detener todo:**
```powershell
docker compose down                # App
docker stop jenkins                # Jenkins
.\scripts\setup_artifactory.ps1 -Stop  # Artifactory
```

**Iniciar todo:**
```powershell
docker compose up -d               # App
docker start jenkins               # Jenkins
.\scripts\setup_artifactory.ps1    # Artifactory
```

---

## 🔍 VERIFICACIÓN COMPLETA

### ✅ **CHECKLIST FINAL:**

```bash
# 1. ¿Docker Desktop está corriendo?
docker version
# ✅ Debe mostrar Client + Server

# 2. ¿Todos los contenedores están UP?
docker ps
# ✅ Debe mostrar 4 contenedores

# 3. ¿La app responde?
curl http://localhost:5000
# ✅ Debe retornar HTML

# 4. ¿Jenkins responde?
curl http://localhost:8080
# ✅ Debe retornar HTML de Jenkins

# 5. ¿Artifactory responde?
curl http://localhost:8082/artifactory/api/system/ping
# ✅ Debe retornar "OK"

# 6. ¿El envío de email funciona?
# ✅ Probar desde el navegador
```

---

## 🎓 CONCEPTOS CLAVE EXPLICADOS SIMPLE

### **1. ¿Qué es un contenedor?**
Es como una caja que contiene todo lo necesario para que un programa funcione:
- Sistema operativo mini
- Dependencias
- Tu código

**Ventaja:** Funciona igual en cualquier computadora.

### **2. ¿Qué es CI/CD?**
**CI** = Continuous Integration (Integración Continua)
- Cada cambio se integra automáticamente
- Se verifica que funcione
- Se empaqueta

**CD** = Continuous Deployment (Despliegue Continuo)
- Cada cambio verificado se despliega automáticamente
- Sin intervención manual
- Rápido y seguro

### **3. ¿Por qué usar Jenkins?**
Sin Jenkins:
```
1. Cambias código
2. Manualmente construyes
3. Manualmente pruebas
4. Manualmente subes
5. Manualmente despliegas
= 😫 Mucho trabajo manual
```

Con Jenkins:
```
1. Cambias código
2. Jenkins hace todo lo demás automáticamente
= 😎 Relajado
```

### **4. ¿Por qué usar Artifactory?**
- **Versionado:** Puedes volver a versiones anteriores
- **Backup:** Tienes copia de todo
- **Compartir:** Otros pueden descargar tus builds
- **Organización:** Todo en un solo lugar

### **5. ¿Por qué usar Docker?**
Sin Docker:
```
Desarrollador: "En mi PC funciona"
Producción: "En mi servidor no funciona"
= 😭 Problemas de compatibilidad
```

Con Docker:
```
Desarrollador: "Aquí está el contenedor"
Producción: "Funciona perfecto"
= 😊 Mismo comportamiento en todos lados
```

---

## 📝 RESUMEN EJECUTIVO

### **¿Qué hace este proyecto?**
1. Muestra una página web bonita
2. Permite suscribirse al newsletter
3. Envía emails reales
4. Todo automatizado con Jenkins
5. Todo versionado en Artifactory

### **¿Para qué sirve?**
- **Aprender DevOps:** CI/CD, Docker, automatización
- **Demostrar habilidades:** Proyecto completo para portafolio
- **Base para proyectos reales:** Estructura escalable

### **¿Qué tecnologías incluye?**
- **Backend:** Flask (Python)
- **Frontend:** HTML + CSS moderno
- **Contenedores:** Docker + Docker Compose
- **CI/CD:** Jenkins
- **Artefactos:** Artifactory OSS
- **Base de Datos:** PostgreSQL
- **Email:** SMTP Gmail

### **¿Qué aprendiste con esto?**
✅ Desarrollo web con Flask  
✅ Contenerización con Docker  
✅ Automatización con Jenkins  
✅ Gestión de artefactos  
✅ Integración continua  
✅ Despliegue continuo  
✅ Configuración de servicios  
✅ Manejo de secretos y credenciales  

---

## 🎉 CONCLUSIÓN

Tienes un proyecto **profesional y completo** que incluye:

1. ✅ **Aplicación funcional** (envía emails reales)
2. ✅ **Contenerizada** (funciona en cualquier lugar)
3. ✅ **Automatizada** (Jenkins hace todo)
4. ✅ **Versionada** (Artifactory guarda todo)
5. ✅ **Documentada** (este archivo + README + análisis)

**¡Felicitaciones!** 🎊 Tienes un proyecto digno de:
- Portafolio profesional
- Entrevistas técnicas
- Base para proyectos reales
- Certificaciones DevOps

---

## 📞 TROUBLESHOOTING RÁPIDO

### Problema: "Docker no funciona"
```powershell
# Solución: Iniciar Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
Start-Sleep -Seconds 30
docker ps
```

### Problema: "Jenkins no responde"
```powershell
# Solución: Reiniciar Jenkins
docker restart jenkins
Start-Sleep -Seconds 20
curl http://localhost:8080
```

### Problema: "No llegan los emails"
1. Verifica tu App Password de Gmail
2. Revisa los logs: `docker logs cafe-aroma-app`
3. Verifica que el archivo `.env` tenga los datos correctos
4. Revisa la carpeta de spam

### Problema: "Artifactory muy lento"
```powershell
# Solución: Darle más memoria a Docker
# Docker Desktop → Settings → Resources → Memory: 6GB
docker restart artifactory-oss
```

---

**📅 Última actualización:** 26 de Octubre, 2025  

**📦 Proyecto:** Café Aroma - DevOps Complete Stack
