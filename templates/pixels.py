"""Grain de pixels de la page d'accueil doue, pour les gabarits LinkedIn.

Portage de src/lib/pixel-field.ts (site doue) : même bruit par case, même grille, mêmes trois couches
d'opacité. Le motif de la marque n'est plus le champ de bulles : ce sont ces pixels carrés, denses dans
un coin ou contre un bord, qui s'effacent vers le texte.
"""
import math

PAPER = "#F6F3ED"
# Opacités des trois couches sur Charbon, un peu plus fortes que sur le site : LinkedIn recompresse
# les images en JPEG et efface les carrés les plus pâles.
DARK_OPACITIES = (0.05, 0.09, 0.16)


def cell_noise(i, j):
    """Valeur stable dans [0, 1) pour une case (identique à cellNoise du site)."""
    v = math.sin(i * 12.9898 + j * 78.233) * 43758.5453
    return v - math.floor(v)


def pixel_field(width, height, cell, density, offset=0):
    """Carrés de (cell - 2) px sur une grille `cell`, gardés là où le bruit passe sous la densité.
    Retourne trois chemins SVG (couches faible, moyenne, forte). `offset` décale le bruit de N cases
    (d'une diapositive à l'autre, le grain bouge sans changer de forme)."""
    d1, d2, d3 = [], [], []
    size = cell - 2
    for y in range(0, height, cell):
        for x in range(0, width, cell):
            d = density(x, y)
            if d <= 0:
                continue
            n = cell_noise(x / cell + offset, y / cell)
            if n > d:
                continue
            level = d - n
            sq = f"M{x} {y}h{size}v{size}h-{size}z"
            (d3 if level > 0.35 else d2 if level > 0.15 else d1).append(sq)
    return "".join(d1), "".join(d2), "".join(d3)


def corner_density(width, height, reach, corner="tr"):
    """Densité depuis un coin (tl, tr, bl, br), en quart de cercle de rayon `reach`."""
    def density(x, y):
        dx = x if "l" in corner else width - x
        dy = y if "t" in corner else height - y
        t = max(0.0, 1 - math.hypot(dx, dy) / reach)
        return t ** 1.2 * 0.9
    return density


def corner_pixels(width=1200, height=1200, reach=620, corner="tr", cell=10, offset=0,
                  color=PAPER, opacities=DARK_OPACITIES):
    """Groupe SVG prêt à poser derrière le texte : un coin de pixels qui s'efface vers le message."""
    layers = pixel_field(width, height, cell, corner_density(width, height, reach, corner), offset)
    paths = "".join(f'<path fill-opacity="{o}" d="{d}"/>' for o, d in zip(opacities, layers) if d)
    return f'<g fill="{color}">{paths}</g>'
