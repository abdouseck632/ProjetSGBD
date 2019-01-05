import sys
import json
from jsonschema import validate
import svgwrite
import xml.etree.ElementTree as ET
# fonction de validation du ficheir json
cx=100
cy=100
longeur=400
largeur=600
clas=[]
def CreateSvgFile(SvgFileName):
    svg_document = svgwrite.Drawing(filename =SvgFileName,
                                    size = (2500,2500))
def ValidateXml(file):
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(file)
def CreateTable(cx,cy,nomclasse,attribut,nbreattribut):

    largeurp=largeur
    if nbreattribut>5:
        largeurp+=largeur*0.15*(nbreattribut-5)

    svg_document.add(svg_document.rect(insert = (cx, cy),
                                       size = (longeur-100, largeurp/3),
                                       stroke_width = "1",
                                       stroke = "black",
                                       fill = "rgb(255,255,244)"))

    svg_document.add(svg_document.text(nomclasse,
                                   textLength=110,
                                   insert = (50+cx,30+cy)))
    x=0;
    for value in attribut:

        svg_document.add(svg_document.text(value,
                                       insert = (longeur/10+cx, longeur/5+x+cy)))
        x+=25
    # svg_document.add(svgwrite.shapes.Circle(center=(cx,100), r=100,
    #                                             fill = "rgb(255,255,255)",
    #                                             stroke = "black"))

    svg_document.add(svg_document.rect(insert = (cx, cy+50),
                                       size = (longeur-100,5),
                                       color= "black",
                                       stroke_width = "3",
                                       stroke = "black",
                                       fill = "rgb(255,0,0)"))

class Classes():
    def __init__(self,classe,attribut,valeur):
        self.classe=classe
        self.attribut=attribut
        self.valeur=valeur
def XmlFile(xmlfile):
    xmlTree = ET.parse(xmlfile)
    root=xmlTree.getroot()
    # print("***************************")
    entite=[]
    element=[]
    valeur=[]
    i=0
    for child in root:
        entite.append(child.tag)
        # print()
        # print("-------------------")
        # print("-"+child.tag+"    -")

        for attribut in child:
            element.append(attribut.tag)
            valeur.append(attribut.text)
            # print("-"+attribut.tag+"  -")
        clas.append(Classes(entite[i],element,valeur))
        # print("-------------------")
        # print()
        i+=1
        element=[]
        valeur=[]
    Dessin(clas)
def ValidateJson(fichier_json):
    ok = True
    try:
        with open(fichier_json, 'r') as fp:
            obj = json.load(fp)
    except Exception as error:
        print("invalid json: %s" % error)
        ok = False
        return ok

def ValidatorAndExtractorJson(fichier_json):
    ok = True
    try:
        with open(fichier_json, 'r') as fp:
            obj = json.load(fp)
    except Exception as error:
        print("invalid json: %s" % error)
        ok = False
    if ok:
        l=[]
        valeur=[]
        nomcl=[]
        i=0
        j=0
        n=0
        for obh in obj.values():
            # print(obh)
            for hgh in obh:
                # print(hgh)
                nomcl.append(hgh)

        for obji in obj.values():
            # print(obji)

            for ob in obji.values():

                    # print("---------------------------------------------------")
                    for obb in ob:
                        # print(obb)
                        l.append(obb)
                    for obb in ob.values():
                        # print(obb)
                        valeur.append(obb)
                    # clas.append(Classes(nomcl[i],l,valeur))
                    clas.append(Classes(nomcl[i],l,valeur))
                    i+=1
                    # for n in range(0,len(l)):
                    #     print(l[n],"",valeur[n])
                    l=[]
                    valeur=[]

        print(clas)
        return clas
     # Dessin(clas)
def Dessin(clas):
    y=0
    for value in clas:
        # print(value.classe)
        # for value1 in value.attribut:
            # print(value1)
        # print("-------------+--------------------------------")

        if y%2 :
            CreateTable(400*(y//2),600,value.classe,value.attribut,len(value.attribut))
        else:

            CreateTable(400*(y//2),100,value.classe,value.attribut,len(value.attribut))
        y+=1
    # svg_document.add(svgwrite.shapes.Line(start=(0,0), end=(100,500)))
    print(svg_document.tostring())
    svg_document.save()

if __name__ == '__main__':
    i=1
    tmp=1
    if sys.argv[i]=="-i":
        i+=1
        if sys.argv[i]=="xml":
            i+=1
            print("traitement avec un fichier xml")
            if sys.argv[i]=="-t":
                i+=1
                xmlTree = ET.parse(sys.argv[sys.argv.index("-f")+1])
                root=xmlTree.getroot()
                print ("Nom de la base de donnees : "+root.tag)
                #Donnes les tables, les attributs et leurs instances

                for noeud in root:
                	print("-+---+---+---+---+---+")
                	print(noeud.tag)
                	print("-+---+---+---+---+---+-")
                	for noeud1 in noeud:
                		print(noeud1.tag + " : "+ noeud1.text)
                	print("")
                print(" permet de dire si on veut les traces car -t est present ")
            if sys.argv[i]=="-h":
                i+=1
                print("permet de désigner un input en flux http car -h est bien present"+sys.argv[i])
                i+=1
            if sys.argv[i]=="-f":
                print("permet de désigner un input de type fichier "+sys.argv[i+1]+" car le -f est présent")
                i+=2
                if sys.argv[i]=="-o":
                    print(" le -o est bien présent "+sys.argv[i+1])
                    print("Ce qui reste c'est de creer un fichier svg valide respectant les normes du MLD")

                    svg_document = svgwrite.Drawing(filename =sys.argv[i+1],
                                                            size = (2500,2500))
                    XmlFile(sys.argv[i-1])



        elif sys.argv[2]=="json":
            print("traitement avec un fichier json")
            i+=1

            if sys.argv[i]=="-t":
                i+=1
                classe=ValidatorAndExtractorJson(sys.argv[sys.argv.index("-f")+1])
                for cl in classe:
                    print("------------------------------")
                    print(cl.classe)
                    print("------------------------------")
                    for n in range(0,len(cl.attribut)):
                        print(cl.attribut[n],":",cl.valeur[n])
                        print("")
                print(" permet de dire si on veut les traces car -t est present ")
            if sys.argv[i]=="-h":
                i+=1
                print("permet de désigner un input en flux http car -h est bien present"+sys.argv[i])
                i+=1
            if sys.argv[i]=="-f":
                print("permet de désigner un input de type fichier "+sys.argv[i+1]+" car le -f est présent")
                i+=2
                if sys.argv[i]=="-o":
                    print(" le -o est bien présent")
                    print("Ce qui reste c'est de creer un fichier svg valide respectant les normes du MLD")
                    svg_document = svgwrite.Drawing(filename =sys.argv[i+1],
                                                    size = (2500,2500))
                    classes=ValidatorAndExtractorJson(sys.argv[i-1])
                    Dessin(classes)

        else:
            print("format de fichier non prise en compte")
