import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Camera, UserCheck, Shield, ShieldAlert, ShieldCheck, RefreshCw, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = "http://localhost:8000";

function App() {
  const [mode, setMode] = useState('training'); // 'training' or 'detection'
  const [name, setName] = useState('');
  const [capturedImages, setCapturedImages] = useState([]);
  const [isCapturing, setIsCapturing] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);
  const [detectionResult, setDetectionResult] = useState(null);
  const [isDetecting, setIsDetecting] = useState(false);
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  // Initialize Camera
  useEffect(() => {
    async function setupCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 1280, height: 720, facingMode: "user" } 
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          streamRef.current = stream;
        }
      } catch (err) {
        console.error("Error accessing camera:", err);
        alert("Camera access denied. Please allow camera permissions.");
      }
    }
    setupCamera();
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  // Capture Image function
  const captureFrame = () => {
    if (!videoRef.current || !canvasRef.current) return null;
    const canvas = canvasRef.current;
    const video = videoRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg', 0.8);
  };

  // Training: Add shot
  const takeShot = () => {
    if (capturedImages.length >= 5) return;
    const img = captureFrame();
    if (img) {
      setCapturedImages(prev => [...prev, img]);
    }
  };

  // Training: Register
  const handleRegister = async () => {
    if (!name || capturedImages.length < 5) return;
    setIsRegistering(true);
    try {
      await axios.post(`${API_BASE}/register`, {
        name,
        images: capturedImages
      });
      alert("Registration Successful!");
      setMode('detection');
    } catch (err) {
      console.error(err);
      alert("Registration failed: " + (err.response?.data?.detail || "Unknown error"));
    } finally {
      setIsRegistering(false);
    }
  };

  // Detection: Continuous Loop
  useEffect(() => {
    let interval;
    if (mode === 'detection' && !isDetecting) {
      interval = setInterval(async () => {
        const img = captureFrame();
        if (img) {
          try {
            const res = await axios.post(`${API_BASE}/detect`, { image: img });
            setDetectionResult(res.data);
          } catch (err) {
            console.error("Detection error:", err);
          }
        }
      }, 1000); // 1-second interval for stability
    }
    return () => clearInterval(interval);
  }, [mode]);

  return (
    <div className="app-container">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card"
      >
        <header className="header">
          <h1>SentinAI</h1>
          <p style={{color: 'var(--text-muted)'}}>Precision Face Access Control</p>
        </header>

        <div className="camera-container">
          <video ref={videoRef} autoPlay playsInline muted />
          <canvas ref={canvasRef} />
          
          <AnimatePresence>
            {mode === 'detection' && (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="scan-line" 
              />
            )}
            
            {detectionResult && mode === 'detection' && (
              <motion.div 
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className={`door-status ${detectionResult.match ? 'status-unlocked' : 'status-locked'}`}
              >
                {detectionResult.match ? <ShieldCheck size={18}/> : <ShieldAlert size={18}/>}
                {detectionResult.match ? "Unlocked" : "Locked"}
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <div className="ui-content">
          <AnimatePresence mode="wait">
            {mode === 'training' ? (
              <motion.div 
                key="training"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
              >
                <div style={{ marginBottom: '1.5rem' }}>
                    <h3 style={{ marginBottom: '0.5rem' }}>User Registration</h3>
                    <input 
                      type="text" 
                      placeholder="Enter Name..." 
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                    />
                </div>
                
                <div style={{ display: 'flex', gap: '8px', justifyContent: 'center', marginBottom: '1rem' }}>
                    {[...Array(5)].map((_, i) => (
                        <div 
                          key={i} 
                          style={{ 
                            width: '50px', 
                            height: '50px', 
                            borderRadius: '8px', 
                            background: capturedImages[i] ? `url(${capturedImages[i]}) center/cover` : 'rgba(255,255,255,0.05)',
                            border: '1px solid var(--glass-border)'
                          }} 
                        />
                    ))}
                </div>

                <div className="controls">
                  <button onClick={takeShot} disabled={capturedImages.length >= 5}>
                    <Camera size={20} />
                    {capturedImages.length < 5 ? `Capture (${capturedImages.length}/5)` : 'Ready'}
                  </button>
                  
                  <button 
                    onClick={handleRegister} 
                    className="secondary" 
                    disabled={capturedImages.length < 5 || !name || isRegistering}
                  >
                    {isRegistering ? <Loader2 className="spinner" size={20}/> : <UserCheck size={20} />}
                    Continue
                  </button>
                </div>
              </motion.div>
            ) : (
              <motion.div 
                key="detection"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                 <div style={{ marginBottom: '1.5rem' }}>
                    <h3 style={{ marginBottom: '0.5rem', color: detectionResult?.match ? 'var(--success)' : 'white' }}>
                        {detectionResult?.match ? `Welcome Back, ${detectionResult.name}` : 'Awaiting Detection...'}
                    </h3>
                    <p style={{ color: 'var(--text-muted)' }}>
                        {detectionResult?.status || 'System Active'}
                    </p>
                </div>

                <div className="controls">
                    <button onClick={() => { setMode('training'); setCapturedImages([]); setName(''); setDetectionResult(null); }} className="secondary">
                        <RefreshCw size={20} />
                        New Training
                    </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </div>
  );
}

export default App;
