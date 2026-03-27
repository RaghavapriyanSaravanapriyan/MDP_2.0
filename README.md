# SentinAI: High-Accuracy Face Access Control

SentinAI is a full-stack deep learning project that identifies individuals from a live camera feed. This system is designed for high accuracy and minimal false positives, suitable for securing a "smart door".

## Windows Setup (Powershell/CMD)

1.  **Clone/Copy the project** to your local machine.
2.  **Initialize Virtual Environment**:
    ```powershell
    python -m venv venv
    ```
3.  **Install Backend Dependencies**:
    ```powershell
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```
4.  **Install Frontend Dependencies**:
    ```powershell
    cd frontend
    npm install
    cd ..
    ```

## How to Run

Run the following command in the project root:
```powershell
python start.py
```

## Access the Interface
- Frontend: [http://localhost:5173](http://localhost:5173) (User interface)
- Backend API: [http://localhost:8000](http://localhost:8000) (Automation API)

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
- **Strict Verification**: Employs conservative distance thresholding.
- **Multi-Shot Training**: Captures 5 distinct frames during registration.
- **Premium UI**: Glassmorphic, dark-mode interface with real-time feedback.

---
> [!IMPORTANT]
> Ensure your room is well-lit for maximum accuracy during both training and detection.
