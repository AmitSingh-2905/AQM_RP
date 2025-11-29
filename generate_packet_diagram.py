import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_packet_diagram():
    fig, ax = plt.subplots(figsize=(12, 4))
    fig.patch.set_facecolor('white')
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 4)
    ax.axis('off')

    def add_box(x, y, w, h, text, subtext, color='#ffffff', edge='#000000'):
        # Shadow
        shadow = patches.FancyBboxPatch((x+0.05, y-0.05), w, h, boxstyle="round,pad=0.1", fc='#dddddd', ec='none', zorder=1)
        ax.add_patch(shadow)
        # Box
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", fc=color, ec=edge, lw=2, zorder=2)
        ax.add_patch(box)
        # Text
        ax.text(x + w/2, y + h/2 + 0.2, text, ha='center', va='center', fontsize=11, fontweight='bold', zorder=3, color='#333333')
        ax.text(x + w/2, y + h/2 - 0.3, subtext, ha='center', va='center', fontsize=9, fontstyle='italic', zorder=3, color='#555555')

    def add_arrow(x1, y1, x2, y2, label):
        # Arrow line
        ax.arrow(x1, y1, x2-x1-0.1, 0, head_width=0.15, head_length=0.15, fc='#333333', ec='#333333', lw=1.5, length_includes_head=True, zorder=4)
        # Label
        ax.text((x1+x2)/2, y1 + 0.2, label, ha='center', va='bottom', fontsize=9, fontweight='bold', color='#333333')

    # 1. Raw Data
    add_box(0.5, 1.5, 2.2, 1.2, "Raw JSON", '{"t":24.5}', color='#e3f2fd', edge='#1565c0')

    # Arrow 1
    add_arrow(2.7, 2.1, 3.7, 2.1, "Padding")

    # 2. Padded Block
    add_box(3.7, 1.5, 2.2, 1.2, "Padded Block", "16 Bytes\n(PKCS7)", color='#fff3e0', edge='#ef6c00')

    # Arrow 2
    add_arrow(5.9, 2.1, 6.9, 2.1, "AES-128\n(Key)")

    # 3. Ciphertext
    add_box(6.9, 1.5, 2.2, 1.2, "Ciphertext", "Encrypted Bytes\n(Binary)", color='#e8f5e9', edge='#2e7d32')

    # Arrow 3
    add_arrow(9.1, 2.1, 10.1, 2.1, "Base64")

    # 4. Payload
    add_box(10.1, 1.5, 2.0, 1.2, "MQTT Payload", "Safe String", color='#f3e5f5', edge='#7b1fa2')

    plt.tight_layout()
    plt.savefig('packet_structure.png', dpi=300, bbox_inches='tight')
    print("Packet diagram generated: packet_structure.png")

if __name__ == "__main__":
    create_packet_diagram()
