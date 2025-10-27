

# Ruta de Trabajo para Proyecto de Videojuegos — Despliegue Gratuito con Render y Linux en WSL2


## 1. Objetivo

Replicar la estructura y funcionalidades del proyecto actual (envío de correos, Flask, Jenkins, Artifactory, Docker), cambiando la temática a videojuegos y añadiendo despliegue con Kubernetes. El desarrollo se realizará sobre Linux virtualizado en tu PC Windows usando WSL2, y el despliegue final será gratuito en línea usando Render.

---


## 2. Herramientas y Aplicativos Necesarios

### Para virtualizar Linux en Windows:
- **WSL2 (Windows Subsystem for Linux)**
  - Permite ejecutar una distribución Linux directamente en Windows.
  - Recomendado para desarrollo rápido y fácil integración.

### Para el desarrollo y despliegue:
- **Python 3.x**
- **pip**
- **Docker**
- **Docker Compose**
- **Jenkins**
- **JFrog Artifactory**
- **Git**

### Para el despliegue en línea:
- **Render.com**
  - Permite desplegar aplicaciones Docker gratis (con recursos limitados).
  - [https://render.com/](https://render.com/)

---

---

## 2. Herramientas y Aplicativos Necesarios

### Para virtualizar Linux en Windows:
- **WSL2 (Windows Subsystem for Linux)**
  - Permite ejecutar una distribución Linux directamente en Windows.
  - Recomendado para desarrollo rápido y fácil integración.
- **VirtualBox + Ubuntu**
  - Alternativa si prefieres una VM completa.

### Para el desarrollo y despliegue:
- **Python 3.x**
- **pip**
- **Docker**
- **Docker Compose**
- **Jenkins**
- **JFrog Artifactory**
- **Kubernetes local (Minikube o Kind)**
- **kubectl**
- **Git**

---


## 3. Instalación Secuencial de Herramientas

### Paso 1: Instalar WSL2 y Ubuntu en Windows
1. Abre PowerShell como administrador.
2. Ejecuta:
  ```pwsh
  wsl --install
  wsl --install -d Ubuntu
  ```
3. Reinicia tu PC si es necesario.
4. Abre Ubuntu desde el menú de inicio y configura tu usuario.

### Paso 2: Validar e Instalar Herramientas en Ubuntu (WSL2)
1. Actualiza paquetes:
  ```bash
  sudo apt update && sudo apt upgrade -y
  ```
2. Instala Python, pip, Docker, Git:
  ```bash
  sudo apt install python3 python3-pip docker.io git -y
  ```
3. Instala Docker Compose:
  ```bash
  sudo apt install docker-compose -y
  ```
4. (Opcional) Instala Jenkins y Artifactory si los necesitas para CI/CD.
5. Verifica instalaciones:
  ```bash
  python3 --version
  pip --version
  docker --version
  docker-compose --version
  git --version
  ```



---

## 4. Estructura del Proyecto

Mantén la misma estructura que el proyecto actual:
```
videojuegos_app/
  app.py
  Dockerfile
  docker-compose.yml
  Jenkinsfile
  requirements.txt
  kubernetes/
    deployment.yaml
    service.yaml
  documentacion/
    README.md
  static/
  templates/
```

---




## 4. Ruta de Trabajo Paso a Paso

### Paso 1: Preparar entorno Linux (WSL2)
1. Instala y valida todas las herramientas necesarias en Ubuntu (WSL2).
2. Clona el repositorio base en Ubuntu:
  ```bash
  git clone <repo_url>
  ```

### Paso 2: Adaptar la temática
1. Cambia nombres, textos y templates a videojuegos.
2. Mantén la funcionalidad de envío de correos.

### Paso 3: Configurar entorno Python
1. Crea y activa el entorno virtual:
  ```bash
  python3 -m venv env
  source env/bin/activate
  ```
2. Instala dependencias:
  ```bash
  pip install -r requirements.txt
  ```

### Paso 4: Configurar Docker
1. Revisa y adapta `Dockerfile` y `docker-compose.yml`.
2. Prueba la app localmente con Docker:
  ```bash
  docker build -t videojuegos_app .
  docker run -p 5000:5000 videojuegos_app
  ```

### Paso 5: Despliegue Gratuito en Render
1. Crea una cuenta en [Render.com](https://render.com/).
2. Sube tu repositorio a GitHub.
3. En Render, crea un nuevo servicio web y conecta tu repositorio.
4. Render detectará el Dockerfile y desplegará la app automáticamente.
5. Configura variables de entorno y puertos si es necesario.
6. Espera a que Render construya y despliegue la app.
7. Obtén la URL pública que Render te proporciona para acceder a tu aplicación desde cualquier dispositivo.

### Paso 6: Validar despliegue
1. Accede a la app desde el navegador usando la URL pública de Render.
2. Verifica que la funcionalidad de envío de correos y la temática de videojuegos estén correctas.

---

## 6. Consejos para Evitar Errores y Optimizar el Proceso
- Documenta cada paso en `documentacion/README.md`.
- Usa Copilot para acelerar desarrollo y evitar errores.
- Prueba comandos en ambos sistemas para validar compatibilidad.
- Mantén control de versiones con Git.
- Si surge algún error, consulta logs y documentación oficial.

---

## 7. Recursos Útiles
- [WSL2](https://docs.microsoft.com/en-us/windows/wsl/)
- [VirtualBox](https://www.virtualbox.org/)
- [Minikube](https://minikube.sigs.k8s.io/docs/)
- [Kind](https://kind.sigs.k8s.io/)
- [Jenkins](https://www.jenkins.io/doc/)
- [Artifactory](https://jfrog.com/artifactory/)

---

**Con esta ruta de trabajo organizada y clara, puedes montar el proyecto en Linux virtualizado sobre Windows, adaptando la temática y añadiendo Kubernetes, con ayuda de Copilot para lograrlo en menos de un día.**