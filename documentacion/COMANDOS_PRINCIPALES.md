# 📋 Comandos Principales - Café Aroma

> **Guía de referencia rápida con todos los comandos necesarios para ejecutar, desplegar y administrar el proyecto Café Aroma.**

---

## 📑 Índice

1. [Inicio Rápido](#-inicio-rápido)
2. [Gestión de Docker](#-gestión-de-docker)
3. [Gestión de Jenkins](#-gestión-de-jenkins)
4. [Gestión de Artifactory](#-gestión-de-artifactory)
5. [Acceso Remoto y Red Local](#-acceso-remoto-y-red-local)
6. [Git y Desarrollo](#-git-y-desarrollo)
7. [Python y Dependencias](#-python-y-dependencias)
8. [Troubleshooting](#-troubleshooting)

---

## 🚀 Inicio Rápido

### **Levantar todo el proyecto desde cero**

```powershell
# 1. Verificar que Docker Desktop esté corriendo
docker version

# 2. Si no está corriendo, iniciarlo
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
Start-Sleep -Seconds 15

# 3. Levantar todos los contenedores
docker-compose up -d

# 4. Verificar que estén corriendo
docker ps

# 5. Abrir las aplicaciones en el navegador
Start-Process "http://localhost:5000"        # Café Aroma
Start-Process "http://localhost:8080"        # Jenkins
Start-Process "http://localhost:8082/ui"     # Artifactory
```

### **Detener todo el proyecto**

```powershell
# Detener todos los contenedores
docker-compose down

# Detener y eliminar volúmenes (CUIDADO: borra datos persistentes)
docker-compose down -v
```

---

## 🐳 Gestión de Docker

### **Comandos Básicos de Docker**

```powershell
# Ver contenedores activos
docker ps

# Ver todos los contenedores (incluidos los detenidos)
docker ps -a

# Ver imágenes locales
docker images

# Ver logs de un contenedor
docker logs cafe-aroma-app
docker logs jenkins
docker logs artifactory-oss

# Ver logs en tiempo real
docker logs -f cafe-aroma-app

# Ejecutar comandos dentro de un contenedor
docker exec -it cafe-aroma-app bash
docker exec -it jenkins bash

# Detener un contenedor
docker stop cafe-aroma-app

# Iniciar un contenedor detenido
docker start cafe-aroma-app

# Reiniciar un contenedor
docker restart cafe-aroma-app

# Eliminar un contenedor
docker rm cafe-aroma-app

# Eliminar una imagen
docker rmi cafe_aroma:latest
```

### **Construcción de Imágenes**

```powershell
# Construir imagen desde Dockerfile
docker build -t cafe_aroma:latest .

# Construir sin usar caché
docker build --no-cache -t cafe_aroma:latest .

# Construir con un tag específico
docker build -t cafe_aroma:1.0.0 .

# Construir y hacer tag simultáneamente
docker build -t cafe_aroma:17 -t cafe_aroma:latest .
```

### **Gestión de la Aplicación Café Aroma**

```powershell
# Detener el contenedor actual
docker stop cafe-aroma-app

# Eliminar el contenedor
docker rm cafe-aroma-app

# Ejecutar nuevo contenedor con variables de entorno
docker run -d `
  --name cafe-aroma-app `
  -p 5000:5000 `
  -e SMTP_HOST=smtp.gmail.com `
  -e SMTP_PORT=465 `
  -e SMTP_USER=tu-email@gmail.com `
  -e SMTP_PASS=tu-app-password `
  -e SMTP_FROM="Café Aroma <tu-email@gmail.com>" `
  -e SECRET_KEY=tu-secret-key-aqui `
  cafe_aroma:latest

# Ver logs de la aplicación
docker logs cafe-aroma-app

# Acceder al contenedor
docker exec -it cafe-aroma-app bash

# Ver consumo de recursos
docker stats cafe-aroma-app
```

### **Limpieza de Docker**

```powershell
# Limpiar imágenes no utilizadas
docker image prune -f

# Limpiar contenedores detenidos
docker container prune -f

# Limpiar todo lo no utilizado (contenedores, redes, imágenes)
docker system prune -f

# Limpiar TODO incluyendo volúmenes (CUIDADO!)
docker system prune -a --volumes -f
```

### **Docker Compose**

```powershell
# Levantar servicios
docker-compose up -d

# Levantar y reconstruir imágenes
docker-compose up -d --build

# Detener servicios
docker-compose down

# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs cafe-aroma-app

# Reiniciar un servicio
docker-compose restart cafe-aroma-app

# Ver estado de los servicios
docker-compose ps
```

---

## 🔧 Gestión de Jenkins

### **Acceso y Configuración Inicial**

```powershell
# Abrir Jenkins en el navegador
Start-Process "http://localhost:8080"

# Obtener contraseña inicial de Jenkins
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Contraseña actual del proyecto: 958f7c349b8c4362bd898cd98481c1fe
```

### **Gestión del Contenedor Jenkins**

```powershell
# Ver logs de Jenkins
docker logs jenkins

# Ver logs en tiempo real
docker logs -f jenkins

# Reiniciar Jenkins
docker restart jenkins

# Acceder al contenedor
docker exec -it jenkins bash

# Verificar Docker CLI dentro de Jenkins
docker exec jenkins docker version

# Verificar que Jenkins puede acceder a Docker
docker exec jenkins docker ps
```

### **Instalación de Herramientas en Jenkins**

```powershell
# Instalar Docker CLI en Jenkins (si no está instalado)
docker exec -u root jenkins bash -c "apt-get update && apt-get install -y docker-ce-cli"

# Instalar zip/unzip en Jenkins
docker exec -u root jenkins bash -c "apt-get update && apt-get install -y zip unzip"

# Instalar curl en Jenkins
docker exec -u root jenkins bash -c "apt-get update && apt-get install -y curl"

# Verificar instalaciones
docker exec jenkins which docker
docker exec jenkins which zip
docker exec jenkins which curl
```

### **Ejecución de Builds**

```powershell
# Abrir el job específico
Start-Process "http://localhost:8080/job/cafe-aroma/"

# Ver console output del último build
Start-Process "http://localhost:8080/job/cafe-aroma/lastBuild/console"

# Ver console output de un build específico (ej: build #17)
Start-Process "http://localhost:8080/job/cafe-aroma/17/console"
```

### **Configuración de Credenciales en Jenkins**

```powershell
# Abrir página de credenciales
Start-Process "http://localhost:8080/manage/credentials/"

# Crear credencial SMTP (smtp-gmail)
# - Username: tu-email@gmail.com
# - Password: tu-app-password-de-16-caracteres

# Crear credencial Artifactory (artifactory-creds)
# - Username: admin
# - Password: password (o la que hayas configurado)
```

---

## 📦 Gestión de Artifactory

### **Acceso y Configuración**

```powershell
# Abrir Artifactory en el navegador
Start-Process "http://localhost:8082/ui"

# Credenciales por defecto
# Username: admin
# Password: password
```

### **Gestión del Contenedor Artifactory**

```powershell
# Ver logs de Artifactory
docker logs artifactory-oss

# Reiniciar Artifactory
docker restart artifactory-oss

# Ver estado de salud
docker exec artifactory-oss curl -u admin:password http://localhost:8082/artifactory/api/system/ping

# Acceder al contenedor
docker exec -it artifactory-oss bash
```

### **Operaciones con Artefactos**

```powershell
# Subir un archivo a Artifactory manualmente
curl -u admin:password `
  -T dist/cafe_aroma-17.zip `
  "http://localhost:8082/artifactory/generic-local/cafe-aroma/cafe_aroma-17.zip"

# Descargar un archivo de Artifactory
curl -u admin:password `
  -O "http://localhost:8082/artifactory/generic-local/cafe-aroma/cafe_aroma-17.zip"

# Verificar que un archivo existe
curl -u admin:password `
  -I "http://localhost:8082/artifactory/generic-local/cafe-aroma/cafe_aroma-17.zip"

# Listar archivos en un repositorio
curl -u admin:password `
  "http://localhost:8082/artifactory/api/storage/generic-local/cafe-aroma"
```

### **Configuración de Repositorios**

```powershell
# Abrir configuración de repositorios
Start-Process "http://localhost:8082/ui/admin/repositories/local"

# Repositorio usado: generic-local
# Tipo: Generic
# Path: cafe-aroma/
```

---

## 🌐 Acceso Remoto y Red Local

### **Obtener tu IP Local**

```powershell
# Método 1: Obtener IP de WiFi
Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*" | `
  Where-Object {$_.IPAddress -notlike "169.254.*"} | `
  Select-Object -ExpandProperty IPAddress

# Método 2: Método alternativo
ipconfig | Select-String "IPv4"

# Tu IP actual: 192.168.20.183
```

### **Configurar Firewall para Acceso Remoto**

```powershell
# Abrir PowerShell como ADMINISTRADOR y ejecutar:

# Crear regla para puerto 5000 (Café Aroma)
New-NetFirewallRule `
  -DisplayName "Cafe Aroma - Puerto 5000" `
  -Direction Inbound `
  -LocalPort 5000 `
  -Protocol TCP `
  -Action Allow `
  -Profile Private,Public `
  -Description "Permite acceso a Cafe Aroma desde la red local"

# Crear regla para puerto 8080 (Jenkins)
New-NetFirewallRule `
  -DisplayName "Jenkins - Puerto 8080" `
  -Direction Inbound `
  -LocalPort 8080 `
  -Protocol TCP `
  -Action Allow `
  -Profile Private,Public

# Crear regla para puerto 8082 (Artifactory)
New-NetFirewallRule `
  -DisplayName "Artifactory - Puerto 8082" `
  -Direction Inbound `
  -LocalPort 8082 `
  -Protocol TCP `
  -Action Allow `
  -Profile Private,Public

# Verificar reglas creadas
Get-NetFirewallRule -DisplayName "*Cafe*","*Jenkins*","*Artifactory*" | `
  Select-Object DisplayName, Enabled, Action | Format-Table
```

### **Probar Acceso desde la Red**

```powershell
# Probar acceso a Café Aroma desde tu PC
curl http://192.168.20.183:5000

# Abrir en navegador
Start-Process "http://192.168.20.183:5000"

# Probar desde PowerShell con detalles
Invoke-WebRequest -Uri "http://192.168.20.183:5000" -UseBasicParsing
```

### **Generar Código QR para Acceso Móvil**

```powershell
# Método 1: Abrir URL de generación de QR
Start-Process "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=http://192.168.20.183:5000"

# Método 2: Mostrar información con QR
Write-Host "`n╔════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  📱 ACCESO DESDE TU TELÉFONO  ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════╝`n" -ForegroundColor Cyan
Write-Host "🌐 URL: http://192.168.20.183:5000`n" -ForegroundColor Yellow
Start-Process "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=http://192.168.20.183:5000"
```

### **URLs de Acceso desde la Red Local**

| Servicio | URL Local | URL Red Local |
|----------|-----------|---------------|
| **Café Aroma** | http://localhost:5000 | http://192.168.20.183:5000 |
| **Jenkins** | http://localhost:8080 | http://192.168.20.183:8080 |
| **Artifactory** | http://localhost:8082/ui | http://192.168.20.183:8082/ui |

---

## 🔀 Git y Desarrollo

### **Comandos Git Básicos**

```powershell
# Ver estado del repositorio
git status

# Ver commits recientes
git log --oneline -10

# Agregar cambios al staging
git add .

# Hacer commit
git commit -m "Descripción del cambio"

# Subir cambios a GitHub
git push origin master

# Ver cambios no commiteados
git diff

# Ver ramas
git branch

# Cambiar de rama
git checkout nombre-rama

# Crear nueva rama
git checkout -b nueva-rama
```

### **Workflow de Desarrollo**

```powershell
# 1. Hacer cambios en el código
code app.py

# 2. Probar localmente
docker-compose up -d --build

# 3. Verificar que funciona
Start-Process "http://localhost:5000"

# 4. Agregar cambios a Git
git add .
git status

# 5. Commit con mensaje descriptivo
git commit -m "Feature: Agregar nueva funcionalidad X"

# 6. Push a GitHub
git push origin master

# 7. Jenkins detectará el cambio y ejecutará el pipeline automáticamente
# O ejecutar build manualmente en Jenkins
Start-Process "http://localhost:8080/job/cafe-aroma/"
```

### **Ver Historial del Proyecto**

```powershell
# Ver todos los commits
git log --oneline --graph --all

# Ver cambios de un archivo específico
git log --oneline -- Jenkinsfile

# Ver detalles de un commit
git show 357cc0d
```

---

## 🐍 Python y Dependencias

### **Gestión del Entorno Virtual**

```powershell
# Activar entorno virtual
.\env\Scripts\Activate.ps1

# Desactivar entorno virtual
deactivate

# Ver paquetes instalados
pip list

# Instalar dependencias del proyecto
pip install -r requirements.txt

# Actualizar requirements.txt
pip freeze > requirements.txt
```

### **Ejecutar la Aplicación Localmente (sin Docker)**

```powershell
# 1. Activar entorno virtual
.\env\Scripts\Activate.ps1

# 2. Configurar variables de entorno
$env:SMTP_HOST = "smtp.gmail.com"
$env:SMTP_PORT = "465"
$env:SMTP_USER = "tu-email@gmail.com"
$env:SMTP_PASS = "tu-app-password"
$env:SMTP_FROM = "Café Aroma <tu-email@gmail.com>"
$env:SECRET_KEY = "tu-secret-key"

# 3. Ejecutar aplicación
python app.py

# 4. Abrir en navegador
Start-Process "http://localhost:5000"
```

### **Probar Funcionalidad SMTP**

```powershell
# Ejecutar snippet de prueba
docker exec cafe-aroma-app python -c "
import smtplib
import os
from email.mime.text import MIMEText

msg = MIMEText('Prueba desde Café Aroma')
msg['Subject'] = 'Test Email'
msg['From'] = os.getenv('SMTP_FROM')
msg['To'] = 'destinatario@ejemplo.com'

with smtplib.SMTP_SSL(os.getenv('SMTP_HOST'), int(os.getenv('SMTP_PORT'))) as server:
    server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASS'))
    server.send_message(msg)
    print('✅ Email enviado correctamente')
"
```

---

## 🔧 Troubleshooting

### **Docker no está corriendo**

```powershell
# Verificar estado de Docker
docker version

# Si falla, iniciar Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
Start-Sleep -Seconds 15

# Verificar nuevamente
docker version
```

### **Contenedor no inicia correctamente**

```powershell
# Ver logs del contenedor
docker logs cafe-aroma-app

# Ver logs en tiempo real
docker logs -f cafe-aroma-app

# Reiniciar contenedor
docker restart cafe-aroma-app

# Si persiste, recrear el contenedor
docker stop cafe-aroma-app
docker rm cafe-aroma-app
docker-compose up -d cafe-aroma-app
```

### **Puerto ya está en uso**

```powershell
# Verificar qué proceso está usando el puerto 5000
Get-NetTCPConnection -LocalPort 5000 | Select-Object State, OwningProcess

# Matar el proceso (reemplaza PID con el número real)
Stop-Process -Id PID -Force

# O cambiar el puerto en docker-compose.yml
# ports:
#   - "5001:5000"  # Cambiar 5000 por otro puerto
```

### **Jenkins no puede acceder a Docker**

```powershell
# Verificar que Docker CLI está instalado en Jenkins
docker exec jenkins which docker

# Si no está, instalarlo
docker exec -u root jenkins bash -c "apt-get update && apt-get install -y docker-ce-cli"

# Verificar que Docker daemon está expuesto en tcp://2375
# Docker Desktop → Settings → General → "Expose daemon on tcp://localhost:2375 without TLS"

# Probar conexión
docker exec jenkins docker version
```

### **Artifactory retorna 401 Unauthorized**

```powershell
# Verificar credenciales
curl -u admin:password http://localhost:8082/artifactory/api/system/ping

# Si falla, resetear contraseña en la UI
Start-Process "http://localhost:8082/ui/admin/security/users"

# O reiniciar Artifactory
docker restart artifactory-oss
docker logs -f artifactory-oss
```

### **No puedo acceder desde mi teléfono**

```powershell
# 1. Verificar IP local
Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*" | `
  Where-Object {$_.IPAddress -notlike "169.254.*"} | `
  Select-Object IPAddress

# 2. Verificar firewall (ejecutar como ADMINISTRADOR)
Get-NetFirewallRule -DisplayName "*Cafe*" | Select-Object DisplayName, Enabled

# 3. Si no existe, crear regla
New-NetFirewallRule -DisplayName "Cafe Aroma - Puerto 5000" `
  -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow

# 4. Probar desde tu PC
curl http://192.168.20.183:5000

# 5. Verificar que ambos dispositivos estén en la misma red WiFi
```

### **Pipeline de Jenkins falla**

```powershell
# Ver console output del build
Start-Process "http://localhost:8080/job/cafe-aroma/lastBuild/console"

# Verificar logs de Jenkins
docker logs jenkins

# Limpiar workspace de Jenkins
docker exec jenkins rm -rf /var/jenkins_home/workspace/cafe-aroma/*

# Ejecutar nuevo build
# En Jenkins UI → Build Now
```

### **Limpiar y empezar de cero**

```powershell
# CUIDADO: Esto eliminará TODOS los contenedores y volúmenes

# 1. Detener todos los contenedores
docker-compose down -v

# 2. Eliminar imágenes del proyecto
docker rmi cafe_aroma:latest
docker rmi $(docker images -q cafe_aroma)

# 3. Limpiar sistema Docker
docker system prune -a --volumes -f

# 4. Reconstruir todo
docker-compose up -d --build

# 5. Verificar
docker ps
```

---

## 📚 Referencias Rápidas

### **Puertos Utilizados**

| Puerto | Servicio | Acceso |
|--------|----------|--------|
| 5000 | Café Aroma | http://localhost:5000 |
| 8080 | Jenkins | http://localhost:8080 |
| 8081 | Artifactory Docker Registry | No usado (OSS) |
| 8082 | Artifactory Web UI | http://localhost:8082/ui |
| 5432 | PostgreSQL (Artifactory) | Interno |
| 2375 | Docker Daemon | tcp://localhost:2375 |

### **Credenciales del Proyecto**

| Servicio | Username | Password | Notas |
|----------|----------|----------|-------|
| Jenkins | Admin Cafe Aroma | 958f7c349b8c4362bd898cd98481c1fe | Contraseña inicial |
| Artifactory | admin | password | Por defecto |
| Gmail SMTP | tu-email@gmail.com | App Password (16 dígitos) | En Jenkins Credentials |

### **Archivos Importantes**

| Archivo | Ubicación | Propósito |
|---------|-----------|-----------|
| `app.py` | Raíz | Aplicación Flask principal |
| `Dockerfile` | Raíz | Construcción de imagen Docker |
| `docker-compose.yml` | Raíz | Orquestación de contenedores |
| `Jenkinsfile` | Raíz | Pipeline CI/CD |
| `requirements.txt` | Raíz | Dependencias Python |
| `.env.example` | Raíz | Template de variables de entorno |

---

## 🎯 Comandos de Uso Diario

```powershell
# Iniciar el día
docker-compose up -d
Start-Process "http://localhost:5000"

# Ver estado de todo
docker ps

# Ver logs si algo falla
docker logs cafe-aroma-app

# Hacer cambios y deployar
git add .
git commit -m "Update: descripción"
git push origin master
# Jenkins desplegará automáticamente

# Acceder desde teléfono
# http://192.168.20.183:5000

# Terminar el día
docker-compose down
```

---

**Documentación actualizada:** 27 de Octubre, 2025  
**Versión del proyecto:** Build #17 (Exitoso)  
**IP de red local:** 192.168.20.183
