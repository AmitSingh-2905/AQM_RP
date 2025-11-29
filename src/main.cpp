#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <mbedtls/aes.h>
#include <mbedtls/base64.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "Amits24";
const char* password = "abcd1729";

// MQTT Broker settings
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "encryption_tls/data"; // Unique topic

WiFiClient espClient;
PubSubClient client(espClient);

// Web server on port 80
WebServer server(80);

// AES-128 encryption key (16 bytes)
const unsigned char aes_key[16] = {
  0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
  0xab, 0xf7, 0x97, 0x75, 0x46, 0x89, 0x45, 0x31
};

// Storage for sensor data
struct SensorData {
  float temperature;
  float humidity;
  int lightLevel;
  unsigned long timestamp;
  String encryptedData;
  String decryptedData;
};

SensorData latestData;
int dataCounter = 0;

// Function to pad data to multiple of 16 bytes (AES block size)
String padData(String data) {
  int padding = 16 - (data.length() % 16);
  for (int i = 0; i < padding; i++) {
    data += char(padding);
  }
  return data;
}

// Function to remove padding
String removePadding(String data) {
  if (data.length() == 0) return data;
  int padding = data.charAt(data.length() - 1);
  if (padding > 0 && padding <= 16) {
    return data.substring(0, data.length() - padding);
  }
  return data;
}

// Function to encrypt data using AES-128
String encryptData(String plaintext) {
  String padded = padData(plaintext);
  
  unsigned char output[256];
  mbedtls_aes_context aes;
  
  mbedtls_aes_init(&aes);
  mbedtls_aes_setkey_enc(&aes, aes_key, 128);
  
  // Encrypt each 16-byte block
  for (size_t i = 0; i < padded.length(); i += 16) {
    mbedtls_aes_crypt_ecb(&aes, MBEDTLS_AES_ENCRYPT,
                          (const unsigned char*)padded.c_str() + i,
                          output + i);
  }
  
  mbedtls_aes_free(&aes);
  
  // Convert to base64
  unsigned char base64_output[512];
  size_t olen;
  mbedtls_base64_encode(base64_output, sizeof(base64_output), &olen,
                        output, padded.length());
  
  return String((char*)base64_output);
}

// Function to decrypt data using AES-128
String decryptData(String ciphertext) {
  // Decode from base64
  unsigned char decoded[256];
  size_t decoded_len;
  mbedtls_base64_decode(decoded, sizeof(decoded), &decoded_len,
                        (const unsigned char*)ciphertext.c_str(),
                        ciphertext.length());
  
  unsigned char output[256];
  mbedtls_aes_context aes;
  
  mbedtls_aes_init(&aes);
  mbedtls_aes_setkey_dec(&aes, aes_key, 128);
  
  // Decrypt each 16-byte block
  for (size_t i = 0; i < decoded_len; i += 16) {
    mbedtls_aes_crypt_ecb(&aes, MBEDTLS_AES_DECRYPT,
                          decoded + i, output + i);
  }
  
  mbedtls_aes_free(&aes);
  
  String result = String((char*)output);
  return removePadding(result);
}

// Function to generate simulated sensor data
void generateSensorData() {
  // Normal data generation
  latestData.temperature = 20.0 + random(0, 100) / 10.0;
  latestData.humidity = 40.0 + random(0, 400) / 10.0;
  latestData.lightLevel = random(0, 1024);

  // Introduce Anomalies (30% chance for demonstration)
  if (random(0, 100) < 30) {
    Serial.println("!!! INJECTING ANOMALY !!!");
    int type = random(0, 3);
    if (type == 0) {
      // Temperature Spike (Extreme heat or cold)
      latestData.temperature = (random(0, 2) == 0) ? 85.5 : -15.0;
    } else if (type == 1) {
      // Humidity Spike (Impossible values)
      latestData.humidity = (random(0, 2) == 0) ? 120.0 : 5.0;
    } else {
      // Light Spike (Out of 10-bit ADC range)
      latestData.lightLevel = 2000; 
    }
  }

  latestData.timestamp = millis();
  
  // Create JSON string
  String jsonData = "{";
  jsonData += "\"counter\":" + String(dataCounter++) + ",";
  jsonData += "\"temperature\":" + String(latestData.temperature, 1) + ",";
  jsonData += "\"humidity\":" + String(latestData.humidity, 1) + ",";
  jsonData += "\"light\":" + String(latestData.lightLevel) + ",";
  jsonData += "\"timestamp\":" + String(latestData.timestamp);
  jsonData += "}";
  
  latestData.decryptedData = jsonData;
  latestData.encryptedData = encryptData(jsonData);
  
  Serial.println("\n=== New Data Generated ===");
  Serial.println("Decrypted: " + latestData.decryptedData);
  Serial.println("Encrypted: " + latestData.encryptedData);
}

// HTML page with encrypted and decrypted data display
// String getWebPage() {
//   String html = "<!DOCTYPE html><html><head>";
//   html += "<meta name='viewport' content='width=device-width, initial-scale=1'>";
//   html += "<meta charset='UTF-8'>";
//   html += "<title>ESP32 Encrypted Data Monitor</title>";
//   html += "<style>";
//   html += "body { font-family: Arial, sans-serif; margin: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }";
//   html += ".container { max-width: 900px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); }";
//   html += "h1 { text-align: center; margin-bottom: 10px; }";
//   html += ".subtitle { text-align: center; margin-bottom: 30px; font-size: 14px; opacity: 0.8; }";
//   html += ".card { background: rgba(255,255,255,0.2); padding: 20px; margin: 20px 0; border-radius: 10px; border: 1px solid rgba(255,255,255,0.3); }";
//   html += ".card h2 { margin-top: 0; color: #fff; border-bottom: 2px solid rgba(255,255,255,0.3); padding-bottom: 10px; }";
//   html += ".data-item { margin: 10px 0; padding: 10px; background: rgba(0,0,0,0.2); border-radius: 5px; }";
//   html += ".data-label { font-weight: bold; color: #ffd700; }";
//   html += ".encrypted { font-family: monospace; word-break: break-all; background: rgba(255,0,0,0.2); padding: 15px; border-radius: 5px; border-left: 4px solid #ff6b6b; }";
//   html += ".decrypted { font-family: monospace; word-break: break-all; background: rgba(0,255,0,0.2); padding: 15px; border-radius: 5px; border-left: 4px solid #51cf66; }";
//   html += ".stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }";
//   html += ".stat-box { background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px; text-align: center; }";
//   html += ".stat-value { font-size: 32px; font-weight: bold; color: #ffd700; }";
//   html += ".stat-label { font-size: 14px; margin-top: 5px; opacity: 0.9; }";
//   html += ".encryption-info { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #4dabf7; }";
//   html += ".refresh-btn { background: #4dabf7; color: white; border: none; padding: 12px 30px; border-radius: 25px; cursor: pointer; font-size: 16px; margin: 20px auto; display: block; }";
//   html += "</style>";
//   html += "<script>";
//   html += "function autoRefresh() { location.reload(); }";
//   html += "setInterval(autoRefresh, 5000);";
//   html += "</script>";
//   html += "</head><body>";
  
//   html += "<div class='container'>";
//   html += "<h1>🔐 ESP32 Encrypted Data Monitor</h1>";
//   html += "<div class='subtitle'>Real-time sensor data with AES-128 encryption</div>";
  
//   html += "<div class='encryption-info'>";
//   html += "<strong>🔒 Security Features:</strong><br>";
//   html += "• AES-128 Encryption<br>";
//   html += "• Secure WiFi transmission<br>";
//   html += "• Auto-refresh every 5 seconds";
//   html += "</div>";
  
//   html += "<div class='stats'>";
//   html += "<div class='stat-box'>";
//   html += "<div class='stat-value'>" + String(latestData.temperature, 1) + "°C</div>";
//   html += "<div class='stat-label'>Temperature</div>";
//   html += "</div>";
//   html += "<div class='stat-box'>";
//   html += "<div class='stat-value'>" + String(latestData.humidity, 1) + "%</div>";
//   html += "<div class='stat-label'>Humidity</div>";
//   html += "</div>";
//   html += "<div class='stat-box'>";
//   html += "<div class='stat-value'>" + String(latestData.lightLevel) + "</div>";
//   html += "<div class='stat-label'>Light Level</div>";
//   html += "</div>";
//   html += "</div>";
  
//   html += "<div class='card'>";
//   html += "<h2>🔒 Encrypted Data (AES-128)</h2>";
//   html += "<div class='encrypted'>" + latestData.encryptedData + "</div>";
//   html += "</div>";
  
//   html += "<div class='card'>";
//   html += "<h2>🔓 Decrypted Data (Plain JSON)</h2>";
//   html += "<div class='decrypted'>" + latestData.decryptedData + "</div>";
//   html += "</div>";
  
//   html += "<div class='card'>";
//   html += "<h2>📊 Data Details</h2>";
//   html += "<div class='data-item'><span class='data-label'>Sample Count:</span> " + String(dataCounter) + "</div>";
//   html += "<div class='data-item'><span class='data-label'>Timestamp:</span> " + String(latestData.timestamp) + " ms</div>";
//   html += "<div class='data-item'><span class='data-label'>Encrypted Size:</span> " + String(latestData.encryptedData.length()) + " bytes</div>";
//   html += "<div class='data-item'><span class='data-label'>Decrypted Size:</span> " + String(latestData.decryptedData.length()) + " bytes</div>";
//   html += "<div class='data-item'><span class='data-label'>ESP32 IP:</span> " + WiFi.localIP().toString() + "</div>";
//   html += "</div>";
  
//   html += "<button class='refresh-btn' onclick='location.reload()'>🔄 Refresh Now</button>";
  
//   html += "</div>";
//   html += "</body></html>";
  
//   return html;
// }

// Handle root page request
void handleRoot() {
  generateSensorData();
  server.send(200, "text/html", getWebPage());
}

// Handle API endpoint
void handleAPI() {
  server.sendHeader("Access-Control-Allow-Origin", "*");
  String json = "{";
  json += "\"encrypted\":\"" + latestData.encryptedData + "\",";
  json += "\"decrypted\":" + latestData.decryptedData;
  json += "}";
  server.send(200, "application/json", json);
}

void handleNotFound() {
  server.send(404, "text/plain", "404: Not Found");
}

void reconnectMQTT() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n========================================");
  Serial.println("ESP32 Encrypted Data Platform");
  Serial.println("========================================");
  
  Serial.println("\nConnecting to WiFi...");
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✓ WiFi Connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n✗ Failed to connect");
    ESP.restart();
  }

  client.setServer(mqtt_server, mqtt_port);
  client.setBufferSize(512); // Increase buffer size for large JSON packets
  
  server.on("/", handleRoot);
  server.on("/api", handleAPI);
  server.onNotFound(handleNotFound);
  
  server.begin();
  
  generateSensorData();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    ESP.restart();
  }
  
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();
  server.handleClient();
  
  static unsigned long lastUpdate = 0;
  if (millis() - lastUpdate > 3000) {
    generateSensorData();
    
    // Publish to MQTT
    String json = "{";
    json += "\"encrypted\":\"" + latestData.encryptedData + "\",";
    json += "\"decrypted\":" + latestData.decryptedData;
    json += "}";
    
    if (client.publish(mqtt_topic, json.c_str())) {
      Serial.println("Published to MQTT: " + String(mqtt_topic));
    } else {
      Serial.println("MQTT Publish Failed! (Check buffer size or connection)");
    }
    
    lastUpdate = millis();
  }
}

// void loop() {
//   if (WiFi.status() == WL_CONNECTED) {
//     Serial.println("\n✓ WiFi Connected!");
//     Serial.print("IP Address: ");
//     Serial.println(WiFi.localIP());
//     Serial.print("Signal Strength: ");
//     Serial.print(WiFi.RSSI());
//     Serial.println(" dBm");
//   } else {
//     Serial.println("\n✗ Failed to connect");
//     ESP.restart();
//   }
//   delay(2000);
//   server.handleClient();
  
//   static unsigned long lastUpdate = 0;
//   if (millis() - lastUpdate > 3000) {
//     generateSensorData();
//     lastUpdate = millis();
//   }
// }