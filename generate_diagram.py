import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_professional_diagram():
    # Create figure with white background
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor('white')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Helper for boxes with shadow effect
    def add_box(x, y, w, h, text, color='#ffffff', edge='#000000', fontsize=10):
        # Shadow
        shadow = patches.FancyBboxPatch((x+0.08, y-0.08), w, h, boxstyle="round,pad=0.1", fc='#dddddd', ec='none', zorder=1)
        ax.add_patch(shadow)
        # Box
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", fc=color, ec=edge, lw=2, zorder=2)
        ax.add_patch(box)
        # Text
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fontsize, fontweight='bold', zorder=3, color='#333333')

    # --- 1. Secure Sensor Node (Left Column) ---
    # Container
    ax.add_patch(patches.Rectangle((0.5, 1.0), 3.5, 6.5, fill=False, edgecolor='#555555', linestyle='--', lw=2))
    ax.text(2.25, 7.7, "Secure Sensor Node\n(ESP32 Firmware)", ha='center', fontsize=13, fontweight='bold', color='#333333')

    # Components (Top to Bottom)
    add_box(1, 6.0, 2.5, 0.8, "Data Acquisition\n(Sensors + Noise)", color='#e3f2fd', edge='#1565c0')
    
    # Arrow Down
    ax.arrow(2.25, 6.0, 0, -0.5, head_width=0.15, head_length=0.15, fc='#333333', ec='#333333', zorder=4, lw=1.5)
    
    add_box(1, 4.5, 2.5, 0.8, "AES-128 Encryption\n(mbedtls / ECB)", color='#e8f5e9', edge='#2e7d32')
    
    # Arrow Down
    ax.arrow(2.25, 4.5, 0, -0.5, head_width=0.15, head_length=0.15, fc='#333333', ec='#333333', zorder=4, lw=1.5)
    
    add_box(1, 3.0, 2.5, 0.8, "MQTT Client\n(PubSubClient)", color='#fff3e0', edge='#ef6c00')

    # --- 2. Transport Layer (Bottom Middle) ---
    # Arrow Right from Node to Broker
    ax.arrow(3.6, 3.4, 1.3, 0, head_width=0.15, head_length=0.15, fc='#333333', ec='#333333', zorder=4, lw=1.5)
    ax.text(4.25, 3.6, "Publish\n(Encrypted)", ha='center', fontsize=9, fontstyle='italic')

    # Broker Box
    add_box(5.0, 3.0, 4.0, 0.8, "MQTT Broker (HiveMQ)\nOver Secure WebSockets (WSS)", color='#f3e5f5', edge='#7b1fa2')

    # Arrow Right from Broker to Browser
    ax.arrow(9.1, 3.4, 1.3, 0, head_width=0.15, head_length=0.15, fc='#333333', ec='#333333', zorder=4, lw=1.5)
    ax.text(9.75, 3.6, "Subscribe\n(WSS Port 8884)", ha='center', fontsize=9, fontstyle='italic')

    # --- 3. Web Dashboard (Right Column) ---
    # Container
    ax.add_patch(patches.Rectangle((10.5, 1.0), 3.0, 6.5, fill=False, edgecolor='#555555', linestyle='--', lw=2))
    ax.text(12.0, 7.7, "Intelligent Dashboard\n(Browser / JS)", ha='center', fontsize=13, fontweight='bold', color='#333333')

    # Components (Bottom to Top - Processing Pipeline)
    # 1. Decrypt (Receives Data)
    add_box(10.75, 3.0, 2.5, 0.8, "Decryption\n(CryptoJS)", color='#e8f5e9', edge='#2e7d32')
    
    # Arrow Up
    ax.arrow(12.0, 3.9, 0, 0.5, head_width=0.15, head_length=0.15, fc='#333333', ec='#333333', zorder=4, lw=1.5)
    
    # 2. AI
    add_box(10.75, 4.5, 2.5, 0.8, "Edge AI Pipeline\n(Z-Score & Clamping)", color='#ffebee', edge='#c62828')
    
    # Arrow Up
    ax.arrow(12.0, 5.4, 0, 0.5, head_width=0.15, head_length=0.15, fc='#333333', ec='#333333', zorder=4, lw=1.5)
    
    # 3. Vis
    add_box(10.75, 6.0, 2.5, 0.8, "Visualization\n(Chart.js)", color='#e3f2fd', edge='#1565c0')

    # --- Legend / Specs Box ---
    specs_text = (
        "SYSTEM SPECIFICATIONS\n"
        "-----------------------------------\n"
        "• Microcontroller: ESP32 (240MHz Dual Core)\n"
        "• Cryptography: AES-128 ECB (128-bit Key)\n"
        "• Transport: MQTT 3.1.1 over WSS (TLS 1.2)\n"
        "• Anomaly Detection: Z-Score > 3σ (Client-Side)"
    )
    ax.text(7, 0.8, specs_text, ha='center', va='center', fontsize=10, family='monospace',
            bbox=dict(boxstyle="round,pad=0.8", fc="#f5f5f5", ec="#999999", lw=1))

    plt.tight_layout()
    plt.savefig('system_block_diagram.png', dpi=300, bbox_inches='tight')
    print("Professional diagram generated: system_block_diagram.png")

if __name__ == "__main__":
    create_professional_diagram()
