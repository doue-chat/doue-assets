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
Prérequis : cairosvg, pypdf, police Geist installée (npm i geist, copier les TTF dans ~/.fonts).
"""
import json, re, sys
from pathlib import Path
import cairosvg
from pypdf import PdfWriter, PdfReader

HERE = Path(__file__).parent
wm = (HERE / "wordmark-blanc.svg").read_text()
WM_D = re.search(r' d="([^"]+)"', wm).group(1)
COAL, BUBBLE, PAPER, ORANGE = "#171A1F", "#22262D", "#F6F3ED", "#FF5A36"
BUBBLE_D = ("M89 14.5 L221 14.5 Q290.5 14.5 290.5 84 L290.5 199 L264 199 Q250 199 250 213 "
            "L250 220 Q250 232 238 232 L230 232 Q216 232 216 246 L216 272.5 L92.8 272.5 "
            "L42.6 309.6 A14.5 14.5 0 0 1 19.5 298 L19.5 84 Q19.5 14.5 89 14.5 Z")
BUBBLES = [(900, -40, 0.95, 1), (1010, 300, 0.55, -1), (760, 250, 0.40, 1), (-60, 380, 0.80, -1),
           (330, 1010, 0.42, 1), (900, 1030, 0.60, -1), (1060, 700, 0.38, 1), (560, -70, 0.50, -1),
           (-20, 960, 0.50, 1)]
TANGLE = ("M96 980 C96 900 222 900 222 962 C222 1032 128 1032 150 962 "
          "C172 898 292 930 270 992 C256 1034 336 1030 366 980 L1000 980")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def bubbles(shift):
    out = []
    for x, y, s, f in BUBBLES:
        x = x - shift * 14  # léger défilement d'une page à l'autre
        if f == 1:
            out.append(f'<path d="{BUBBLE_D}" transform="translate({x:.1f} {y}) scale({s})"/>')
        else:
            out.append(f'<path d="{BUBBLE_D}" transform="translate({x + 291 * s:.1f} {y}) scale({-s} {s})"/>')
    return "\n".join(out)


def slide_svg(i, n, sl):
    first, last = i == 0, i == n - 1
    y = 400
    parts = []
    if sl.get("big"):
        parts.append(f'<text x="96" y="{y + 110}" font-size="230" font-weight="600" letter-spacing="-8">{esc(sl["big"])}</text>')
        y += 190
    size = 112 if len(sl.get("lines", [])) <= 3 else 96
    for k, line in enumerate(sl.get("lines", [])):
        parts.append(f'<text x="96" y="{y + 20 + k * (size + 14)}" font-size="{size}" font-weight="600" letter-spacing="-3">{esc(line)}</text>')
    y2 = y + 20 + len(sl.get("lines", [])) * (size + 14) + 30
    for k, line in enumerate(sl.get("sub", [])):
        parts.append(f'<text x="96" y="{y2 + k * 50}" font-size="36" font-weight="500" fill-opacity="0.78">{esc(line)}</text>')
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
<g fill="{BUBBLE}">
{bubbles(i)}
</g>
<svg x="96" y="92" width="190" height="58.4" viewBox="357.29 14.5 840.21 258"><path fill-rule="evenodd" fill="{PAPER}" d="{WM_D}"/></svg>
<g font-family="Geist, Arial, sans-serif" fill="{PAPER}">
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
