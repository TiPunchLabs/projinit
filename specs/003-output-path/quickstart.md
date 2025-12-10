# Quickstart & Test Scenarios: Chemin de Destination Personnalisé

**Feature**: 003-output-path
**Date**: 2025-12-09

## Prerequisites

- projinit installé (`uv sync` exécuté)
- Accès en écriture sur `/tmp` et le home directory

## Test Scenarios

### Scenario 1: Comportement par défaut (User Story 1) - P1

**Objectif**: Vérifier que sans argument `--path`, le projet est créé dans le dossier courant.

```bash
# Préparation
cd /tmp
mkdir -p test-projinit-default
cd test-projinit-default

# Exécution
uv run projinit

# Réponses au questionnaire:
# - Nom: mon-projet
# - Description: (laisser vide)
# - Owner: (choisir le premier)
# - Visibilité: public
# - Direnv: non
# - Technologies: Terraform (par défaut)
# - Confirmer: oui

# Vérification
ls -la mon-projet/
# Doit afficher: .gitignore, README.md, LICENSE, terraform/
```

**Attendu**:
- [x] Le projet est créé dans `/tmp/test-projinit-default/mon-projet`
- [x] Aucune question sur le chemin n'est posée
- [x] Le récapitulatif affiche le chemin complet

---

### Scenario 2: Chemin absolu (User Story 2) - P1

**Objectif**: Vérifier que `--path` avec un chemin absolu fonctionne.

```bash
# Préparation
rm -rf /tmp/custom-projects

# Exécution
uv run projinit --path /tmp/custom-projects

# Réponses: nom=test-app, autres valeurs par défaut

# Vérification
ls -la /tmp/custom-projects/test-app/
```

**Attendu**:
- [x] Le dossier `/tmp/custom-projects` est créé automatiquement
- [x] Le projet est dans `/tmp/custom-projects/test-app`
- [x] Le récapitulatif affiche `/tmp/custom-projects/test-app`

---

### Scenario 3: Chemin relatif (User Story 2) - P1

**Objectif**: Vérifier que les chemins relatifs sont résolus correctement.

```bash
# Préparation
cd /tmp
mkdir -p test-relative
cd test-relative

# Exécution
uv run projinit -p ../other-projects

# Réponses: nom=relative-test, autres valeurs par défaut

# Vérification
ls -la /tmp/other-projects/relative-test/
```

**Attendu**:
- [x] Le chemin relatif `../other-projects` est résolu vers `/tmp/other-projects`
- [x] Le projet est créé dans `/tmp/other-projects/relative-test`
- [x] Le récapitulatif affiche le chemin absolu résolu

---

### Scenario 4: Chemin avec tilde (User Story 2) - P1

**Objectif**: Vérifier que le tilde est résolu vers le home directory.

```bash
# Exécution
uv run projinit --path ~/test-projinit

# Réponses: nom=tilde-test, autres valeurs par défaut

# Vérification
ls -la ~/test-projinit/tilde-test/
```

**Attendu**:
- [x] Le tilde est résolu vers `/home/<user>`
- [x] Le projet est créé dans le home directory
- [x] Le récapitulatif affiche le chemin absolu complet

---

### Scenario 5: Chemin inexistant avec création automatique (User Story 3) - P2

**Objectif**: Vérifier que les dossiers intermédiaires sont créés.

```bash
# Préparation
rm -rf /tmp/deep/nested/path

# Exécution
uv run projinit --path /tmp/deep/nested/path

# Réponses: nom=deep-test, autres valeurs par défaut

# Vérification
ls -la /tmp/deep/nested/path/deep-test/
```

**Attendu**:
- [x] `/tmp/deep/nested/path` est créé automatiquement
- [x] Le projet est dans `/tmp/deep/nested/path/deep-test`
- [x] Pas d'erreur lors de la génération

---

### Scenario 6: Chemin sans permission (User Story 3) - P2

**Objectif**: Vérifier qu'un message d'erreur clair est affiché si pas de permission.

```bash
# Exécution (requiert que /root ne soit pas accessible en écriture)
uv run projinit --path /root/test

# Attendu: Message d'erreur avant le questionnaire
```

**Attendu**:
- [x] Message d'erreur: `Erreur: Pas de permission d'écriture sur '/root'`
- [x] Le programme s'arrête immédiatement
- [x] Aucune question n'est posée

---

### Scenario 7: Chemin pointant vers un fichier (User Story 3) - P2

**Objectif**: Vérifier que le système détecte si le chemin est un fichier.

```bash
# Préparation
touch /tmp/existing-file

# Exécution
uv run projinit --path /tmp/existing-file

# Attendu: Message d'erreur
```

**Attendu**:
- [x] Message d'erreur: `Erreur: Le chemin '/tmp/existing-file' est un fichier, pas un dossier`
- [x] Le programme s'arrête immédiatement

---

### Scenario 8: Chemin vide (Edge Case)

**Objectif**: Vérifier que `--path ""` utilise le dossier courant.

```bash
# Préparation
cd /tmp/test-empty-path
mkdir -p /tmp/test-empty-path

# Exécution
uv run projinit --path ""

# Réponses: nom=empty-path-test, autres valeurs par défaut

# Vérification
ls -la /tmp/test-empty-path/empty-path-test/
```

**Attendu**:
- [x] Le comportement est identique à sans argument `--path`
- [x] Le projet est créé dans le dossier courant

---

### Scenario 9: Projet existant dans le chemin cible (Edge Case)

**Objectif**: Vérifier que l'erreur de projet existant fonctionne toujours.

```bash
# Préparation
mkdir -p /tmp/test-existing/already-exists

# Exécution
uv run projinit --path /tmp/test-existing

# Réponses: nom=already-exists

# Attendu: Erreur "Le dossier existe déjà"
```

**Attendu**:
- [x] Le système détecte que le dossier `already-exists` existe
- [x] Message d'erreur identique au comportement actuel

---

## Cleanup

```bash
# Nettoyer tous les dossiers de test
rm -rf /tmp/test-projinit-default
rm -rf /tmp/custom-projects
rm -rf /tmp/other-projects
rm -rf /tmp/test-relative
rm -rf ~/test-projinit
rm -rf /tmp/deep
rm -rf /tmp/existing-file
rm -rf /tmp/test-empty-path
rm -rf /tmp/test-existing
```

## Help Option Verification

```bash
# Vérifier que l'aide affiche l'option --path
uv run projinit --help
```

**Attendu dans l'aide**:
```
  -p PATH, --path PATH  Chemin de destination pour le projet (défaut: dossier courant)
```
