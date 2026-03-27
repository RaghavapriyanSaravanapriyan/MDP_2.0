import subprocess
import os
import signal
import sys
import time

def run():
    # Backend
    backend = subprocess.Popen(
        ["./venv/bin/python", "main.py"],
        cwd=os.getcwd()
    )
    
    # Frontend
    frontend = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=os.path.join(os.getcwd(), "frontend")
    )

    print("\n🚀 SentinAI Started!")
    print("Backend: http://localhost:8000")
    print("Frontend: http://localhost:5173")
    print("\nPress Ctrl+C to stop both servers.")

    try:
        while True:
            time.sleep(1)
            if backend.poll() is not None:
                print("Backend stopped.")
                break
            if frontend.poll() is not None:
                print("Frontend stopped.")
                break
    except KeyboardInterrupt:
        print("\nStopping servers...")
        backend.terminate()
        frontend.terminate()
        sys.exit(0)

if __name__ == "__main__":
    run()
