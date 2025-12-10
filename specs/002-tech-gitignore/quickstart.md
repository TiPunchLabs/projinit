# Quickstart: Test de la Sélection de Technologies

**Feature**: 002-tech-gitignore
**Date**: 2025-12-09

## Prérequis

- Python >= 3.10
- uv installé
- Projet projinit cloné

## Installation Dev

```bash
cd /path/to/projinit
uv sync
```

## Scénarios de Test

### Scénario 1: Sélection par défaut (Terraform seul)

**Objectif**: Vérifier que Terraform est présélectionné et que le .gitignore minimal fonctionne.

```bash
# Lancer projinit
uv run projinit

# Répondre aux questions :
# - Nom: test-default
# - Description: (vide)
# - Owner: (premier choix)
# - Visibilité: public
# - Direnv: non
# - Technologies: [garder Terraform sélectionné, valider]

# Vérifier le résultat
cat test-default/.gitignore
```

**Résultat attendu**:
```
# Common
.DS_Store
Thumbs.db
*.log
.direnv/
*~

# Terraform
.terraform/
*.tfstate
*.tfstate.*
*.tfvars.backup
.terraform.lock.hcl
```

### Scénario 2: Multi-technologies (Python + Terraform + Docker)

**Objectif**: Vérifier la concaténation de plusieurs fragments.

```bash
uv run projinit

# Technologies: sélectionner Python, Terraform, Docker
```

**Résultat attendu**: .gitignore contenant les 3 sections + common.

### Scénario 3: Toutes les technologies

**Objectif**: Vérifier que tous les fragments se concatènent correctement.

```bash
uv run projinit

# Technologies: tout sélectionner
```

**Résultat attendu**: .gitignore avec 7 sections (common + 6 technos).

### Scénario 4: Aucune technologie

**Objectif**: Vérifier le cas limite où l'utilisateur désélectionne tout.

```bash
uv run projinit

# Technologies: tout désélectionner
```

**Résultat attendu**: .gitignore contenant uniquement la section common.

### Scénario 5: Affichage dans le résumé

**Objectif**: Vérifier que les technologies sélectionnées apparaissent dans le récapitulatif.

```bash
uv run projinit

# Sélectionner Python et Go
# Vérifier le récapitulatif avant confirmation
```

**Résultat attendu**:
```
Récapitulatif :
  Nom        : mon-projet
  Description: Projet mon-projet
  Owner      : mon-owner
  Visibilité : public
  Direnv     : non
  Technologies: Python, Go
```

## Validation Manuelle

Après chaque test, vérifier :

1. ✅ Le fichier .gitignore existe dans le projet généré
2. ✅ Chaque section est précédée d'un commentaire identifiant
3. ✅ Pas de lignes vides excessives entre sections
4. ✅ Le commit initial inclut le .gitignore

## Nettoyage

```bash
# Supprimer les projets de test
rm -rf test-default test-multi test-all test-none mon-projet
```
