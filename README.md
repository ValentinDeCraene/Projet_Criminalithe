# Projet Criminalithé :

Projet Python réalisé par Valentin De Craene dans le cadre du module de formation au langage de programmation Python du master TNAH de l'Ecole Nationale des Chartes, 2021-2022. Le projet Criminalithé a donc pour but de mettre à disposition d'un public de chercheurs et d'érudits les données constituées des amendes extraites des registres du bailliage de Lille pour la période 1429-1441, conservés aux Archives Départementales du Nord. A ce jour, les années 1430 à 1434 sont couvertes. Ce travail se fonde sur les travaux de Valentin De Craene réalisés dans le cadre d'un mémoire de master 1, soutenu à l'Université de Lille en 2018.

Les consignes initiales sont les suivantes :

- Réalisation d'une application avec base de données relationnelle, comprenant formulaire pour ajout, suppression, édition.
- Il doit être possible de naviguer dans la collection, d'y faire une recherche simple voire complexe, un index doit y être inclus.
- Pour plus de détails, se référer à ce document (https://github.com/PonteIneptique/cours-python/wiki/2021-2022-Devoir).



# Installation et utilisation :

Nota : commandes à exécuter dans le terminal (Linux ou macOS).

Cloner le dossier : ```git clone https://github.com/ValentinDeCraene/Projet-Criminalithe.git```

Installer l'environnement virtuel : ```sudo apt-get install python3 libfreetype6-dev python3-pip python3-virtualenv```

Vérifier que la version de Python est bien 3.x : ```python --version```;

Aller dans le dossier : ```cd Projet-Criminalithe```;

Installer l'environnement : ```virtualenv ~/.Projet-Criminalithe -p python3```;

Activer l'environnement : ```source ~/.Projet-Criminalithe/bin/activate```;
        
Lancer la commande: ```pip install -r requirements.txt```.

(!) Déplacez-vous dans le dossier de l'application (!) : ```cd Criminalithe```

Lancer l'application : ```python3 run.py``` ;

Aller sur http://127.0.0.1:5000/
