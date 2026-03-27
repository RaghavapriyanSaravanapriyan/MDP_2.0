# SentinAI: High-Accuracy Face Access Control

SentinAI is a full-stack deep learning project that identifies individuals from a live camera feed. This version is **Python-only** and does not require Node.js or npm.

## Windows One-Click Setup

1.  **Clone/Copy the project** to your local machine.
2.  **Run the Setup Script**:
    ```powershell
    python setup.py
    ```
    This will automatically create a virtual environment and install all necessary dependencies.

## How to Run

After setup, run the following command in the project root:
```powershell
python start.py
```

## Access the Interface
- UI & API: [http://localhost:8000](http://localhost:8000)

## Usage Instructions

### 1. Training Phase
1.  Enter the name of the person to be authorized.
2.  Click the **Capture** button 5 times to take different angles/expressions.
3.  Click **Continue** to process and save the training data.

### 2. Detection Phase
1.  The system will automatically switch to detection mode.
2.  Face the camera.
3.  If you are the authorized person, the system will display **"Unlocked"** and show your name.
4.  If an unauthorized person is detected, the system will display **"Locked"**.

## Key Features

- **High Accuracy (Facenet512)**: Uses the state-of-the-art Facenet512 model.
- **No Node.js Required**: The frontend is a single-file React/Tailwind implementation served directly via FastAPI.
- **Elite UI**: Glassmorphic, dark-mode interface with real-time feedback and smooth animations.
- **Bio-Access Logic**: Secure threshold-based verification for elite security.

---
> [!IMPORTANT]
> Ensure your room is well-lit for maximum accuracy during both training and detection.
