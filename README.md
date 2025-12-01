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

> 🏗️ CLI pour générer la structure d'un projet avec configuration [Terraform](https://www.terraform.io/) + [GitHub](https://github.com/).

## 🔗 Technologies

| Outil | Description |
|-------|-------------|
| [Terraform](https://www.terraform.io/docs) | Infrastructure as Code |
| [GitHub Provider](https://registry.terraform.io/providers/integrations/github/latest/docs) | Provider Terraform pour GitHub |
| [uv](https://docs.astral.sh/uv/) | Package manager Python ultra-rapide |
| [direnv](https://direnv.net/) | Chargement automatique des variables d'environnement |
| [pass](https://www.passwordstore.org/) | Gestionnaire de mots de passe Unix |

## 📦 Installation

```bash
# Avec uv (recommandé)
uv tool install projinit

# Ou exécution directe
uvx projinit

# Ou installation classique
pip install projinit
```

> 💡 [uv](https://docs.astral.sh/uv/) est le gestionnaire de packages Python recommandé pour sa rapidité.

## 🚀 Utilisation

```bash
projinit
```

L'outil pose les questions suivantes de manière interactive :

1. 📝 **Nom du projet** — en slug-case (ex: `mon-projet`)
2. 💬 **Description** — optionnelle, auto-générée si vide
3. 👤 **Owner GitHub** — configurable via fichier de config
4. 👁️ **Visibilité** — `public` ou `private`
5. 🔐 **Direnv + pass** — pour la gestion sécurisée du token

## 📁 Structure générée

```
<nom-projet>/
├── .envrc                 # Si direnv activé
├── .gitignore
├── README.md
├── LICENSE
└── terraform/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    ├── versions.tf
    └── terraform.tfvars
```

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
# Cloner le projet
git clone https://github.com/xgueret/projinit.git
cd projinit

# Copier la configuration exemple
cp config.example.yaml config.yaml

# Installer en mode développement
uv sync

# Exécuter
uv run projinit
```

## 📄 Licence

MIT
