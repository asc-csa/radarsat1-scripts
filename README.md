<p align="center">
    <img src="https://github.com/asc-csa/radarsat1-scripts/blob/main/radarsat1-image.jpg?raw=true" height="200">
</p>

<p align="center">
    <a href="#stars">
        <img alt="Étoiles sur GitHub | GitHub Repo stars" src="https://img.shields.io/github/stars/asc-csa/radarsat1-scripts">
    </a>
    <a href="#watchers">
        <img alt="Spectateurs sur Github | GitHub watchers" src="https://img.shields.io/github/watchers/asc-csa/radarsat1-scripts">
    </a>
    <a href="https://github.com/asc-csa/radarsat1-scripts/commits/main">
        <img alt="Dernier commit sur GitHub | GitHub last commit" src="https://img.shields.io/github/last-commit/asc-csa/radarsat1-scripts">
    </a>
    <a href="https://github.com/asc-csa/radarsat1-scripts/graphs/contributors">
        <img alt="Contributeurs sur GitHub | GitHub contributors" src="https://img.shields.io/github/contributors/asc-csa/radarsat1-scripts">
    </a>
    <a href="https://twitter.com/intent/follow?screen_name=csa_asc">
        <img alt="Suivre sur Twitter | Twitter Follow" src="https://img.shields.io/twitter/follow/csa_asc?style=social">
    </a>
</p>

# Scripts RADARSAT-1 (English follows)

Dépôt contenant des fonctions d'aide utilisées pour accéder à des fichiers et les télécharger à partir d'un compartiment S3 contenant des images .tiff de RADARSAT-1. Pour obtenir de plus amples renseignements sur le compartiment S3, consultez le [Registre de données ouvert AWS](https://registry.opendata.aws/radarsat-1/). Pour en savoir plus sur RADARSAT-1, consultez le [site Web de l'Agence spatiale canadienne](https://www.asc-csa.gc.ca/fra/satellites/radarsat1/quest-ce-que-radarsat1.asp).

Le fichier /src/ contient plusieurs exemples de scripts pour commencer :

- [downloading_files.py](src/downloading_files.py) est utilisé pour télécharger facilement des fichiers à partir du compartiment s3 en fonction de divers paramètres tels que la date, le pays ou les coordonnées.
- [get_metadata.py](src/get_metadata.py) est utilisé pour lire les métadonnées des fichiers sans avoir à les télécharger depuis le compartiment s3.
- [sample_algorithms.py](src/sample_algorithms.py) contient divers algorithmes simples qui peuvent être appliqués aux images pour démontrer les cas d'utilisation possibles.

Pour voir des exemples de résultats des scripts, nous avons un [fichier de résultats](src/README.md) qui explique leurs résultats.

# RADARSAT-1 Scripts (Le français précède)

Repository containing helper functions used to access and download files from an S3 bucket containing .tiff RADARSAT-1 images. More information regarding the AWS bucket can be found on the [AWS Open Data Registry](https://registry.opendata.aws/radarsat-1/). More information about RADARSAT-1 can be found on the [Canadian Space Agency website](https://www.asc-csa.gc.ca/eng/satellites/radarsat1/what-is-radarsat1.asp).

Inside the /src/ file are several sample scripts to start with:

- [downloading_files.py](src/downloading_files.py) is used to easily download files from the S3 bucket based on various metrics such as date, country, or coordinates.
- [get_metadata.py](src/get_metadata.py) is used to read metadata from the files without having to download them from the S3 bucket.
- [sample_algorithms.py](src/sample_algorithms.py) contains various simple algorithms that can be applied to the images to demonstrate possible use cases.

To view sample outputs from the scripts, we have an [outputs file](src/README.md) that explains their results.
