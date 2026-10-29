"""Carrousel LinkedIn doue (PDF 1200x1200, une page par diapositive), même style que les posts.

Usage : python3 build_carousel.py spec.json sortie_dir
spec.json :
{
  "slug": "sujet",
  "slides": [
    {"lines": ["Titre ligne 1", "ligne 2"], "sub": ["phrase courte", "suite"]},
    {"big": "9 %", "lines": ["des répondants..."], "sub": ["Source : ..."]},
    ...
  ]
}
- Première diapositive = couverture (fil emmêlé), dernière = conclusion (met doue.ai en avant).
- Les diapositives intermédiaires : fil qui se déroule en ligne droite, proportionnel à la progression.
- "lines" : titre (max 4 lignes, ~14 caractères par ligne à 112 px) ; "sub" : max 4 lignes de ~48 caractères.
- "big" : grand chiffre ou mot (optionnel). Un chiffre ne figure que s'il est vérifié et sourcé.
Sorties : <slug>_NN.svg, <slug>_NN.png, <slug>.pdf
Prérequis : cairosvg, pypdf ; polices installées dans ~/.fonts : Geist (npm i geist) et Doue Bulle (doue-brand-kit/police bulle/Doue-Bulle/OTF/DoueBulle-Bold.otf, puis fc-cache -f). La police est interne à doue : ne jamais la publier dans un dépôt public.
"""
import json, os, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pixels import corner_pixels  # noqa: E402

# Kit de marque : dépôt privé doue-chat/doue-brand-kit, cloné en lecture (variable BRAND_KIT).
BRAND = Path(os.environ.get("BRAND_KIT", "/home/claude/doue-brand-kit"))
LOGO = (BRAND / "kit logo" / "logo" / "doue-logo-blanc.svg").read_text()
LOGO_INNER = re.search(r"<svg[^>]*>(.*)</svg>", LOGO, re.S).group(1).replace("<title>doue</title>", "")
TITLE_FONT = "Doue Bulle, Geist, Arial, sans-serif"  # OTF installées depuis brand-kit/police bulle (voir LISEZMOI)
COAL, PAPER, ORANGE = "#171A1F", "#F6F3ED", "#FF5A36"
TANGLE = ("M96 980 C96 900 222 900 222 962 C222 1032 128 1032 150 962 "
          "C172 898 292 930 270 992 C256 1034 336 1030 366 980 L1000 980")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pixels(i):
    # Grain de pixels de la page d'accueil, coin haut droit ; il glisse d'une case par diapositive.
    return corner_pixels(reach=620, corner="tr", offset=i)


def slide_svg(i, n, sl):
    first, last = i == 0, i == n - 1
    y = 400
    parts = []
    if sl.get("big"):
        parts.append(f'<text x="96" y="{y + 110}" font-size="230" font-weight="700" letter-spacing="-6">{esc(sl["big"])}</text>')
        y += 190
    size = 112 if len(sl.get("lines", [])) <= 3 else 96
    for k, line in enumerate(sl.get("lines", [])):
        parts.append(f'<text x="96" y="{y + 20 + k * (size + 14)}" font-size="{size}" font-weight="700" letter-spacing="-2">{esc(line)}</text>')
    y2 = y + 20 + len(sl.get("lines", [])) * (size + 14) + 30
    for k, line in enumerate(sl.get("sub", [])):
        parts.append(f'<text x="96" y="{y2 + k * 50}" font-family="Geist, Arial, sans-serif" font-size="36" font-weight="500" fill-opacity="0.78">{esc(line)}</text>')
    if first:
        thread = TANGLE
        end_x = 1000
    else:
        end_x = 96 + int(904 * i / (n - 1))
        thread = f"M96 980 L{end_x} 980"
    node = ""
    if last:
        node = (f'<circle cx="1056" cy="980" r="14" fill="{ORANGE}"/>'
                f'<circle cx="1056" cy="980" r="30" fill="none" stroke="{ORANGE}" stroke-width="5"/>')
        thread = "M96 980 L1000 980"
    elif not first:
        node = f'<circle cx="{end_x + 24}" cy="980" r="12" fill="{ORANGE}"/>'
    footer_right = "doue.ai" if last or first else f"{i + 1} / {n}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200" width="1200" height="1200">
<rect width="1200" height="1200" fill="{COAL}"/>
{pixels(i)}
<svg x="96" y="84" width="230" height="58.3" viewBox="19.5 14.5 1178 298">{LOGO_INNER}</svg>
<g font-family="{TITLE_FONT}" fill="{PAPER}">
{chr(10).join(parts)}
</g>
<path d="{thread}" fill="none" stroke="{ORANGE}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
{node}
<g font-family="Geist, Arial, sans-serif" fill="{PAPER}" font-size="30" font-weight="500">
<text x="96" y="1100" fill-opacity="0.85">Le service client, sans perdre le fil.</text>
<text x="1104" y="1100" text-anchor="end">{footer_right}</text>
</g>
</svg>
'''


def main(spec_path, out_dir):
    # Imports du rendu ici : slide_svg reste utilisable sans cairo (aperçus, autres moteurs de rendu).
    import cairosvg
    from pypdf import PdfReader, PdfWriter
    spec = json.loads(Path(spec_path).read_text())
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    slides, slug = spec["slides"], spec["slug"]
    n = len(slides)
    writer = PdfWriter()
    for i, sl in enumerate(slides):
        base = out / f"{slug}_{i + 1:02d}"
        svg = slide_svg(i, n, sl)
        base.with_suffix(".svg").write_text(svg)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=str(base.with_suffix(".png")), output_width=1200, output_height=1200)
        cairosvg.svg2pdf(bytestring=svg.encode(), write_to=str(base.with_suffix(".pdf")))
        writer.add_page(PdfReader(str(base.with_suffix(".pdf"))).pages[0])
        base.with_suffix(".pdf").unlink()
    with open(out / f"{slug}.pdf", "wb") as f:
        writer.write(f)
    print("ok", out / f"{slug}.pdf", n, "diapositives")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
