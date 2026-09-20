<#
.SYNOPSIS
    Arranca todo SIGAM (MySQL + backend Django + frontend Angular) con un solo comando.

.DESCRIPTION
    Por defecto: verifica MySQL (lo arranca si hace falta y hay un datadir local),
    abre el backend en una ventana y el frontend en otra, y deja los PID anotados
    para poder cerrarlo todo con -Stop.

.EXAMPLE
    .\dev.ps1                 # arranca todo
    .\dev.ps1 -Setup          # primera vez: crea venv, instala dependencias, migra
    .\dev.ps1 -Migrate        # arranca aplicando migraciones antes
    .\dev.ps1 -Stop           # cierra todo lo que arranco este script
    .\dev.ps1 -Status         # solo dice que esta corriendo
    .\dev.ps1 -NoFrontend     # solo MySQL + backend
#>
[CmdletBinding()]
param(
    [switch]$Setup,
    [switch]$Migrate,
    [switch]$Stop,
    [switch]$Status,
    [switch]$NoFrontend,
    [switch]$NoBackend,
    [switch]$NoMysql,
    # Solo si necesitas una instancia aparte (otro puerto / otro datadir).
    [int]$MysqlPort = 3306,
    [string]$MysqlDataDir,
    [int]$BackendPort = 8000
)

$ErrorActionPreference = 'Stop'

# --- Rutas -------------------------------------------------------------------
$Root       = $PSScriptRoot
$BackendDir = Join-Path $Root 'backend'
$FrontDir   = Join-Path $Root 'frontend'
$VenvDir    = Join-Path $BackendDir '.venv'
$VenvPy     = Join-Path $VenvDir 'Scripts\python.exe'
$VenvPip    = Join-Path $VenvDir 'Scripts\pip.exe'
$EnvFile    = Join-Path $BackendDir '.env'
$PidFile    = Join-Path $Root '.sigam-dev.pids'

if (-not $MysqlDataDir) { $MysqlDataDir = Join-Path $env:USERPROFILE 'mysql-data\sigam' }
$MysqlLog = Join-Path (Split-Path $MysqlDataDir) 'mysqld-console.log'

# --- Utilidades --------------------------------------------------------------
function Write-Step ($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }
function Write-Ok   ($msg) { Write-Host "    OK  $msg" -ForegroundColor Green }
function Write-Warn ($msg) { Write-Host "    !   $msg" -ForegroundColor Yellow }
function Write-Err  ($msg) { Write-Host "    X   $msg" -ForegroundColor Red }

function Test-Port ($portNumber) {
    $c = Get-NetTCPConnection -LocalPort $portNumber -State Listen -ErrorAction SilentlyContinue
    return $null -ne $c
}

function Wait-Port ($portNumber, $timeoutSec = 40) {
    $sw = [Diagnostics.Stopwatch]::StartNew()
    while ($sw.Elapsed.TotalSeconds -lt $timeoutSec) {
        if (Test-Port $portNumber) { return $true }
        Start-Sleep -Milliseconds 500
    }
    return $false
}

function Get-Mysqld {
    $candidates = Get-ChildItem 'C:\Program Files\MySQL' -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -like 'MySQL Server*' } |
        Sort-Object Name -Descending |
        ForEach-Object { Join-Path $_.FullName 'bin\mysqld.exe' } |
        Where-Object { Test-Path $_ }
    # Preferir 8.4: es la version con la que se creo el datadir de esta maquina
    $preferred = $candidates | Where-Object { $_ -like '*8.4*' } | Select-Object -First 1
    if ($preferred) { return $preferred }
    return ($candidates | Select-Object -First 1)
}

# Escribe texto plano sin BOM (Set-Content -Encoding utf8 en PS 5.1 si lo mete).
function Write-TextFile ($ruta, [string[]]$lineas) {
    [IO.File]::WriteAllText($ruta, ($lineas -join "`r`n") + "`r`n", (New-Object Text.UTF8Encoding($false)))
}

function Save-Pid ($label, $processId) {
    "$label=$processId" | Add-Content -Path $PidFile -Encoding ascii
}

function Get-MysqlClient {
    $mysqld = Get-Mysqld
    if (-not $mysqld) { return $null }
    $client = Join-Path (Split-Path $mysqld) 'mysql.exe'
    if (Test-Path $client) { return $client }
    return $null
}

function Read-EnvValue ($clave) {
    if (-not (Test-Path $EnvFile)) { return $null }
    foreach ($line in Get-Content $EnvFile) {
        if ($line -match "^\s*$clave\s*=\s*(.*)$") { return $Matches[1].Trim() }
    }
    return $null
}

# Arranca mysqld en segundo plano y espera a que acepte conexiones.
function Start-Mysqld {
    $mysqld = Get-Mysqld
    if (-not $mysqld) {
        Write-Err 'No encontre mysqld.exe en C:\Program Files\MySQL'
        Write-Host '        Instalalo con:  winget install Oracle.MySQL' -ForegroundColor Yellow
        return $false
    }
    Start-Process -FilePath $mysqld `
        -ArgumentList "--datadir=$MysqlDataDir", "--port=$MysqlPort", '--console' `
        -RedirectStandardError $MysqlLog `
        -WindowStyle Hidden | Out-Null
    return (Wait-Port $MysqlPort)
}

# --- -Status -----------------------------------------------------------------
if ($Status) {
    Write-Step 'Estado de SIGAM'
    if (Test-Port $MysqlPort) { Write-Ok "MySQL escuchando en $MysqlPort" } else { Write-Warn 'MySQL apagado' }
    if (Test-Port $BackendPort) { Write-Ok "Backend  http://127.0.0.1:$BackendPort" } else { Write-Warn 'Backend apagado' }
    if (Test-Port 4200)       { Write-Ok 'Frontend http://localhost:4200' } else { Write-Warn 'Frontend apagado' }
    return
}

# --- -Stop -------------------------------------------------------------------
if ($Stop) {
    Write-Step 'Cerrando SIGAM'
    if (Test-Path $PidFile) {
        foreach ($line in Get-Content $PidFile) {
            if ($line -notmatch '^(.+)=(\d+)$') { continue }
            $label  = $Matches[1]
            $procId = [int]$Matches[2]
            if (Get-Process -Id $procId -ErrorAction SilentlyContinue) {
                # /T mata tambien los hijos (el reloader de Django, el node de ng serve)
                taskkill /PID $procId /T /F | Out-Null
                Write-Ok "$label detenido (PID $procId)"
            }
        }
        Remove-Item $PidFile -Force
    } else {
        Write-Warn 'No hay procesos anotados por este script.'
    }
    # mysqld arranca sin ventana, se busca aparte
    Get-Process mysqld -ErrorAction SilentlyContinue | ForEach-Object {
        Stop-Process -Id $_.Id -Force
        Write-Ok "mysqld detenido (PID $($_.Id))"
    }
    return
}

Write-Host ''
Write-Host '  SIGAM - entorno de desarrollo' -ForegroundColor Magenta
Write-Host ''

# --- -Setup: dejar lista una maquina recien clonada --------------------------
if ($Setup) {

    # 1) MySQL: instalado, datadir inicializado, base y usuario creados
    if (-not $NoMysql) {
        Write-Step 'MySQL'
        if (-not (Get-Mysqld)) {
            Write-Err 'MySQL no esta instalado.'
            Write-Host '        Instalalo y vuelve a correr .\dev.ps1 -Setup :' -ForegroundColor Yellow
            Write-Host '          winget install Oracle.MySQL' -ForegroundColor Yellow
            Write-Host '        (o usa una base remota: llena backend\.env y corre .\dev.ps1 -Setup -NoMysql)' -ForegroundColor Yellow
            exit 1
        }

        $datadirRecienCreado = $false
        if (-not (Test-Path $MysqlDataDir)) {
            Write-Step 'Inicializando base de datos local'
            New-Item -ItemType Directory -Path $MysqlDataDir -Force | Out-Null
            & (Get-Mysqld) "--initialize-insecure" "--datadir=$MysqlDataDir" "--console"
            if ($LASTEXITCODE -ne 0) {
                Write-Err "mysqld --initialize-insecure fallo (codigo $LASTEXITCODE)"
                exit 1
            }
            $datadirRecienCreado = $true
            Write-Ok "datadir creado en $MysqlDataDir"
        }

        if (Test-Port $MysqlPort) {
            Write-Ok "ya estaba escuchando en $MysqlPort"
        } elseif (Start-Mysqld) {
            Write-Ok "arrancado en $MysqlPort"
        } else {
            Write-Err "no levanto. Revisa $MysqlLog"
            exit 1
        }

        # Crear base + usuario solo si acabamos de inicializar el datadir:
        # ahi root no tiene contrasena todavia y sabemos que la base no existe.
        if ($datadirRecienCreado) {
            $mysqlCli = Get-MysqlClient
            if (-not $mysqlCli) {
                Write-Warn 'No encontre mysql.exe; crea la base y el usuario a mano.'
            } else {
                $dbPass = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 24 | ForEach-Object { [char]$_ })
                $sql = @"
CREATE DATABASE IF NOT EXISTS sigam CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'sigam_app'@'localhost' IDENTIFIED BY '$dbPass';
CREATE USER IF NOT EXISTS 'sigam_app'@'127.0.0.1' IDENTIFIED BY '$dbPass';
GRANT ALL PRIVILEGES ON sigam.* TO 'sigam_app'@'localhost';
GRANT ALL PRIVILEGES ON sigam.* TO 'sigam_app'@'127.0.0.1';
FLUSH PRIVILEGES;
"@
                $sql | & $mysqlCli --host=127.0.0.1 --port=$MysqlPort --user=root --skip-password
                if ($LASTEXITCODE -ne 0) {
                    Write-Err 'No pude crear la base/usuario.'
                    exit 1
                }
                Write-Ok "base 'sigam' y usuario 'sigam_app' creados"

                if (-not (Test-Path $EnvFile)) {
                    # Sin BOM: python-decouple lo leeria como parte del nombre de la
                    # primera variable y DB_NAME "no existiria".
                    Write-TextFile $EnvFile @(
                        'DB_NAME=sigam',
                        'DB_USER=sigam_app',
                        "DB_PASSWORD=$dbPass",
                        'DB_HOST=127.0.0.1',
                        "DB_PORT=$MysqlPort",
                        'DB_SSL_CA='
                    )
                    Write-Ok 'backend\.env generado con esas credenciales'
                } else {
                    Write-Warn 'Ya existia backend\.env; no lo toque.'
                    Write-Warn "Contrasena de sigam_app: $dbPass"
                }
            }
        }
    }

    # 2) .env, si nada lo creo todavia
    if (-not (Test-Path $EnvFile)) {
        Copy-Item (Join-Path $BackendDir '.env.example') $EnvFile
        Write-Warn 'Cree backend\.env desde la plantilla - llena DB_PASSWORD antes de seguir.'
    }

    # 3) Dependencias
    Write-Step 'Dependencias de Python'
    if (-not (Test-Path $VenvPy)) {
        python -m venv $VenvDir
        Write-Ok 'virtualenv creado en backend\.venv'
    }
    & $VenvPip install -q -r (Join-Path $BackendDir 'requirements.txt')
    if ($LASTEXITCODE -ne 0) {
        Write-Err 'pip install fallo'
        exit 1
    }
    Write-Ok 'instaladas'

    if (-not $NoFrontend -and -not (Test-Path (Join-Path $FrontDir 'node_modules'))) {
        Write-Step 'Dependencias del frontend (npm install)'
        Push-Location $FrontDir
        try { npm install } finally { Pop-Location }
        Write-Ok 'node_modules listo'
    }
}

# --- Chequeos previos --------------------------------------------------------
if (-not (Test-Path $EnvFile)) {
    Write-Err 'Falta backend\.env'
    Write-Host '        Corre  .\dev.ps1 -Setup  para dejar todo listo desde cero.' -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path $VenvPy)) {
    Write-Err 'Falta backend\.venv'
    Write-Host '        Corre  .\dev.ps1 -Setup' -ForegroundColor Yellow
    exit 1
}

$caConfigurado = Read-EnvValue 'DB_SSL_CA'
if ($null -eq $caConfigurado -and -not (Test-Path (Join-Path $BackendDir 'certs\ca.pem'))) {
    Write-Warn 'Sin backend\certs\ca.pem: la conexion a MySQL ira sin TLS (ok en local).'
}

# --- MySQL -------------------------------------------------------------------
if (-not $NoMysql) {
    Write-Step 'MySQL'
    if (Test-Port $MysqlPort) {
        Write-Ok "ya estaba escuchando en $MysqlPort"
    }
    elseif (Test-Path $MysqlDataDir) {
        if (Start-Mysqld) {
            Write-Ok "arrancado en $MysqlPort (log: $MysqlLog)"
        } else {
            Write-Err "no levanto en 40s. Revisa $MysqlLog"
            exit 1
        }
    }
    else {
        Write-Warn "No hay datadir local en $MysqlDataDir y el puerto $MysqlPort esta libre."
        Write-Warn 'Si usas una base remota, ignora esto (o corre con -NoMysql).'
    }
}

# --- Migraciones -------------------------------------------------------------
if ($Migrate -or $Setup) {
    Write-Step 'Aplicando migraciones'
    Push-Location $BackendDir
    try { & $VenvPy manage.py migrate } finally { Pop-Location }
    if ($LASTEXITCODE -ne 0) {
        Write-Err 'migrate fallo - revisa el error de arriba (credenciales en backend\.env, MySQL arriba?)'
        exit 1
    }
    Write-Ok 'migraciones al dia'
}

# --- Arrancar backend y frontend --------------------------------------------
if (Test-Path $PidFile) { Remove-Item $PidFile -Force }

if (-not $NoBackend) {
    Write-Step 'Backend (Django)'
    if (Test-Port $BackendPort) {
        Write-Warn "el puerto $BackendPort ya esta ocupado, no arranco otro"
    } else {
        $cmd = "`$Host.UI.RawUI.WindowTitle = 'SIGAM backend'; Set-Location '$BackendDir'; & '$VenvPy' manage.py runserver $BackendPort"
        $p = Start-Process -FilePath 'powershell.exe' -ArgumentList '-NoExit', '-Command', $cmd -PassThru
        Save-Pid 'backend' $p.Id
        if (Wait-Port $BackendPort) { Write-Ok "http://127.0.0.1:$BackendPort  (docs: /swagger/)" }
        else { Write-Warn 'no respondio en 40s - mira la ventana "SIGAM backend"' }
    }
}

if (-not $NoFrontend) {
    Write-Step 'Frontend (Angular)'
    if (-not (Test-Path (Join-Path $FrontDir 'node_modules'))) {
        Write-Err 'Falta frontend\node_modules - corre .\dev.ps1 -Setup'
    }
    elseif (Test-Port 4200) {
        Write-Warn 'el puerto 4200 ya esta ocupado, no arranco otro'
    } else {
        $cmd = "`$Host.UI.RawUI.WindowTitle = 'SIGAM frontend'; Set-Location '$FrontDir'; npm start"
        $p = Start-Process -FilePath 'powershell.exe' -ArgumentList '-NoExit', '-Command', $cmd -PassThru
        Save-Pid 'frontend' $p.Id
        if (Wait-Port 4200 90) { Write-Ok 'http://localhost:4200' }
        else { Write-Warn 'todavia compilando - mira la ventana "SIGAM frontend"' }
    }
}

Write-Host ''
Write-Host '  Listo.' -ForegroundColor Green
Write-Host '    App        http://localhost:4200'
Write-Host "    API        http://127.0.0.1:$BackendPort"
Write-Host "    Swagger    http://127.0.0.1:$BackendPort/swagger/"
Write-Host ''
Write-Host '    Para cerrar todo:  .\dev.ps1 -Stop' -ForegroundColor DarkGray
Write-Host ''
