# Configuración de variables de entorno para Python
# Evita la generación de archivos .pyc y __pycache__

# Previene la generación de archivos .pyc
$env:PYTHONDONTWRITEBYTECODE = "1"

# Mejora el output de Python
$env:PYTHONUNBUFFERED = "1"

Write-Host "Variables de entorno configuradas:"
Write-Host "PYTHONDONTWRITEBYTECODE = $env:PYTHONDONTWRITEBYTECODE"
Write-Host "PYTHONUNBUFFERED = $env:PYTHONUNBUFFERED"

# Para que las variables persistan en la sesión actual
[System.Environment]::SetEnvironmentVariable("PYTHONDONTWRITEBYTECODE", "1", "User")
[System.Environment]::SetEnvironmentVariable("PYTHONUNBUFFERED", "1", "User")

Write-Host "Variables guardadas en el perfil de usuario"
