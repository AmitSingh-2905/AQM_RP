import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_flowchart():
    fig, ax = plt.subplots(figsize=(10, 12))
    fig.patch.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Helper for boxes
    def add_box(x, y, w, h, text, color='#ffffff', edge='#000000', shape='rect'):
        if shape == 'rect':
            box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", fc=color, ec=edge, lw=2)
        elif shape == 'diamond':
            box = patches.RegularPolygon((x + w/2, y + h/2), numVertices=4, radius=w/1.8, orientation=0, fc=color, ec=edge, lw=2)
        elif shape == 'circle': # Ellipse for Start/End
            box = patches.Ellipse((x + w/2, y + h/2), w, h, fc=color, ec=edge, lw=2)
        
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=10, fontweight='bold', color='#333333')

    # Helper for arrows
    def add_arrow(x1, y1, x2, y2, text=None):
        ax.arrow(x1, y1, x2-x1, y2-y1, head_width=0.15, head_length=0.15, fc='#333333', ec='#333333', lw=1.5, length_includes_head=True)
        if text:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            ax.text(mid_x + 0.2, mid_y, text, fontsize=9, fontstyle='italic')

    # --- Nodes ---
    
    # 1. Start (ESP32)
    add_box(3.5, 10.5, 3, 1, "Start\n(Sensor Node)", color='#e0e0e0', shape='circle')
    add_arrow(5, 10.5, 5, 9.8)

    # 2. Read Data
    add_box(3.5, 9.0, 3, 0.8, "Read Sensor Data\n(Temp, Hum, Light)", color='#e3f2fd', edge='#1565c0')
    add_arrow(5, 9.0, 5, 8.3)

    # 3. Encrypt
    add_box(3.5, 7.5, 3, 0.8, "Encrypt Payload\n(AES-128 ECB)", color='#e8f5e9', edge='#2e7d32')
    add_arrow(5, 7.5, 5, 6.8)

    # 4. Publish
    add_box(3.5, 6.0, 3, 0.8, "MQTT Publish\n(Topic: data)", color='#fff3e0', edge='#ef6c00')
    add_arrow(5, 6.0, 5, 5.3, text="WSS")

    # 5. Decrypt (Browser)
    add_box(3.5, 4.5, 3, 0.8, "Decrypt Payload\n(CryptoJS)", color='#e8f5e9', edge='#2e7d32')
    add_arrow(5, 4.5, 5, 3.8)

    # 6. Decision (Diamond)
    # Using a rectangle visually but labeled as decision for simplicity in matplotlib patches
    # Actually let's try to make it look like a diamond
    # add_box(3.5, 2.5, 3, 1.3, "Is Z-Score > 3?", color='#ffebee', edge='#c62828', shape='diamond') 
    # Diamond shape is tricky with text, using a box with '?'
    add_box(3.5, 2.8, 3, 1.0, "Anomaly Check\n|Z-Score| > 3?", color='#ffebee', edge='#c62828')
    
    # Paths from Decision
    # No (Down)
    add_arrow(5, 2.8, 5, 1.8, text="No")
    
    # Yes (Right -> Down -> Left)
    ax.plot([6.5, 7.5], [3.3, 3.3], color='#333333', lw=1.5) # Right
    ax.plot([7.5, 7.5], [3.3, 1.3], color='#333333', lw=1.5) # Down
    ax.plot([7.5, 6.5], [1.3, 1.3], color='#333333', lw=1.5) # Left
    ax.arrow(7.5, 1.3, -1.0, 0, head_width=0.15, head_length=0.15, fc='#333333', ec='#333333', lw=1.5)
    
    ax.text(7.0, 3.4, "Yes", fontsize=9, fontstyle='italic')
    
    # Correction Box (Side)
    add_box(7.8, 2.0, 2.0, 0.8, "Correct Data\n(Clamp/Avg)", color='#ffcdd2', edge='#b71c1c')
    # Connect line to box
    ax.plot([7.5, 7.8], [2.4, 2.4], color='#333333', lw=1.5)


    # 7. Visualize
    add_box(3.5, 0.8, 3, 1.0, "Visualize Data\n(Chart.js)", color='#e1bee7', edge='#4a148c')
    
    # Connect Yes path back to visualize
    # The arrow above points to (6.5, 1.3), need to connect to box at (5, 1.3) roughly
    # Let's just draw arrow from Correction to Visualize
    # Actually, let's simplify the Yes path:
    # Decision -> Right -> Correction -> Down -> Visualize
    
    # Redraw Yes Path
    # Clear previous lines? No, just draw over or ignore. 
    # Let's just make a simple flow:
    
    # Decision -> No -> Visualize
    # Decision -> Yes -> Correction -> Visualize
    
    # Correction Box Positioned to the Right of Decision
    # add_box(7.0, 2.8, 2.5, 1.0, "Correct Data", ...)
    
    # Let's stick to the vertical flow for "No" and side loop for "Yes"
    
    plt.tight_layout()
    plt.savefig('algorithm_flowchart.png', dpi=300, bbox_inches='tight')
    print("Flowchart generated: algorithm_flowchart.png")

if __name__ == "__main__":
    create_flowchart()
