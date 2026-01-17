# GitHub Repository Terraform

Configuration Terraform pour gérer le dépôt GitHub [TiPunchLabs/projinit](https://github.com/TiPunchLabs/projinit).

## Prérequis

- Terraform >= 1.11.0
- Un Personal Access Token GitHub avec les permissions `repo` et `admin:org`

## Utilisation

1. Copier le fichier d'exemple des variables :
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. Éditer `terraform.tfvars` avec votre token :
   ```hcl
   github_token = "ghp_votre_token"
   github_owner = "TiPunchLabs"
   ```

3. Initialiser Terraform :
   ```bash
   terraform init
   ```

4. Importer le repo existant (première fois uniquement) :
   ```bash
   terraform import github_repository.projinit projinit
   ```

5. Vérifier le plan :
   ```bash
   terraform plan
   ```

6. Appliquer les changements :
   ```bash
   terraform apply
   ```

## Ressources créées

- **github_repository.projinit** : Le dépôt GitHub avec :
  - Issues activées
  - Wiki désactivé
  - Suppression automatique des branches après merge
  - Topics pour la découvrabilité

## Outputs

| Output | Description |
|--------|-------------|
| `repository_name` | Nom du dépôt |
| `repository_url` | URL web du dépôt |
| `repository_id` | ID interne GitHub |
| `clone_url` | URL SSH pour cloner |
