# Fondations LLM et mémoire conversationnelle

Exemples Python autonomes autour de trois briques LangChain, exécutées avec un
modèle Ollama local :

- consignes de prompt qui séparent rôle, contexte et demande;
- sortie structurée validée par un schéma Pydantic;
- historique de conversation tronqué selon une estimation de budget de tokens.

L'estimation de tokens est volontairement indicative; elle ne remplace pas le
tokenizer du modèle. L'historique reste en mémoire du processus et n'est pas
persisté sur disque.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows : .venv\Scripts\activate
python -m pip install -e ".[dev]"
cp .env.example .env
ollama pull llama3.2
```

Le nom du modèle, l'URL Ollama et le budget de l'historique se configurent dans
`.env`.

## Démarrer le chat

```bash
python main.py
```

Quittez avec `exit` ou `quit`. Les exemples de sortie structurée se trouvent
dans `structured_output.py`.

## Tests

```bash
pytest
```

## Variables d’environnement

- `OLLAMA_MODEL` : modèle local (défaut `llama3.2`).
- `OLLAMA_BASE_URL` : URL du serveur Ollama (défaut `http://localhost:11434`).
- `MAX_HISTORY_TOKENS` : budget indicatif de l’historique (défaut `388`, doit être positif).

## Exemple de sortie structurée

Exemple indicatif conforme au schéma Pydantic `ReviewOutput` :

```json
{
  "summary": "Le retour apprécie l’interface et signale un chargement lent.",
  "positive_points": ["L’interface est appréciée."],
  "improvement_points": ["Améliorer la vitesse de chargement."]
}
```
