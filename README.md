# mister-bean 🗑️

> Site d'affiliation programmatic SEO — niche poubelles et accessoires.

Stratégie : 5 985 pages ciblées, générées et hiérarchisées via analyse Haloscan + SEO programmatic. Modèle : affiliation Amazon PA-API + LeroyMerlin + Cdiscount + ManoMano.

---

## Concept

Site spécialisé sur **toutes les poubelles possibles et imaginables** : domestique, professionnelle, design, tri sélectif, compost, cache-poubelle, par taille, matériau, couleur, usage, mécanisme...

Chaque page = un produit, un comparatif ou un guide → affiliation.

**Quick win identifié** : cache-poubelle extérieur (8 300/mois, KGR 0,05, zéro concurrent spécialisé).

---

## Corpus de pages

| Métrique | Valeur |
|----------|--------|
| Total pages | **5 985** |
| Enrichies Haloscan | 598 (10%) |
| Catégories | 92 |
| Priorité top/high | 1 096 |
| Priorité medium | 2 044 |
| Priorité low | 2 845 |

### Répartition par type

| Catégorie | Pages | Exemple |
|-----------|-------|---------|
| Volume × Usage | 572 | poubelle-50l-cuisine |
| Couleur × Volume | 540 | poubelle-noir-30l |
| Matériau × Volume | 459 | poubelle-inox-50l |
| Couleur × Usage | 420 | poubelle-blanc-salle-de-bain |
| Matériau × Usage | 357 | poubelle-bambou-cuisine |
| Fonction × Volume | 351 | poubelle-compost-10l |
| Volume × Mécanisme | 243 | poubelle-30l-pedale |
| Local | 115 | collecte-dechets-lyon |
| Cache-poubelle | 88+ | cache-poubelle-bois-2-bacs |
| Guides | 70 | comment-choisir-poubelle-cuisine |
| Comparatifs | 54 | comparatif-poubelle-automatique |
| PAA / Questions | 20 | quelle-poubelle-sdb |
| Métiers pro | 20 | poubelle-restaurant, poubelle-hopital |
| DIY | 12 | fabriquer-cache-poubelle |
| Van-life / Mobilité | 12 | poubelle-van, poubelle-camping-car |
| Zéro déchet | 12 | compost-appartement-sans-odeur |

### Top keywords Haloscan (volume mensuel)

| Keyword | Volume/mois |
|---------|-------------|
| Poubelle (root) | 54 100 |
| Conteneur | 20 800 |
| Corbeille | 14 600 |
| Composteur gratuit | 9 000 |
| Poubelle de tri | 8 600 |
| Cache poubelle extérieur | 8 300 |
| Poubelle de cuisine | 4 500 |
| Poubelle compost | 4 100 |
| Composteur appartement | 4 300 |

---

## Stratégie

### Modèle de monétisation
**Affiliation** (NO-GO dropshipping — marges + SAV + CGU AliExpress).

Partenaires :
- Amazon PA-API (principal)
- Leroy Merlin Affiliation
- Cdiscount Affiliation
- ManoMano

### Entrée SEO recommandée
1. **Cluster cache-poubelle** : KGR 0,05 sur le mot-clé principal, 88+ pages, zéro concurrent spécialisé
2. **Cluster compost/biodéchets** : tailwind AGEC 2024 (biodéchets obligatoires)
3. **Long tail taille × usage** : 572 pages, intent transactionnel fort

### Tailwind
- **Loi AGEC 2024** : collecte biodéchets obligatoire — marché composteur/biodéchets en croissance structurelle
- Cache-poubelle extérieur : tendance déco jardin forte, aucun leader

---

## Stack technique cible

| Composant | Choix |
|-----------|-------|
| Framework | Next.js SSG (ou Astro) |
| Données produits | Amazon PA-API |
| Génération contenu | GPT-4o + templates JSON |
| Affiliation | Amazon + Leroy Merlin + Cdiscount |
| Hébergement | Vercel |
| Analytics | Umami (no cookies) |
| Suivi SEO | GSC + Haloscan mensuel |

---

## Structure du repo

```
mister-bean/
├── data/
│   ├── pages.json          ← Liste complète des 5 985 pages (source de vérité)
│   └── pages.csv           ← Export tableur (slug, titre, catégorie, priorité, volume, KD, CPC)
├── scripts/
│   ├── generate_pages.py   ← Générateur systématique de pages (combinatoires)
│   └── monitor.sh          ← Script de monitoring/restart job nuit
├── docs/
│   ├── analyse-argo.md     ← Analyse stratégique complète (Argo, 2026-02-21)
│   └── roadmap.md          ← Roadmap de développement
└── README.md
```

---

## Roadmap

- [ ] Enregistrer le domaine (cache-poubelle.fr ou abripoubelle.fr)
- [ ] Créer les templates de pages programmatic (Next.js SSG)
- [ ] Brancher Amazon PA-API
- [ ] Générer les 50 premières pages cluster cache-poubelle
- [ ] 5 articles éditoriaux AGEC/biodéchets (signal E-E-A-T)
- [ ] Passer les pages priority:top en production en premier

---

*Analyse Argo — 2026-02-21 | Corpus généré le 2026-02-22 | Données SEO : Haloscan API*
