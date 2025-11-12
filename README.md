# Projet Spark - Exercices

Courte description
- Ensemble d'exercices et d'exemples pour travailler avec Kafka, Spark Structured Streaming, et la sortie vers HDFS.

Fichiers importants
- `dashboard.py` — script principal à pousser.
- `exercices.ipynb` — notebook d'exercices à pousser.
- `checkpoint/`, `checkpoint_hdfs_write/` — dossiers de checkpoint (ignorés par défaut).
- `model/` — notebooks supplémentaires et modèles (ignorés par défaut).

Dépendances minimales
- Python 3.8+
- kafka-python
- requests
- pyspark
- streamlit (optionnel)

Commandes rapides (PowerShell)
```powershell
# Afficher l'état Git
git status

# Ajouter tous les changements et commiter
git add .
git commit -m "Ajout README et .gitignore"

# Pousser vers la branche principale
git push origin main
```

Remarques
- Le `.gitignore` du projet est configuré pour n'inclure que `dashboard.py` et `exercices.ipynb` au niveau racine. Pour autoriser d'autres fichiers, modifiez `.gitignore`.
