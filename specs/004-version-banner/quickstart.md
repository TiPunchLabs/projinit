# Quickstart: Version Banner Stylisé

## Test Manuel

### Scénario 1: Affichage avec --version

```bash
cd /home/xgueret/Workspace/01-projets/tools/projinit
uv run projinit --version
```

**Résultat attendu**:
- Banner ASCII "PROJINIT" en bleu
- Tagline sous le banner
- Version du CLI
- Section Description
- Section Features (5 items)
- Section Usage (3 exemples)

### Scénario 2: Affichage avec -v (alias court)

```bash
uv run projinit -v
```

**Résultat attendu**: Identique à `--version`

### Scénario 3: Cohérence avec sous-commande version

```bash
uv run projinit version
```

**Résultat attendu**: Même affichage que `--version`

## Validation

- [ ] Le banner ASCII s'affiche correctement
- [ ] La version affichée correspond à `__version__`
- [ ] Les 5 features sont listées
- [ ] Les 3 exemples d'usage sont présents
- [ ] `-v` et `--version` produisent le même résultat
- [ ] `projinit version` produit le même résultat
