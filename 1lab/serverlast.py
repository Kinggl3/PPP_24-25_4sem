import socket
import threading
import subprocess
import time
import os

commands = {}
running_commands = {}
interval = 10
server_running = True
log_dir = "logs"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

def sanitize_filename(name):
    """Заменяет пробелы и спецсимволы в имени команды, чтобы не было проблем с файлами."""
    return name.replace(" ", "_").replace("'", "").replace('"', '').replace("/", "_")

def run_command(command_name):
    """Функция для многократного запуска команды с заданным интервалом."""
    command = commands.get(command_name)
    if not command:
        return

    log_path = os.path.join(log_dir, f"{sanitize_filename(command_name)}.log")

    while running_commands.get(command_name, False):
        try:
            print(f"Запускаю: {command}")

            with open(log_path, "a") as log_file:
                process = subprocess.Popen(
                    command, stdout=log_file, stderr=log_file, text=True, shell=True
                )
                process.wait()
                log_file.flush()

            time.sleep(interval)

        except Exception as e:
            print(f"Ошибка при запуске {command}: {e}")
            break

def handle_client(conn):
    """Обработчик запросов клиента."""
    global interval
    try:
        while server_running:
            conn.settimeout(0.1)
            try:
                command = conn.recv(1024).decode().strip()
                if not command:
                    break
            except socket.timeout:
                continue

            print(f"Получено: {command}")
            parts = command.split(" ", 1)
            action = parts[0]

            if action == "add":
                cmd = parts[1]
                cmd_name = sanitize_filename(cmd)
                commands[cmd_name] = cmd
                open(os.path.join(log_dir, f"{cmd_name}.log"), "w").close()
                response = f"Команда '{cmd}' добавлена под именем '{cmd_name}'.\n"

            elif action == "run":
                cmd_name = sanitize_filename(parts[1])
                if cmd_name in commands:
                    if not running_commands.get(cmd_name, False):
                        running_commands[cmd_name] = True
                        threading.Thread(target=run_command, args=(cmd_name,), daemon=True).start()
                        response = f"Команда '{cmd_name}' запущена.\n"
                    else:
                        response = f"Команда '{cmd_name}' уже выполняется.\n"
                else:
                    response = f"Команда '{cmd_name}' не найдена.\n"

            elif action == "stop":
                cmd_name = sanitize_filename(parts[1])
                if cmd_name in running_commands:
                    running_commands[cmd_name] = False
                    response = f"Команда '{cmd_name}' остановлена.\n"
                else:
                    response = f"Команда '{cmd_name}' не запущена.\n"

            elif action == "remove":
                cmd_name = sanitize_filename(parts[1])
                if cmd_name in commands:
                    del commands[cmd_name]
                    running_commands[cmd_name] = False
                    log_path = os.path.join(log_dir, f"{cmd_name}.log")
                    if os.path.exists(log_path):
                        os.remove(log_path)
                    response = f"Команда '{cmd_name}' удалена.\n"
                else:
                    response = f"Команда '{cmd_name}' не найдена.\n"

            elif action == "list":
                available = "\n".join(commands.keys()) or "Нет добавленных команд"
                response = f"Сохраненные команды:\n{available}\n"

            elif action == "interval":
                try:
                    new_interval = int(parts[1])
                    interval = new_interval
                    response = f"Интервал изменен на {interval} секунд.\n"
                except:
                    response = "Некорректный интервал. Используйте целое число.\n"

            elif action == "log":
                cmd_name = sanitize_filename(parts[1])
                log_path = os.path.join(log_dir, f"{cmd_name}.log")
                if os.path.exists(log_path):
                    with open(log_path, "r") as log_file:
                        logs = log_file.read()
                    response = logs or "Лог пуст.\n"
                else:
                    response = "Лог-файл не найден.\n"

            elif action == "exit":
                response = "Сервер завершает работу...\n"
                break

            else:
                response = "Неизвестная команда.\n"

            conn.sendall(response.encode())

    except Exception as e:
        print(f"Ошибка клиента: {e}")
    finally:
        conn.close()

def start_server():

    global server_running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 12347))
    server.listen(5)
    print("Сервер запущен...")

    try:
        while server_running:
            conn, addr = server.accept()
            print(f"Подключение от {addr}")
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()
    except KeyboardInterrupt:
        server_running = False
        print("\nСервер завершает работу...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
