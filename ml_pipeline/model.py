import numpy as np
from collections import deque

class AnomalyDetector:
    def __init__(self, window_size=20):
        self.window_size = window_size
        self.history = {
            'temperature': deque(maxlen=window_size),
            'humidity': deque(maxlen=window_size),
            'light': deque(maxlen=window_size)
        }
        # Define expected ranges based on typical sensor values
        # Adjust these based on your specific environment
        self.bounds = {
            'temperature': (10.0, 40.0),  # Expecting 20-30C usually
            'humidity': (20.0, 90.0),     # Expecting 40-80% usually
            'light': (0, 1024)            # 10-bit ADC range
        }

    def process_point(self, data):
        """
        Process a single data point: detect anomalies and rectify them.
        """
        corrected = data.copy()
        anomalies = {
            'temperature': False,
            'humidity': False,
            'light': False
        }

        for key in ['temperature', 'humidity', 'light']:
            if key not in data:
                continue
                
            val = float(data[key])
            is_anomaly = False
            rectified_val = val

            # 1. Physical Range Check
            min_val, max_val = self.bounds[key]
            if val < min_val or val > max_val:
                is_anomaly = True
                # Rectify by clamping or using historical mean
                if len(self.history[key]) > 0:
                    rectified_val = float(np.mean(self.history[key]))
                else:
                    rectified_val = max(min_val, min(val, max_val))

            # 2. Statistical Spike Detection (if not already out of bounds)
            if not is_anomaly and len(self.history[key]) >= 5:
                history_arr = np.array(self.history[key])
                mean = np.mean(history_arr)
                std = np.std(history_arr)
                
                # If we have some variation, check Z-score
                if std > 0.1: 
                    z_score = abs(val - mean) / std
                    if z_score > 3.0: # 3 Sigma rule
                        is_anomaly = True
                        rectified_val = float(mean) # Replace with mean
            
            if is_anomaly:
                anomalies[key] = True
                corrected[key] = float(f"{rectified_val:.2f}") # Round for display
                # Add the rectified value to history to maintain stability
                self.history[key].append(rectified_val)
            else:
                # Add the valid value to history
                self.history[key].append(val)

        # Convert numpy bools to standard Python bools for JSON serialization
        # Also ensure corrected values are standard floats, not numpy floats
        anomalies = {k: bool(v) for k, v in anomalies.items()}
        corrected = {k: float(v) if isinstance(v, (np.float32, np.float64)) else v for k, v in corrected.items()}

        return corrected, anomalies
