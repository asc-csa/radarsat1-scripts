# 2 - Analyse de la couverture de glace des lacs (English Follows)

Ce dossier contient divers fichiers relatifs à notre analyse de la couverture de glace des lacs du Canada et des États-Unis basée sur la couverture RADARSAT-1.

L'objectif de ce travail était de voir, à partir d'un ensemble de données d'entraînement, si nous pouvions créer un script qui détermine si une image d'un lac présente une couverture de glace significative ou non.

Les fichiers contenus dans ce dossier comprennent :

* /shapefile - Contient les fichiers de forme qui peuvent éventuellement être utilisés pour découper l'imagerie pour un apprentissage automatique plus précis.
* clip_with_shapefile.py - Script pour tenter de découper l'imagerie, ne fonctionne actuellement que pour certaines images.
* download_matching_imagery.jpynb - Carnet de notes pour télécharger toutes les images qui correspondent aux mesures prises dans lakeice-measurements.xlsx.
* Ice_Coverage_Analysis_r1.jpynb - Notebook pour analyser les images téléchargées par le script ci-dessus en les convertissant en histogrammes, en les traçant de différentes manières, et finalement en utilisant un algorithme d'apprentissage automatique sklearn pour prédire si une image contient de la glace ou non.
* lakeice-measurements.xlsx - Données d'entraînement pour le script, utilisées avec la permission du programme du Service canadien des glaces.
* r1_data_with_aws.csv - Métadonnées produites par les scripts dans le dossier 1 - Basic AWS Access and Usage.

# 2 - Lake Ice Coverage Analysis (Le français précède)

This folder contains various files related to our analysis of ice coverage of lakes in Canada and the United States based on the RADARSAT-1 coverage.

The objective of this work was to see, given a training set of data, whether we could create a script that determines if an image of a lake shows significant ice coverage or not.

The files contained in this folder include:

* /shapefile - Contains the shape files that can eventually be used for clipping the imagery for more accurate machine learning.
* clip_with_shapefile.py - Script to attempt to clip imagery, only currently working for some imagery.
* download_matching_imagery.jpynb - Notebook to download all imagery that matches measurements taken in lakeice-measurements.xlsx.
* Ice_Coverage_Analysis_r1.jpynb - Notebook to analyze images downloaded by the above script by converting them to histograms, plotting them in various ways, and finally using an sklearn machine learning algorithm to predict if an image contains ice or not.
* lakeice-measurements.xlsx - Training data for the script, used with permission of the Canadian Ice Service program.
* r1_data_with_aws.csv - Metadata produced by scripts in the 1 - Basic AWS Access and Usage folder.