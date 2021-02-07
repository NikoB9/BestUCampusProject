import pyproj
from shapely.geometry import Polygon
from xml.dom import minidom
from random import randrange
import os

#python -W ignore projet.py


class TypeBatiment(object):
	
	"""docstring for Batiment"""
	def __init__(self, nom, surface):
		super(TypeBatiment, self).__init__()
		self.nom = nom
		self.aireTotale = surface
		self.nombre = 1
		self.vote = False

	def addSurface(self, surface):
		self.aireTotale += surface
		self.nombre += 1

	def voter(self):
		self.vote = True

	def __str__(self):
		return "type : "+self.nom + "; nombre de bâtiments : " + str(self.nombre) + "; aire : " + str(self.aireTotale) + "; vote : " + str(self.vote)


class Projet(object):	

	"""docstring for Projet"""
	def __init__(self, nom, file):
		super(Projet, self).__init__()
		self.nom = nom
		self.file = file
		self.BatList = {}
		self.votes = 0

	def addBatiment(self, TypeBatiment):
		self.BatList[TypeBatiment.nom] = TypeBatiment

	def editBatiment(self, aire, nomB):
		self.BatList[nomB].addSurface(aire)

	def voter(self):
		self.votes += 1

	def __str__(self):
		tostr = "nom : " + self.nom + "; file : " + self.file + "; votes : " + str(self.votes) + "; batiments : \n"
		for bat in self.BatList :
			tostr += str(self.BatList[bat]) + "\n"
		return tostr

#liste des tailles pour choisir la médiane
medList= {}
medList["bâtiment scolaire"] = []
medList["parking"] = []
medList["lieu de vie"] = []
medList["jardin"] = []
medList["potager"] = []
medList["laboratoire"] = []
medList["complexe sportif"] = []

#liste de dict projets pour accéder aux projets et procéder au vote {nom : projet}
projets = []

#Dossier contenant tous les projets
path = 'StudentProjects' 
#On récupère tous les fichiers du dossier
files = os.listdir(path)
#Pour chaque fichier
for name in files:
	#On charge le fichier dans le DOM
	projetKml = minidom.parse('StudentProjects/' + name)
	#On récupère la racine
	root = projetKml.documentElement
	#balise générale "Document" du kml 
	genBalise = root.getElementsByTagName("Document")
	if len(genBalise) > 0:

		#nom du projet
		print()
		nomProjet = genBalise[0].getElementsByTagName("name")
		nomP = "Projet sans nom"
		if len(nomProjet) > 0:
			nomP = nomProjet[0].firstChild.data
			print("Nom du projet : ", nomP)
		else :
			print(nomP)

		print()

		#création du projet
		projet = Projet(nomP, 'StudentProjects/' + name)

		#On va aller chercher tous les bâtiments et leurs données
		batiments = genBalise[0].getElementsByTagName("Placemark")
		for b in batiments :
			#nom du bâtiment
			nomBatiment = b.getElementsByTagName("name")
			nomB = "Bâtiment sans nom"
			if len(nomBatiment) > 0:
				nomB = nomBatiment[0].firstChild.data
				print("Nom du bâtiment : ", nomB)
			else :
				print(nomB)


			#coordonnées
			coordonnees = b.getElementsByTagName("coordinates")
			aire = 0
			if len(coordonnees) > 0:
				#Mise en forme des coordonnées
				corSplit = coordonnees[0].firstChild.data.replace("\n", "").replace("\t", "").split(" ")
				coordinates_wgs84 = []
				for c in corSplit :
					xyz = c.split(",")
					if len(xyz) == 3:
						coordinates_wgs84.append([xyz[0], xyz[1]])


				#Convertion des coordonnées sur un plan orthonormé 
				coordinates_lambert = []
				for c in coordinates_wgs84:
					x, y = c[0], c[1]
					WGS84_in = pyproj.Proj(init='epsg:4326')
					lambert93_out = pyproj.Proj(init='epsg:2154')
					lat, lon = pyproj.transform(WGS84_in,lambert93_out,x,y)

					coordinates_lambert.append([lat, lon])

				aire = Polygon(coordinates_lambert).area
				print("aire : ",aire)


			else :
				print("Bâtiment sans coordonnées")

			#si le type batiment existe on incrémente la surface
			if nomB in projet.BatList :
				projet.editBatiment(aire, nomB)
				
			#sinon on enregistre le type de bâtiment avec sa surface
			else :
				projet.addBatiment(TypeBatiment(nomB, aire))

			print()

		print()


		#remplissage des tableaux pour calcul de mediane
		for cle in projet.BatList :
			medList[cle].append(projet.BatList[cle].aireTotale)

		projets.append(projet)


	else : 
		print("Le projet kml est mal formé")


#liste des médianes
mediane= {}


def purifieEtTrouveMediane(typeBatiment, minV, maxV):

	#épurer bâtiments scolaires avec nos critère min max
	i=0
	while i < len(medList[typeBatiment]):


		if medList[typeBatiment][i] < minV or medList[typeBatiment][i] > maxV:

			medList[typeBatiment].pop(i)

		else :
			i += 1

	#trier des valeurs du tableaux
	medList[typeBatiment].sort()

	#récupération médiane(s)
	length = len(medList[typeBatiment])
	mid = length / 2
	if length % 2 == 0:
		mediane[typeBatiment] = [medList[typeBatiment][int(mid)-1], medList[typeBatiment][int(mid)]]
	else:
		mediane[typeBatiment] = [medList[typeBatiment][int(mid)]]


purifieEtTrouveMediane("bâtiment scolaire", 50000, 90000)
purifieEtTrouveMediane("parking", 10000, 30000)
purifieEtTrouveMediane("lieu de vie", 4000, 15000)
purifieEtTrouveMediane("jardin", 10000, 40000)
purifieEtTrouveMediane("potager", 5000, 20000)
purifieEtTrouveMediane("laboratoire", 15000, 40000)
purifieEtTrouveMediane("complexe sportif", 15000, 50000)

'''
print()
print(medList)
print()
print(mediane)
print()
'''

#votes et enregistrement du vote max
voteMax = 0
#pour chaque projet
for p in projets:
	#pour chaque type de batiment
	for tb in p.BatList :
		#on récupère l'objet batiment
		typeBat = p.BatList[tb]
		#si l'aire du batiment correspond à la médiane enregistré le bâtiment obtient un vote
		if typeBat.aireTotale in mediane[tb]:
			typeBat.voter()
			p.voter()
			#si le nombre de votre du projet est le max on l'enregistre
			if p.votes > voteMax:
				voteMax = p.votes


elus = []

#enregistrement du ou des projets élus
#pour chaque projet
for p in projets:
	if p.votes == voteMax:
		elus.append(p)

#sélection aléatoire d'un indice de projet entre 0 et le nombre d'élus (-1)
#(si un élu => aléatoire entre 0 et 0 => automatiquement choisi)
elu = elus[randrange(len(elus))]

print(elu)




'''print()

for p in projets:
	print(p)

print()'''


#création du xml de resultat
resultat = minidom.Document()
#noeud principal du fichier
root = resultat.createElement('resultat')

#description du projet et explication du resultat sous forme de commentaire
textComment = "Pour ce projet participatif, nous avons décidé d'élire le projet qui correspondrait au mieux à nos besoin défini ci-dessous : \n\n"
textComment += "|        Nom        |    Nombre    | Surface totale min | Surface totale max |\n"
textComment += "|___________________|______________|____________________|____________________|\n"
textComment += "| Bâtiment scolaire |       3      |     50 000 m²      |      90 000 m²     |\n"
textComment += "| Lieu de vie       |       1      |      4 000 m²      |      15 000 m²     |\n"
textComment += "| Jardin            |       2      |     10 000 m²      |      40 000 m²     |\n"
textComment += "| Potager           |       1      |      5 000 m²      |      20 000 m²     |\n"
textComment += "| Laboratoire       |       1      |     15 000 m²      |      40 000 m²     |\n"
textComment += "| Parking           |       2      |     10 000 m²      |      30 000 m²     |\n"
textComment += "| Complexe sportif  |       1      |     15 000 m²      |      50 000 m²     |\n\n"
textComment += "Nous avons imposé le nombre de bâtiments et le type de bâtiment mais les surfaces étaient libres. \n" 
textComment += "Pour noter un projet, nous avons choisi la valeur médiane de tous les projets qui correspondaient à nos critères. \n" 
textComment += "Exemple : Si le projet A a des bâtiments scolaire d'une surface totale de 55 000 m², le projet B, pour les mêmes bâtiments, une surface totale de 80 000 m², le projet C une surface de 68 000 m² et enfin le projet D une surface de 100 000m², le projet D sera exclu du concours pour cette catégorie et c'est le projet C qui prendra le point pour l'évaluation des bâtiments scolaire, car il a la surface médiane parmi les projets.\n" 
textComment += "Le projet qui gagne, est le projet qui aura le plus de vote. En cas d'égalité, le gagnant sera tiré au sort.\n"
comment = resultat.createComment(textComment)
root.appendChild(comment)

#Création des balises pour annoncer le projet retenu :
gagnant = resultat.createElement('gagnant')
gagnant.setAttribute('nom', elu.nom)
gagnant.setAttribute('fichier', elu.file)
gagnant.setAttribute('nbVotes', str(elu.votes))

winElems = resultat.createElement('batiments')

for bat in elu.BatList :
	batiment = resultat.createElement('batiment')
	batiment.setAttribute('nom', bat)
	batiment.setAttribute('surface', str(elu.BatList[bat].aireTotale))
	batiment.setAttribute('retenu', str(elu.BatList[bat].vote))
	batiment.setAttribute('nbBatiments', str(elu.BatList[bat].nombre))

	winElems.appendChild(batiment)

gagnant.appendChild(winElems)
root.appendChild(gagnant)

#balise de stats
stats = resultat.createElement('stats')
#stats par projets
projs = resultat.createElement('projets')
for p in projets : 

	#Création des balises pour les infos du proje
	proj = resultat.createElement('projet')
	proj.setAttribute('nom', p.nom)
	proj.setAttribute('fichier', p.file)
	proj.setAttribute('nbVotes', str(p.votes))
	#balise qui contient la liste des batiments
	batiments = resultat.createElement('batiments')

	for bat in p.BatList:
		batiment = resultat.createElement('batiment')
		batiment.setAttribute('nom', bat)
		batiment.setAttribute('surface', str(p.BatList[bat].aireTotale))
		batiment.setAttribute('retenu', str(p.BatList[bat].vote))
		batiment.setAttribute('nbBatiments', str(p.BatList[bat].nombre))

		batiments.appendChild(batiment)

	proj.appendChild(batiments)
	projs.appendChild(proj)


stats.appendChild(projs)

#stats générales
gen = resultat.createElement('general')
#balise des médianes 
med = resultat.createElement('medianes')
#ajout des médianes 
for meuh in mediane:
	m = resultat.createElement('mediane')
	m.setAttribute("reference", meuh)
	m.setAttribute("value", str(mediane[meuh]))

	med.appendChild(m)

gen.appendChild(med)
stats.appendChild(gen)

root.appendChild(stats)

resultat.appendChild(root)


#ENREGISTREMENT
xml_str = resultat.toprettyxml(indent ="\t")  
save_path_file = "resultat.xml"
  
with open(save_path_file, "w", encoding="utf8") as f: 
    f.write(xml_str)
