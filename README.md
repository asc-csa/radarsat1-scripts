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

Le dossier /src/ comprend plusieurs sous-dossiers contenant les différents scripts produits :

- [src/1 - Basic AWS Access and Usage](src/1%20-%20Basic%20AWS%20Access%20and%20Usage/README.md) contient les scripts produits au cours du travail exploratoire et de l'apprentissage du compartiment AWS.
- [src/2 - Lake Ice Coverage Analysis](src/2%20-%20Lake%20Ice%20Coverage%20Analysis/README.md) contient des scripts permettant d'analyser les images du satellite RADARSAT-1 et de déterminer si elles contiennent des lacs couverts de glace.

Pour voir des exemples de résultats des scripts, nous avons un [fichier de résultats](src/README.md) qui explique leurs résultats.

# RADARSAT-1 Scripts (Le français précède)

Repository containing helper functions used to access and download files from an S3 bucket containing .tiff RADARSAT-1 images. More information regarding the AWS bucket can be found on the [AWS Open Data Registry](https://registry.opendata.aws/radarsat-1/). More information about RADARSAT-1 can be found on the [Canadian Space Agency website](https://www.asc-csa.gc.ca/eng/satellites/radarsat1/what-is-radarsat1.asp).

Inside the /src/ folder are several sub-folders containing the various scripts produced:

- [src/1 - Basic AWS Access and Usage](src/1%20-%20Basic%20AWS%20Access%20and%20Usage/README.md) contains scripts produced during exploratory work and learning about the AWS bucket.
- [src/2 - Lake Ice Coverage Analysis](src/2%20-%20Lake%20Ice%20Coverage%20Analysis/README.md) contains scripts to analyze imagery from the RADARSAT-1 satellite and determine if they contain ice-covered lakes.