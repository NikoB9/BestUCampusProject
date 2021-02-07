import pyproj
from shapely.geometry import Polygon
from xml.dom import minidom
import os

#python -W ignore projet.py


class TypeBatiment(object):
	nom = ""
	nombre = 0
	aireTotale = 0
	vote = False
	"""docstring for Batiment"""
	def __init__(self, nom, surface):
		super(TypeBatiment, self).__init__()
		self.nom = nom
		self.aireTotale = surface
		self.nombre = 1

	def addSurface(self, surface):
		self.aireTotale += surface
		self.nombre += 1

	def __str__(self):
		return "type : "+self.nom + "; nombre de bâtiments : " + str(self.nombre) + "; aire : " + str(self.aireTotale) + "; vote : " + str(self.vote)


class Projet(object):
	nom = ""
	BatList = {}
	votes = 0

	"""docstring for Projet"""
	def __init__(self, nom):
		super(Projet, self).__init__()
		self.nom = nom

	def addBatiment(self, TypeBatiment):
		self.BatList[TypeBatiment.nom] = TypeBatiment

	def editBatiment(self, aire, nomB):
		self.BatList[nomB].addSurface(aire)

	def __str__(self):
		tostr = "nom : " + self.nom + "; votes : " + str(self.votes) + "; batiments : \n"
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
		projet = Projet(nomP)

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

		print(projet)


		#remplissage des tableaux pour calcul de mediane
		for cle in projet.BatList :
			medList[cle].append(projet.BatList[cle].aireTotale)

		projets.append(projet)


	else : 
		print("Le projet kml est mal formé")



print()

for p in projets:
	print(p)

print()




#épurer bâtiments scolaires avec nos critère min max
i=0
while i < len(medList["bâtiment scolaire"]):

	print(medList["bâtiment scolaire"][i])

	if medList["bâtiment scolaire"][i] < 50000 or medList["bâtiment scolaire"][i] > 90000:

		medList["bâtiment scolaire"].pop(i)

	else :
		i += 1

#trier des valeurs du tableaux
medList["bâtiment scolaire"].sort()

#épurer parking avec nos critère min max
i=0
while i < len(medList["parking"]):

	if medList["parking"][i] < 10000 or medList["parking"][i] > 30000:

		medList["parking"].pop(i)

	else :
		i += 1

#trier des valeurs du tableaux
medList["parking"].sort()

#épurer lieu de vie avec nos critère min max
i=0
while i < len(medList["lieu de vie"]):

	if medList["lieu de vie"][i] < 4000 or medList["lieu de vie"][i] > 15000:

		medList["lieu de vie"].pop(i)

	else :
		i += 1

#trier des valeurs du tableaux
medList["lieu de vie"].sort()

#épurer jardin avec nos critère min max
i=0
while i < len(medList["jardin"]):

	if medList["jardin"][i] < 10000 or medList["jardin"][i] > 40000:

		medList["jardin"].pop(i)

	else :
		i += 1

#trier des valeurs du tableaux
medList["jardin"].sort()

#épurer potager avec nos critère min max
i=0
while i < len(medList["potager"]):

	if medList["potager"][i] < 5000 or medList["potager"][i] > 20000:

		medList["potager"].pop(i)

	else :
		i += 1

#trier des valeurs du tableaux
medList["potager"].sort()

#épurer laboratoire avec nos critère min max
i=0
while i < len(medList["laboratoire"]):

	if medList["laboratoire"][i] < 15000 or medList["laboratoire"][i] > 40000:

		medList["laboratoire"].pop(i)

	else :
		i += 1

#trier des valeurs du tableaux
medList["laboratoire"].sort()

#épurer complexe sportif avec nos critère min max
i=0
while i < len(medList["complexe sportif"]):

	if medList["complexe sportif"][i] < 15000 or medList["complexe sportif"][i] > 50000:

		medList["complexe sportif"].pop(i)

	else :
		i += 1

#trier des valeurs du tableaux
medList["complexe sportif"].sort()

print(medList)



"""test batiment polytech Salome : 
coordinates_wgs84 = [[2.17052259106493,48.70894558902779],
[2.171390007585461,48.70895373305775],
[2.171403232974205,48.70831874959825],
[2.172532756656471,48.70829960928263],
[2.172548045801741,48.70921677995045],
[2.170467957253095,48.70925473741478],
[2.17052259106493,48.70894558902779]]"""

"""test batiment central Nicolas : 
coordinates_wgs84 = [[2.166537374751398,48.71095132821508],
[2.166468602998526,48.70983576711469],
[2.167582929990826,48.70982504104365],
[2.16866302300933,48.70982927134865],
[2.168673027378643,48.71093357426656],
[2.167807403199806,48.71094768419172],
[2.166537374751398,48.71095132821508]]"""

'''
coordinates_lambert = []

for c in coordinates_wgs84:
	x, y = c[0], c[1]
	WGS84_in = pyproj.Proj(init='epsg:4326')
	lambert93_out = pyproj.Proj(init='epsg:2154')
	lat, lon = pyproj.transform(WGS84_in,lambert93_out,x,y)

	coordinates_lambert.append([lat, lon])

p = Polygon(coordinates_lambert)
print()
print()
print(p.area)'''