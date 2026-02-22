# Roadmap — mister-bean

## Phase 0 — Fondations (Semaine 1)

- [ ] Choisir et enregistrer le domaine
  - Candidats : `cache-poubelle.fr`, `abripoubelle.fr`, `mister-bean.fr` (fun), `poubelle-guide.fr`
- [ ] Setup Next.js SSG (ou Astro) + Vercel
- [ ] Inscription Amazon Partenaires (PA-API)
- [ ] Inscription Leroy Merlin Affiliation
- [ ] Intégrer Umami (analytics sans cookies)

## Phase 1 — Cluster cache-poubelle (Semaine 2-3)

Priorité absolue — KGR 0,05 sur le mot-clé principal.

- [ ] Template de page cache-poubelle (matériau × nb bacs)
- [ ] Générer les 88 pages `cache-poubelle-*` depuis `data/pages.json` (filter: category=cache-poubelle*)
- [ ] 5 articles éditoriaux :
  - "Comment choisir un cache-poubelle extérieur"
  - "Cache-poubelle bois : guide et comparatif"
  - "Fabriquer un cache-poubelle soi-même"
  - "Cache-poubelle 2 bacs vs 3 bacs"
  - "Meilleur abri poubelle extérieur 2025"
- [ ] Brancher Amazon PA-API sur les produits cache-poubelle
- [ ] Submit sitemap GSC

## Phase 2 — Cluster compost/biodéchets (Semaine 4-5)

Tailwind AGEC 2024.

- [ ] Template de page composteur/compost
- [ ] Générer les pages `poubelle-compost-*`, `composteur-*` (~50 pages)
- [ ] 3 articles AGEC :
  - "Loi AGEC biodéchets : ce qui change en 2024"
  - "Meilleur composteur cuisine 2025"
  - "Composteur gratuit : comment en obtenir un ?"
- [ ] Affiliation composteurs (Amazon + LeroyMerlin)

## Phase 3 — Long tail taille × usage (Mois 2)

- [ ] Template de page produit générique (poubelle-NL-usage)
- [ ] Générer les 572 pages volume-usage (priority: high)
- [ ] Affiliation dynamique via PA-API (recherche par keyword)

## Phase 4 — Scale programmatic (Mois 3-6)

- [ ] Pipeline GPT-4o bulk : JSON produits → contenu unique par page
- [ ] Générer les pages priority:medium (2 044 pages)
- [ ] Scraper LeroyMerlin/ManoMano pour enrichir les données produits (Reader quand VPS 16GB+)
- [ ] Suivi mensuel GSC + Haloscan (évolution positions)

## Phase 5 — Optimisation & Scale (Mois 6+)

- [ ] A/B test formats (comparatif vs guide vs fiche produit)
- [ ] Email capture (newsletter déco/jardinage)
- [ ] Expansion Belgique/Suisse FR (domaine .be ou sous-dossier)
- [ ] Pages low priority si trafic organique confirmé

---

## KPIs cibles

| Horizon | Trafic organique | Revenus affiliation |
|---------|-----------------|---------------------|
| M3 | 500 visites/mois | 0–200€ |
| M6 | 3 000 visites/mois | 200–800€ |
| M12 | 15 000 visites/mois | 1 000–3 000€ |
| M24 | 50 000+ visites/mois | 3 000–8 000€ |

---

## Notes techniques

### Génération programmatic depuis pages.json

```python
import json
from pathlib import Path

pages = json.loads(Path("data/pages.json").read_text())

# Filtrer par catégorie et priorité
cache_pages = [p for p in pages.values()
               if "cache-poubelle" in p["category"]
               and p["priority"] in ("top", "high")]

print(f"{len(cache_pages)} pages cache-poubelle à générer en priorité")
```

### Ordre de génération recommandé
1. `priority: top` (19 pages) — à la main, contenu premium
2. `category: cache-poubelle*` (88 pages) — template automatique
3. `category: guide` + `category: comparatif` (124 pages) — contenu rédactionnel
4. `priority: high` restant (965 pages) — template automatique
5. `priority: medium` (2 044 pages) — bulk GPT-4o
