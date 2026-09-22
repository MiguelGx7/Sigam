$ErrorActionPreference = 'Stop'

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $Root 'backend'
$EnvFile = Join-Path $BackendDir '.env'
$MysqlDataDir = Join-Path $env:USERPROFILE 'mysql-data\sigam'

function Find-MySqlBinary {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    $result = Get-ChildItem 'C:\Program Files\MySQL' -Recurse -Filter $Name -ErrorAction SilentlyContinue |
        Sort-Object FullName |
        Select-Object -First 1 -ExpandProperty FullName

    if (-not $result) {
        throw "No encontré $Name dentro de C:\Program Files\MySQL. Instala MySQL antes de continuar."
    }

    return $result
}

function Wait-For-Listen {
    param(
        [int]$Port,
        [int]$TimeoutSeconds = 45
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $portOpen = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
        if ($null -ne $portOpen) {
            return $true
        }
        Start-Sleep -Milliseconds 500
    }

    return $false
}

Write-Host '==> Deteniendo instancias MySQL viejas' -ForegroundColor Cyan
foreach ($svc in @('MySQL80', 'MySQL')) {
    try {
        Stop-Service -Name $svc -Force -ErrorAction SilentlyContinue
    } catch {
        # ignorar
    }
}

Get-Process mysqld -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "  - matando PID $($_.Id)" -ForegroundColor Yellow
    taskkill /PID $_.Id /T /F | Out-Null
}

Write-Host '==> Borrando datadir local de desarrollo' -ForegroundColor Cyan
if (Test-Path $MysqlDataDir) {
    Remove-Item -Path $MysqlDataDir -Recurse -Force -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Force -Path $MysqlDataDir | Out-Null

$mysqld = Find-MySqlBinary -Name 'mysqld.exe'
Write-Host "Usando $mysqld" -ForegroundColor DarkGray

Write-Host '==> Inicializando MySQL sin contraseña para root' -ForegroundColor Cyan
& $mysqld '--initialize-insecure' '--datadir=' + $MysqlDataDir '--console'
if ($LASTEXITCODE -ne 0) {
    throw "mysqld --initialize-insecure falló con código $LASTEXITCODE"
}

Write-Host '==> Arrancando MySQL local' -ForegroundColor Cyan
Start-Process -FilePath $mysqld -ArgumentList @("--datadir=$MysqlDataDir", '--port=3306', '--console') -WindowStyle Hidden | Out-Null

if (-not (Wait-For-Listen -Port 3306)) {
    throw 'MySQL no quedó escuchando en el puerto 3306.'
}

$mysql = Find-MySqlBinary -Name 'mysql.exe'
$dbPassword = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 24 | ForEach-Object { [char]$_ })

$sql = @"
CREATE DATABASE IF NOT EXISTS sigam CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'sigam_app'@'localhost' IDENTIFIED BY '$dbPassword';
CREATE USER IF NOT EXISTS 'sigam_app'@'127.0.0.1' IDENTIFIED BY '$dbPassword';
GRANT ALL PRIVILEGES ON sigam.* TO 'sigam_app'@'localhost';
GRANT ALL PRIVILEGES ON sigam.* TO 'sigam_app'@'127.0.0.1';
FLUSH PRIVILEGES;
"@

Write-Host '==> Creando base y usuario de la app' -ForegroundColor Cyan
$sql | & $mysql --host=127.0.0.1 --port=3306 --user=root --skip-password
if ($LASTEXITCODE -ne 0) {
    throw 'No pude crear la base sigam ni el usuario sigam_app.'
}

Write-Host '==> Escribiendo backend/.env' -ForegroundColor Cyan
$lines = @(
    'DB_NAME=sigam',
    'DB_USER=sigam_app',
    "DB_PASSWORD=$dbPassword",
    'DB_HOST=127.0.0.1',
    'DB_PORT=3306',
    'DB_SSL_CA='
)
[System.IO.File]::WriteAllText($EnvFile, ($lines -join "`r`n") + "`r`n", (New-Object System.Text.UTF8Encoding($false)))

Write-Host ''
Write-Host 'Listo. Ya quedó la base local reconstruida.' -ForegroundColor Green
Write-Host 'Ahora corre esto desde la raiz del proyecto:' -ForegroundColor Green
Write-Host '  .\dev.ps1 -Setup' -ForegroundColor Yellow
Write-Host 'o directamente:' -ForegroundColor Green
Write-Host '  .\dev.ps1' -ForegroundColor Yellow
