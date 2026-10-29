import os, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pixels import corner_pixels  # noqa: E402

# Kit de marque : dépôt privé doue-chat/doue-brand-kit, cloné en lecture (variable BRAND_KIT).
BRAND = Path(os.environ.get("BRAND_KIT", "/home/claude/doue-brand-kit"))
LOGO = (BRAND / "kit logo" / "logo" / "doue-logo-blanc.svg").read_text()
LOGO_INNER = re.search(r"<svg[^>]*>(.*)</svg>", LOGO, re.S).group(1).replace("<title>doue</title>", "")
# Polices dans ~/.fonts : Doue Bulle (doue-brand-kit/police bulle/Doue-Bulle/OTF, interne à doue, ne pas publier) + Geist.

COAL, PAPER, ORANGE = "#171A1F", "#F6F3ED", "#FF5A36"

# Fond : le grain de pixels de la page d'accueil, dense dans le coin haut droit, effacé avant le texte
# (le champ de bulles n'est plus un motif de la marque).
pixels = corner_pixels(reach=620, corner="tr")

thread = (
    "M96 980 C96 900 222 900 222 962 C222 1032 128 1032 150 962 "
    "C172 898 292 930 270 992 C256 1034 336 1030 366 980 L1000 980"
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200" width="1200" height="1200">
<title>Répondre, ce n’est pas régler.</title>
<desc>Un fil orange emmêlé se déroule en ligne droite jusqu'à un point d'arrivée, sur fond sombre. Texte : Répondre, ce n’est pas régler.</desc>
<rect width="1200" height="1200" fill="{COAL}"/>
{pixels}
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
