import re
from core.command_executor import safe_execute

def extract_bash_code(text: str) -> str | None:
    # Ищем блок кода в формате ```bash ... ```
    match = re.search(r"```(?:bash|sh|zsh)\n(.*?)\n```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # На случай, если ИИ забыл указать язык
    match2 = re.search(r"```(.*?)\n```", text, re.DOTALL)
    if match2:
        return match2.group(1).strip()
    return None

def run_cli(ai_client):
    print("🚀 AI Hacker Assistant (CLI) запущен.")
    print("💡 Совет: спросите 'Как просканировать 192.168.1.1?' или 'Помоги найти уязвимости'\n")
    
    while True:
        try:
            user_input = input("👤 Вы: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "выйти"):
                print("👋 До встречи!")
                break

            print("\n⏳ Думаю...")
            reply = ai_client.send_message(user_input)
            print(f"\n🤖 ИИ:\n{reply}\n")

            # Пытаемся извлечь команду
            cmd = extract_bash_code(reply)
            if cmd:
                output = safe_execute(cmd)
                print(f"💻 Вывод:\n{output}\n")
                # Отправляем результат обратно ИИ для анализа
                ai_client.send_message(f"Результат выполнения:\n{output}")

        except KeyboardInterrupt:
            print("\n\n👋 Принудительный выход.")
            break
        except Exception as e:
            print(f"[!] Критическая ошибка: {e}")