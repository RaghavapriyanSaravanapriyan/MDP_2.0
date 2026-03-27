import subprocess
import os
import sys

def run_command(command, cwd=None):
    print(f"Executing: {command}")
    try:
        subprocess.check_call(command, shell=True, cwd=cwd)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False

def setup():
    print("--- SentinAI Windows Setup ---")
    
    # 1. Create venv
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        if not run_command("python -m venv venv"):
            print("Failed to create virtual environment. Ensure Python is installed.")
            return
    else:
        print("Virtual environment already exists.")

    # 2. Determine pip path
    pip_executable = os.path.join("venv", "Scripts", "pip.exe")
    if not os.path.exists(pip_executable):
        # Fallback for Linux/macOS if run there accidentally
        pip_executable = os.path.join("venv", "bin", "pip")

    # 3. Install requirements
    if os.path.exists("requirements.txt"):
        print("Installing backend dependencies...")
        if not run_command(f"{pip_executable} install -r requirements.txt"):
            print("Failed to install dependencies.")
            return
    else:
        print("requirements.txt not found. Skipping dependency installation.")

    print("\n✅ Setup Complete!")
    print("\nTo start the project, run:")
    print("python start.py")
    print("\nAccess the UI at: http://localhost:8000")

if __name__ == "__main__":
    setup()
