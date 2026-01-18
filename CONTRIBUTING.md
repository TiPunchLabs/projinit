# Contributing to projinit

Merci de votre interet pour contribuer a projinit !

## Comment Contribuer

### Signaler un Bug

1. Verifiez que le bug n'a pas deja ete signale dans les [issues](https://github.com/TiPunchLabs/projinit/issues)
2. Creez une nouvelle issue avec:
   - Description claire du probleme
   - Etapes pour reproduire
   - Comportement attendu vs obtenu
   - Version de projinit (`projinit version`)

### Proposer une Fonctionnalite

1. Ouvrez une issue pour discuter de l'idee
2. Attendez la validation avant de coder
3. Suivez le processus de Pull Request

### Soumettre du Code

1. Forkez le repository
2. Creez une branche feature (`git checkout -b feature/amazing-feature`)
3. Commitez vos changements (`git commit -m 'feat: add amazing feature'`)
4. Pushez la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## Convention de Commits

Nous utilisons [Conventional Commits](https://www.conventionalcommits.org/):

| Type | Description |
|------|-------------|
| `feat:` | Nouvelle fonctionnalite |
| `fix:` | Correction de bug |
| `docs:` | Documentation uniquement |
| `style:` | Formatage (pas de changement de code) |
| `refactor:` | Refactoring sans changement fonctionnel |
| `test:` | Ajout ou modification de tests |
| `chore:` | Maintenance, dependencies |

Exemple: `feat(cli): add --verbose flag to check command`

## Style de Code

### Python

- Python >= 3.10
- Formatage avec `ruff format`
- Linting avec `ruff check`
- Type hints obligatoires pour les fonctions publiques

### Verification avant commit

```bash
# Linting
uvx ruff check src/

# Formatage
uvx ruff format src/

# Tests
uv run pytest
```

## Structure du Projet

```
projinit/
├── src/projinit/
│   ├── cli/           # Commandes CLI
│   ├── core/          # Logique metier
│   ├── standards/     # Standards YAML
│   └── templates/     # Templates Jinja2
├── tests/             # Tests pytest
└── docs/              # Documentation technique
```

## Tests

- Tous les tests doivent passer avant merge
- Ajoutez des tests pour les nouvelles fonctionnalites
- Coverage minimum : 50%

```bash
# Lancer les tests
uv run pytest

# Avec coverage
uv run pytest --cov=projinit
```

## Documentation

- Mettez a jour la documentation si necessaire
- Docstrings Google style pour les fonctions publiques
- README.md pour les changements majeurs

## Questions ?

Ouvrez une issue pour toute question ou suggestion.
