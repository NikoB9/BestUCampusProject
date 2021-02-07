import pyproj
from shapely.geometry import Polygon
from xml.dom import minidom
import os

#python -W ignore projet.py


class TypeBatiment(object):
	nom = ""
	nombre = 0
	aireTotale = 0
	"""docstring for Batiment"""
	def __init__(self, nom):
		super(Batiment, self).__init__()
		self.nom = nom


class Projet(object):
	nom = ""
	description = ""
	BatList = []
	votes = 0

	"""docstring for Projet"""
	def __init__(self, nom, description):
		super(Projet, self).__init__()
		self.nom = nom
		self.description = description

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
		if len(nomProjet) > 0:
			print("Nom du projet : ", nomProjet[0].firstChild.data)
		else :
			print("Projet sans nom")

		#description du projet
		descProjet = genBalise[0].getElementsByTagName("description")
		if len(descProjet) > 0:
			print("Description du projet : ", descProjet[0].firstChild.data)
		else :
			print("Projet sans description")

		print()

		#On va aller chercher tous les bâtiments et leurs données
		batiments = genBalise[0].getElementsByTagName("Placemark")
		for b in batiments :
			#nom du bâtiment
			nomBatiment = b.getElementsByTagName("name")
			if len(nomBatiment) > 0:
				print("Nom du bâtiment : ", nomBatiment[0].firstChild.data)
			else :
				print("Bâtiment sans nom")


			#coordonnées
			coordonnees = b.getElementsByTagName("coordinates")
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

			print()

		print()


	else : 
		print("Le projet kml est mal formé")



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