import subprocess
import os
import signal
import sys
import time

def run():
    # Detect OS to select the correct python path and npm command
    if sys.platform == "win32":
        python_executable = os.path.join("venv", "Scripts", "python.exe")
        npm_command = "npm.cmd"
    else:
        python_executable = os.path.join("venv", "bin", "python")
        npm_command = "npm"

    # Backend
    print(f"Starting Backend with {python_executable}...")
    try:
        backend = subprocess.Popen(
            [python_executable, "main.py"],
            cwd=os.getcwd()
        )
    except FileNotFoundError:
        print(f"❌ Error: Could not find {python_executable}. Did you create the virtual environment?")
        sys.exit(1)
    
    # Frontend
    print(f"Starting Frontend with {npm_command}...")
    try:
        frontend = subprocess.Popen(
            [npm_command, "run", "dev"],
            cwd=os.path.join(os.getcwd(), "frontend")
        )
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{npm_command}'. Is Node.js installed?")
        backend.terminate()
        sys.exit(1)

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
