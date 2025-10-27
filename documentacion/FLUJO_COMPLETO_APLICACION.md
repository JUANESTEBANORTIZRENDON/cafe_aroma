# 🔄 Flujo Completo de la Aplicación - Café Aroma

> **Guía detallada del flujo de trabajo, integración de servicios y funcionamiento del proyecto Café Aroma desde el desarrollo hasta el despliegue.**

---

## 📑 Índice

1. [Visión General del Proyecto](#-visión-general-del-proyecto)
2. [Arquitectura del Sistema](#-arquitectura-del-sistema)
3. [Flujo de Desarrollo Completo](#-flujo-de-desarrollo-completo)
4. [Integración con Docker](#-integración-con-docker)
5. [Integración con Jenkins](#-integración-con-jenkins)
6. [Integración con Artifactory](#-integración-con-artifactory)
7. [Pipeline CI/CD Detallado](#-pipeline-cicd-detallado)
8. [Gestión de Credenciales](#-gestión-de-credenciales)
9. [Networking y Acceso Remoto](#-networking-y-acceso-remoto)
10. [Monitoreo y Mantenimiento](#-monitoreo-y-mantenimiento)

---

## 🎯 Visión General del Proyecto

### **¿Qué es Café Aroma?**

Café Aroma es una aplicación web Flask para una cafetería artesanal que permite a los usuarios:
- Explorar información sobre la cafetería
- Suscribirse a un newsletter mediante email
- Recibir confirmaciones por correo electrónico vía SMTP

### **Stack Tecnológico**

```
┌─────────────────────────────────────────────────────────────┐
│                     CAFÉ AROMA STACK                        │
├─────────────────────────────────────────────────────────────┤
│  Frontend:      HTML5 + CSS3 + JavaScript (Vanilla)        │
│  Backend:       Python 3.11 + Flask 2.3.3                  │
│  Base de Datos: No requiere (stateless)                    │
│  Email:         Gmail SMTP (smtp.gmail.com:465)            │
│  Contenedores:  Docker + Docker Compose                     │
│  CI/CD:         Jenkins (jenkins/jenkins:lts)              │
│  Artifacts:     JFrog Artifactory OSS                       │
│  VCS:           Git + GitHub                                │
│  Entorno:       Windows 10/11 + WSL2                        │
└─────────────────────────────────────────────────────────────┘
```

### **Componentes del Proyecto**

| Componente | Tecnología | Puerto | Propósito |
|------------|------------|--------|-----------|
| **Aplicación Web** | Flask + Gunicorn | 5000 | Servidor web principal |
| **Jenkins** | Jenkins LTS | 8080 | Automatización CI/CD |
| **Artifactory** | JFrog OSS | 8082 | Gestión de artefactos |
| **PostgreSQL** | PostgreSQL 13 | 5432 | Base de datos de Artifactory |

---

## 🏗️ Arquitectura del Sistema

### **Diagrama de Arquitectura**

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CAPA DE USUARIO                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  Navegador   │  │   Teléfono   │  │    Tablet    │             │
│  │   Desktop    │  │    Móvil     │  │              │             │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘             │
│         │                 │                 │                       │
│         └─────────────────┴─────────────────┘                       │
│                           │                                         │
│                           │  HTTP Request                           │
│                           ▼                                         │
├─────────────────────────────────────────────────────────────────────┤
│                    CAPA DE NETWORKING                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Windows Firewall (Puertos: 5000, 8080, 8082)               │  │
│  │  IP Local: 192.168.20.183                                    │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                           │                                         │
├─────────────────────────────────────────────────────────────────────┤
│                   CAPA DE CONTENEDORES (Docker)                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  Docker Desktop (Docker Engine 28.4.0)                        │ │
│  │  Docker Daemon: tcp://localhost:2375                          │ │
│  │                                                                │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │ │
│  │  │  cafe-aroma-app │  │    jenkins      │  │ artifactory  │ │ │
│  │  │  Flask 2.3.3    │  │  Jenkins LTS    │  │  OSS + PG13  │ │ │
│  │  │  Port: 5000     │  │  Port: 8080     │  │  Port: 8082  │ │ │
│  │  └─────────────────┘  └─────────────────┘  └──────────────┘ │ │
│  │         │                      │                    │         │ │
│  └─────────┼──────────────────────┼────────────────────┼─────────┘ │
│            │                      │                    │           │
├────────────┼──────────────────────┼────────────────────┼───────────┤
│            │                      │                    │           │
│            ▼                      ▼                    ▼           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐  │
│  │  Docker Volume  │  │  Docker Volume  │  │  Docker Volume   │  │
│  │  (app data)     │  │  (jenkins_home) │  │  (pgdata-art)    │  │
│  └─────────────────┘  └─────────────────┘  └──────────────────┘  │
├─────────────────────────────────────────────────────────────────────┤
│                      CAPA DE SERVICIOS EXTERNOS                     │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────────┐  │
│  │  Gmail SMTP    │  │    GitHub      │  │  QR Code Server     │  │
│  │  Port: 465     │  │  (Git Remote)  │  │  api.qrserver.com   │  │
│  └────────────────┘  └────────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### **Flujo de Datos**

```
┌─────────────┐
│   Usuario   │
│  (Browser)  │
└──────┬──────┘
       │ 1. HTTP GET http://192.168.20.183:5000
       ▼
┌─────────────────┐
│  Windows Host   │
│  Firewall Pass  │
└──────┬──────────┘
       │ 2. Forward to Docker
       ▼
┌─────────────────────┐
│  Docker Container   │
│  cafe-aroma-app     │
│                     │
│  ┌───────────────┐  │
│  │  Flask App    │  │ 3. Process Request
│  │  app.py       │  │
│  └───────┬───────┘  │
│          │          │
│          │ 4. POST /send
│          │ with email
│          ▼          │
│  ┌───────────────┐  │
│  │ SMTP Client   │  │
│  │ smtplib       │  │
│  └───────┬───────┘  │
└──────────┼──────────┘
           │ 5. Connect to Gmail
           ▼
    ┌──────────────┐
    │  Gmail SMTP  │
    │  Port: 465   │
    └──────┬───────┘
           │ 6. Send Email
           ▼
    ┌──────────────┐
    │  Recipient   │
    │  Inbox       │
    └──────────────┘
```

---

## 🔄 Flujo de Desarrollo Completo

### **1. Desarrollo Local (Sin Docker)**

```
Desarrollador
    │
    │ 1. Edita código
    ▼
┌────────────────┐
│  VS Code       │
│  - app.py      │
│  - templates/  │
│  - static/     │
└────────┬───────┘
         │ 2. Activar venv
         │    .\env\Scripts\Activate.ps1
         ▼
┌────────────────┐
│  Python venv   │
│  + Flask       │
│  + dotenv      │
└────────┬───────┘
         │ 3. python app.py
         ▼
┌────────────────┐
│  Flask Server  │
│  localhost:5000│
└────────┬───────┘
         │ 4. Test in Browser
         ▼
┌────────────────┐
│  Browser       │
│  Pruebas       │
└────────────────┘
```

**Comandos:**
```powershell
# Activar entorno
.\env\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py

# Abrir en navegador
Start-Process "http://localhost:5000"
```

### **2. Construcción de Imagen Docker**

```
Desarrollador
    │
    │ 1. docker build
    ▼
┌────────────────┐
│  Dockerfile    │
│                │
│  FROM python   │
│  COPY .        │
│  RUN pip install
│  CMD python app│
└────────┬───────┘
         │ 2. Build Process
         ▼
┌────────────────┐
│  Docker Engine │
│  - Pull base   │
│  - Copy files  │
│  - Install deps│
│  - Create image│
└────────┬───────┘
         │ 3. Image Created
         ▼
┌────────────────┐
│  cafe_aroma:17 │
│  Size: 210MB   │
│  Layers: 5     │
└────────────────┘
```

**Comandos:**
```powershell
# Build imagen
docker build -t cafe_aroma:latest .

# Tag con versión
docker tag cafe_aroma:latest cafe_aroma:17

# Ver imagen creada
docker images cafe_aroma
```

### **3. Commit y Push a GitHub**

```
Desarrollador
    │
    │ 1. git add .
    │ 2. git commit
    │ 3. git push
    ▼
┌────────────────┐
│  Local Git     │
│  .git/         │
└────────┬───────┘
         │ 4. Push to remote
         ▼
┌────────────────────────┐
│  GitHub Remote         │
│  JUANESTEBANORTIZRENDON│
│  /cafe_aroma           │
│                        │
│  Branch: master        │
│  Commit: 357cc0d       │
└────────┬───────────────┘
         │ 5. Webhook (opcional)
         │    o polling por Jenkins
         ▼
┌────────────────┐
│  Jenkins       │
│  Detecta cambio│
│  Inicia build  │
└────────────────┘
```

**Comandos:**
```powershell
# Verificar cambios
git status

# Agregar al staging
git add .

# Commit con mensaje
git commit -m "Feature: Nueva funcionalidad"

# Push a GitHub
git push origin master

# Ver commits recientes
git log --oneline -5
```

---

## 🐳 Integración con Docker

### **¿Qué es Docker en este Proyecto?**

Docker se usa para **contenerizar** la aplicación, asegurando que:
- ✅ Funcione igual en cualquier máquina
- ✅ Todas las dependencias estén incluidas
- ✅ Se pueda desplegar fácilmente
- ✅ Se aísle del sistema host

### **Componentes Docker**

#### **1. Dockerfile**

```dockerfile
# Archivo: Dockerfile (líneas principales)

FROM python:3.11-slim          # Imagen base ligera de Python
WORKDIR /app                   # Directorio de trabajo
COPY requirements.txt .        # Copiar dependencias
RUN pip install --no-cache-dir -r requirements.txt  # Instalar
COPY . .                       # Copiar código de la app
EXPOSE 5000                    # Exponer puerto
CMD ["python", "app.py"]       # Comando de inicio
```

**¿Qué hace cada línea?**

| Línea | Propósito | Resultado |
|-------|-----------|-----------|
| `FROM python:3.11-slim` | Base minimalista con Python 3.11 | Imagen de ~150MB |
| `WORKDIR /app` | Establece directorio de trabajo | Todo se ejecuta en /app |
| `COPY requirements.txt` | Copia solo las dependencias primero | Aprovecha caché de Docker |
| `RUN pip install` | Instala Flask, dotenv, etc. | Layer de dependencias |
| `COPY . .` | Copia todo el código de la app | Layer del código |
| `EXPOSE 5000` | Documenta puerto a exponer | No abre el puerto aún |
| `CMD ["python", "app.py"]` | Comando por defecto al iniciar | Ejecuta la aplicación |

#### **2. Docker Compose**

```yaml
# Archivo: docker-compose.yml (simplificado)

services:
  cafe-aroma-app:
    build: .                    # Construir desde Dockerfile local
    ports:
      - "5000:5000"            # Mapear puerto host:contenedor
    environment:
      - SMTP_HOST=smtp.gmail.com
      - SMTP_PORT=465
      # ... más variables
    restart: unless-stopped    # Reiniciar automáticamente
```

**¿Qué hace Docker Compose?**

1. **Orquesta múltiples contenedores** (app, Jenkins, Artifactory)
2. **Gestiona redes** entre contenedores
3. **Persiste datos** con volúmenes
4. **Simplifica comandos** (un solo `docker-compose up`)

### **Ciclo de Vida del Contenedor**

```
┌─────────────────────────────────────────────────────────────┐
│                   CICLO DE VIDA                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. BUILD                                                   │
│     docker build -t cafe_aroma:17 .                        │
│     └─> Crea imagen desde Dockerfile                       │
│                                                             │
│  2. CREATE                                                  │
│     docker create --name cafe-aroma-app cafe_aroma:17      │
│     └─> Crea contenedor (no lo inicia)                     │
│                                                             │
│  3. START                                                   │
│     docker start cafe-aroma-app                            │
│     └─> Inicia el contenedor                               │
│                                                             │
│  4. RUNNING (Estado actual)                                 │
│     - Flask escuchando en 0.0.0.0:5000                     │
│     - Procesando requests HTTP                              │
│     - Enviando emails via SMTP                              │
│                                                             │
│  5. STOP                                                    │
│     docker stop cafe-aroma-app                             │
│     └─> Detiene el contenedor (SIGTERM → SIGKILL)         │
│                                                             │
│  6. RESTART                                                 │
│     docker restart cafe-aroma-app                          │
│     └─> Stop + Start                                        │
│                                                             │
│  7. REMOVE                                                  │
│     docker rm cafe-aroma-app                               │
│     └─> Elimina el contenedor (debe estar stopped)         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Networking en Docker**

```
┌─────────────────────────────────────────────────────────────┐
│              DOCKER NETWORKING                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Host Machine (Windows)                                     │
│  ├─ localhost / 127.0.0.1                                  │
│  ├─ 192.168.20.183 (WiFi IP)                               │
│  │                                                          │
│  └─ Docker Engine                                           │
│     │                                                       │
│     ├─ Bridge Network (default)                            │
│     │  ├─ cafe-aroma-app     → 172.17.0.3:5000            │
│     │  ├─ jenkins            → 172.17.0.2:8080            │
│     │  └─ host.docker.internal → 192.168.20.183           │
│     │                                                       │
│     └─ art-net (custom)                                    │
│        ├─ artifactory-oss   → IP interna                   │
│        └─ postgres          → IP interna                   │
│                                                             │
│  Port Mappings:                                             │
│  - 5000 (host) → 5000 (cafe-aroma-app)                    │
│  - 8080 (host) → 8080 (jenkins)                            │
│  - 8082 (host) → 8082 (artifactory-oss)                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**¿Por qué `host.docker.internal`?**

- **Problema:** Jenkins (contenedor) no puede acceder a `localhost` porque `localhost` en un contenedor apunta al contenedor mismo
- **Solución:** `host.docker.internal` es un hostname especial que apunta a la máquina host
- **Uso:** En Health Check, Jenkins usa `curl http://host.docker.internal:5000` para verificar la app

---

## 🤖 Integración con Jenkins

### **¿Qué es Jenkins en este Proyecto?**

Jenkins es la herramienta de **automatización CI/CD** que:
- 🔄 Detecta cambios en Git
- 📦 Empaqueta la aplicación en ZIP
- 🐳 Construye imágenes Docker
- 🚀 Despliega contenedores automáticamente
- ✅ Verifica que la app funcione (Health Check)

### **Configuración de Jenkins**

#### **1. Estructura del Contenedor**

```
jenkins (Contenedor)
├─ /var/jenkins_home/              # Home de Jenkins (volumen persistente)
│  ├─ jobs/                        # Definiciones de jobs
│  │  └─ cafe-aroma/               # Nuestro job
│  │     ├─ config.xml             # Configuración del job
│  │     └─ builds/                # Historial de builds
│  │        ├─ 1/ ... 17/          # Cada build
│  │        └─ lastSuccessfulBuild → 17
│  ├─ workspace/                   # Workspaces de builds
│  │  └─ cafe-aroma/               # Código clonado de Git
│  │     ├─ app.py
│  │     ├─ Dockerfile
│  │     ├─ Jenkinsfile
│  │     └─ dist/                  # ZIPs generados
│  ├─ secrets/                     # Credenciales
│  │  ├─ initialAdminPassword
│  │  └─ ...
│  └─ credentials.xml              # Credenciales cifradas
├─ /usr/bin/docker                 # Docker CLI (instalado extra)
└─ /usr/bin/zip                    # Utilidad zip (instalado extra)
```

#### **2. Credenciales en Jenkins**

```
Jenkins Credentials Store
├─ System
│  └─ Global credentials (unrestricted)
│     ├─ smtp-gmail                    # ID: smtp-gmail
│     │  ├─ Kind: Username with password
│     │  ├─ Username: juanestebanortizrendon24072004@gmail.com
│     │  └─ Password: **** (App Password de 16 dígitos)
│     │
│     └─ artifactory-creds             # ID: artifactory-creds
│        ├─ Kind: Username with password
│        ├─ Username: admin
│        └─ Password: password
```

**¿Cómo se usan en el pipeline?**

```groovy
// En Jenkinsfile
withCredentials([
    usernamePassword(
        credentialsId: 'smtp-gmail',
        usernameVariable: 'SMTP_USER',
        passwordVariable: 'SMTP_PASS'
    )
]) {
    // Aquí SMTP_USER y SMTP_PASS están disponibles
    sh '''
        docker run -e SMTP_USER=${SMTP_USER} ...
    '''
}
```

### **Flujo de Ejecución en Jenkins**

```
Usuario hace clic en "Build Now"
    │
    ▼
┌─────────────────────────────────┐
│  Jenkins Master                 │
│  - Programa el build            │
│  - Asigna a un agent (any)      │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Workspace Preparation          │
│  - Crea /var/jenkins_home/      │
│    workspace/cafe-aroma/        │
│  - Limpia si es necesario       │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Checkout SCM (Jenkinsfile)     │
│  - Git clone desde GitHub       │
│  - Branch: master               │
│  - Commit: 357cc0d              │
│  - Obtiene Jenkinsfile          │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Parse Jenkinsfile              │
│  - Lee pipeline definición      │
│  - Valida sintaxis Groovy       │
│  - Identifica 7 stages          │
└─────────┬───────────────────────┘
          │
          ▼ Empieza ejecución del pipeline
┌─────────────────────────────────┐
│  Stage 0: Checkout              │
│  - checkout scm                 │
│  - Clona todo el repo           │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Stage 1: Prepare Workspace     │
│  - ls -lah                      │
│  - Verifica archivos            │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Stage 2: Package ZIP           │
│  - mkdir -p dist                │
│  - zip -r cafe_aroma-17.zip     │
│  - Excluye .git, venv, etc.     │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Stage 3: Upload to Artifactory │
│  - withCredentials              │
│  - curl -T dist/cafe_aroma.zip  │
│  - Maneja error con try-catch   │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Stage 4: Docker Build          │
│  - docker build                 │
│  - docker tag :17 :latest       │
│  - Verifica imagen creada       │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Stage 5: Deploy Locally        │
│  - docker stop cafe-aroma-app   │
│  - docker rm cafe-aroma-app     │
│  - docker run con SMTP vars     │
│  - Espera 10 segundos           │
│  - Muestra logs                 │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Stage 6: Health Check          │
│  - Loop 5 intentos              │
│  - curl host.docker.internal    │
│  - Verifica HTTP 200            │
│  - Sale en el primer éxito      │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Post Actions                   │
│  - docker image prune           │
│  - Mensaje de éxito             │
│  - Archiva artefactos           │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Build Complete                 │
│  Status: SUCCESS                │
│  Duration: ~2-3 minutos         │
│  Artifacts: cafe_aroma-17.zip   │
└─────────────────────────────────┘
```

### **¿Cómo Jenkins Accede a Docker?**

```
Jenkins Container
    │
    │ 1. Ejecuta: docker build
    ▼
┌──────────────────────┐
│ Docker CLI           │
│ /usr/bin/docker      │
└──────┬───────────────┘
       │ 2. Conecta via DOCKER_HOST
       │    tcp://host.docker.internal:2375
       ▼
┌──────────────────────┐
│ Docker Daemon        │
│ (En host Windows)    │
│                      │
│ - Construye imágenes │
│ - Ejecuta containers │
│ - Gestiona volúmenes │
└──────────────────────┘
```

**Configuración necesaria:**

1. **Docker CLI en Jenkins:**
   ```bash
   docker exec -u root jenkins apt-get install -y docker-ce-cli
   ```

2. **Docker Daemon expuesto:**
   - Docker Desktop → Settings → General
   - ✅ "Expose daemon on tcp://localhost:2375 without TLS"

3. **Variable DOCKER_HOST en Jenkinsfile:**
   ```groovy
   environment {
       DOCKER_HOST = 'tcp://host.docker.internal:2375'
   }
   ```

---

## 📦 Integración con Artifactory

### **¿Qué es Artifactory en este Proyecto?**

JFrog Artifactory OSS es un **repositorio de artefactos** que:
- 📦 Almacena ZIPs de cada build
- 📜 Mantiene historial de versiones
- 🔒 Gestiona acceso con credenciales
- 📊 Proporciona metadata de artefactos

**⚠️ Limitación:** Artifactory OSS **NO soporta** repositorios Docker (solo Pro/Enterprise), por eso:
- ✅ Usamos `generic-local` para ZIPs
- ❌ No usamos `docker-local` para imágenes Docker

### **Estructura de Artifactory**

```
Artifactory OSS
├─ Repositories
│  ├─ generic-local (Generic Repository)
│  │  └─ cafe-aroma/                    # Nuestro proyecto
│  │     ├─ cafe_aroma-1.zip
│  │     ├─ cafe_aroma-2.zip
│  │     ├─ ...
│  │     └─ cafe_aroma-17.zip           # Último build exitoso
│  │
│  └─ docker-local (No disponible en OSS)
│
├─ Users
│  └─ admin (Administrador)
│
└─ Permissions
   └─ Anything (Full access para admin)
```

### **Flujo de Subida de Artefactos**

```
Jenkins (Stage 3)
    │
    │ 1. Genera ZIP en dist/cafe_aroma-17.zip
    ▼
┌───────────────────────┐
│  withCredentials      │
│  - ART_USER: admin    │
│  - ART_PASS: ****     │
└──────┬────────────────┘
       │ 2. curl -T (PUT request)
       ▼
┌───────────────────────┐
│  HTTP PUT             │
│  URL: http://host...  │
│  /artifactory/        │
│  generic-local/       │
│  cafe-aroma/          │
│  cafe_aroma-17.zip    │
└──────┬────────────────┘
       │ 3. Authentication
       ▼
┌───────────────────────┐
│  Artifactory Server   │
│  - Verifica usuario   │
│  - Verifica password  │
│  - Verifica permisos  │
└──────┬────────────────┘
       │ 4. Store artifact
       ▼
┌───────────────────────┐
│  PostgreSQL DB        │
│  - Metadata           │
│  - Checksums (SHA256) │
│  - Timestamp          │
└──────┬────────────────┘
       │
       ▼
┌───────────────────────┐
│  File System          │
│  /var/opt/jfrog/      │
│  artifactory/data/    │
│  filestore/           │
│  └─ cafe_aroma-17.zip │
└───────────────────────┘
```

### **Gestión de Artefactos**

#### **Metadata de cada Artefacto**

```json
{
  "repo": "generic-local",
  "path": "/cafe-aroma/cafe_aroma-17.zip",
  "created": "2025-10-27T03:49:27.123Z",
  "createdBy": "admin",
  "lastModified": "2025-10-27T03:49:27.123Z",
  "modifiedBy": "admin",
  "size": "23025 bytes",
  "mimeType": "application/zip",
  "checksums": {
    "sha1": "a1b2c3d4e5...",
    "md5": "1a2b3c4d...",
    "sha256": "abc123def456..."
  },
  "originalChecksums": {
    "sha256": "abc123def456..."
  }
}
```

#### **¿Por qué Artifactory sigue dando 401?**

En el proyecto actual, Artifactory retorna `401 Unauthorized` en los builds, pero el pipeline continúa gracias al `try-catch`:

```groovy
try {
    // Intentar subir a Artifactory
    sh 'curl -u ${ART_USER}:${ART_PASS} ...'
} catch (Exception e) {
    echo "⚠️  Error al subir a Artifactory: ${e.message}"
    echo "⏭️  Continuando con el pipeline..."
}
```

**Posibles causas del 401:**
1. Contraseña incorrecta en Jenkins Credentials
2. Usuario `admin` bloqueado o deshabilitado
3. Artifactory aún inicializándose
4. Permisos insuficientes en el repositorio

**Solución recomendada:**
```powershell
# 1. Resetear contraseña de Artifactory
Start-Process "http://localhost:8082/ui/admin/security/users"

# 2. Actualizar credenciales en Jenkins
Start-Process "http://localhost:8080/manage/credentials/"

# 3. Probar manualmente
curl -u admin:nueva-password http://localhost:8082/artifactory/api/system/ping
```

---

## 🔐 Gestión de Credenciales

### **Tipos de Credenciales en el Proyecto**

| Tipo | Ubicación | Propósito | Formato |
|------|-----------|-----------|---------|
| **Gmail App Password** | Jenkins Credentials | Envío de emails desde la app | 16 dígitos (xxxx xxxx xxxx xxxx) |
| **Jenkins Admin** | Jenkins Server | Acceso a Jenkins UI | Contraseña: 958f7c349b8c4362bd898cd98481c1fe |
| **Artifactory Admin** | Artifactory Server | Gestión de artefactos | Usuario: admin, Password: configurable |
| **GitHub Personal Token** | Opcional | Push/Pull privado | Token de GitHub |

### **Flujo de Credenciales SMTP**

```
Gmail Account
    │
    │ 1. Crear App Password
    │    (Configuración → Seguridad → Verificación en 2 pasos)
    ▼
┌──────────────────────┐
│  App Password        │
│  xxxx xxxx xxxx xxxx │
│  (16 dígitos)        │
└──────┬───────────────┘
       │ 2. Guardar en Jenkins
       ▼
┌──────────────────────┐
│  Jenkins Credentials │
│  ID: smtp-gmail      │
│  User: email@gmail   │
│  Pass: ************  │
└──────┬───────────────┘
       │ 3. Pipeline usa withCredentials
       ▼
┌──────────────────────┐
│  Docker Container    │
│  Environment:        │
│  SMTP_USER=email@... │
│  SMTP_PASS=****      │
└──────┬───────────────┘
       │ 4. Flask app lee env vars
       ▼
┌──────────────────────┐
│  Python SMTP Client  │
│  - smtp.gmail.com    │
│  - Port 465 (SSL)    │
│  - Login con creds   │
└──────┬───────────────┘
       │ 5. Envía email
       ▼
┌──────────────────────┐
│  Gmail SMTP Server   │
│  - Verifica creds    │
│  - Envía mensaje     │
└──────────────────────┘
```

### **Seguridad de Credenciales**

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPAS DE SEGURIDAD                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Capa 1: Archivo .env                                       │
│  ├─ NO commiteado a Git (.gitignore)                       │
│  ├─ Solo en desarrollo local                               │
│  └─ Ejemplo: .env.example (sin credenciales reales)        │
│                                                             │
│  Capa 2: Jenkins Credentials Store                          │
│  ├─ Cifrado con master key de Jenkins                      │
│  ├─ Almacenado en credentials.xml                          │
│  ├─ Solo accesible dentro del pipeline                     │
│  └─ Máscaras en logs (****) automáticas                    │
│                                                             │
│  Capa 3: Variables de Entorno del Contenedor               │
│  ├─ Solo visible dentro del contenedor                     │
│  ├─ No persiste en la imagen                               │
│  ├─ Se elimina con el contenedor                           │
│  └─ No aparece en docker inspect (si se usa secrets)       │
│                                                             │
│  Capa 4: Gmail App Password                                 │
│  ├─ NO es la contraseña principal de Gmail                 │
│  ├─ Se puede revocar sin afectar la cuenta                 │
│  ├─ Solo funciona para SMTP                                │
│  └─ Requiere verificación en 2 pasos activa                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Buenas Prácticas Implementadas:**

✅ **NO hardcodear** credenciales en el código  
✅ **NO commitear** `.env` a Git  
✅ **Usar** Jenkins Credentials para CI/CD  
✅ **Usar** App Passwords en lugar de contraseñas principales  
✅ **Rotar** credenciales periódicamente  
✅ **Separar** credenciales de desarrollo y producción  

---

## 🌐 Networking y Acceso Remoto

### **Configuración de Red Local**

```
┌─────────────────────────────────────────────────────────────┐
│                      TOPOLOGÍA DE RED                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Router WiFi (192.168.20.1)                                 │
│    │                                                        │
│    ├─ PC Windows (192.168.20.183)                          │
│    │  ├─ Docker Desktop                                     │
│    │  │  ├─ cafe-aroma-app:5000                            │
│    │  │  ├─ jenkins:8080                                   │
│    │  │  └─ artifactory:8082                               │
│    │  │                                                     │
│    │  └─ Windows Firewall                                   │
│    │     ├─ Puerto 5000 → Abierto (Inbound)                │
│    │     ├─ Puerto 8080 → Abierto (Inbound)                │
│    │     └─ Puerto 8082 → Abierto (Inbound)                │
│    │                                                        │
│    ├─ Teléfono Móvil (192.168.20.x)                        │
│    │  └─ Navegador → http://192.168.20.183:5000            │
│    │                                                        │
│    ├─ Tablet (192.168.20.y)                                │
│    │  └─ Navegador → http://192.168.20.183:5000            │
│    │                                                        │
│    └─ Otros dispositivos...                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Habilitación de Acceso Remoto**

#### **Paso 1: Configurar Firewall**

```powershell
# Ejecutar como ADMINISTRADOR

# Regla para Café Aroma (Puerto 5000)
New-NetFirewallRule `
  -DisplayName "Cafe Aroma - Puerto 5000" `
  -Direction Inbound `
  -LocalPort 5000 `
  -Protocol TCP `
  -Action Allow `
  -Profile Private,Public `
  -Description "Permite acceso a Cafe Aroma desde la red local"

# Verificar regla creada
Get-NetFirewallRule -DisplayName "Cafe Aroma*" | `
  Select-Object DisplayName, Enabled, Action
```

#### **Paso 2: Obtener IP Local**

```powershell
# Obtener IP de WiFi
$ip = Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*" | `
  Where-Object {$_.IPAddress -notlike "169.254.*"} | `
  Select-Object -ExpandProperty IPAddress

Write-Host "Tu IP local es: $ip" -ForegroundColor Green
Write-Host "Accede desde otros dispositivos: http://$ip:5000" -ForegroundColor Cyan
```

#### **Paso 3: Generar Código QR**

```powershell
# Generar QR para acceso fácil desde móvil
$url = "http://192.168.20.183:5000"
Start-Process "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=$url"
```

### **Acceso desde Diferentes Dispositivos**

| Dispositivo | Ubicación | URL | Requisitos |
|-------------|-----------|-----|------------|
| **PC Local** | Misma máquina | http://localhost:5000 | Ninguno |
| **PC Local (IP)** | Misma máquina | http://192.168.20.183:5000 | Firewall abierto |
| **Teléfono** | Misma WiFi | http://192.168.20.183:5000 | Firewall abierto |
| **Tablet** | Misma WiFi | http://192.168.20.183:5000 | Firewall abierto |
| **Laptop** | Misma WiFi | http://192.168.20.183:5000 | Firewall abierto |

### **Opciones de Acceso desde Internet**

```
┌─────────────────────────────────────────────────────────────┐
│             OPCIONES PARA ACCESO DESDE INTERNET             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Opción 1: Ngrok (Recomendado para pruebas)                │
│  ┌────────────────────────────────────────────────────────┐│
│  │  1. Instalar: choco install ngrok                      ││
│  │  2. Ejecutar: ngrok http 5000                          ││
│  │  3. Obtener URL pública:                               ││
│  │     https://abc123.ngrok.io → localhost:5000           ││
│  │  ⏰ Duración: Hasta que detengas ngrok                 ││
│  └────────────────────────────────────────────────────────┘│
│                                                             │
│  Opción 2: Cloudflare Tunnel (Gratis, permanente)          │
│  ┌────────────────────────────────────────────────────────┐│
│  │  1. Crear cuenta en Cloudflare                         ││
│  │  2. Instalar cloudflared                               ││
│  │  3. Ejecutar: cloudflared tunnel --url localhost:5000  ││
│  │  4. Configurar dominio personalizado                   ││
│  │  🔒 Con HTTPS automático                               ││
│  └────────────────────────────────────────────────────────┘│
│                                                             │
│  Opción 3: Port Forwarding en Router                        │
│  ┌────────────────────────────────────────────────────────┐│
│  │  1. Acceder al router (192.168.20.1)                   ││
│  │  2. Configurar port forwarding:                        ││
│  │     Puerto externo: 5000                               ││
│  │     IP interna: 192.168.20.183                         ││
│  │     Puerto interno: 5000                               ││
│  │  3. Obtener IP pública: whatismyip.com                 ││
│  │  ⚠️ Requiere IP pública estática o DNS dinámico        ││
│  └────────────────────────────────────────────────────────┘│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Monitoreo y Mantenimiento

### **Monitoreo de Contenedores**

```powershell
# Ver estado de todos los contenedores
docker ps

# Ver consumo de recursos en tiempo real
docker stats

# Ver logs de la aplicación
docker logs cafe-aroma-app

# Ver logs en tiempo real (Ctrl+C para salir)
docker logs -f cafe-aroma-app

# Ver últimas 50 líneas de logs
docker logs --tail 50 cafe-aroma-app

# Ver logs con timestamps
docker logs -t cafe-aroma-app
```

### **Health Checks**

```powershell
# Verificar que la app responde
curl http://localhost:5000

# Verificar con detalles
Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing

# Verificar desde la red
curl http://192.168.20.183:5000

# Verificar Jenkins
curl http://localhost:8080

# Verificar Artifactory
curl http://localhost:8082/ui
```

### **Mantenimiento Regular**

#### **Limpieza de Docker**

```powershell
# Limpiar imágenes no utilizadas
docker image prune -f

# Limpiar contenedores detenidos
docker container prune -f

# Limpiar todo (CUIDADO)
docker system prune -a -f

# Ver espacio usado por Docker
docker system df
```

#### **Backup de Datos**

```powershell
# Backup de Jenkins (incluye jobs, configuración, credenciales)
docker run --rm -v jenkins_home:/data -v ${PWD}/backup:/backup `
  busybox tar czf /backup/jenkins-backup-$(Get-Date -Format 'yyyy-MM-dd').tar.gz /data

# Backup de Artifactory
docker run --rm -v artifactory-data:/data -v ${PWD}/backup:/backup `
  busybox tar czf /backup/artifactory-backup-$(Get-Date -Format 'yyyy-MM-dd').tar.gz /data

# Restaurar Jenkins desde backup
docker run --rm -v jenkins_home:/data -v ${PWD}/backup:/backup `
  busybox tar xzf /backup/jenkins-backup-2025-10-27.tar.gz -C /
```

### **Actualización de Componentes**

```powershell
# Actualizar imagen de la aplicación
docker-compose build --no-cache cafe-aroma-app
docker-compose up -d cafe-aroma-app

# Actualizar Jenkins
docker-compose pull jenkins
docker-compose up -d jenkins

# Actualizar Artifactory
docker-compose pull artifactory-oss
docker-compose up -d artifactory-oss
```

---

## 🎯 Resumen del Flujo Completo

```
┌───────────────────────────────────────────────────────────────────────┐
│                     FLUJO END-TO-END COMPLETO                         │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  1. DESARROLLO                                                        │
│     └─> Editar código en VS Code                                     │
│         └─> Probar localmente (python app.py)                        │
│                                                                       │
│  2. VERSION CONTROL                                                   │
│     └─> git add . && git commit -m "..." && git push                 │
│         └─> Código en GitHub                                         │
│                                                                       │
│  3. CI/CD (Jenkins detecta cambio o se ejecuta manualmente)          │
│     └─> Stage 0: Checkout código desde GitHub                        │
│         └─> Stage 1: Preparar workspace                              │
│             └─> Stage 2: Crear ZIP del proyecto                      │
│                 └─> Stage 3: Subir ZIP a Artifactory (opcional)      │
│                     └─> Stage 4: Build imagen Docker                 │
│                         └─> Stage 5: Deploy contenedor               │
│                             └─> Stage 6: Health check                │
│                                                                       │
│  4. APLICACIÓN EN PRODUCCIÓN                                          │
│     └─> Contenedor cafe-aroma-app corriendo                          │
│         └─> Flask escuchando en 0.0.0.0:5000                         │
│             └─> Accesible desde:                                     │
│                 ├─> localhost:5000 (local)                           │
│                 ├─> 192.168.20.183:5000 (red local)                  │
│                 └─> ngrok/cloudflare (internet)                      │
│                                                                       │
│  5. USUARIO FINAL                                                     │
│     └─> Accede desde navegador/móvil                                 │
│         └─> Ve la página de Café Aroma                               │
│             └─> Ingresa email para suscribirse                       │
│                 └─> Flask envía email via Gmail SMTP                 │
│                     └─> Usuario recibe confirmación                  │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

---

**Documentación actualizada:** 27 de Octubre, 2025  
**Build exitoso:** #17  
**Estado:** Producción  
**Acceso:** http://192.168.20.183:5000
