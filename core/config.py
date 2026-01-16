import json
import os
import platform

def detect_platform():
    system = platform.system().lower()
    if system == "linux":
        # Проверим, Kali ли
        try:
            with open("/etc/os-release") as f:
                if "kali" in f.read().lower():
                    return "kali"
        except:
            pass
        return "linux"
    elif system == "windows":
        return "windows"
    else:
        return "unknown"

def load_config(config_path="config.json"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Файл конфигурации не найден: {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    if config.get("platform") == "auto":
        config["platform"] = detect_platform()
    
    return config