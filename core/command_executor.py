import subprocess
import platform
import os
import sys

# Базовый список опасных команд (можно расширить)
DANGEROUS_PATTERNS = [
    "rm -rf", "mkfs", "dd if=", ":(){", "shutdown", "reboot",
    "format", "del /s", "rmdir /s", "cipher /w"
]

def is_dangerous(command: str) -> bool:
    cmd_lower = command.lower()
    return any(pattern in cmd_lower for pattern in DANGEROUS_PATTERNS)

def get_system_encoding():
    if sys.platform == "win32":
        # На Windows часто используется cp866 (cmd) или cp1251 (PowerShell)
        # Лучше использовать encoding из локали
        return "cp866"  # или "cp1251", но cp866 — стандарт для cmd
    else:
        return "utf-8"


def safe_execute(command: str, confirm=True) -> str:
    if is_dangerous(command):
        return "[!] Отклонено: команда потенциально опасна."

    if confirm:
        print(f"\n[?] ИИ предлагает выполнить:\n{command}\n")
        if input("Выполнить? (y/N): ").lower() != 'y':
            return "[Отменено пользователем]"

    try:
        encoding = get_system_encoding()
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding=encoding,  # ← КЛЮЧЕВОЕ ИЗМЕНЕНИЕ
            errors="replace",   # заменять некорректные символы
            timeout=120
        )
        output = (result.stdout or "") + (result.stderr or "")
        return output if output else "[Команда завершена, вывод пуст]"
    except subprocess.TimeoutExpired:
        return "[Ошибка: команда превысила лимит времени (120 сек)]"
    except Exception as e:
        return f"[Ошибка выполнения: {e}]"