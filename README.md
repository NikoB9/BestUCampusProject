# BestUCampusProject
Différents élèves crééent un kml à partir de google earth représentant le campus de leur rêve. Notre programme permet de choisir le projet qui fait plaisir au plus de monde parmis les différents projets. Le résultat est fait en XML avec un schema propre.

# Projets
Les projets sont dans le dossier StudentProjects.

# Contraintes de sélection
Formes des bâtiments : 
* Carré
* Rectangle
* Forme en L

Type de bâtiments :
````
(Surface Terrain 350 000m²)
/*** TODO : Pourquoi ces critères ? ***/
````

 Nom | Nombre | Surface totale min | Surface totale max
--------------|--------------|--------------|--------------
 Bâtiment scolaire | 3 | 50 000 | 90 000 m²
 Lieu de vie | 1 | 4 000 | 15 000 m²
 Jardin | 2 | 10 000 | 40 000 m²
 Potager | 1 | 5 000 | 20 000 m²
 Laboratoire | 1 | 15 000 | 40 000 m²
 Parking | 2 | 10 000 | 30 000 m²
 Complexe sportif | 1 | 15 000 | 50 000 m²

# Système pour retenir le "meilleur projet"
````php
Votes = Array("étudiant" => nbVotes = 0)

Pour chaque type de bâtiment :
|	TabSurfs = Array(surface)
|	Pour chaque projet étudiant :
|	|	surfBS = surface du bâtiment du type correspondant
|	|	Si surfBS > surfMin ET surfBS > surfMin:
|	|	|	TabSurfs <-- surfBS
|	Recherche Mediane dans TabSurfs
|	Incrémentation du vote pour l'élève (ou les) qui on la surface Médiane 
On retient le projet de l'étudiant qui à le plus de votes (si plusieurs random parmis les gagnants)
````
