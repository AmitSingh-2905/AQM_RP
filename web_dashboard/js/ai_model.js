class AnomalyDetector {
  constructor(windowSize = 20) {
    this.windowSize = windowSize
    this.history = {
      temperature: [],
      humidity: [],
      light: [],
    }
    // Define expected ranges based on typical sensor values
    this.bounds = {
      temperature: [10.0, 40.0], // Expecting 20-30C usually
      humidity: [20.0, 90.0], // Expecting 40-80% usually
      light: [0, 1024], // 10-bit ADC range
    }
  }

  processPoint(data) {
    // Clone data to avoid modifying original
    let corrected = { ...data }
    let anomalies = {
      temperature: false,
      humidity: false,
      light: false,
    }

    ;["temperature", "humidity", "light"].forEach((key) => {
      if (data[key] === undefined) return

      let val = parseFloat(data[key])
      let isAnomaly = false
      let rectifiedVal = val
      let hist = this.history[key]

      // 1. Physical Range Check
      const [min, max] = this.bounds[key]
      if (val < min || val > max) {
        isAnomaly = true
        // Rectify by clamping or using historical mean
        if (hist.length > 0) {
          const sum = hist.reduce((a, b) => a + b, 0)
          rectifiedVal = sum / hist.length
        } else {
          rectifiedVal = Math.max(min, Math.min(val, max))
        }
      }

      // 2. Statistical Spike Detection (if not already out of bounds)
      if (!isAnomaly && hist.length >= 5) {
        const mean = hist.reduce((a, b) => a + b, 0) / hist.length
        const variance =
          hist.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / hist.length
        const std = Math.sqrt(variance)

        // If we have some variation, check Z-score
        if (std > 0.1) {
          const zScore = Math.abs(val - mean) / std
          if (zScore > 3.0) {
            // 3 Sigma rule
            isAnomaly = true
            rectifiedVal = mean // Replace with mean
          }
        }
      }

      if (isAnomaly) {
        anomalies[key] = true
        corrected[key] = parseFloat(rectifiedVal.toFixed(2)) // Round for display
        // Add the rectified value to history to maintain stability
        hist.push(rectifiedVal)
      } else {
        // Add the valid value to history
        hist.push(val)
      }

      // Maintain window size
      if (hist.length > this.windowSize) {
        hist.shift()
      }
    })

    return { corrected, anomalies }
  }
}
