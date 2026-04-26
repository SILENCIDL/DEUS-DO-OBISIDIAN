"""
session_watcher.py v2 — DEUS-DO-OBSIDIAN
==========================================
Monitora o INBOX do vault por novos arquivos (.md / .txt / .json).
Quando detecta um arquivo novo, aguarda DEBOUNCE segundos (para o usuário
terminar de editar) e dispara o vault_injector.py automaticamente.

Também monitora o Claude Desktop para detectar quando ele fecha,
sugerindo criar uma nota de sessão.

Roda via Task Scheduler ao login (setup_task_scheduler.ps1).
"""

import os
import sys
import time
import json
import signal
import logging
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from threading import Event

# ─── CONFIGURAÇÃO ─────────────────────────────────────────────────────────────

# Detecção automática do vault (scripts\ está dentro do vault)
_SCRIPT_DIR    = Path(__file__).resolve().parent
_VAULT_CAND    = _SCRIPT_DIR.parent
_MARKERS       = ["FOTOGRAFIA", "CODIFICAÇÃO + IA", "INBOX", "PROJETOS E IDEIAS"]
if any((_VAULT_CAND / m).exists() for m in _MARKERS):
    VAULT_ROOT = _VAULT_CAND
else:
    for _p in _SCRIPT_DIR.parents:
        if "OBSIDIAN" in _p.name.upper() or "OBISIDIAN" in _p.name.upper():
            VAULT_ROOT = _p
            break
    else:
        VAULT_ROOT = _VAULT_CAND

INBOX          = VAULT_ROOT / "INBOX"
INJECTOR_PATH  = _SCRIPT_DIR / "vault_injector.py"
PYTHON_EXE     = sys.executable
PID_FILE       = VAULT_ROOT / ".injector" / "watcher.pid"
WATCHER_LOG    = VAULT_ROOT / ".injector" / "watcher.log"

# Segundos de inatividade no arquivo antes de disparar (debounce de edição)
DEBOUNCE       = 30   # 30s após o arquivo parar de ser modificado

# Intervalo de polling
POLL_INTERVAL  = 10   # verifica a cada 10s

# ─── LOGGING ──────────────────────────────────────────────────────────────────

def setup_logging(debug=False):
    WATCHER_LOG.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="[%(asctime)s] %(levelname)s  %(message)s",
        datefmt="%H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(WATCHER_LOG, encoding="utf-8", mode="a"),
        ]
    )

log = logging.getLogger("session_watcher")

# ─── INSTÂNCIA ÚNICA ──────────────────────────────────────────────────────────

def verificar_instancia_unica() -> bool:
    if not PID_FILE.exists():
        return True
    try:
        pid = int(PID_FILE.read_text().strip())
        r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV"],
                           capture_output=True, text=True)
        if str(pid) in r.stdout:
            log.warning(f"Watcher já rodando (PID {pid}). Saindo.")
            return False
    except Exception:
        pass
    return True

def registrar_pid():
    PID_FILE.parent.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()))

def limpar_pid():
    try:
        PID_FILE.unlink(missing_ok=True)
    except Exception:
        pass

# ─── WATCHER ──────────────────────────────────────────────────────────────────

class InboxWatcher:
    def __init__(self, debounce=DEBOUNCE):
        self.debounce = debounce
        self._stop = Event()
        # Rastreia: caminho → último mtime visto
        self._arquivos_vistos: dict[str, float] = {}
        # Arquivos aguardando debounce: caminho → timestamp da última modificação
        self._pendentes: dict[str, float] = {}

    def snapshot_inbox(self) -> dict[str, float]:
        """Retorna {caminho: mtime} para todos os arquivos relevantes no INBOX."""
        if not INBOX.exists():
            return {}
        resultado = {}
        for ext in ("*.md", "*.txt", "*.json"):
            for p in INBOX.glob(ext):
                if p.is_file() and not p.name.startswith("_"):
                    resultado[str(p)] = p.stat().st_mtime
        return resultado

    def disparar_injecao(self, arquivos: list[str]):
        log.info("━" * 44)
        log.info(f"Novos arquivos detectados ({len(arquivos)}) — disparando injector")
        for a in arquivos:
            log.info(f"  {Path(a).name}")
        try:
            r = subprocess.run(
                [PYTHON_EXE, str(INJECTOR_PATH)],
                capture_output=True, text=True, timeout=120
            )
            if r.returncode == 0:
                log.info("✓ vault_injector concluído")
                for linha in r.stdout.splitlines():
                    if "✓" in linha or "Resumo" in linha:
                        log.info(f"  {linha.strip()}")
            else:
                log.error(f"vault_injector saiu com código {r.returncode}")
                if r.stderr:
                    log.error(r.stderr[:300])
        except subprocess.TimeoutExpired:
            log.error("vault_injector excedeu timeout de 2 minutos")
        except FileNotFoundError:
            log.error(f"vault_injector não encontrado: {INJECTOR_PATH}")
        log.info("━" * 44)

    def run(self):
        log.info("session_watcher v2 iniciado")
        log.info(f"Monitorando INBOX: {INBOX}")
        log.info(f"Debounce: {self.debounce}s | Poll: {POLL_INTERVAL}s")

        # Snapshot inicial — não dispara para arquivos já existentes
        self._arquivos_vistos = self.snapshot_inbox()
        log.info(f"Arquivos existentes no INBOX: {len(self._arquivos_vistos)}")

        while not self._stop.is_set():
            agora = time.time()
            snapshot_atual = self.snapshot_inbox()

            # Detecta arquivos novos ou modificados
            for caminho, mtime in snapshot_atual.items():
                mtime_anterior = self._arquivos_vistos.get(caminho, 0)
                if mtime > mtime_anterior:
                    if caminho not in self._pendentes:
                        log.debug(f"Arquivo detectado: {Path(caminho).name}")
                    self._pendentes[caminho] = mtime
                    self._arquivos_vistos[caminho] = mtime

            # Remove do pendente arquivos que sumiram (foram processados/movidos)
            removidos = [c for c in self._pendentes if c not in snapshot_atual]
            for c in removidos:
                del self._pendentes[c]
                self._arquivos_vistos.pop(c, None)

            # Verifica quais pendentes passaram o debounce
            prontos = []
            for caminho, mtime_detectado in list(self._pendentes.items()):
                silencio = agora - mtime_detectado
                if silencio >= self.debounce:
                    prontos.append(caminho)

            if prontos:
                for c in prontos:
                    del self._pendentes[c]
                self.disparar_injecao(prontos)

            self._stop.wait(POLL_INTERVAL)

        log.info("session_watcher v2 parado.")

    def parar(self, *_):
        log.info("Sinal de parada recebido.")
        self._stop.set()

# ─── STATUS ───────────────────────────────────────────────────────────────────

def mostrar_status():
    print("\n═══ DEUS-DO-OBSIDIAN — session_watcher v2 status ═══")
    print(f"Python:          {sys.executable}")
    v = VAULT_ROOT
    print(f"Vault:           {v} {'✓' if v.exists() else '✗ NÃO EXISTE'}")
    i = INBOX
    print(f"INBOX:           {i} {'✓' if i.exists() else '✗ NÃO EXISTE'}")
    inj = INJECTOR_PATH
    print(f"vault_injector:  {inj} {'✓' if inj.exists() else '✗ NÃO EXISTE'}")

    if INBOX.exists():
        arqs = [p for ext in ("*.md","*.txt","*.json") for p in INBOX.glob(ext)
                if not p.name.startswith("_")]
        print(f"Arquivos INBOX:  {len(arqs)} arquivo(s) aguardando injeção")

    rodando = False
    if PID_FILE.exists():
        pid = PID_FILE.read_text().strip()
        r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV"],
                           capture_output=True, text=True)
        rodando = pid in r.stdout
    print(f"Watcher ativo:   {'✓ SIM (PID ' + PID_FILE.read_text().strip() + ')' if rodando and PID_FILE.exists() else '✗ NÃO'}")
    print("═" * 50 + "\n")

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="DEUS-DO-OBSIDIAN — Session Watcher v2")
    parser.add_argument("--debug",    action="store_true")
    parser.add_argument("--status",   action="store_true")
    parser.add_argument("--debounce", type=int, default=DEBOUNCE)
    parser.add_argument("--force",    action="store_true")
    args = parser.parse_args()

    VAULT_ROOT.joinpath(".injector").mkdir(parents=True, exist_ok=True)
    setup_logging(args.debug)

    if args.status:
        mostrar_status()
        return

    if not args.force and not verificar_instancia_unica():
        sys.exit(1)

    registrar_pid()
    watcher = InboxWatcher(debounce=args.debounce)
    signal.signal(signal.SIGINT,  watcher.parar)
    signal.signal(signal.SIGTERM, watcher.parar)

    try:
        watcher.run()
    finally:
        limpar_pid()

if __name__ == "__main__":
    main()
