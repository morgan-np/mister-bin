#!/usr/bin/env python3
"""
Générateur de pages programmatic SEO — Niche Poubelles
Output : /workspace/output/poubelles_pages.json + poubelles_pages.csv

Phases :
  1. Génération systématique de toutes les combinaisons
  2. Enrichissement Haloscan (volumes, KD, CPC)
  3. Expansion créative (comparatifs, guides, accessoires)

Usage :
  python3 poubelles_pages.py --phase all
  python3 poubelles_pages.py --phase systematic
  python3 poubelles_pages.py --phase haloscan
  python3 poubelles_pages.py --phase creative
  python3 poubelles_pages.py --stats
"""

import json
import csv
import sys
import os
import time
import argparse
import itertools
import subprocess
from pathlib import Path
from datetime import datetime

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "poubelles"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PAGES_FILE   = OUTPUT_DIR / "pages.json"
HALOSCAN_FILE = OUTPUT_DIR / "haloscan_data.json"
LOG_FILE     = OUTPUT_DIR / "progress.log"
HALOSCAN_SCRIPT = BASE_DIR / "scripts" / "haloscan.py"
PYTHON_BIN   = "/home/ubuntu/.venv/bin/python3"

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def load_pages():
    if PAGES_FILE.exists():
        return json.loads(PAGES_FILE.read_text())
    return {}

def save_pages(pages):
    PAGES_FILE.write_text(json.dumps(pages, ensure_ascii=False, indent=2))

# ─── Taxonomie complète ───────────────────────────────────────────────────────

# Types principaux
TYPES_PRINCIPAUX = {
    "poubelle": "Poubelle",
    "corbeille": "Corbeille à papier",
    "bac": "Bac",
    "container": "Container",
    "poubelle-roulante": "Poubelle roulante",
}

# Usages / fonctions
USAGES = {
    "cuisine":           "cuisine",
    "salle-de-bain":     "salle de bain",
    "bureau":            "bureau",
    "salon":             "salon",
    "chambre":           "chambre",
    "garage":            "garage",
    "jardin":            "jardin",
    "exterieur":         "extérieur",
    "terrasse":          "terrasse",
    "cave":              "cave",
    "van":               "van",
    "camping-car":       "camping-car",
    "camping":           "camping",
    "bateaux":           "bateau",
    "restaurant":        "restaurant",
    "hotel":             "hôtel",
    "bureau-open-space": "open space",
    "ecole":             "école",
    "hopital":           "hôpital",
    "collectivites":     "collectivités",
    "industrie":         "industrie",
}

# Usages fonctionnels (type de déchet)
FONCTIONS = {
    "ordures-menageres":   "ordures ménagères",
    "tri-selectif":        "tri sélectif",
    "recyclage-papier":    "recyclage papier",
    "recyclage-plastique": "recyclage plastique",
    "recyclage-verre":     "recyclage verre",
    "compost":             "compost",
    "biodechets":          "biodéchets",
    "carton":              "carton",
    "metal":               "métal",
    "alimentaire":         "déchets alimentaires",
    "sanitaire":           "déchets sanitaires",
    "couches":             "couches bébé",
    "medical":             "déchets médicaux",
    "electronique":        "DEEE",
}

# Matériaux
MATERIAUX = {
    "plastique":  "plastique",
    "inox":       "inox",
    "acier":      "acier",
    "bambou":     "bambou",
    "bois":       "bois",
    "rotin":      "rotin",
    "osier":      "osier",
    "metal":      "métal",
    "aluminium":  "aluminium",
    "cuir":       "cuir",
    "tissu":      "tissu",
    "silicone":   "silicone",
    "beton":      "béton",
    "resine":     "résine",
    "pierre":     "pierre",
    "chrome":     "chrome",
    "zinc":       "zinc",
}

# Couleurs
COULEURS = {
    "blanc":    "blanc",
    "noir":     "noir",
    "gris":     "gris",
    "beige":    "beige",
    "marron":   "marron",
    "rouge":    "rouge",
    "bleu":     "bleu",
    "vert":     "vert",
    "rose":     "rose",
    "jaune":    "jaune",
    "orange":   "orange",
    "violet":   "violet",
    "or":       "or",
    "cuivre":   "cuivre",
    "argent":   "argent",
    "turquoise":"turquoise",
    "nude":     "nude",
    "anthracite":"anthracite",
    "taupe":    "taupe",
    "emeraude": "émeraude",
}

# Volumes / tailles
VOLUMES = {
    "1l": "1L", "2l": "2L", "3l": "3L", "5l": "5L",
    "7l": "7L", "8l": "8L", "10l": "10L", "12l": "12L",
    "15l": "15L", "16l": "16L", "20l": "20L", "25l": "25L",
    "30l": "30L", "40l": "40L", "50l": "50L", "60l": "60L",
    "70l": "70L", "80l": "80L", "90l": "90L", "100l": "100L",
    "120l": "120L", "140l": "140L", "180l": "180L",
    "240l": "240L", "360l": "360L", "600l": "600L", "1100l": "1100L",
}

# Mécanismes d'ouverture
MECANISMES = {
    "pedale":        "à pédale",
    "automatique":   "automatique",
    "capteur":       "à capteur",
    "balancier":     "à balancier",
    "push":          "à couvercle push",
    "couvercle":     "avec couvercle",
    "sans-couvercle":"sans couvercle",
    "rabattable":    "à couvercle rabattable",
    "coulissant":    "coulissant",
}

# Nombre de compartiments
COMPARTIMENTS = {
    "1-bac": "1 bac", "2-bacs": "2 bacs",
    "3-bacs": "3 bacs", "4-bacs": "4 bacs", "5-bacs": "5 bacs",
}

# Styles design
STYLES = {
    "design":       "design",
    "minimaliste":  "minimaliste",
    "scandinave":   "scandinave",
    "industriel":   "industriel",
    "vintage":      "vintage",
    "retro":        "rétro",
    "moderne":      "moderne",
    "luxe":         "luxe",
    "fantaisie":    "fantaisie",
    "enfant":       "pour enfant",
    "fun":          "fun",
    "deco":         "décoratif",
    "transparent":  "transparent",
    "personnalisable":"personnalisable",
}

# Caractéristiques spéciales
CARACTERISTIQUES = {
    "anti-odeur":       "anti-odeur",
    "filtre-charbon":   "filtre à charbon",
    "etanche":          "étanche",
    "avec-roues":       "avec roues",
    "empilable":        "empilable",
    "compresseur":      "avec compresseur",
    "demontable":       "démontable",
    "silencieux":       "silencieux",
    "verrouillable":    "verrouillable",
    "mural":            "mural",
    "encastrable":      "encastrable",
    "pliant":           "pliable",
    "suspendu":         "suspendu",
    "portable":         "portable",
}

# Marques (affiliation)
MARQUES = {
    "brabantia":    "Brabantia",
    "simplehuman":  "simplehuman",
    "joseph-joseph":"Joseph Joseph",
    "ikea":         "IKEA",
    "addis":        "Addis",
    "curver":       "Curver",
    "authentics":   "Authentics",
    "wesco":        "Wesco",
    "burak":        "Burak",
    "rotho":        "Rotho",
    "sulo":         "Sulo",
    "vileda":       "Vileda",
    "elletipi":     "Elletipi",
    "umbra":        "Umbra",
    "alessi":       "Alessi",
    "magis":        "Magis",
}

# Produits connexes / cache-poubelle
CACHE_POUBELLE_MATERIAUX = {
    "bois":    "bois", "metal": "métal", "pvc": "PVC",
    "resine":  "résine", "beton": "béton", "osier": "osier",
    "rotin":   "rotin", "bambou": "bambou", "acier": "acier",
    "grillage":"grillage", "parpaing": "parpaing",
}

CACHE_POUBELLE_NBACS = {
    "1-bac": "1 bac", "2-bacs": "2 bacs",
    "3-bacs": "3 bacs", "4-bacs": "4 bacs",
}

# Accessoires
ACCESSOIRES = {
    "sac-poubelle":           "sac poubelle",
    "sac-compostable":        "sac compostable",
    "sac-biodegradable":      "sac biodégradable",
    "filtre-a-charbon":       "filtre à charbon",
    "chariot-poubelle":       "chariot poubelle",
    "support-poubelle":       "support poubelle",
    "couvercle-remplacement": "couvercle de remplacement",
    "pedal-remplacement":     "pédale de remplacement",
    "bac-interieur":          "bac intérieur",
    "notice-tri":             "notice de tri",
    "autocollant-tri":        "autocollant tri sélectif",
    "seau-compost":           "seau compost",
    "composteur":             "composteur",
    "vermicomposteur":        "vermicomposteur",
    "bac-collecte":           "bac de collecte",
}

# Sacs poubelle (dimensions)
SAC_VOLUMES = ["10l","15l","20l","25l","30l","35l","40l","45l","50l",
               "60l","70l","80l","100l","110l","130l","150l","240l"]

# ─── Générateur de pages ─────────────────────────────────────────────────────

def make_slug(*parts):
    return "-".join(p.strip().lower().replace(" ", "-").replace("'", "").replace("é","e").replace("è","e").replace("à","a").replace("ê","e").replace("â","a").replace("î","i").replace("ô","o").replace("û","u") for p in parts if p)

def add_page(pages, category, slug, title, description="", priority="medium"):
    if slug not in pages:
        pages[slug] = {
            "slug": slug,
            "category": category,
            "title": title,
            "description": description,
            "priority": priority,
            "haloscan_volume": None,
            "haloscan_kd": None,
            "haloscan_cpc": None,
        }

def generate_systematic(pages):
    log("=== PHASE 1 : Génération systématique ===")
    count_start = len(pages)

    # ── 1. Pages par type + pièce/usage
    log("  → Type × Usage")
    for uk, uv in USAGES.items():
        add_page(pages, "type-usage", f"poubelle-{uk}", f"Poubelle {uv}", priority="high")
        add_page(pages, "type-usage", f"corbeille-{uk}", f"Corbeille {uv}", priority="medium")

    # ── 2. Pages par volume seul
    log("  → Volumes")
    for vk, vv in VOLUMES.items():
        add_page(pages, "volume", f"poubelle-{vk}", f"Poubelle {vv}", priority="high")
        add_page(pages, "volume", f"bac-{vk}", f"Bac {vv}", priority="low")

    # ── 3. Volume × Usage (ex: poubelle-50l-cuisine)
    log("  → Volume × Usage")
    for vk, vv in VOLUMES.items():
        for uk, uv in USAGES.items():
            add_page(pages, "volume-usage", f"poubelle-{vk}-{uk}", f"Poubelle {vv} {uv}", priority="high")

    # ── 4. Volume × Mécanisme (ex: poubelle-30l-pedale)
    log("  → Volume × Mécanisme")
    for vk, vv in VOLUMES.items():
        for mk, mv in MECANISMES.items():
            add_page(pages, "volume-mecanisme", f"poubelle-{vk}-{mk}", f"Poubelle {vv} {mv}", priority="medium")

    # ── 5. Couleur seule
    log("  → Couleurs")
    for ck, cv in COULEURS.items():
        add_page(pages, "couleur", f"poubelle-{ck}", f"Poubelle {cv}", priority="medium")
        add_page(pages, "couleur", f"corbeille-{ck}", f"Corbeille {cv}", priority="low")

    # ── 6. Couleur × Usage
    log("  → Couleur × Usage")
    for ck, cv in COULEURS.items():
        for uk, uv in USAGES.items():
            add_page(pages, "couleur-usage", f"poubelle-{ck}-{uk}", f"Poubelle {cv} {uv}", priority="low")

    # ── 7. Couleur × Volume
    log("  → Couleur × Volume")
    for ck, cv in COULEURS.items():
        for vk, vv in VOLUMES.items():
            add_page(pages, "couleur-volume", f"poubelle-{ck}-{vk}", f"Poubelle {cv} {vv}", priority="low")

    # ── 8. Matériau seul
    log("  → Matériaux")
    for mk, mv in MATERIAUX.items():
        add_page(pages, "materiau", f"poubelle-{mk}", f"Poubelle {mv}", priority="medium")
        add_page(pages, "materiau", f"corbeille-{mk}", f"Corbeille {mv}", priority="low")

    # ── 9. Matériau × Usage
    log("  → Matériau × Usage")
    for mk, mv in MATERIAUX.items():
        for uk, uv in USAGES.items():
            add_page(pages, "materiau-usage", f"poubelle-{mk}-{uk}", f"Poubelle {mv} {uv}", priority="medium")

    # ── 10. Matériau × Volume
    log("  → Matériau × Volume")
    for mk, mv in MATERIAUX.items():
        for vk, vv in VOLUMES.items():
            add_page(pages, "materiau-volume", f"poubelle-{mk}-{vk}", f"Poubelle {mv} {vv}", priority="low")

    # ── 11. Matériau × Couleur
    log("  → Matériau × Couleur")
    for mk, mv in MATERIAUX.items():
        for ck, cv in COULEURS.items():
            add_page(pages, "materiau-couleur", f"poubelle-{mk}-{ck}", f"Poubelle {mv} {cv}", priority="low")

    # ── 12. Mécanisme seul
    log("  → Mécanismes")
    for mk, mv in MECANISMES.items():
        add_page(pages, "mecanisme", f"poubelle-{mk}", f"Poubelle {mv}", priority="high")

    # ── 13. Mécanisme × Usage
    log("  → Mécanisme × Usage")
    for mk, mv in MECANISMES.items():
        for uk, uv in USAGES.items():
            add_page(pages, "mecanisme-usage", f"poubelle-{mk}-{uk}", f"Poubelle {mv} {uv}", priority="medium")

    # ── 14. Tri sélectif : compartiments × usage
    log("  → Tri sélectif × Compartiments")
    for ck, cv in COMPARTIMENTS.items():
        add_page(pages, "tri-compartiments", f"poubelle-tri-{ck}", f"Poubelle de tri sélectif {cv}", priority="high")
        for uk, uv in {k:v for k,v in USAGES.items() if k in ["cuisine","bureau","garage","exterieur","collectivites"]}.items():
            add_page(pages, "tri-compartiments-usage", f"poubelle-tri-{ck}-{uk}", f"Poubelle tri sélectif {cv} {uv}", priority="high")

    # ── 15. Fonctions/type de déchet
    log("  → Fonctions × Usage")
    for fk, fv in FONCTIONS.items():
        add_page(pages, "fonction", f"poubelle-{fk}", f"Poubelle {fv}", priority="high")
        for uk, uv in USAGES.items():
            add_page(pages, "fonction-usage", f"poubelle-{fk}-{uk}", f"Poubelle {fv} {uv}", priority="medium")
        for vk, vv in VOLUMES.items():
            add_page(pages, "fonction-volume", f"poubelle-{fk}-{vk}", f"Poubelle {fv} {vv}", priority="medium")

    # ── 16. Style/Design
    log("  → Styles")
    for sk, sv in STYLES.items():
        add_page(pages, "style", f"poubelle-{sk}", f"Poubelle {sv}", priority="medium")
        for uk, uv in USAGES.items():
            add_page(pages, "style-usage", f"poubelle-{sk}-{uk}", f"Poubelle {sv} {uv}", priority="low")
        for mk, mv in MATERIAUX.items():
            add_page(pages, "style-materiau", f"poubelle-{sk}-{mk}", f"Poubelle {sv} {mv}", priority="low")

    # ── 17. Caractéristiques spéciales
    log("  → Caractéristiques")
    for ck, cv in CARACTERISTIQUES.items():
        add_page(pages, "caracteristique", f"poubelle-{ck}", f"Poubelle {cv}", priority="medium")
        for uk, uv in USAGES.items():
            add_page(pages, "caracteristique-usage", f"poubelle-{ck}-{uk}", f"Poubelle {cv} {uv}", priority="low")

    # ── 18. Marques
    log("  → Marques")
    for brk, brv in MARQUES.items():
        add_page(pages, "marque", f"poubelle-{brk}", f"Poubelle {brv}", priority="medium")
        add_page(pages, "marque-avis", f"avis-{brk}", f"Avis {brv} — guide complet", priority="medium")
        for uk, uv in {k:v for k,v in USAGES.items() if k in ["cuisine","bureau","salle-de-bain","exterieur"]}.items():
            add_page(pages, "marque-usage", f"poubelle-{brk}-{uk}", f"Poubelle {brv} {uv}", priority="medium")

    # ── 19. Cache-poubelle (sous-niche prioritaire)
    log("  → Cache-poubelle")
    add_page(pages, "cache-poubelle", "cache-poubelle", "Cache-poubelle", priority="top")
    add_page(pages, "cache-poubelle", "cache-poubelle-exterieur", "Cache-poubelle extérieur", priority="top")
    add_page(pages, "cache-poubelle", "cache-poubelle-jardin", "Cache-poubelle jardin", priority="top")
    add_page(pages, "cache-poubelle", "abri-poubelle", "Abri poubelle", priority="top")
    add_page(pages, "cache-poubelle", "abri-bac-roulant", "Abri bac roulant", priority="top")

    for mk, mv in CACHE_POUBELLE_MATERIAUX.items():
        add_page(pages, "cache-poubelle-materiau", f"cache-poubelle-{mk}", f"Cache-poubelle {mv}", priority="high")
        add_page(pages, "cache-poubelle-materiau", f"cache-poubelle-exterieur-{mk}", f"Cache-poubelle extérieur {mv}", priority="high")
        add_page(pages, "cache-poubelle-materiau", f"abri-poubelle-{mk}", f"Abri poubelle {mk}", priority="high")

    for nk, nv in CACHE_POUBELLE_NBACS.items():
        add_page(pages, "cache-poubelle-nbacs", f"cache-poubelle-{nk}", f"Cache-poubelle {nv}", priority="high")
        add_page(pages, "cache-poubelle-nbacs", f"cache-poubelle-exterieur-{nk}", f"Cache-poubelle extérieur {nv}", priority="high")
        add_page(pages, "cache-poubelle-nbacs", f"abri-poubelle-{nk}", f"Abri poubelle {nv}", priority="high")
        for mk, mv in CACHE_POUBELLE_MATERIAUX.items():
            add_page(pages, "cache-poubelle-materiau-nbacs", f"cache-poubelle-{mk}-{nk}", f"Cache-poubelle {mv} {nv}", priority="high")
            add_page(pages, "cache-poubelle-materiau-nbacs", f"abri-poubelle-{mk}-{nk}", f"Abri poubelle {mv} {nv}", priority="medium")

    # Cache-poubelle × usage
    for uk, uv in {"exterieur":"extérieur","jardin":"jardin","terrasse":"terrasse","garage":"garage"}.items():
        for mk, mv in CACHE_POUBELLE_MATERIAUX.items():
            add_page(pages, "cache-poubelle-usage-materiau",
                     f"cache-poubelle-{uk}-{mk}",
                     f"Cache-poubelle {uv} {mv}", priority="medium")

    # ── 20. Accessoires
    log("  → Accessoires")
    for ak, av in ACCESSOIRES.items():
        add_page(pages, "accessoire", ak, av.capitalize(), priority="medium")

    # Sacs poubelle × volume
    log("  → Sacs × Volume")
    for sv in SAC_VOLUMES:
        add_page(pages, "sac-volume", f"sac-poubelle-{sv}", f"Sac poubelle {sv.upper()}", priority="medium")
        add_page(pages, "sac-volume", f"sac-compostable-{sv}", f"Sac compostable {sv.upper()}", priority="medium")
        add_page(pages, "sac-volume", f"sac-biodegradable-{sv}", f"Sac biodégradable {sv.upper()}", priority="low")

    # ── 21. Comparatifs
    log("  → Comparatifs")
    comparatifs = [
        ("comparatif-poubelle-cuisine", "Comparatif poubelles de cuisine"),
        ("comparatif-poubelle-tri", "Comparatif poubelles de tri sélectif"),
        ("comparatif-poubelle-automatique", "Comparatif poubelles automatiques"),
        ("comparatif-poubelle-compost", "Comparatif poubelles à compost"),
        ("comparatif-poubelle-inox", "Comparatif poubelles inox"),
        ("comparatif-poubelle-bambou", "Comparatif poubelles bambou"),
        ("comparatif-poubelle-pedale", "Comparatif poubelles à pédale"),
        ("comparatif-cache-poubelle", "Comparatif cache-poubelle extérieur"),
        ("comparatif-simplehuman-brabantia", "Comparatif simplehuman vs Brabantia"),
        ("comparatif-poubelle-enfant", "Comparatif poubelles enfant"),
        ("comparatif-composteur-interieur", "Comparatif composteurs intérieurs"),
        ("comparatif-bac-roulant", "Comparatif bacs roulants"),
    ]
    for uk in USAGES:
        comparatifs.append((f"comparatif-poubelle-{uk}", f"Comparatif poubelles {USAGES[uk]}"))
    for vk in ["10l","20l","30l","50l","80l","120l"]:
        comparatifs.append((f"comparatif-poubelle-{vk}", f"Comparatif poubelles {vk.upper()}"))
    for brk in MARQUES:
        comparatifs.append((f"meilleure-poubelle-{brk}", f"Meilleure poubelle {MARQUES[brk]}"))

    for slug, title in comparatifs:
        add_page(pages, "comparatif", slug, title, priority="high")

    # ── 22. Guides informationnels
    log("  → Guides informationnels")
    guides = [
        ("comment-choisir-poubelle-cuisine", "Comment choisir sa poubelle de cuisine"),
        ("comment-choisir-poubelle-tri", "Comment choisir une poubelle de tri sélectif"),
        ("comment-choisir-cache-poubelle", "Comment choisir un cache-poubelle"),
        ("quelle-taille-poubelle-cuisine", "Quelle taille de poubelle pour la cuisine ?"),
        ("quelle-taille-poubelle-salle-de-bain", "Quelle taille de poubelle pour la salle de bain ?"),
        ("comment-recycler-plastique", "Comment recycler le plastique"),
        ("comment-recycler-verre", "Comment recycler le verre"),
        ("comment-recycler-papier", "Comment recycler le papier"),
        ("comment-composter", "Comment composter chez soi"),
        ("loi-agec-biodechets", "Loi AGEC : biodéchets obligatoires — ce qu'il faut savoir"),
        ("guide-tri-selectif-maison", "Guide du tri sélectif à la maison"),
        ("couleurs-bacs-poubelles-france", "Couleurs des bacs poubelles en France"),
        ("trier-dechets-appartement", "Comment trier ses déchets en appartement"),
        ("compost-appartement", "Faire son compost en appartement"),
        ("poubelle-bac-roulant-difference", "Différence entre poubelle et bac roulant"),
        ("nettoyer-poubelle", "Comment nettoyer sa poubelle"),
        ("poubelle-anti-odeur-test", "Poubelles anti-odeur : quelles sont les meilleures ?"),
        ("poubelle-automatique-vaut-il", "Poubelle automatique : ça vaut vraiment le coup ?"),
        ("matiere-poubelle-guide", "Quel matériau choisir pour sa poubelle ?"),
        ("entretien-bac-roulant", "Comment entretenir son bac roulant"),
        ("volume-poubelle-personne", "Quel volume de poubelle selon le nombre de personnes ?"),
        ("poubelle-cuisine-meilleure-marque", "Quelle est la meilleure marque de poubelle cuisine ?"),
        ("poubelle-design-pas-cher", "Poubelle design pas chère : les meilleures options"),
        ("biodechets-obligations-2024", "Biodéchets : obligations 2024 (loi AGEC)"),
        ("fabriquer-cache-poubelle-diy", "Fabriquer un cache-poubelle soi-même"),
        ("installer-cache-poubelle", "Comment installer un cache-poubelle extérieur"),
        ("poubelle-professionnelle-guide", "Choisir sa poubelle professionnelle"),
        ("poubelle-hopital-normes", "Poubelles hôpital : normes et obligations"),
        ("poubelle-restaurant-reglementation", "Poubelles restaurant : réglementation"),
        ("composteur-vs-vermicomposteur", "Composteur vs vermicomposteur : que choisir ?"),
        ("bac-compost-interieur-exterieur", "Compost intérieur ou extérieur : lequel choisir ?"),
        ("poubelle-cuisine-encastrable", "Poubelle de cuisine encastrable : guide"),
        ("poubelle-sous-evier", "Poubelle sous évier : les meilleures"),
        ("poubelle-mural-cuisine", "Poubelle murale pour cuisine"),
        ("bac-roulant-120l-240l", "Bac roulant 120L ou 240L : que choisir ?"),
        ("poubelle-noire-jaune-verte", "Poubelle noire, jaune ou verte : à quoi ça correspond ?"),
    ]
    for uk in USAGES:
        guides.append((f"guide-poubelle-{uk}", f"Guide poubelle {USAGES[uk]}"))
    for fk in FONCTIONS:
        guides.append((f"guide-{fk}", f"Guide {FONCTIONS[fk]}"))

    for slug, title in guides:
        add_page(pages, "guide", slug, title, priority="high")

    # ── 23. Questions (PAA — People Also Ask)
    log("  → Questions PAA")
    questions = [
        ("quelle-poubelle-sdb", "Quelle poubelle pour la salle de bain ?"),
        ("poubelle-sdb-taille", "Quelle taille de poubelle pour la salle de bain ?"),
        ("poubelle-cuisine-30l-assez", "30 litres suffisent pour une poubelle cuisine ?"),
        ("poubelle-automatique-hygienique", "La poubelle automatique est-elle plus hygiénique ?"),
        ("bambou-poubelle-ecologique", "La poubelle en bambou est-elle vraiment écologique ?"),
        ("inox-ou-plastique-poubelle", "Poubelle inox ou plastique : laquelle choisir ?"),
        ("poubelle-pedale-ou-capteur", "Poubelle à pédale ou capteur : quelle différence ?"),
        ("comment-eviter-mauvaises-odeurs", "Comment éviter les mauvaises odeurs de poubelle ?"),
        ("poubelle-tri-cuisine-pratique", "Comment organiser le tri sélectif dans la cuisine ?"),
        ("quelle-couleur-bac-recyclage", "Quelle couleur pour le bac de recyclage ?"),
        ("poubelle-compost-odeur", "La poubelle à compost sent-elle mauvais ?"),
        ("sac-poubelle-30l-dimensions", "Dimensions d'un sac poubelle 30L ?"),
        ("cache-poubelle-exterieur-diy", "Comment faire un cache-poubelle extérieur soi-même ?"),
        ("quelle-poubelle-van", "Quelle poubelle pour un van ?"),
        ("poubelle-bureau-quelle-taille", "Quelle taille de poubelle pour le bureau ?"),
        ("bac-jaune-quoi-dedans", "Que met-on dans le bac jaune ?"),
        ("poubelle-noire-que-mettre", "Que mettre dans la poubelle noire ?"),
        ("verre-poubelle-verte", "Le verre va-t-il dans la poubelle verte ?"),
        ("poubelle-camping-car-quelle", "Quelle poubelle pour camping-car ?"),
        ("poubelle-hopital-couleur", "Quelles sont les couleurs des poubelles à l'hôpital ?"),
    ]
    for slug, title in questions:
        add_page(pages, "question-paa", slug, title, priority="medium")

    # ── 24. Pages locales / géographiques
    log("  → Pages locales")
    villes = [
        "paris","lyon","marseille","toulouse","nice","nantes","bordeaux",
        "strasbourg","lille","rennes","reims","saint-etienne","toulon",
        "grenoble","dijon","angers","nimes","villeurbanne","le-mans",
        "aix-en-provence","clermont-ferrand","brest","limoges","tours",
        "amiens","metz","besancon","perpignan","orleans","rouen",
        "mulhouse","caen","nancy","argenteuil","montreuil","versailles"
    ]
    for v in villes:
        add_page(pages, "local", f"collecte-dechets-{v}", f"Collecte des déchets à {v.replace('-',' ').title()}", priority="low")
        add_page(pages, "local", f"jours-collecte-{v}", f"Jours de collecte des ordures à {v.replace('-',' ').title()}", priority="low")
        add_page(pages, "local", f"bac-roulant-{v}", f"Commander un bac roulant à {v.replace('-',' ').title()}", priority="low")

    # ── 25. Saisonnalité / événements
    log("  → Saisonnalité")
    saisonnier = [
        ("poubelle-noel-promo", "Promo poubelle Noël"),
        ("poubelle-soldes", "Poubelle : les meilleures offres des soldes"),
        ("poubelle-black-friday", "Poubelle Black Friday"),
        ("poubelle-saint-valentin", "Poubelle Saint-Valentin"),
        ("poubelle-demenagement", "Quelle poubelle choisir pour un déménagement"),
        ("poubelle-cuisine-renovation", "Quelle poubelle pour une cuisine rénovée"),
        ("poubelle-jardin-ete", "Poubelle jardin été : les meilleures options"),
        ("poubelle-pas-chere-budget", "Poubelle pas chère : les meilleures options budget"),
        ("poubelle-haut-de-gamme", "Poubelles haut de gamme : les meilleures"),
    ]
    for slug, title in saisonnier:
        add_page(pages, "saisonnalite", slug, title, priority="low")

    # ── 26. Trilingual / international (si expansion)
    log("  → Variantes BE/CH")
    intl = [
        ("poubelle-belgique", "Poubelle Belgique : guide complet"),
        ("poubelle-suisse", "Poubelle Suisse : guide complet"),
        ("sac-poubelle-officiel-belgique", "Sac poubelle officiel Belgique"),
        ("taxe-dechets-suisse", "Taxe déchets en Suisse : ce qu'il faut savoir"),
    ]
    for slug, title in intl:
        add_page(pages, "international", slug, title, priority="low")

    added = len(pages) - count_start
    log(f"  ✓ Phase 1 terminée : {added} pages ajoutées, total = {len(pages)}")
    return pages

# ─── Enrichissement Haloscan ──────────────────────────────────────────────────

def enrich_haloscan(pages, limit=200):
    """Interroge Haloscan sur les keywords les plus prioritaires."""
    log(f"=== PHASE 2 : Enrichissement Haloscan (max {limit} requêtes) ===")

    # Prioriser les pages sans données Haloscan
    to_enrich = [p for p in pages.values() if p["haloscan_volume"] is None and p["priority"] in ("top","high")]
    to_enrich = to_enrich[:limit]
    log(f"  → {len(to_enrich)} pages à enrichir")

    enriched = 0
    for page in to_enrich:
        keyword = page["title"]
        try:
            result = subprocess.run(
                [PYTHON_BIN, str(HALOSCAN_SCRIPT), "keyword", keyword, "highlights"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                results = data.get("results", [])
                if results:
                    top = results[0]
                    pages[page["slug"]]["haloscan_volume"] = top.get("volume")
                    pages[page["slug"]]["haloscan_kd"]     = top.get("allintitle")
                    pages[page["slug"]]["haloscan_cpc"]    = top.get("cpc")
                    enriched += 1
            time.sleep(0.5)  # respecter rate limit
        except Exception as e:
            log(f"    ⚠ Haloscan error pour '{keyword}': {e}")
            continue

        if enriched % 20 == 0 and enriched > 0:
            save_pages(pages)
            log(f"    → Sauvegarde : {enriched} enrichis")

    save_pages(pages)
    log(f"  ✓ Phase 2 : {enriched} pages enrichies")
    return pages

# ─── Export CSV ──────────────────────────────────────────────────────────────

def export_csv(pages):
    csv_file = OUTPUT_DIR / "pages.csv"
    categories = {}
    for p in pages.values():
        cat = p["category"]
        categories.setdefault(cat, []).append(p)

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Catégorie","Slug","Titre","Priorité","Volume","KD","CPC"])
        for cat in sorted(categories):
            for p in sorted(categories[cat], key=lambda x: x["title"]):
                writer.writerow([
                    cat, p["slug"], p["title"], p["priority"],
                    p["haloscan_volume"] or "", p["haloscan_kd"] or "", p["haloscan_cpc"] or ""
                ])
    log(f"  ✓ CSV exporté : {csv_file}")
    return csv_file

# ─── Stats ────────────────────────────────────────────────────────────────────

def print_stats(pages):
    from collections import Counter
    cats = Counter(p["category"] for p in pages.values())
    prios = Counter(p["priority"] for p in pages.values())
    enriched = sum(1 for p in pages.values() if p["haloscan_volume"] is not None)

    print(f"\n{'='*50}")
    print(f"TOTAL PAGES : {len(pages)}")
    print(f"Enrichies Haloscan : {enriched}")
    print(f"\nPar priorité :")
    for prio in ["top","high","medium","low"]:
        print(f"  {prio:8s} : {prios.get(prio, 0)}")
    print(f"\nTop 10 catégories :")
    for cat, count in cats.most_common(10):
        print(f"  {cat:40s} : {count}")
    print(f"{'='*50}\n")

# ─── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", default="all", choices=["all","systematic","haloscan","export","stats"])
    parser.add_argument("--limit", type=int, default=300, help="Nb max requêtes Haloscan")
    args = parser.parse_args()

    pages = load_pages()
    log(f"Pages existantes au démarrage : {len(pages)}")

    if args.phase in ("all", "systematic"):
        pages = generate_systematic(pages)
        save_pages(pages)
        export_csv(pages)

    if args.phase in ("all", "haloscan"):
        pages = enrich_haloscan(pages, limit=args.limit)
        export_csv(pages)

    if args.phase in ("all", "export"):
        export_csv(pages)

    if args.phase == "stats":
        print_stats(pages)
    else:
        print_stats(pages)

    log("Job terminé.")
