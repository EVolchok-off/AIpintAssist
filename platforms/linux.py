import subprocess

def is_tool_installed(tool: str) -> bool:
    try:
        subprocess.run(["which", tool], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except:
        return False

def check_kali_tools():
    tools = ["nmap", "gobuster", "sqlmap", "nikto", "hydra"]
    missing = [t for t in tools if not is_tool_installed(t)]
    if missing:
        print(f"[⚠️] Некоторые инструменты отсутствуют: {', '.join(missing)}")
        return False
    else:
        print("[✅] Все основные Kali-инструменты доступны.")
        return True