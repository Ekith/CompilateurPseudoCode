# Compilateur de langage pseudo code

## Introduction

Ce projet est un compilateur pour un langage de pseudo code. Le but du langage est de permettre la description d'algorithmes de manière simple et intuitive à l'aide d'un grand nombre de mots clés permettant une meilleure compréhension.

## Structure du projet

- `analex.py`: Contient l'analyseur lexical.
- `anasyn.py`: Contient l'analyseur syntaxique.
- `symboltable.py`: Contient la table des symboles.
- `main_test.py`: Il permet d'exécuter le processus de compilation sur le fichier `example/input.pcode`. Il génère un fichier `example/output.txt` contenant la sortie de l'analyseur lexical ainsi qu'un fichier `example/symbol_table.txt` pour la table des symboles.
- `main.py`: Point d'entrée du compilateur.

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

```bash
./pcodeCompiler.sh input_file
```
Options :
- `-o <fichier>` : Spécifie le fichier de sortie.
- `-st <fichier>` : Spécifie le fichier de la table des symboles.
- `-al <fichier>` : Spécifie le fichier de sortie de l'analyse lexicale.
- `-h` : Affiche l'aide.

## Exemples

Vous trouverez un exemple de code en pseudo code dans le fichier `example/input.pcode`.
Le résultat de l'analyse lexicale sera écrit dans `example/output.txt` et la table des symboles dans `example/symbol_table.txt`.

## Utilisation des instructions

### Corps principal du programme

```pcode
Programme <nom du programme>
    <Optionnel>
Debut Programme
    instruction1
    instruction2
Fin Programme
```

Vous pouvez ajouter des instructions supplémentaires dans le corps principal du programme. Soit l'un, soit l'autre soit les 2 mais dans cet ordre.

#### Déclarations des fonctions/procédures

```pcode
Prototypes :
    Fonction <nom de la fonction>(<paramètres>) -> <type de retour>
    Procedure <nom de la fonction>(<paramètres>)

Definitions :
    Fonction <nom de la fonction>(<paramètres>) -> <type de retour> :
    Debut
        instruction1
        instruction2
    Fin

    Procedure <nom de la fonction>(<paramètres>) :
    Debut
        instruction1
        instruction2
    Fin

```

#### Déclarations des variables

```pcode
Variables :
    <nom de la variable> : <type de la variable>
    <liste de variables> : <type des variables>
```

### Boucles

```pcode
Tant que <condition> Faire
    instruction1
    instruction2
Fin Tant que
```

### Conditions

```pcode
Si <condition> Alors
    instruction1
    instruction2
Fin Si
```

```pcode
Si <condition> Alors
    instruction1
    instruction2
Fin Si
Sinon
    instruction3
Fin Sinon
```

### Entrée-Sortie
Pour afficher une variable :
```pcode
afficher(<expression>)
```
Pour entrer une valeur dans une variable :
```pcode
lire(<variable>)
```

### Comparaison

Il a été décidé dans ce langage de s'affranchir des opérateurs de comparaison traditionnels tels que "==" et "!=". À la place, les mots clés "egal" et "diff" sont utilisés pour effectuer des comparaisons d'égalité et d'inégalité.
De même, les mots clés "inf", "infegal", "sup" et "supegal" sont utilisés pour les comparaisons de valeurs numériques.



## Fonctionnalité incomplète

- Instructions `lire()` non fonctionnelle
- Gestion des modes entrée sortie des paramètres de fonctions et de procédures
- Gestion des erreurs et des exceptions