# 2 - Analyse de la couverture de glace des lacs (English Follows)

Ce dossier contient divers fichiers relatifs à notre analyse de la couverture de glace des lacs du Canada et des États-Unis basée sur la couverture RADARSAT-1.

L'objectif de ce travail était de voir, à partir d'un ensemble de données d'entraînement, si nous pouvions créer un script qui détermine si une image d'un lac présente une couverture de glace significative ou non.

Les fichiers contenus dans ce dossier comprennent :

* lakeice-measurements.xlsx - Données d'entraînement disponibles pour utilisation. Couvre les périodes avant et après la couverture de RADARSAT-1. Fournit les coordonnées et la couverture de glace pour divers lacs (0 = 0%, 10 = 100%).
* find_if_has_imagery.py - Un script pour déterminer s'il y a de l'imagerie pour une coordonnée donnée à un moment donné, en utilisant le fichier ci-dessus. Il produit des fichiers avec une indication de la présence ou non d'une couverture.

# 2 - Lake Ice Coverage Analysis (Le français précède)

This folder contains various files related to our analysis of ice coverage of lakes in Canada and the United States based on the RADARSAT-1 coverage.

The objective of this work was to see, given a training set of data, whether we could create a script that determines if an image of a lake shows significant ice coverage or not.

The files contained in this folder include:

* lakeice-measurements.xlsx - Training data available for use. Spans periods before and after RADARSAT-1 coverage. Provides coordinates and ice coverage for various lakes (0 = 0%, 10 = 100%).
* find_if_has_imagery.py - A script to determine whether there is imagery of a given coordinate at a given time, using the above file. Outputs files with an indication of whether there is coverage or not.