@echo off
setlocal EnableDelayedExpansion
chcp 65001 > nul
title Instalação — Obsidian MCP Server v3

echo.
echo  ╔══════════════════════════════════════╗
echo  ║   Obsidian MCP Server v3             ║
echo  ║   Instalação automática              ║
echo  ╚══════════════════════════════════════╝
echo.

:: ─────────────────────────────────────────────
:: Verificar Python
:: ─────────────────────────────────────────────
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado. Instale em python.org e tente novamente.
    pause & exit /b 1
)
for /f "tokens=*" %%v in ('python --version') do echo [OK] %%v

:: ─────────────────────────────────────────────
:: Criar virtualenv
:: ─────────────────────────────────────────────
set VENV=.venv
if not exist "%VENV%\Scripts\activate.bat" (
    echo [INFO] Criando virtualenv em %VENV%...
    python -m venv %VENV%
    if errorlevel 1 ( echo [ERRO] Falha ao criar venv. & pause & exit /b 1 )
    echo [OK] Virtualenv criado.
) else (
    echo [OK] Virtualenv ja existe.
)

:: ─────────────────────────────────────────────
:: Instalar dependências
:: ─────────────────────────────────────────────
echo [INFO] Instalando dependencias...
call "%VENV%\Scripts\activate.bat"
pip install --quiet --upgrade pip
pip install --quiet "mcp[cli]>=1.3.0" python-frontmatter
if errorlevel 1 ( echo [ERRO] Falha ao instalar pacotes. & pause & exit /b 1 )
echo [OK] Dependencias instaladas.

:: ─────────────────────────────────────────────
:: Testar importações
:: ─────────────────────────────────────────────
echo [INFO] Testando importacoes...
python -c "from mcp.server.fastmcp import FastMCP; import frontmatter; print('[OK] Imports OK')"
if errorlevel 1 ( echo [ERRO] Falha nos imports. & pause & exit /b 1 )

:: ─────────────────────────────────────────────
:: Caminho absoluto do servidor
:: ─────────────────────────────────────────────
set SERVER_SCRIPT=%~dp0obsidian_mcp_server.py
set PYTHON_EXE=%~dp0%VENV%\Scripts\python.exe

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║   PRÓXIMO PASSO — configure o Claude Desktop                ║
echo  ╠══════════════════════════════════════════════════════════════╣
echo  ║                                                              ║
echo  ║   Abra (ou crie) o arquivo:                                  ║
echo  ║   %%APPDATA%%\Claude\claude_desktop_config.json               ║
echo  ║                                                              ║
echo  ║   Mescle o conteúdo de claude_desktop_config.json           ║
echo  ║   (está na mesma pasta deste .bat)                           ║
echo  ║                                                              ║
echo  ║   Python exe : %PYTHON_EXE%
echo  ║   Servidor   : %SERVER_SCRIPT%
echo  ║                                                              ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

:: Exibe o JSON pronto para copiar
echo Conteudo para copiar no claude_desktop_config.json:
echo.
echo {
echo   "mcpServers": {
echo     "obsidian": {
echo       "command": "%PYTHON_EXE:\=\\%",
echo       "args": ["%SERVER_SCRIPT:\=\\%"],
echo       "env": {
echo         "OBSIDIAN_VAULT_PATH": "C:\\Users\\Usuário\\Desktop\\V1"
echo       }
echo     }
echo   }
echo }
echo.
echo [CONCLUÍDO] Reinicie o Claude Desktop após mesclar o JSON.
echo.
pause
