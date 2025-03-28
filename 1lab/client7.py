import socket

def main():
    host = "localhost"
    port = 12345

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print("Подключение к серверу...")
            sock.connect((host, port))
            print("Подключено!")

            while True:
                print("\n1. Добавить команду")
                print("2. Запустить команду")
                print("3. Остановить команду")
                print("4. Удалить команду")
                print("5. Просмотреть список команд")
                print("6. Изменить интервал (секунды)")
                print("7. Получить лог-файл")
                print("8. Выйти")

                choice = input("Выберите действие: ").strip()

                if choice == "1":
                    command = input("Введите команду (например, echo 'Hello'): ").strip()
                    sock.sendall(f"add {command}".encode())
                elif choice == "2":
                    cmd_name = input("Введите имя команды: ").strip()
                    sock.sendall(f"run {cmd_name}".encode())
                elif choice == "3":
                    cmd_name = input("Введите имя команды для остановки: ").strip()
                    sock.sendall(f"stop {cmd_name}".encode())
                elif choice == "4":
                    cmd_name = input("Введите имя команды для удаления: ").strip()
                    sock.sendall(f"remove {cmd_name}".encode())
                elif choice == "5":
                    sock.sendall("list".encode())
                elif choice == "6":
                    new_interval = input("Введите новый интервал (секунды): ").strip()
                    sock.sendall(f"interval {new_interval}".encode())
                elif choice == "7":
                    cmd_name = input("Введите имя команды для получения лога: ").strip()
                    sock.sendall(f"log {cmd_name}".encode())
                elif choice == "8":
                    sock.sendall("exit".encode())
                    print("Завершение работы клиента.")
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
                    continue

                # Ожидание ответа от сервера
                response = sock.recv(4096).decode()
                print("Ответ от сервера:", response)

    except Exception as e:
        print("Ошибка:", e)

if __name__ == "__main__":
    main()



