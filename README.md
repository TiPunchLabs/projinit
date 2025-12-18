# projinit

```
██████╗ ██████╗  ██████╗      ██╗██╗███╗   ██╗██╗████████╗
██╔══██╗██╔══██╗██╔═══██╗     ██║██║████╗  ██║██║╚══██╔══╝
██████╔╝██████╔╝██║   ██║     ██║██║██╔██╗ ██║██║   ██║
██╔═══╝ ██╔══██╗██║   ██║██   ██║██║██║╚██╗██║██║   ██║
██║     ██║  ██║╚██████╔╝╚█████╔╝██║██║ ╚████║██║   ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝
            Project Scaffolding with Terraform + GitHub
```

[![CI](https://github.com/TiPunchLabs/projinit/actions/workflows/ci.yml/badge.svg)](https://github.com/TiPunchLabs/projinit/actions/workflows/ci.yml)

> 🏗️ CLI pour générer la structure d'un projet avec configuration [Terraform](https://www.terraform.io/) + [GitHub](https://github.com/).

> 🐧 **Linux first** — Conçu pour les environnements Linux. Peut fonctionner sur macOS, non testé sur Windows.

## 🔗 Technologies

| Outil | Description |
|-------|-------------|
| [Terraform](https://www.terraform.io/docs) | Infrastructure as Code |
| [GitHub Provider](https://registry.terraform.io/providers/integrations/github/latest/docs) | Provider Terraform pour GitHub |
| [uv](https://docs.astral.sh/uv/) | Package manager Python ultra-rapide |
| [direnv](https://direnv.net/) | Chargement automatique des variables d'environnement |
| [pass](https://www.passwordstore.org/) | Gestionnaire de mots de passe Unix |

## 📦 Installation

### Depuis les sources

```bash
# Cloner le dépôt
git clone https://github.com/xgueret/projinit.git
cd projinit

# Installer les dépendances
uv sync

# Copier et personnaliser la configuration
cp config.example.yaml ~/.config/projinit/config.yaml
```

### Installation globale (recommandé)

```bash
# Installer comme outil global
uv tool install /chemin/vers/projinit

# Ou directement depuis GitHub
uv tool install git+https://github.com/xgueret/projinit.git

# Configurer (obligatoire)
mkdir -p ~/.config/projinit
curl -o ~/.config/projinit/config.yaml https://raw.githubusercontent.com/xgueret/projinit/main/config.example.yaml
# Puis éditer ~/.config/projinit/config.yaml avec vos owners
```

> ⚠️ **Important** : Sans fichier de configuration, le CLI utilisera des valeurs par défaut génériques.

### 🔄 Mise à jour

```bash
# Si installé depuis les sources
cd /chemin/vers/projinit
git pull
uv sync

# Si installé globalement depuis un dossier local
uv tool upgrade projinit

# Si installé depuis GitHub
uv tool upgrade projinit --reinstall
```

> 💡 [uv](https://docs.astral.sh/uv/) est le gestionnaire de packages Python recommandé pour sa rapidité.

## 🚀 Utilisation

```bash
# Si installé globalement (génère dans le dossier courant)
projinit

# Spécifier un chemin de destination
projinit --path ~/mes-projets

# Depuis le dossier du projet projinit (après uv sync)
uv run projinit

# Avec un chemin personnalisé
uv run projinit -p /tmp/projets
```

### Options

| Option | Description |
|--------|-------------|
| `-p PATH`, `--path PATH` | Chemin de destination pour le projet (défaut: dossier courant) |
| `-v`, `--version` | Affiche les informations de version détaillées avec banner ASCII |
| `-h`, `--help` | Affiche l'aide |

L'outil pose les questions suivantes de manière interactive :

1. 📝 **Nom du projet** — en slug-case (ex: `mon-projet`)
2. 💬 **Description** — optionnelle, auto-générée si vide
3. 👤 **Owner GitHub** — configurable via fichier de config
4. 👁️ **Visibilité** — `public` ou `private`
5. 🔐 **Direnv + pass** — pour la gestion sécurisée du token
6. 🛠️ **Technologies** — sélection multiple organisée par catégories :
   - **Langages** : Python, Node.js, Go, Rust, Java/Kotlin
   - **Front-end** : HTML/CSS, React, Vue.js, Angular, Svelte, Next.js/Nuxt.js
   - **Infrastructure** : Terraform, Pulumi, Kubernetes/Helm
   - **Conteneurs** : Docker
   - **Automation** : Ansible, Shell/Bash
   - **Outils** : IDE (VSCode/JetBrains), GitHub Actions

## 📁 Structure générée

```
<nom-projet>/
├── .envrc                      # Si direnv activé
├── .gitignore                  # Adapté aux technologies sélectionnées
├── .pre-commit-config.yaml     # Hooks pre-commit selon les technologies
├── README.md
├── LICENSE
└── terraform/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    ├── versions.tf
    └── terraform.tfvars
```

> 💡 Les fichiers `.gitignore` et `.pre-commit-config.yaml` sont générés dynamiquement en fonction des technologies sélectionnées (19 technologies disponibles organisées en 6 catégories).

## ⚙️ Configuration

projinit utilise un fichier de configuration YAML pour personnaliser les options.

### 📍 Emplacement du fichier

Le fichier est recherché dans l'ordre suivant :

1. `./config.yaml` (dossier courant)
2. `~/.config/projinit/config.yaml` (configuration globale)

### 🔧 Créer votre configuration

```bash
# Copier l'exemple
cp config.example.yaml config.yaml

# Ou pour une config globale
mkdir -p ~/.config/projinit
cp config.example.yaml ~/.config/projinit/config.yaml
```

### 📋 Options disponibles

```yaml
# Propriétaires GitHub disponibles
owners:
  - name: "mon-user"
    label: "mon-user (personnel)"
  - name: "mon-org"
    label: "mon-org (organisation)"

# Chemin du secret dans pass
pass_secret_path: "github/terraform-token"

# Valeurs par défaut
defaults:
  visibility: "public"
  use_direnv: false
```

## 🔐 Prérequis pour direnv

Si vous activez l'option direnv + pass :

- ✅ [`direnv`](https://direnv.net/) doit être installé
- ✅ [`pass`](https://www.passwordstore.org/) doit être installé
- ✅ Le secret configuré dans `pass_secret_path` doit exister

## 🛠️ Développement

```bash
# Cloner et installer (voir section Installation)
git clone https://github.com/xgueret/projinit.git
cd projinit
uv sync

# Exécuter en développement
uv run projinit

# Lancer les tests (à venir)
uv run pytest
```

## 📄 Licence

MIT
