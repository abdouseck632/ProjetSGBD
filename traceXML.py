import xml.etree.ElementTree as ET
# load and parse the file
xmlTree = ET.parse('test.xml')
root=xmlTree.getroot()
#Donne le nom de la base de donnees 
print "Nom de la base de donnees : "+root.tag
#Donne les tables, les attributs et leurs instances
for noeud in root:
	print(noeud.tag)
	for noeud1 in noeud:
		print(noeud1.tag + " : "+ noeud1.text)


