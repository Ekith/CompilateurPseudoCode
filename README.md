# Compilateur de langage pseudo code

## Introduction

Ce projet est un compilateur pour un langage de pseudo code. Le but du langage est de permettre la description d'algorithmes de manière simple et intuitive à l'aide d'un grand nombre de mots clés permettant une meilleure compréhension.

## Structure du projet

- `analex.py`: Contient l'analyseur lexical.
- `anasyn.py`: Contient l'analyseur syntaxique.
- `symboltable.py`: Contient la table des symboles.
- `main.py`: Point d'entrée dau compilateur. Il permet d'exécuter le processus de compilation sur le fichier `example/input.pcode`. Il génère un fichier `example/output.txt` contenant la sortie de l'analyseur lexical ainsi qu'un fichier `example/symbol_table.txt` pour la table des symboles.

## Fonctionnalités

- Analyse lexicale: Identification des mots clés, des identifiants et des symboles.
- Analyse syntaxique: Vérification de la structure syntaxique et sémantique du code.
- Gestion de la table des symboles: Stockage et récupération des informations sur les variables, les procédures et les fonctions. Les informations sont : 
  - Nom 
  - Type
  - Portée
  - Paramètres (pour les fonctions et procédures)
  - Mode (pour les paramètres des fonctions et procédures)

## Utilisation

Pour utiliser le compilateur, il suffit de fournir un fichier contenant du pseudo code. Le compilateur analysera le code et signalera les erreurs éventuelles.


## Exemples

Vous trouverez un exemple de code en pseudo code dans le fichier `example/input.pcode`.
Le résultat de l'analyse lexicale sera écrit dans `example/output.txt` et la table des symboles dans `example/symbol_table.txt`.

