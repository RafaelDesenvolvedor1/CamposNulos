# Limpa o terminal
Clear-Host

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "          PROCESSADOR DE CAMPOS NULOS (Windows)     " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Sugere um caminho padrão (Ajuste se necessário)
$DefaultPath = "S:\Bauk\boraFazerMerda\baixas\vox"

Write-Host "Qual pasta deseja processar?"
Write-Host "Pressione ENTER para usar o padrão: $DefaultPath"
$UserPath = Read-Host "Caminho"

# Se o usuário apenas der ENTER, usa o padrão
if ([string]::IsNullOrWhiteSpace($UserPath)) {
    $UserPath = $DefaultPath
}

# 2. Verifica se o diretório existe
if (-not (Test-Path -Path $UserPath)) {
    Write-Host ""
    Write-Host "❌ ERRO: O diretório '$UserPath' não existe." -ForegroundColor Red
    Pause
    exit
}

Write-Host ""
Write-Host "  Iniciando Container Docker..." -ForegroundColor Yellow
Write-Host "  Mapeando: $UserPath -> /app/dados"
Write-Host "----------------------------------------------------"

# 3. Execução do Docker
# No PowerShell, usamos aspas duplas para variáveis e garantimos o modo interativo
docker run -it --rm `
  -v "${UserPath}:/app/dados" `
  -e CAMINHO_TRABALHO="/app/dados/" `
  campos-nulos-app

Write-Host ""
Write-Host "✅ Execução finalizada." -ForegroundColor Green
Pause