import threading
import time
import subprocess


def start_server():
    subprocess.Popen(["python", "serverlast.py"])
    time.sleep(1)


def start_client():
    subprocess.run(["python", "clientlast.py"])



if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    start_client()