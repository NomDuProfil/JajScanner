# JajScanner

Ces scripts permettent d'executer des commandes de scan à distance via une interface graphique.

# Fichiers et configuration

## Côté client

Le client possède les éléments suivants :
  * main.py : Qui est le programme principal
  * network.py : Qui permet la gestion des communications avec le serveur

A noter que l'addresse et le port du serveur sont modifiable dans le fichier "network.py" au début du fichier :
```
SERVER_ADDR = "127.0.0.1"
SERVER_PORT = 1234
```

## Côté serveur

Le serveur possède les éléments suivants :
  * server.py : Qui est le programme principal
  * process.py : Qui gère le lancement des processus de scan
  * tools.txt : Qui est le fichier qui contient les outils et les arguments des outils de scan
  * ./inprogress/inprogress.txt : Qui est le fichier où se trouveront les commandes en cours
  * ./inprogress/ : Qui est le dossier où se trouveront les sorties des scans en cours
  * ./done/ : Qui est le dossier où se trouveront les sorties des scans terminés

Le fichier tools ressemble à ceci :
```
nametool = nmap
outputoption = -oN
default = -p-
nametool = dirb
outputoption = -o
```

Il est important de garder la même syntax c'est-à-dire :
  * nametool = nom de l'outil
  * outputoption = argument de l'outil permettant la sortie dans un fichier
  * UnNomPersonnalise = arguments avec lequel on va executer l'outil

# Utilisation

## Lancement du serveur

Sur le serveur distant il suffit d'executer le serveur via la commande ```python server.py```

## Utilisation du client

Dans l'onglet "Scan en cours", on choisi l'outil, les arguments et la cible de l'outil puis on clique sur "Start".

Le scan en cours apparait alors dans le cadre du bas. Lorsqu'il est terminé celui-ci se retrouve dans l'onglet "Scan terminé". Il est alors possible de double cliquer sur les scans pour voir le résultat. Il est aussi possible de télécharger le résultat. Celui-ci sera stocké de la forme : CIBLE.txt
