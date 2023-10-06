# STARTER-BACK

<img src="./doc/assets/genee.png" alt="Image 1" width="150px">

STARTER-BACK est un projet de backend développé avec [Python](https://www.python.org/)
et [Flask](https://flask.palletsprojects.com/en/2.3.x/).

## Gestion de version Git
- Respect du [Git Flow](https://www.atlassian.com/fr/git/tutorials/comparing-workflows/gitflow-workflow) : 
  - Une branche "develop" commune aux développements en cours
    - Chaque branche de dev part de la branche "develop"
  - Une branche "release" de recette
  - Une branche "master" de production

- Gestion des commits
  - Commits "utiles" uniquement (pas de succession de commits "Fix TU")
  - Messages de commit en français

## Style
- Suivi des règles du PEP8
  - La longueur des lignes a été augmenté à 140 caractères pour encourager les noms de méthode explicites
- Le code est inspecté/clean à chaque commit grâce au pre-commit exécutant 3 outils
  - [Black](https://black.readthedocs.io/en/stable/) qui re-formatte le code suivant les règles de PEP8
  - [Flake8](https://flake8.pycqa.org/en/latest/) qui suit également les règles de PEP8 et annule le commit en cas d'erreur de lint
  - [iSort](https://pycqa.github.io/isort/) qui reformatte les imports
> **INFO** : Lors d'un commit, si Black reformate un fichier, alors le pre-commit sera failed. C'est normal, car Black estime que
si un fichier est modifié, alors il ne doit pas être commit automatiquement.
> Dans ce cas, relancer le commit et celui-ci passera.
- Le code est ensuite une nouvelle fois analysé par SonarQube
  - Si l'analyse Sonar fail, la branche ne peut être mergée

### Règles plus précises
- Ce qui est en lien avec le métier en français, le reste en anglais
- Attention à l'abus de commentaires : Python est très expressif et un bon code avec de
  méthodes explicites se comprend de lui même la plupart du temps
- Attention a ne pas dupliquer du code, pensez à réutiliser ou factoriser
  - Make it Work, Make it Right, Make it Fast
- Prendre le temps de tout nommer correctement
- Pas de `except` global ou de `except Exception`
- Pas de fonction trop longue (~30 Lignes)
- Pas de fichier trop long (~300 Lignes)
- Pour les chaînes de caractères comportant des variables : utiliser les fstring plutôt que % ou format :
```python
exemple = f'le texte avec { une_variable } en utilisant les f-string'
```
- Sur les API de listes, préférer un retour de liste vide en 200 plutôt qu'une erreur si jamais 
aucun résultat n'est trouvé.
- Les chaînes en dur doivent être extraites dans des constantes si elles sont réutilisées
- Les noms de variables doivent être pertinents et explicites
- Attention au code mort !

## Process de dev
- Pour les chantiers moyens à gros, réalisation d'un DCT avant de débuter les développements
- Lorsqu'un choix technique doit être réalisé (ex.: choix d'une librairie plutôt qu'une autre), écriture d'un
ADR (Architecture Decision Record)
- Profiter des chantiers pour mettre à jour les versions mineures des dépendances présentes dans
`app/requirements.txt` et `app/requirements-dev.txt`
- La fonctionnalité doit être testée en local par le développeur
- Si la méthode d'installation et/ou d'exploitation est modifiée suite à un chantier, rédiger
une nouvelle version des manuels adéquats

## Création d'une release
Afin de modifier le numéro de version du projet, il suffit de lancer la commande suivante dans le virtual-env Python 
à la racine du projet :
```shell
bumpversion <major|minor|patch>
```
Exemple, pour passer de la version 1.2.3 à la version 1.3.0 :
```shell
bumpversion minor
```

## Gestion des dépendances
La gestion des dépendances du projet utilise pip-tools. Cet outil permet, à la manière des package-lock.json sur les
projets Node, de freeze la totalité des dépendances (directes et indirectes) du projet.

pour installer pip-tools :
```shell
pip install pip-tools
```

Les dépendances directes sont spécifiées dans le fichier `pyproject.toml`à la racine du projet.

Les fichiers requirements.txt et requirements-dev.txt situés dans le dossier app ne doivent pas être modifiés manuellement.

En cas de changement de dépendance directe (ajout, modification, suppression) :
- Modifier le fichier pyproject.toml
  - Si la dépendance sert au fonctionnement nominal de l'application
    - Toucher à la section [project] > dependencies
    - Lancer les commandes suivantes :
      ```shell
      pip-compile --upgrade --output-file=app/requirements.txt pyproject.toml
      pip-compile --upgrade --extra=dev --output-file=app/requirements-dev.txt pyproject.toml
      ```
    > **INFO** : sur macos, si les commandes precedentes ne marchent pas executez les commandes suivantes :
    > - ``brew install postgresql``
    > - ``pip install psycopg2-binary ``
    - Si la dépendance sert uniquement à l'environnement de dev ou de CI
      - Toucher à la section [project.optional-dependencies] > dependencies
      - Lancer la commande suivante :
      ```shell
      pip-compile --upgrade --extra=dev --output-file=app/requirements-dev.txt pyproject.toml 
      ```
La commande pip-compile permet de générer les fichiers requirements.txt et requirements-dev.txt, qui contiennent les dépendances
directes et indirectes et leurs versions figées.