# Gabarits visuels LinkedIn doue

- `build_post.py` : visuel de post 1200×1200 (style de référence du 2026-10-23, `python3 build_post.py sortie.svg`, à adapter : titre, sous-titre).
- `build_carousel.py` : carrousel PDF 1200×1200 (voir l'en-tête du fichier pour le format du `spec.json`). Exemple dans `exemple-carrousel/`.
- Logo : lu depuis le kit de marque (`kit logo/logo/doue-logo-blanc.svg`). Ne jamais le redessiner ni le copier dans ce dépôt.

Couleurs : charbon #171A1F, bulle #22262D, papier #F6F3ED, orange #FF5A36 (rare). Police : Geist en attendant Doue Bulle.

## Kit de marque

La variable d'environnement `BRAND_KIT` doit pointer vers le dossier cloné du dépôt privé `doue-chat/doue-brand-kit` (par défaut `/home/claude/doue-brand-kit`). Les polices Doue Bulle (dossier `police bulle/`) s'installent dans `~/.fonts` depuis ce dépôt privé uniquement.
