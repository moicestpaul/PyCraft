## Introduction

Ce projet vise à recréer le concept de fonctionnement de Minecraft en python. Pour cela, le programme utilise le moteur Ursina.  

Fonctionnalités :
- Génération aléatoire d'une map (avec height map aléatoire et placement d'arbres aléatoires également)
- Déplacements, pose et casse de blocs

> Chaque bloc est considéré comme une entité unique, le programme ne permet donc pas de générer de grandes cartes de manière fluide. Pour garder une bonne fluidité, il vaut mieux ne pas dépasser une taille de carte de 25*25 blocs. Si le programme ne tourne pas de manière fluide sur votre ordinateur, baissez la taille de la carte.

[![PyCraft_Screenshot](https://i.postimg.cc/ydS3ZGCy/333135456-780258066939173-826262856911322325-n.png "PyCraft_Screenshot")](https://i.postimg.cc/ydS3ZGCy/333135456-780258066939173-826262856911322325-n.png "PyCraft_Screenshot")

## Installation

Utilisez [pip](https://pip.pypa.io/en/stable/) pour installer ursina

```bash
pip install ursina
```

## Contrôles

Déplacement : ZQSD  
Saut : Espace  
Poser un bloc : Clic gauche  
Détruire un bloc : Clic droit  

Choisir le type de bloc à poser :  
1 : Herbe  
2 : Pierre  
3 : Bois  
4 : Feuilles  

Quitter : Echap

## Configuration
Voici la liste des variables que vous pouvez modifier pour influencer la génération de carte
```python
mapWidth  = 25 # Taille de la carte
waterLevel= 0 # Niveau de la mer

negAmp    = -1    # Amplitude négative de la gen de height map
posAmp    = 1     # Amplitude positive de la gen de height map
minHeight = -1 # Altitude minimum de la map

treeSpawnRate = 80 # Les arbres on une chance sur --treeSpawnRate-- de spawn
```
