# BestUCampusProject
Différents élèves crééent un kml à partir de google earth représentant le campus de leur rêve. Notre programme permet de choisir le projet qui fait plaisir au plus de monde parmis les différents projets. Le résultat est fait en XML avec un schema propre.

# Projets
Les projets sont dans le dossier StudentProjects.

# Contraintes de sélection
polygones : carré, rectangle ou forme en L
Type de bâtiments :
-Bâtiment scolaire (*3) ; surface totale min : ; surface totale max :
-lieu de vie (*1) ; surface totale min : ; surface totale max :
-jardin (*2) ; surface totale min : ; surface totale max :
-potager (*1) ; surface totale min : ; surface totale max :
-laboratoire (*1) ; surface totale min : ; surface totale max :
-parking (*2) ; surface totale min : ; surface totale max :
-complexe sportif (*1) ; surface totale min : ; surface totale max :

# Système pour retenir le "meilleur projet"

Votes = Array("étudiant" => nbVotes = 0)

Pour chaque type de bâtiment :
|	TabSurfs = Array(surface)
|	Pour chaque projet étudiant :
|	|	surfBS = surface du bâtiment du type correspondant
|	|	Si surfBS > surfMin ET surfBS > surfMin:
|	|	|	TabSurfs <-- surfBS
|	Recherche Mediane dans TabSurfs
|	Incrémentation du vote pour l'élève (ou les) qui on la surface Médiane 
On retient le projet de l'étudiant qui à le plus de votes	