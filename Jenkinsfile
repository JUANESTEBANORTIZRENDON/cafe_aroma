/*
 * ============================================================================
 * Jenkinsfile para Café Aroma - Pipeline CI/CD Completo
 * ============================================================================
 * 
 * Este pipeline implementa un flujo completo de CI/CD para la aplicación
 * Flask Café Aroma, incluyendo:
 * - Checkout del código desde Git
 * - Empaquetado ZIP y publicación en Artifactory OSS (generic-local)
 * - Build de imagen Docker local (Artifactory OSS no soporta Docker registry)
 * - Deploy local con credenciales SMTP desde Jenkins Credentials
 * 
 * REQUISITOS PREVIOS:
 * 1. Docker Desktop con daemon expuesto en tcp://localhost:2375 sin TLS
 * 2. Credenciales en Jenkins:
 *    - smtp-gmail: Credenciales de Gmail (usuario + App Password)
 *    - artifactory-creds: Credenciales de Artifactory (admin/password)
 * 3. Repositorio en Artifactory: generic-local
 * 4. Repositorio Git configurado en el job de Jenkins
 * 
 * RAMA PRINCIPAL: master
 * ============================================================================
 */

pipeline {
    agent any
    
    environment {
        // ========================================================================
        // CONFIGURACIÓN DE ARTIFACTORY
        // ========================================================================
        // URL base de Artifactory (usar host.docker.internal para contenedores Jenkins)
        ART_URL = 'http://host.docker.internal:8082/artifactory'
        
        // Repositorio genérico para artefactos ZIP
        ART_GEN = 'generic-local'
        
        // Repositorio Docker para imágenes (opcional)
        ART_DOCK = 'docker-local'
        
        // ========================================================================
        // CONFIGURACIÓN DE DOCKER
        // ========================================================================
        // Nombre de la imagen Docker
        IMG_NAME = 'cafe_aroma'
        
        // Registry Docker de Artifactory
        DOCKER_REG = 'host.docker.internal:8081'
        
        // Host Docker para conexión desde Jenkins
        DOCKER_HOST = 'tcp://host.docker.internal:2375'
        
        // ========================================================================
        // CONFIGURACIÓN DE LA APLICACIÓN
        // ========================================================================
        APP_NAME = 'cafe-aroma'
        VERSION = "${env.BUILD_NUMBER}"
        ARTIFACT_NAME = "cafe_aroma-${VERSION}.zip"
    }
    
    stages {
        // ========================================================================
        // STAGE 0: Checkout del Código
        // ========================================================================
        // Clona el repositorio Git en el workspace de Jenkins
        stage('Checkout') {
            steps {
                echo '📥 Obteniendo código desde Git...'
                checkout scm
            }
        }
        
        // ========================================================================
        // STAGE 1: Preparar Workspace
        // ========================================================================
        // Verifica el contenido del workspace y muestra información del entorno
        stage('Prepare Workspace') {
            steps {
                echo '📂 Listando archivos del proyecto...'
                script {
                    if (isUnix()) {
                        sh '''
                            echo "========================================="
                            echo "CONTENIDO DEL WORKSPACE:"
                            echo "========================================="
                            ls -lah
                            echo ""
                            echo "Archivos principales:"
                            ls -lh app.py requirements.txt Dockerfile 2>/dev/null || echo "Algunos archivos no encontrados"
                        '''
                    } else {
                        bat '''
                            echo =========================================
                            echo CONTENIDO DEL WORKSPACE:
                            echo =========================================
                            dir
                            echo.
                            echo Archivos principales:
                            dir app.py requirements.txt Dockerfile 2>nul || echo Algunos archivos no encontrados
                        '''
                    }
                }
            }
        }
        
        // ========================================================================
        // STAGE 2: Empaquetar ZIP
        // ========================================================================
        // Crea un archivo ZIP con todos los archivos necesarios para despliegue
        // Excluye archivos innecesarios como venv, .git, __pycache__, etc.
        stage('Package ZIP') {
            steps {
                echo '📦 Empaquetando aplicación en ZIP...'
                script {
                    // Crear directorio dist si no existe
                    if (isUnix()) {
                        sh '''
                            # Crear directorio de distribución
                            mkdir -p dist
                            
                            # Crear archivo ZIP con todos los archivos necesarios
                            # Excluir: venv, env, .git, __pycache__, .env (secretos)
                            echo "Empaquetando archivos..."
                            zip -r dist/${ARTIFACT_NAME} . \
                                -x "*.git*" \
                                -x "*venv/*" \
                                -x "*env/*" \
                                -x "*__pycache__/*" \
                                -x "*.pyc" \
                                -x "*.pyo" \
                                -x "*.env" \
                                -x "*dist/*" \
                                -x "*.log"
                            
                            # Verificar contenido del ZIP
                            echo ""
                            echo "Contenido del ZIP:"
                            unzip -l dist/${ARTIFACT_NAME} | head -20
                            
                            # Mostrar tamaño
                            echo ""
                            echo "Tamaño del artefacto:"
                            ls -lh dist/${ARTIFACT_NAME}
                        '''
                    } else {
                        bat '''
                            REM Crear directorio de distribución
                            if not exist dist mkdir dist
                            
                            REM Crear archivo ZIP (requiere 7-Zip o similar instalado)
                            echo Empaquetando archivos...
                            powershell -Command "Compress-Archive -Path app.py,requirements.txt,Dockerfile,docker-compose.yml,templates,static,README.md -DestinationPath dist\\%ARTIFACT_NAME% -Force"
                            
                            REM Mostrar tamaño
                            echo.
                            echo Tamaño del artefacto:
                            dir dist\\%ARTIFACT_NAME%
                        '''
                    }
                }
            }
        }
        
        // ========================================================================
        // STAGE 3: Subir ZIP a Artifactory
        // ========================================================================
        // Publica el archivo ZIP en el repositorio generic-local de Artifactory
        // usando las credenciales configuradas en Jenkins
        stage('Upload ZIP to Artifactory') {
            steps {
                echo '⬆️  Subiendo ZIP a Artifactory...'
                script {
                    // Usar credenciales de Artifactory desde Jenkins
                    // Hacer este stage opcional - no falla el pipeline si hay error
                    try {
                        withCredentials([usernamePassword(
                            credentialsId: 'artifactory-creds',
                            usernameVariable: 'ART_USER',
                            passwordVariable: 'ART_PASS'
                        )]) {
                        if (isUnix()) {
                            sh '''
                                # Subir artefacto usando curl
                                echo "Subiendo ${ARTIFACT_NAME} a Artifactory..."
                                curl -u ${ART_USER}:${ART_PASS} \
                                     -T dist/${ARTIFACT_NAME} \
                                     "${ART_URL}/${ART_GEN}/cafe-aroma/${ARTIFACT_NAME}"
                                
                                # Verificar que se subió correctamente
                                echo ""
                                echo "Verificando artefacto en Artifactory..."
                                curl -u ${ART_USER}:${ART_PASS} \
                                     -I "${ART_URL}/${ART_GEN}/cafe-aroma/${ARTIFACT_NAME}"
                            '''
                        } else {
                            bat '''
                                REM Subir artefacto usando curl (debe estar instalado)
                                echo Subiendo %ARTIFACT_NAME% a Artifactory...
                                curl -u %ART_USER%:%ART_PASS% -T dist\\%ARTIFACT_NAME% "%ART_URL%/%ART_GEN%/cafe-aroma/%ARTIFACT_NAME%"
                                
                                REM Verificar que se subió correctamente
                                echo.
                                echo Verificando artefacto en Artifactory...
                                curl -u %ART_USER%:%ART_PASS% -I "%ART_URL%/%ART_GEN%/cafe-aroma/%ARTIFACT_NAME%"
                            '''
                        }
                    }
                    } catch (Exception e) {
                        echo "⚠️  Error al subir a Artifactory: ${e.message}"
                        echo "⏭️  Continuando con el pipeline..."
                    }
                }
            }
        }
        
        // ========================================================================
        // STAGE 4: Build Docker Image (Local - Sin push a Artifactory)
        // ========================================================================
        // Construye la imagen Docker localmente
        // NOTA: Artifactory OSS no soporta repositorios Docker (solo Pro/Enterprise)
        // La imagen se guarda localmente y se usa en el Stage 5
        stage('Docker Build') {
            steps {
                echo '🐳 Construyendo imagen Docker localmente...'
                script {
                    if (isUnix()) {
                        sh '''
                            # Build de la imagen
                            echo "Construyendo imagen Docker..."
                            docker build -t ${IMG_NAME}:${VERSION} .
                            docker tag ${IMG_NAME}:${VERSION} ${IMG_NAME}:latest
                            
                            # Verificar que se creó
                            echo ""
                            echo "Imagen creada:"
                            docker images ${IMG_NAME}
                        '''
                    } else {
                        bat '''
                            REM Build de la imagen
                            echo Construyendo imagen Docker...
                            docker build -t %IMG_NAME%:%VERSION% .
                            docker tag %IMG_NAME%:%VERSION% %IMG_NAME%:latest
                            
                            REM Verificar que se creó
                            echo.
                            echo Imagen creada:
                            docker images %IMG_NAME%
                        '''
                    }
                }
            }
        }
        
        // ========================================================================
        // STAGE 5: Deploy Local con SMTP desde Jenkins Credentials
        // ========================================================================
        // Despliega el contenedor localmente usando credenciales SMTP de Jenkins
        // NO usa archivo .env, todas las variables vienen de Jenkins Credentials
        stage('Deploy Locally') {
            steps {
                echo '🚀 Desplegando aplicación localmente...'
                script {
                    // Usar credenciales SMTP desde Jenkins
                    withCredentials([
                        usernamePassword(
                            credentialsId: 'smtp-gmail',
                            usernameVariable: 'SMTP_USER',
                            passwordVariable: 'SMTP_PASS'
                        )
                    ]) {
                        if (isUnix()) {
                            sh '''
                                # Detener contenedor anterior si existe
                                echo "Deteniendo contenedor anterior..."
                                docker stop cafe-aroma-app 2>/dev/null || true
                                docker rm cafe-aroma-app 2>/dev/null || true
                                
                                # Ejecutar nuevo contenedor con variables de entorno
                                echo "Iniciando nuevo contenedor..."
                                docker run -d \
                                    --name cafe-aroma-app \
                                    -p 5000:5000 \
                                    -e SMTP_HOST=smtp.gmail.com \
                                    -e SMTP_PORT=465 \
                                    -e SMTP_USER=${SMTP_USER} \
                                    -e SMTP_PASS=${SMTP_PASS} \
                                    -e SMTP_FROM="Café Aroma <${SMTP_USER}>" \
                                    -e SECRET_KEY=jenkins-secret-key-production \
                                    ${IMG_NAME}:latest
                                
                                # Esperar a que el contenedor esté listo
                                echo "Esperando a que la aplicación esté lista..."
                                sleep 10
                                
                                # Verificar logs
                                echo ""
                                echo "Logs del contenedor:"
                                docker logs cafe-aroma-app
                            '''
                        } else {
                            bat '''
                                REM Detener contenedor anterior si existe
                                echo Deteniendo contenedor anterior...
                                docker stop cafe-aroma-app 2>nul || echo No hay contenedor previo
                                docker rm cafe-aroma-app 2>nul || echo No hay contenedor previo
                                
                                REM Ejecutar nuevo contenedor con variables de entorno
                                echo Iniciando nuevo contenedor...
                                docker run -d ^
                                    --name cafe-aroma-app ^
                                    -p 5000:5000 ^
                                    -e SMTP_HOST=smtp.gmail.com ^
                                    -e SMTP_PORT=465 ^
                                    -e SMTP_USER=%SMTP_USER% ^
                                    -e SMTP_PASS=%SMTP_PASS% ^
                                    -e "SMTP_FROM=Café Aroma <%SMTP_USER%>" ^
                                    -e SECRET_KEY=jenkins-secret-key-production ^
                                    %IMG_NAME%:latest
                                
                                REM Esperar a que el contenedor esté listo
                                echo Esperando a que la aplicación esté lista...
                                timeout /t 10 /nobreak
                                
                                REM Verificar logs
                                echo.
                                echo Logs del contenedor:
                                docker logs cafe-aroma-app
                            '''
                        }
                    }
                }
            }
        }
        
        // ========================================================================
        // STAGE 6: Health Check
        // ========================================================================
        // Verifica que la aplicación esté respondiendo correctamente
        stage('Health Check') {
            steps {
                echo '🏥 Verificando salud de la aplicación...'
                script {
                    if (isUnix()) {
                        sh '''
                            # Intentar acceder a la aplicación
                            echo "Verificando endpoint principal..."
                            count=1
                            max_attempts=5
                            while [ $count -le $max_attempts ]; do
                                http_code=$(curl -f http://localhost:5000 -o /dev/null -s -w "%{http_code}" || echo "000")
                                if [ "$http_code" = "200" ]; then
                                    echo "✅ Aplicación responde correctamente (HTTP $http_code)"
                                    exit 0
                                fi
                                echo "Intento $count/$max_attempts - HTTP $http_code - esperando..."
                                sleep 5
                                count=$((count + 1))
                            done
                            echo "❌ La aplicación no responde después de $max_attempts intentos"
                            exit 1
                        '''
                    } else {
                        bat '''
                            REM Verificar endpoint principal
                            echo Verificando endpoint principal...
                            powershell -Command "$attempts = 0; $maxAttempts = 5; while ($attempts -lt $maxAttempts) { try { $response = Invoke-WebRequest -Uri http://localhost:5000 -TimeoutSec 5; if ($response.StatusCode -eq 200) { Write-Host 'Aplicación responde correctamente' -ForegroundColor Green; exit 0 } } catch { $attempts++; Write-Host \"Intento $attempts/$maxAttempts - esperando...\" -ForegroundColor Yellow; Start-Sleep -Seconds 5 } } Write-Host 'La aplicación no responde' -ForegroundColor Red; exit 1"
                        '''
                    }
                }
            }
        }
    }
    
    // ========================================================================
    // POST-BUILD ACTIONS
    // ========================================================================
    post {
        always {
            echo '🧹 Limpieza post-build...'
            script {
                // Limpiar imágenes Docker no utilizadas (opcional)
                if (isUnix()) {
                    sh 'docker image prune -f || true'
                } else {
                    bat 'docker image prune -f || echo Limpieza completada'
                }
            }
        }
        
        success {
            echo '✅ ¡Pipeline ejecutado exitosamente!'
            echo '🔄 Stages completados: Checkout → Package → Upload → Build → Deploy → Health Check'
            echo "📦 Artefacto ZIP: ${ARTIFACT_NAME}"
            echo "🐳 Imagen Docker: ${IMG_NAME}:${VERSION}"
            echo "🌐 Aplicación disponible en: http://localhost:5000"
            // Aquí puedes agregar notificaciones (Slack, email, etc.)
        }
        
        failure {
            echo '❌ Pipeline falló!'
            echo 'Revisa los logs para más detalles.'
            // Aquí puedes agregar notificaciones de error
        }
        
        unstable {
            echo '⚠️  Pipeline completado con advertencias'
        }
    }
}
