# 🎨 INTERFAZ GRÁFICA DE JENKINS - GUÍA COMPLETA

## 🖥️ ¿JENKINS TIENE INTERFAZ GRÁFICA?

**SÍ, ¡Jenkins tiene una interfaz web completa y muy visual!**

Es como Docker Desktop pero para automatización CI/CD.

---

## 🌐 ACCEDER A LA INTERFAZ

### **URL:**
```
http://localhost:8080
```

### **Desde otros dispositivos (misma red WiFi):**
```
http://192.168.20.183:8080
```

---

## 🎯 PANTALLAS PRINCIPALES DE JENKINS

### 1️⃣ **PANTALLA DE LOGIN**


**Tu password actual:** `958f7c349b8c4362bd898cd98481c1fe`

---



### 3️⃣ **CREAR USUARIO ADMIN**

```
┌─────────────────────────────────────────────────────┐
│  👤 Create First Admin User                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Username:     ┌──────────────────────────────┐    │
│                │ admin                         │    │
│                └──────────────────────────────┘    │
│                                                     │
│  Password:     ┌──────────────────────────────┐    │
│                │ admin123                │    │
│                └──────────────────────────────┘    │
│                                                     │
│  Confirm:      ┌──────────────────────────────┐    │
│                │ admin123                     │    │
│                └──────────────────────────────┘    │
│                                                     │
│  Full name:    ┌──────────────────────────────┐    │
│                │ Admin Cafe Aroma              │    │
│                └──────────────────────────────┘    │
│                                                     │
│  Email:        ┌──────────────────────────────┐    │
│                │ admin@localhost               │    │
│                └──────────────────────────────┘    │
│                                                     │
│            [Save and Continue]                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---




### 8️⃣ **MANAGE JENKINS** (Configuración)

```
┌────────────────────────────────────────────────────────────────────────────┐
│  ⚙️ Manage Jenkins                                                         │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  🔧 System Configuration                                                   │
│  ├─ Configure System                                                       │
│  ├─ Global Tool Configuration                                              │
│  ├─ Manage Plugins                                                         │
│  └─ Configure Global Security                                              │
│                                                                            │
│  🔐 Security                                                               │
│  ├─ Manage Credentials                      ◀── Configura aquí SMTP      │
│  ├─ Configure Global Security                                              │
│  ├─ Manage Users                                                           │
│  └─ Security Realm                                                         │
│                                                                            │
│  🔌 Status Information                                                     │
│  ├─ System Information                                                     │
│  ├─ System Log                                                             │
│  ├─ Load Statistics                                                        │
│  └─ About Jenkins                                                          │
│                                                                            │
│  📊 Tools and Actions                                                      │
│  ├─ Reload Configuration                                                   │
│  ├─ Script Console                                                         │
│  ├─ Manage Nodes                                                           │
│  └─ Prepare for Shutdown                                                   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

### 9️⃣ **CREDENTIALS** (Gestión de Secretos)

```
┌────────────────────────────────────────────────────────────────────────────┐
│  🔐 Credentials                                                [Add] [Edit] │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  📁 Stores scoped to Jenkins                                              │
│  ├─ System                                                                 │
│  │  └─ Global credentials (unrestricted)                                  │
│  │     ┌────────────────────────────────────────────────────────────┐    │
│  │     │  ID                  Kind            Description            │    │
│  │     ├────────────────────────────────────────────────────────────┤    │
│  │     │  smtp-gmail          Username/Pass  Gmail SMTP             │    │
│  │     │  artifactory-creds   Username/Pass  Artifactory Admin      │    │
│  │     └────────────────────────────────────────────────────────────┘    │
│  │                                                                         │
│  └─ [Add Credentials] ◀── Click aquí para agregar nuevas                │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---


## 🎮 FUNCIONES INTERACTIVAS

### **1. Build Now (Ejecutar Build)**

Click en "Build Now" y verás:
- Animación de progreso en tiempo real
- Cada stage se va coloreando (verde/rojo)
- Logs aparecen en vivo
- Notificaciones cuando termina

### **2. Console Output (Ver Logs)**

- Logs en tiempo real mientras el build corre
- Auto-scroll activado
- Búsqueda de texto
- Descarga de logs

### **3. Stage View (Vista de Etapas)**

- Visualización gráfica del pipeline
- Tiempo de cada stage
- Click en cada stage para ver logs específicos
- Identificación rápida de fallos

### **4. Build History (Historial)**

- Gráfico de tendencias
- Success rate
- Duración promedio
- Comparación entre builds

---


## 🚀 ACCESO RÁPIDO

### **Desde tu PC:**
```
http://localhost:8080
```

### **Desde otros dispositivos:**
```
http://192.168.20.183:8080
```

### **Páginas importantes:**

| Página | URL |
|--------|-----|
| **Dashboard** | http://localhost:8080 |
| **Job cafe-aroma** | http://localhost:8080/job/cafe-aroma |
| **Blue Ocean** | http://localhost:8080/blue |
| **Manage Jenkins** | http://localhost:8080/manage |
| **Credentials** | http://localhost:8080/credentials |
| **System Log** | http://localhost:8080/log |

---


**Tu IP:** 192.168.20.183  
**Jenkins:** http://localhost:8080
