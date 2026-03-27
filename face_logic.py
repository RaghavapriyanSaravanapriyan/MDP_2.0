import numpy as np
import cv2
from deepface import DeepFace
import base64
from typing import List, Optional

# Constants for high accuracy
MODEL_NAME = "Facenet512"
DETECTOR_BACKEND = "opencv" # opencv is fast, but yunet or retinaface are more accurate. 
# Given the user's request for accuracy, I'll try to use retinaface if available, but opencv is a safe fallback.
# For now, let's use the default "opencv" or "retinaface" if it works.

def get_embedding(image_data: str) -> Optional[List[float]]:
    """
    Decodes base64 image data and returns the face embedding using Facenet512.
    """
    try:
        # Decode base64
        decoded_data = base64.b64decode(image_data.split(",")[1])
        nparr = np.frombuffer(decoded_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Generate embedding
        objs = DeepFace.represent(
            img_path=img, 
            model_name=MODEL_NAME, 
            detector_backend=DETECTOR_BACKEND,
            enforce_detection=True
        )
        
        if objs:
            return objs[0]["embedding"]
        return None
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def verify_face(current_embedding: List[float], stored_embeddings: List[List[float]], threshold: float = 0.3) -> bool:
    """
    Compares current embedding against a list of stored embeddings for a user.
    Uses Euclidean distance (Facenet512 default threshold is ~0.4, but we use a stricter ~0.3).
    """
    if not current_embedding or not stored_embeddings:
        return False
    
    current_arr = np.array(current_embedding)
    
    for stored in stored_embeddings:
        stored_arr = np.array(stored)
        dist = np.linalg.norm(current_arr - stored_arr)
        if dist < threshold:
            return True
    return False

def find_match(current_embedding: List[float], users: List[dict], threshold: float = 0.3) -> Optional[str]:
    """
    Finds the user whose embedding matches the current one.
    """
    best_dist = float('inf')
    best_match = None
    
    current_arr = np.array(current_embedding)
    
    for user in users:
        # user["embeddings"] is a list of stored embeddings
        for stored in user["embeddings"]:
            stored_arr = np.array(stored)
            dist = np.linalg.norm(current_arr - stored_arr)
            if dist < threshold and dist < best_dist:
                best_dist = dist
                best_match = user["name"]
                
    return best_match
