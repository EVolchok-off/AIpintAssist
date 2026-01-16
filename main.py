from core.config import load_config
from core.ai_client import AIClient
from interfaces.cli import run_cli
from platforms import windows, linux
import sys

def main():
    try:
        config = load_config()
        print(f"🔧 Платформа: {config['platform']}")
        
        # Проверка инструментов (опционально)
        if config["platform"] == "kali":
            linux.check_kali_tools()
        elif config["platform"] == "windows":
            windows.check_kali_tools()
            print("[❗] Внимание: инструменты Kali Linux (nmap, sqlmap и др.) недоступны в этой ОС.")
            print("    Рекомендуется:")
            print("    - Использовать Kali Linux")
            print("    - Или установить WSL2 + Kali Linux в Windows")
            print("    - Или использовать облачный пентест-инстанс\n")

        ai = AIClient(
            api_url=config["api_url"],
            model=config["model"],
            api_key=config.get("api_key")
        )

        print(f"🧠 Подключено к модели: {config['model']}")
        run_cli(ai)

    except Exception as e:
        print(f"[КРИТИЧЕСКАЯ ОШИБКА] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()