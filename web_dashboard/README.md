# Secure IoT Dashboard

This is a client-side dashboard to visualize the encrypted and decrypted data from your ESP32.

## How to use

1.  **Upload Firmware**: Make sure you have uploaded the latest code in `src/main.cpp` to your ESP32.
2.  **Start AI Pipeline**:
    *   Open a terminal.
    *   Navigate to the ML pipeline folder: `cd ../ml_pipeline`
    *   Run the setup script: `./run_pipeline.sh`
    *   Keep this terminal open. The server will run on port 8000.
3.  **Get IP Address**: Open the Serial Monitor in PlatformIO (baud rate 115200) and reset your ESP32. Note down the IP address printed (e.g., `192.168.1.105`).
4.  **Open Dashboard**: Double-click `index.html` in this folder to open it in your web browser.
5.  **Connect**: Enter the IP address of your ESP32 in the input field and click "Connect".

## Features

-   **Real-time Charts**: Visualizes Temperature, Humidity, and Light levels.
-   **AI Anomaly Detection**:
    -   Data is processed by a local Python server implementing the AQM pipeline algorithms.
    -   **Raw Data** is shown as a dashed line.
    -   **Corrected Data** is shown as a solid line.
    -   Anomalies (spikes) are detected and automatically corrected in real-time.
-   **Data Inspection**: Shows the raw Encrypted (AES-128) data stream side-by-side with the Decrypted JSON data.
-   **Dark Mode**: Modern UI with a dark theme.

## Troubleshooting

-   **Connection Failed**: Ensure your computer and the ESP32 are on the same WiFi network.
-   **CORS Error**: If you see errors in the browser console about CORS, make sure you uploaded the latest `main.cpp` which includes the `Access-Control-Allow-Origin` header.
