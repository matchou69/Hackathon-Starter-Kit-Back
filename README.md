# Starter-Kit-Back

<img src="./doc/assets/genee.png" alt="Image 1" width="150px">

STARTER est un projet de backend développé avec [Python](https://www.python.org/)
et [Flask](https://flask.palletsprojects.com/en/2.3.x/).

## Dépendances Principales

- [Flask](https://flask.palletsprojects.com/en/2.3.x/) : Une micro framework pour Python.
- [SQLAlchemy](https://www.sqlalchemy.org/) : Un SQL toolkit et ORM pour Python.
- [graphql](https://graphql.org) : Une bibliothèque pour les requetes http et
  pour la communication de données.
- [Docker](https://www.docker.com/) : Une plateforme de conteneurisation.
- [Docker Compose](https://docs.docker.com/compose/) : Un outil pour définir et gérer des applications multi-conteneurs
  avec Docker.

## Structure du Projet

Dans le répertoire `app/`, chaque sous-répertoire représente un module ou une fonctionnalité distincte de l'application.
Chaque module contient les sous-répertoires suivants :

- `data/` : Ce répertoire contient le code source de l'application.
- `error/` : Ce répertoire contient les erreurs pouvant etre survenu pendant l'utilisation de l'application
- `shared/` : Ce répertoire contient les initialisations de l'application.
- `repositories/` : Ce répertoire contient les classes de répertoire qui gèrent la persistance des données pour le
  module.

```markdown
.
├── app
│   ├── data
│   │   └── Contient le code de l'application
│   ├── errors
│   └── shared
├── doc
├── envs
│   ├── dev
│   ├── prod
│   └── shared
├── migrations
│
└── scripts

```

## Installation

### Prérequis

Pour exécuter cette application, vous devez avoir Docker et Docker Compose installés sur votre système.

#### Installation de Docker

##### Sur Linux

1. Mettez à jour l'index du paquet `apt` :
   ```sh
   sudo apt-get update
   ```
2. Installez les paquets permettant à `apt` d'utiliser un dépôt sur HTTPS :
   ```sh
   sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
   ```
3. Ajoutez la clé GPG officielle de Docker :
   ```sh
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   ```
4. Ajoutez le dépôt Docker à vos sources `APT` :
   ```sh
   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
   ```
5. Mettez à jour l'index du paquet `apt` et installez Docker CE :
   ```sh
   sudo apt-get update
   sudo apt-get install docker-ce
   ```

##### Sur Mac

1. Téléchargez Docker Desktop pour Mac
   depuis [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-mac/).
2. Ouvrez le fichier `.dmg` téléchargé et glissez l'icône de Docker dans votre dossier `Applications`.
3. Ouvrez Docker Desktop depuis vos `Applications`.

#### Installation de Docker Compose

##### Sur Linux

1. Téléchargez la version actuelle de Docker Compose :
   ```sh
   sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   ```
2. Appliquez les permissions d'exécution au binaire :
   ```sh
   sudo chmod +x /usr/local/bin/docker-compose
   ```

##### Sur Mac

Docker Compose est déjà inclus dans Docker Desktop pour Mac, donc aucune étape supplémentaire n'est nécessaire.

### Lancement de l'application

Ouvrez une invite de commande ou un terminal.

- lancer les docker 
```shell
docker-compose -f envs/dev/docker-compose.yml up 
``` 

sans oublier le .env prévu pour ``envs/dev/back/.env``

# Installation de Pycharm
Pycharm est l'IDE Python de jetbrains, pour avoir acces au programme par l'IDE sans erreurs demande quelques modification

### changer l'interpreter pour avoir les modules du projet sans les installer localement
- aller là ou il y a possiblement écrit ``Python 3.9`` et cliquer dessus
- ``add new interpreter`` et choisir ``docker-compose``
- définir le docker-compose suivant : ``envs/dev/docker-compose.yml``
- si en bas a gauche il y a ecrit ``Remote docker-Compose`` vous avez tout pour commencer

### explication des scripts
- ``tester.sh`` permet de tester toutes les requetes graphql reférencée
  - les arguments : 
    - -d permet de définir si les dockers sont dépendant du programme,
    si utilisé les dockers se lanceront par le testers et vous n'aurez que le retour du tester en lui meme
    - sinon doit etre rattaché au docker-compose deja lancé
- ``application_resatart.sh`` permet quand les dockers sont lancés, a l'interruption de ceux-ci par le billet du raccourcis ctrl-c ce relance tout seul en nettoyant la base de donnée

### mise en place du format par lint

``black`` permet de formatter le code 
- premièrement bien verifier que Black est bien installé : 

```shell
python3 -m pip install Black
```

- ensuite pour le mettre directement sur la fonction ``format code`` de pycharm il faut aller dans ``parametres>tools>black``, mettre l'``Execution mode`` en ``Binary`` et activer ``on code reformat``

### mise en place de la visualisation de la base de donnée

cliquez sur le logo qui ressemble a une pile de disque sur le coté droit, si vous ne le voyez pas,
assurez vous que le plugin ``Database tools and SQL`` soit bien installé.
une fois le menu ouvert, aller dans le logo ``+`` cherchez dans ``data sources`` ``PostgreSQL`` et mettez les informations suivantes : 
``port: 5432`` ``host: localhost``
``connect with user and password`` ``password: postgres``  ``user: postgres``

> **NOTE**: assurez vous bien pendant la connexion avec le docker postgres que le docker soit lancé

une fois connecté vous verrez a droite : ``postgres@localhost`` cliquez sur ``1 of 4``et cochez ``db_dev`` et ``all schema`` dans ``db_dev``
une fois fait vous aurez vos table dans ``db_dev/public/tables``