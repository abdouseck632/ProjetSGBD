import requests
def creationFichierjson(url):
	a=requests.get(url)
	contenu = a.text
	fic=open("a.json","w")
	fic.write(contenu)
	fic.close()
def creationFichierxml(url):
	a=requests.get(url)
	contenu = a.text
	fic=open("a.json","w")
	fic.write(contenu)
	fic.close()
