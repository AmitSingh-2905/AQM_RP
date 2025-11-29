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

  // --- Expert 1: Moving Average (MA) ---
  // Predicts based on the average of the window.
  // Returns { isAnomaly: bool, prediction: float }
  runMovingAverage(val, hist) {
    if (hist.length < 5) return { isAnomaly: false, prediction: val }

    const mean = hist.reduce((a, b) => a + b, 0) / hist.length
    const variance =
      hist.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / hist.length
    const std = Math.sqrt(variance)

    // Z-Score Check
    const zScore = std > 0 ? Math.abs(val - mean) / std : 0
    const isAnomaly = zScore > 2.5 // Reduced from 3.0 to 2.5 for higher sensitivity

    return { isAnomaly, prediction: mean }
  }

  // --- Expert 2: Auto Regression (AR) ---
  // Uses Linear Regression as a proxy for AR trend prediction.
  // Returns { isAnomaly: bool, prediction: float }
  runAutoRegression(val, hist) {
    if (hist.length < 5) return { isAnomaly: false, prediction: val }

    const n = hist.length
    let sumX = 0,
      sumY = 0,
      sumXY = 0,
      sumXX = 0
    for (let i = 0; i < n; i++) {
      sumX += i
      sumY += hist[i]
      sumXY += i * hist[i]
      sumXX += i * i
    }

    const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX)
    const intercept = (sumY - slope * sumX) / n
    const predicted = slope * n + intercept

    // Dynamic threshold based on recent volatility
    const mean = hist.reduce((a, b) => a + b, 0) / n
    const std = Math.sqrt(
      hist.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / n
    )
    // Reduced threshold multiplier from 3 to 2.5, and min threshold from 2.0 to 1.5
    const threshold = Math.max(std * 2.5, 1.5)

    const isAnomaly = Math.abs(val - predicted) > threshold

    return { isAnomaly, prediction: predicted }
  }

  // --- Expert 3: Random Forest (Simplified Ensemble of Trees) ---
  // Simulates a Random Forest by running multiple "Decision Trees" (Heuristics)
  // Returns { isAnomaly: bool, prediction: float }
  runRandomForest(val, hist, bounds) {
    if (hist.length < 2) return { isAnomaly: false, prediction: val }

    const last = hist[hist.length - 1]
    const diff = Math.abs(val - last)
    const [min, max] = bounds

    // Tree 1: Physical Bounds Check
    const vote1 = val < min || val > max ? 1 : 0

    // Tree 2: Sudden Spike Check (Velocity)
    // If jump is > 15% of the range (reduced from 20%)
    const range = max - min
    const vote2 = diff > range * 0.15 ? 1 : 0

    // Tree 3: Contextual Deviation (Distance from median)
    // Quick median calculation
    const sorted = [...hist].sort((a, b) => a - b)
    const median = sorted[Math.floor(sorted.length / 2)]
    const distMedian = Math.abs(val - median)
    // Reduced from 30% to 20%
    const vote3 = distMedian > range * 0.2 ? 1 : 0

    // Forest Vote
    const votes = vote1 + vote2 + vote3
    const isAnomaly = votes >= 1 // Relaxed: If ANY tree flags it (or at least 1), consider it a vote.
    // Actually, let's keep it at 2 for robustness, but the inputs are more sensitive.
    // Or better: if vote1 (Bounds) is true, it's definitely an anomaly.
    // If vote2 OR vote3 is true, it's suspicious.
    // Let's stick to the previous logic but with the tighter thresholds above.
    const isAnomalyFinal = votes >= 2

    // RF Prediction is usually the average of leaf nodes, here we use median of history
    return { isAnomaly: isAnomalyFinal, prediction: median }
  }

  processPoint(data) {
    let corrected = { ...data }
    let anomalies = {
      temperature: false,
      humidity: false,
      light: false,
    }

    ;["temperature", "humidity", "light"].forEach((key) => {
      if (data[key] === undefined) return

      let val = parseFloat(data[key])
      let hist = this.history[key]

      // 1. Get opinions from all 3 experts
      const ma = this.runMovingAverage(val, hist)
      const ar = this.runAutoRegression(val, hist)
      const rf = this.runRandomForest(val, hist, this.bounds[key])

      // 2. Democratic Voting (Majority Rule)
      let anomalyVotes = 0
      if (ma.isAnomaly) anomalyVotes++
      if (ar.isAnomaly) anomalyVotes++
      if (rf.isAnomaly) anomalyVotes++

      const isAnomaly = anomalyVotes >= 2 // At least 2 out of 3 must agree

      let rectifiedVal = val

      if (isAnomaly) {
        anomalies[key] = true

        // 3. Ensemble Rectification
        // Weighted average of the predictions from the "smartest" models (AR and MA)
        // We trust AR (Trend) slightly more than MA (Mean) for time-series
        rectifiedVal = ar.prediction * 0.6 + ma.prediction * 0.4

        // Add rectified value to history to keep stability
        hist.push(rectifiedVal)
      } else {
        hist.push(val)
      }

      corrected[key] = parseFloat(rectifiedVal.toFixed(2))

      if (hist.length > this.windowSize) {
        hist.shift()
      }
    })

    return { corrected, anomalies }
  }
}
