# Gabarits visuels LinkedIn doue

- `build_post.py` : visuel de post 1200×1200 (style de référence du 2026-10-23, `python3 build_post.py sortie.svg`, à adapter : titre, sous-titre).
- `build_carousel.py` : carrousel PDF 1200×1200 (voir l'en-tête du fichier pour le format du `spec.json`). Exemple dans `exemple-carrousel/`.
- `pixels.py` : le fond commun aux deux gabarits, le grain de pixels de la page d'accueil (portage de `src/lib/pixel-field.ts` du site). Dense dans le coin haut droit, il s'efface avant le texte ; dans un carrousel, il glisse d'une case par diapositive.
- Logo : lu depuis le kit de marque (`kit logo/logo/doue-logo-blanc.svg`). Ne jamais le redessiner ni le copier dans ce dépôt.

Couleurs : charbon #171A1F, papier #F6F3ED (pixels à 5, 9 et 16 % d'opacité), orange #FF5A36 (rare : le fil et le point « Résolu »). Titres en Doue Bulle, texte en Geist.

Depuis le 2026-10-28, le champ de bulles n'est plus un motif de la marque : les nouveaux visuels utilisent les pixels. Les visuels déjà publiés (`linkedin/2026-10-23/`) restent tels quels.

## Kit de marque

La variable d'environnement `BRAND_KIT` doit pointer vers le dossier cloné du dépôt privé `doue-chat/doue-brand-kit` (par défaut `/home/claude/doue-brand-kit`). Les polices Doue Bulle (dossier `police bulle/`) s'installent dans `~/.fonts` depuis ce dépôt privé uniquement.
