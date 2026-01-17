# projinit - Documentation Technique

Documentation technique approfondie du projet projinit v2.0.

## Table des Matieres

| Document | Description |
|----------|-------------|
| [Architecture](architecture.md) | Vue d'ensemble de l'architecture, modules, flux de donnees |
| [Standards YAML](standards.md) | Systeme de standards externalises, types de checks |
| [Templates Jinja2](templates.md) | Systeme de templates, personnalisation |
| [Detection de Projet](detection.md) | Algorithme de detection automatique du type |
| [Commandes CLI](cli.md) | Structure des commandes, ajout de nouvelles commandes |
| [Configuration](configuration.md) | Hierarchie de configuration, options disponibles |
| [Modeles de Donnees](models.md) | Classes et structures de donnees |

## Vue Rapide

```
projinit/
├── cli/           # Commandes CLI (check, new, update, config)
├── core/          # Logique metier (models, detector, checker, updater)
├── standards/     # Standards YAML externalises
└── templates/     # Templates Jinja2 (gitignore, precommit, commands)
```

## Concepts Cles

### 1. Standards-Driven

Le comportement de projinit est entierement defini par des fichiers YAML dans `standards/defaults/`. Chaque type de projet a son propre fichier de standards.

### 2. Template-Based Generation

La generation de fichiers utilise Jinja2. Les templates supportent des conditions basees sur le type de projet.

### 3. Detection Automatique

projinit detecte automatiquement le type de projet via un systeme de marqueurs ponderes.

### 4. Configuration Hierarchique

Configuration en 3 niveaux : defauts < global < local.

## Pour Commencer

1. Lire [Architecture](architecture.md) pour comprendre la structure globale
2. Consulter [Standards YAML](standards.md) pour personnaliser les checks
3. Voir [Templates](templates.md) pour ajouter de nouveaux fichiers generes
