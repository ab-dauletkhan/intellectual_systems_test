import subprocess
import time
# import signal

def run_server():
    return subprocess.Popen(["python", "server.py"])

def run_client():
    return subprocess.Popen(["python", "client.py"])

def terminate_processes(processes):
    for process in processes:
        process.terminate()
    for process in processes:
        process.wait()

if __name__ == "__main__":
    server_process = run_server()
    time.sleep(1)

    client1_process = run_client()
    client2_process = run_client()

    processes = [server_process, client1_process, client2_process]

    try:
        while True:
            for process in processes:
                if process.poll() is not None:
                    processes.remove(process)
            if not processes:
                break
            time.sleep(1)
    except KeyboardInterrupt:
        terminate_processes(processes)
