# Configuración de Jenkins para Cafe Aroma

Esta guía te ayudará a configurar Jenkins para trabajar con Artifactory y automatizar el despliegue de la aplicación Cafe Aroma.

## 📋 Requisitos Previos

- Jenkins instalado y funcionando
- Artifactory OSS funcionando (usar `.\scripts\start-artifactory.ps1`)
- Docker disponible en el sistema Jenkins

## 🔧 Configuración Inicial

### 1. Instalar Plugins Necesarios

En Jenkins, ve a **Manage Jenkins > Manage Plugins** e instala:

- **Artifactory Plugin**
- **Docker Pipeline Plugin**
- **Pipeline Stage View Plugin**
- **Build Timeout Plugin**
- **Timestamper Plugin**

### 2. Configurar Artifactory en Jenkins

1. Ve a **Manage Jenkins > Configure System**
2. Busca la sección **JFrog**
3. Agrega un nuevo servidor Artifactory:
   - **Server ID**: `artifactory-local`
   - **URL**: `http://localhost:8082/artifactory`
   - **Username**: `admin`
   - **Password**: `password` (cambiar después del primer login)

### 3. Configurar Credenciales

Ve a **Manage Jenkins > Manage Credentials** y agrega:

#### Docker Registry Credentials
- **Kind**: Username with password
- **ID**: `artifactory-credentials`
- **Username**: `admin`
- **Password**: `[tu-password-de-artifactory]`

#### Git Credentials (si es necesario)
- **Kind**: Username with password o SSH Username with private key
- **ID**: `git-credentials`

## 🚀 Crear Pipeline

### 1. Crear Nuevo Job

1. En Jenkins, click **New Item**
2. Nombre: `cafe-aroma-pipeline`
3. Tipo: **Pipeline**
4. Click **OK**

### 2. Configurar Pipeline

En la configuración del job:

#### General
- ✅ **Discard old builds**: Keep 10 builds
- ✅ **GitHub project**: `[tu-repo-url]` (si aplica)

#### Build Triggers
- ✅ **Poll SCM**: `H/5 * * * *` (cada 5 minutos)
- ✅ **GitHub hook trigger** (si usas GitHub)

#### Pipeline
- **Definition**: Pipeline script from SCM
- **SCM**: Git
- **Repository URL**: `[tu-repo-url]`
- **Credentials**: `git-credentials`
- **Branch**: `*/main`
- **Script Path**: `Jenkinsfile`

### 3. Configurar Webhooks (Opcional)

Si usas GitHub/GitLab, configura webhooks para trigger automático:
- **Payload URL**: `http://[jenkins-url]/github-webhook/`
- **Content type**: `application/json`
- **Events**: Push, Pull requests

## 📦 Configurar Repositorios en Artifactory

### 1. Acceder a Artifactory UI

1. Ve a `http://localhost:8082/ui`
2. Login: `admin` / `password`
3. Cambia la contraseña en el primer acceso

### 2. Crear Repositorios

#### Docker Repository
1. **Administration > Repositories > Local**
2. **New Local Repository**
3. **Package Type**: Docker
4. **Repository Key**: `cafe-aroma-docker-local`

#### Generic Repository
1. **New Local Repository**
2. **Package Type**: Generic
3. **Repository Key**: `cafe-aroma-generic-local`

#### PyPI Repository (para dependencias Python)
1. **New Remote Repository**
2. **Package Type**: PyPI
3. **Repository Key**: `cafe-aroma-pypi-remote`
4. **URL**: `https://pypi.org/simple`

## 🔄 Flujo de Trabajo

### Desarrollo
1. Developer hace push a `develop` branch
2. Jenkins detecta cambio
3. Ejecuta tests
4. Construye imagen Docker
5. Sube imagen a Artifactory
6. Despliega a staging automáticamente

### Producción
1. Developer hace push a `master` branch
2. Jenkins detecta cambio
3. Ejecuta tests completos
4. Construye imagen Docker
5. Sube imagen a Artifactory
6. **Requiere aprobación manual**
7. Despliega a producción

## 🛠️ Comandos Útiles

### Verificar Estado de Artifactory
```powershell
.\scripts\start-artifactory.ps1 -Status
```

### Ver Logs de Jenkins Pipeline
```bash
# En Jenkins CLI
java -jar jenkins-cli.jar -s http://localhost:8080 console cafe-aroma-pipeline
```

### Limpiar Imágenes Docker Antiguas
```powershell
docker system prune -f
docker image prune -f
```

## 🔍 Troubleshooting

### Pipeline Falla en Docker Build
- Verificar que Docker esté disponible en el agente Jenkins
- Verificar credenciales de Artifactory
- Revisar logs del pipeline

### No Puede Conectar a Artifactory
- Verificar que Artifactory esté funcionando: `.\scripts\start-artifactory.ps1 -Status`
- Verificar URL en configuración Jenkins
- Verificar credenciales

### Tests Fallan
- Verificar que el entorno virtual se cree correctamente
- Verificar que todas las dependencias estén en `requirements.txt`
- Revisar logs específicos del test

## 📊 Monitoreo

### Métricas Importantes
- **Build Success Rate**: >95%
- **Build Duration**: <5 minutos
- **Deployment Frequency**: Diario
- **Lead Time**: <1 hora

### Dashboards Recomendados
- Jenkins Build Trends
- Artifactory Storage Usage
- Application Performance (post-deployment)

## 🔐 Seguridad

### Buenas Prácticas
- Cambiar contraseñas por defecto
- Usar tokens de API en lugar de contraseñas
- Configurar RBAC en Artifactory
- Habilitar audit logs
- Backup regular de configuraciones

### Tokens de API
1. En Artifactory UI: **User Menu > Edit Profile**
2. **Generate API Key**
3. Usar este token en lugar de password en Jenkins
