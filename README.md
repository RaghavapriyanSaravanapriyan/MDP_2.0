# SentinAI: High-Accuracy Face Access Control

SentinAI is a full-stack deep learning project that identifies individuals from a live camera feed. This system is designed for high accuracy and minimal false positives, suitable for securing a "smart door".

## Key Features

- **High Accuracy (Facenet512)**: Uses the state-of-the-art Facenet512 model for generating robust face embeddings.
- **Strict Verification**: Employs conservative distance thresholding to eliminate false positives.
- **Multi-Shot Training**: Captures 5 distinct frames during registration to build a robust profile for each user.
- **Premium UI**: A glassmorphic, dark-mode interface with real-time feedback and smooth animations.
- **Door Control Simulation**: Visual "Locked" and "Unlocked" states based on authorization.

## How to Run

1.  **Dependencies**: I have already set up a virtual environment and installed all necessary Python and Node.js packages.
2.  **Start the System**:
    Run the following command in the project root:
    ```bash
    python3 start.py
    ```
3.  **Access the Interface**:
    - Frontend: [http://localhost:5173](http://localhost:5173)
    - Backend API: [http://localhost:8000](http://localhost:8000)

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

## Verification Status

- ✅ **Face Detection**: Reliable detection via OpenCV backend.
- ✅ **Face Recognition**: Facenet512 provides high-dimensional embeddings for precise matching.
- ✅ **Database**: SQLite correctly stores and retrieves user profiles.
- ✅ **Real-time Performance**: Optimized polling for smooth camera feed and low-latency detection.

---
> [!IMPORTANT]
> Ensure your room is well-lit for maximum accuracy during both training and detection.
