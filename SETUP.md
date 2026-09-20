# SIGAM — cómo levantar el proyecto

Guía de cero a la app corriendo. Todos los comandos van en **PowerShell**, parado en la carpeta del repo.

---

## Resumen ultra corto

```powershell
git clone <url-del-repo> Sigam
cd Sigam
.\dev.ps1 -Setup     # primera vez: instala y configura todo
.\dev.ps1            # día a día: arranca todo
.\dev.ps1 -Stop      # cierra todo
```

---

## Paso a paso (máquina nueva)

### 1. Instalar lo que el repo NO trae

Tres cosas, una sola vez por computador:

```powershell
winget install Python.Python.3.13     # Python (si no lo tienes)
winget install OpenJS.NodeJS.LTS      # Node + npm (para Angular)
winget install Oracle.MySQL           # MySQL Server
```

Cierra y vuelve a abrir la terminal después de instalar, para que tome el PATH.

Verifica:

```powershell
python --version
node --version
npm --version
```

> **¿Toca MySQL sí o sí?** Sí, el proyecto usa MySQL. Pero **no** tienes que
> configurarlo a mano: `-Setup` crea la base, el usuario y la contraseña solo.
> Si tu equipo ya tiene una base MySQL compartida, ver [Usar una base remota](#usar-una-base-remota).

### 2. Clonar

```powershell
git clone <url-del-repo> Sigam
cd Sigam
```

### 3. Setup (una sola vez)

```powershell
.\dev.ps1 -Setup
```

Esto hace, en orden:

1. Inicializa una instancia local de MySQL en `C:\Users\<tu-usuario>\mysql-data\sigam`.
2. Crea la base `sigam` y el usuario `sigam_app` con una contraseña aleatoria.
3. Escribe `backend\.env` con esas credenciales.
4. Crea `backend\.venv` e instala las dependencias de Python.
5. Corre `npm install` en `frontend\`.
6. Aplica las migraciones (`manage.py migrate`).
7. Deja el backend y el frontend corriendo.

Tarda unos minutos la primera vez (npm install es lo más lento).

### 4. Usuario administrador

Para entrar al panel necesitas un usuario. Dos opciones:

```powershell
# a) registrarte desde la app, en http://localhost:4200/registro

# b) o crear un superusuario de Django:
cd backend
.\.venv\Scripts\python.exe manage.py createsuperuser
cd ..
```

### 5. Listo

| Qué | Dónde |
|---|---|
| App (Angular) | http://localhost:4200 |
| API (Django) | http://127.0.0.1:8000 |
| Swagger | http://127.0.0.1:8000/swagger/ |
| Admin de Django | http://127.0.0.1:8000/admin/ |

---

## Uso diario

```powershell
.\dev.ps1            # arranca MySQL + backend + frontend
.\dev.ps1 -Status    # ¿qué está corriendo?
.\dev.ps1 -Stop      # cierra todo
```

El backend y el frontend se abren cada uno en su propia ventana de PowerShell
(títulos **SIGAM backend** y **SIGAM frontend**), así ves los logs y los errores
de compilación. MySQL corre oculto; su log queda en
`C:\Users\<tu-usuario>\mysql-data\mysqld-console.log`.

### Opciones

| Comando | Para qué |
|---|---|
| `.\dev.ps1 -Setup` | instalación inicial (o reparar un entorno incompleto) |
| `.\dev.ps1 -Migrate` | arranca aplicando migraciones antes (después de un `git pull` con modelos nuevos) |
| `.\dev.ps1 -NoFrontend` | solo MySQL + backend |
| `.\dev.ps1 -NoBackend` | solo MySQL + frontend |
| `.\dev.ps1 -NoMysql` | no toca MySQL (base remota, o ya lo tienes corriendo) |
| `.\dev.ps1 -Status` | qué está arriba |
| `.\dev.ps1 -Stop` | cierra todo |

Desde `cmd.exe` o con doble clic: usa `dev.bat`, acepta los mismos parámetros
(`dev.bat -Setup`).

---

## Usar una base remota

Si el equipo tiene un MySQL compartido, sáltate la parte local:

1. Crea `backend\.env` a mano (copia `backend\.env.example`) con los datos del servidor.
2. Si ese servidor exige TLS, pon el certificado en `backend\certs\ca.pem`
   (se usa automáticamente si el archivo existe), o apunta a otra ruta con
   `DB_SSL_CA=C:\ruta\a\ca.pem` en el `.env`.
3. Arranca con `.\dev.ps1 -NoMysql`.

---

## Qué NO está en el repo (y por eso hay que generarlo)

Estos están en `.gitignore`, o sea que cada quien los crea en su máquina:

| Archivo | Lo genera |
|---|---|
| `backend\.env` | `-Setup` |
| `backend\.venv\` | `-Setup` |
| `frontend\node_modules\` | `-Setup` (`npm install`) |
| `backend\certs\ca.pem` | solo si usas una base que exige TLS |
| datos de MySQL | `-Setup` |

---

## Problemas comunes

**`no se puede cargar el archivo dev.ps1 ... ejecución de scripts está deshabilitada`**

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
o usa `dev.bat`, que ya se salta esa restricción.

**`el puerto 8000 ya esta ocupado`** — hay un backend viejo corriendo.
`.\dev.ps1 -Stop`, o arranca en otro puerto: `.\dev.ps1 -BackendPort 8010`.

**`migrate fallo`** — casi siempre son las credenciales de `backend\.env` o MySQL
abajo. Revisa con `.\dev.ps1 -Status` y mira
`C:\Users\<tu-usuario>\mysql-data\mysqld-console.log`.

**`MySQL no esta instalado`** — `winget install Oracle.MySQL`, reabre la terminal,
y repite `.\dev.ps1 -Setup`.

**El frontend no carga / errores de CORS** — el backend solo acepta
`http://localhost:4200` y `http://127.0.0.1:4200` (está en `backend\config\settings.py`).
Entra por esas URLs, no por la IP de la máquina.

**Olvidé la contraseña de la base** — está en `backend\.env` (`DB_PASSWORD`).
