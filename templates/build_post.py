import re, sys
from pathlib import Path

import os
# Kit de marque officiel : dépôt privé doue-chat/doue-website, dossier brand-kit/ (cloné en lecture).
BRAND = Path(os.environ.get("BRAND_KIT", "/home/claude/doue-website/brand-kit"))
LOGO = (BRAND / "kit logo" / "logo" / "doue-logo-blanc.svg").read_text()
LOGO_INNER = re.search(r"<svg[^>]*>(.*)</svg>", LOGO, re.S).group(1).replace("<title>doue</title>", "")
# Polices dans ~/.fonts : Doue Bulle (brand-kit/police bulle/Doue-Bulle/OTF, interne à doue, ne pas publier) + Geist.

COAL, BUBBLE, PAPER, ORANGE = "#171A1F", "#22262D", "#F6F3ED", "#FF5A36"
BUBBLE_D = ("M89 14.5 L221 14.5 Q290.5 14.5 290.5 84 L290.5 199 L264 199 Q250 199 250 213 "
            "L250 220 Q250 232 238 232 L230 232 Q216 232 216 246 L216 272.5 L92.8 272.5 "
            "L42.6 309.6 A14.5 14.5 0 0 1 19.5 298 L19.5 84 Q19.5 14.5 89 14.5 Z")

# (x, y, scale, flip) : champ de bulles discret en arrière-plan (motif de la marque)
bubbles = [
    (900, -40, 0.95, 1), (1010, 300, 0.55, -1), (760, 250, 0.40, 1),
    (-60, 380, 0.80, -1), (330, 1010, 0.42, 1), (900, 1030, 0.60, -1),
    (1060, 700, 0.38, 1), (560, -70, 0.50, -1), (-20, 960, 0.50, 1),
]
bub = []
for x, y, s, f in bubbles:
    if f == 1:
        bub.append(f'<path d="{BUBBLE_D}" transform="translate({x} {y}) scale({s})"/>')
    else:
        bub.append(f'<path d="{BUBBLE_D}" transform="translate({x + 291 * s:.1f} {y}) scale({-s} {s})"/>')

thread = (
    "M96 980 C96 900 222 900 222 962 C222 1032 128 1032 150 962 "
    "C172 898 292 930 270 992 C256 1034 336 1030 366 980 L1000 980"
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200" width="1200" height="1200">
<title>Répondre, ce n’est pas régler.</title>
<desc>Un fil orange emmêlé se déroule en ligne droite jusqu'à un point d'arrivée, sur fond sombre. Texte : Répondre, ce n’est pas régler.</desc>
<rect width="1200" height="1200" fill="{COAL}"/>
<g fill="{BUBBLE}">
{chr(10).join(bub)}
</g>
<svg x="96" y="84" width="230" height="58.3" viewBox="19.5 14.5 1178 298">{LOGO_INNER}</svg>
<g font-family="Doue Bulle, Geist, Arial, sans-serif" fill="{PAPER}">
<text x="96" y="468" font-size="132" font-weight="700" letter-spacing="-3">Répondre,</text>
<text x="96" y="612" font-size="132" font-weight="700" letter-spacing="-3">ce n’est pas</text>
<text x="96" y="756" font-size="132" font-weight="700" letter-spacing="-3">régler.</text>
<text x="96" y="852" font-family="Geist, Arial, sans-serif" font-size="32" font-weight="500" fill-opacity="0.72">Une demande n’est pas fermée tant qu’elle n’est pas résolue.</text>
</g>
<path d="{thread}" fill="none" stroke="{ORANGE}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="1056" cy="980" r="14" fill="{ORANGE}"/>
<circle cx="1056" cy="980" r="30" fill="none" stroke="{ORANGE}" stroke-width="5"/>
<g font-family="Geist, Arial, sans-serif" fill="{PAPER}" font-size="30" font-weight="500">
<text x="96" y="1100" fill-opacity="0.85">Le service client, sans perdre le fil.</text>
<text x="1104" y="1100" text-anchor="end">doue.ai</text>
</g>
</svg>
'''
out = sys.argv[1]
Path(out).write_text(svg)
print("ok", out, len(svg))
