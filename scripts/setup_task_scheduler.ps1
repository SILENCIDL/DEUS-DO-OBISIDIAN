# setup_task_scheduler.ps1 - DEUS-DO-OBSIDIAN
# ==============================================
# Registra duas tarefas no Task Scheduler do Windows 10:
#   1. DEUS-DO-OBSIDIAN_Injector_Diario  — todo dia as 22:00
#   2. DEUS-DO-OBSIDIAN_Session_Watcher  — ao login (background)
#
# COMO USAR (PowerShell como ADMINISTRADOR):
#   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
#   cd "...\DEUS-DO-OBISIDIAN\scripts"
#   .\setup_task_scheduler.ps1
#
# OUTROS MODOS:
#   .\setup_task_scheduler.ps1 -Status   (ver status das tarefas)
#   .\setup_task_scheduler.ps1 -Remover  (remover tarefas)

param(
    [switch]$Remover,
    [switch]$Status,
    [string]$VaultRoot = "",
    [string]$ScriptsDir = "",
    [string]$PythonExe = ""
)

# --- HELPERS ---
function Write-OK   ($msg) { Write-Host "  OK  $msg" -ForegroundColor Green }
function Write-FAIL ($msg) { Write-Host "  ERR $msg" -ForegroundColor Red }
function Write-INFO ($msg) { Write-Host "  --> $msg" -ForegroundColor Cyan }
function Write-WARN ($msg) { Write-Host "  !   $msg" -ForegroundColor Yellow }

Write-Host ""
Write-Host "================================================" -ForegroundColor Magenta
Write-Host "  DEUS-DO-OBSIDIAN -- Task Scheduler Setup" -ForegroundColor Magenta
Write-Host "================================================" -ForegroundColor Magenta
Write-Host ""

# --- AUTO-DETECCAO DE CAMINHOS ---
if (-not $ScriptsDir) {
    $ScriptsDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    if (-not $ScriptsDir) { $ScriptsDir = (Get-Location).Path }
}

if (-not $VaultRoot) {
    $VaultRoot = Split-Path -Parent $ScriptsDir
}

$TASK_INJECTOR = "DEUS-DO-OBSIDIAN_Injector_Diario"
$TASK_WATCHER  = "DEUS-DO-OBSIDIAN_Session_Watcher"

# --- MODO STATUS ---
if ($Status) {
    Write-Host "Status das tarefas:" -ForegroundColor Yellow
    Write-Host ""
    foreach ($nome in @($TASK_INJECTOR, $TASK_WATCHER)) {
        $t = Get-ScheduledTask -TaskName $nome -ErrorAction SilentlyContinue
        if ($t) {
            $info = Get-ScheduledTaskInfo -TaskName $nome -ErrorAction SilentlyContinue
            $ultima = if ($info.LastRunTime) { $info.LastRunTime.ToString("dd/MM/yyyy HH:mm") } else { "nunca" }
            $prox   = if ($info.NextRunTime) { $info.NextRunTime.ToString("dd/MM/yyyy HH:mm") } else { "-" }
            Write-OK  "$nome"
            Write-INFO "  Estado: $($t.State) | Ultima: $ultima | Proxima: $prox"
        } else {
            Write-FAIL "$nome -- NAO REGISTRADA"
        }
    }
    Write-Host ""
    exit 0
}

# --- MODO REMOVER ---
if ($Remover) {
    Write-Host "Removendo tarefas..." -ForegroundColor Yellow
    foreach ($nome in @($TASK_INJECTOR, $TASK_WATCHER)) {
        if (Get-ScheduledTask -TaskName $nome -ErrorAction SilentlyContinue) {
            Unregister-ScheduledTask -TaskName $nome -Confirm:$false
            Write-OK "Removida: $nome"
        } else {
            Write-WARN "Nao encontrada: $nome"
        }
    }
    Write-Host ""
    exit 0
}

# --- VERIFICACOES ---
Write-Host "Verificando ambiente..." -ForegroundColor Yellow

$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if ($isAdmin) {
    Write-OK "Executando como administrador"
} else {
    Write-WARN "Sem admin -- tarefa sera registrada para seu usuario (OK)"
}
Write-OK "Executando como administrador"
Write-INFO "Scripts: $ScriptsDir"
Write-INFO "Vault:   $VaultRoot"

$InjectorPath = Join-Path $ScriptsDir "vault_injector.py"
$WatcherPath  = Join-Path $ScriptsDir "session_watcher.py"

foreach ($script in @($InjectorPath, $WatcherPath)) {
    if (Test-Path $script) {
        Write-OK "Encontrado: $(Split-Path $script -Leaf)"
    } else {
        Write-FAIL "Nao encontrado: $script"
        Write-Host "  Coloque os scripts .py na mesma pasta deste .ps1" -ForegroundColor Yellow
        exit 1
    }
}

# Detecta Python
if (-not $PythonExe) {
    $pyCmd  = Get-Command python  -ErrorAction SilentlyContinue
    $py3Cmd = Get-Command python3 -ErrorAction SilentlyContinue
    $candidates = @(
        $(if ($pyCmd)  { $pyCmd.Source }  else { $null }),
        $(if ($py3Cmd) { $py3Cmd.Source } else { $null }),
        "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "C:\Python314\python.exe",
        "C:\Python313\python.exe",
        "C:\Python312\python.exe",
        "C:\Python311\python.exe"
    )
    foreach ($c in $candidates) {
        if ($c -and (Test-Path $c)) {
            $PythonExe = $c
            break
        }
    }
}

if (-not $PythonExe -or -not (Test-Path $PythonExe)) {
    Write-FAIL "Python nao encontrado!"
    Write-Host "  Passe o caminho manualmente:" -ForegroundColor Yellow
    Write-Host "  .\setup_task_scheduler.ps1 -PythonExe 'C:\Python314\python.exe'" -ForegroundColor Yellow
    exit 1
}

$versao = & $PythonExe --version 2>&1
Write-OK "Python: $versao"
Write-OK "Exe:    $PythonExe"

Write-Host ""

# --- PASTA .injector ---
$InjectorDir = Join-Path $VaultRoot ".injector"
if (-not (Test-Path $InjectorDir)) {
    New-Item -ItemType Directory -Path $InjectorDir -Force | Out-Null
    Write-OK "Criada pasta .injector"
}

# --- TAREFA 1: INJECTOR DIARIO (22:00) ---
Write-Host "Registrando: $TASK_INJECTOR" -ForegroundColor Yellow

if (Get-ScheduledTask -TaskName $TASK_INJECTOR -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TASK_INJECTOR -Confirm:$false
    Write-INFO "Tarefa anterior removida"
}

$acao1 = New-ScheduledTaskAction `
    -Execute $PythonExe `
    -Argument "`"$InjectorPath`"" `
    -WorkingDirectory $ScriptsDir

$trigger1 = New-ScheduledTaskTrigger -Daily -At "22:00"

$config1 = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew

$principal1 = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

try {
    Register-ScheduledTask `
        -TaskName $TASK_INJECTOR `
        -Action $acao1 `
        -Trigger $trigger1 `
        -Settings $config1 `
        -Principal $principal1 `
        -Description "DEUS-DO-OBSIDIAN: injeta sessoes no vault todo dia as 22h" `
        -Force | Out-Null
    Write-OK "$TASK_INJECTOR registrada (22:00 diario)"
} catch {
    Write-FAIL "Falha ao registrar $TASK_INJECTOR`: $_"
}

Write-Host ""

# --- TAREFA 2: SESSION WATCHER (ao login) ---
Write-Host "Registrando: $TASK_WATCHER" -ForegroundColor Yellow

if (Get-ScheduledTask -TaskName $TASK_WATCHER -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TASK_WATCHER -Confirm:$false
    Write-INFO "Tarefa anterior removida"
}

$acao2 = New-ScheduledTaskAction `
    -Execute $PythonExe `
    -Argument "`"$WatcherPath`"" `
    -WorkingDirectory $ScriptsDir

$trigger2 = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$trigger2.Delay = "PT60S"

$config2 = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 24) `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -RestartInterval (New-TimeSpan -Minutes 2) `
    -RestartCount 5

$principal2 = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

try {
    Register-ScheduledTask `
        -TaskName $TASK_WATCHER `
        -Action $acao2 `
        -Trigger $trigger2 `
        -Settings $config2 `
        -Principal $principal2 `
        -Description "DEUS-DO-OBSIDIAN: monitora INBOX e injeta automaticamente" `
        -Force | Out-Null
    Write-OK "$TASK_WATCHER registrada (ao login, delay 60s)"
} catch {
    Write-FAIL "Falha ao registrar $TASK_WATCHER`: $_"
}

Write-Host ""

# --- INICIA O WATCHER AGORA ---
Write-Host "Iniciando session_watcher agora..." -ForegroundColor Yellow
try {
    Start-ScheduledTask -TaskName $TASK_WATCHER
    Start-Sleep -Seconds 3
    $estado = (Get-ScheduledTask -TaskName $TASK_WATCHER).State
    if ($estado -eq "Running") {
        Write-OK "session_watcher rodando em background"
    } else {
        Write-WARN "session_watcher iniciado, estado: $estado"
    }
} catch {
    Write-WARN "Nao foi possivel iniciar agora (sera iniciado no proximo login)"
}

Write-Host ""

# --- RESUMO ---
Write-Host "================================================" -ForegroundColor Magenta
Write-Host "  Setup concluido!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Magenta
Write-Host ""
Write-OK "$TASK_INJECTOR  -->  todo dia as 22:00"
Write-OK "$TASK_WATCHER   -->  ao login + rodando agora"
Write-Host ""
Write-INFO "Ver status:   .\setup_task_scheduler.ps1 -Status"
Write-INFO "Testar:       python vault_injector.py --dry-run"
Write-INFO "Nova sessao:  python vault_injector.py --nova-sessao"
Write-INFO "Remover:      .\setup_task_scheduler.ps1 -Remover"
Write-Host ""
Write-INFO "Logs em: $InjectorDir"
Write-Host ""