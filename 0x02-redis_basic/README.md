# Cache System with Redis

## Description

Ce projet implémente un système de cache simple en utilisant Redis. Il permet de stocker, récupérer et suivre les données avec des fonctionnalités telles que le comptage des appels et l'historique des entrées/sorties. Ce projet utilise des décorateurs Python pour étendre la fonctionnalité de la méthode principale de stockage.

## Fonctionnalités

- **Stockage des données** : Permet de stocker des données avec des clés générées aléatoirement dans Redis.
- **Récupération de données** : Permet de récupérer des données stockées en utilisant leur clé.
- **Conversion des données** : Supporte la conversion des données en chaîne de caractères (`str`) ou en entiers (`int`) lors de la récupération.
- **Suivi des appels** : Compte combien de fois une méthode spécifique est appelée.
- **Historique des appels** : Enregistre les arguments et les résultats de chaque appel de méthode pour un suivi facile.

## Prérequis

- Python 3.x
- Redis

## Installation

1. Assurez-vous d'avoir Python et Redis installés sur votre machine.
2. Installez la bibliothèque Redis pour Python :
   ```bash
   pip install redis

