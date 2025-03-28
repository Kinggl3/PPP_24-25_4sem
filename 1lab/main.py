import threading
import time
import subprocess


def start_server():
    subprocess.Popen(["python", "server7.py"])
    time.sleep(1)


def start_client():
    subprocess.run(["python", "client7.py"])


if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    start_client()
