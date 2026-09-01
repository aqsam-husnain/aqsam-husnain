"""
make_info_card.py — Generate a neofetch-style terminal info card SVG.
Generates info-card.svg with system info, tech stack, and social links.
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BG = "#0d0d0d"
BORDER = "#2a2a2a"
GOLD = "#D4AF37"
SILVER = "#c0c0c0"
MUTED = "#666666"
RADIUS = 12
FONT = "'SF Mono','Fira Code','Cascadia Code',monospace"
FONT_SIZE = 11.5
LINE_H = 22
PAD_X = 24
PAD_Y = 55
CARD_W = 490
SEPARATOR = "─" * 36

INFO_LINES = [
    ("OS", "Full Stack Developer v3.0"),
    ("Host", "Aqsam Husnain"),
    ("Role", "Full Stack Engineer @ CraftSetup"),
    ("Location", "Punjab, Pakistan 🇵🇰"),
    ("", SEPARATOR),
    ("Frontend", "React · Next.js · TypeScript · Tailwind"),
    ("Backend", "Node.js · Python · FastAPI · Django"),
    ("3D / Motion", "Three.js · R3F · Framer Motion"),
    ("Database", "PostgreSQL · MongoDB · Redis · Prisma"),
    ("Mobile", "React Native"),
    ("Tools", "Docker · Git · VS Code · Vercel"),
    ("", SEPARATOR),
    ("Portfolio", "craftsetup.com/team/aqsam-husnain"),
    ("LinkedIn", "in/aqsam-husnain-b729a7270"),
    ("GitHub", "github.com/aqsam-husnain"),
    ("Email", "aqsamhusnain@gmail.com"),
    ("", SEPARATOR),
    ("", "💡 Constantly shipping. Always learning."),
]


def main():
    root = Path(__file__).resolve().parent.parent
    num_lines = len(INFO_LINES)
    card_h = PAD_Y + num_lines * LINE_H + 30

    svg = []
    svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{card_h}" viewBox="0 0 {CARD_W} {card_h}">
<defs>
  <style>
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateX(-8px); }}
      to   {{ opacity: 1; transform: translateX(0); }}
    }}
    .info-line {{
      opacity: 0;
      animation: fadeIn 0.4s ease forwards;
    }}
  </style>
</defs>

<!-- Card Background -->
<rect x="2" y="2" width="{CARD_W - 4}" height="{card_h - 4}" rx="{RADIUS}" ry="{RADIUS}"
      fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>

<!-- Terminal Dots -->
<circle cx="20" cy="20" r="5" fill="#ff5f57"/>
<circle cx="36" cy="20" r="5" fill="#febc2e"/>
<circle cx="52" cy="20" r="5" fill="#28c840"/>

<!-- Terminal Title -->
<text x="{CARD_W / 2}" y="24" fill="#888" font-family="{FONT}" font-size="10" text-anchor="middle">The Cipher Stack</text>
''')

    for i, (key, val) in enumerate(INFO_LINES):
        y = PAD_Y + i * LINE_H
        delay = 0.4 + i * 0.06

        if key == "" and val == SEPARATOR:
            # Separator line
            svg.append(
                f'<text class="info-line" x="{PAD_X}" y="{y}" fill="{MUTED}" '
                f'font-family="{FONT}" font-size="{FONT_SIZE}" '
                f'style="animation-delay:{delay:.2f}s" xml:space="preserve">{val}</text>'
            )
        elif key == "":
            # Quote / standalone line
            svg.append(
                f'<text class="info-line" x="{PAD_X}" y="{y}" fill="{SILVER}" '
                f'font-family="{FONT}" font-size="{FONT_SIZE}" '
                f'style="animation-delay:{delay:.2f}s">{val}</text>'
            )
        else:
            # Key: Value pair
            svg.append(
                f'<text class="info-line" x="{PAD_X}" y="{y}" font-family="{FONT}" '
                f'font-size="{FONT_SIZE}" style="animation-delay:{delay:.2f}s">'
                f'<tspan fill="{GOLD}">{key}</tspan>'
                f'<tspan fill="{MUTED}"> ~ </tspan>'
                f'<tspan fill="{SILVER}">{val}</tspan>'
                f'</text>'
            )

    svg.append("</svg>")

    out = root / "info-card.svg"
    out.write_text("\n".join(svg), encoding="utf-8")
    print(f"✅ Generated {out} ({num_lines} lines, {CARD_W}x{card_h})")


if __name__ == "__main__":
    main()
