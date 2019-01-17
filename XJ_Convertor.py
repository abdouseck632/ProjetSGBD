import json
import sys
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from glob import glob
from jsonschema import validate
import svgwrite
import xml.etree.ElementTree as ET
import requests
def creationFichierjson(url):
    a=requests.get(url)
    contenu = a.text
    fic=open("fluxjson.json","w")
    fic.write(contenu)
    fic.close()
    return fic
def creationFichierxml(url):
    a=requests.get(url)
    contenu = a.text
    fic=open("fluxxml.xml","w")
    fic.write(contenu)
    fic.close()
    return fic
cx=100
cy=100
longeur=400
largeur=600
clas=[]
coord=[]
class coordonnee():
    def __init__(self,nomclasse,cx,cy):
        self.nomclasse=nomclasse
        self.cx=cx
        self.cy=cy
class Classes():
    def __init__(self,classe,attribut,valeur):
        self.classe=classe
        self.attribut=attribut
        self.valeur=valeur
class Relations():
    def __init__(self,classes,otherclass,relationstype,nomrelations):
        self.classes=classes
        self.otherclass=otherclass
        self.relationstype=relationstype
        self.nomrelations=nomrelations
def CreateSvgFile(SvgFileName):
    svg_document = svgwrite.Drawing(filename =SvgFileName,
                                    size = (2500,2500))
def parsefile(file):
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(file)
def XmlExtraction(xmlfile):
    xmlTree = ET.parse(xmlfile)
    root=xmlTree.getroot()
    entite=[]
    element=[]
    valeur=[]
    i=0
    for child in root:
        entite.append(child.tag)

        for attribut in child:
            element.append(attribut.tag)
            valeur.append(attribut.text)
        clas.append(Classes(entite[i],element,valeur))
        i+=1
        element=[]
        valeur=[]
    Dessin(clas)
def CreateTable(cx,cy,nomclasse,attribut,nbreattribut):
#augmente de la largeur du table si le nbre d'argument est superieur a 5
    largeurp=largeur
    if nbreattribut>5:
        largeurp+=largeur*0.15*(nbreattribut-5)

    svg_document.add(svg_document.rect(insert = (cx, cy),
                                       size = (longeur-200, largeurp/3),
                                       stroke_width = "1",
                                       stroke = "black",
                                       fill = "rgb(0,240,200)"))

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
                                       size = (longeur-200,5),
                                       color= "black",
                                       stroke_width = "3",
                                       stroke = "black",
                                       fill = "rgb(255,255,0)"))

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
        typerela=[]
        cle=[]
        val=[]
        clas=[]
        i=0
        j=0
        n=0
        for obh in obj.values():
                for hgh in obh:
                    # print(hgh)
                    typerela.append(hgh)
        for obji in obj.values():
                    # print(obji)
                    for obb in obji:
                        # print(obb)
                        typerela.append(obb)
                    for obb in obji.values():
                        for attribut in obb.values():
                            if type(attribut) is list:
                                for attrilist in attribut:
                                    for attribut1 in attrilist:
                                        # print(attribut1)
                                        cle.append(attribut1)
                                        print(type(attribut1))
                                    for valeur in attrilist.values():
                                        # print(valeur)
                                        val.append(valeur)
                            else:
                                for attribut1 in attribut:
                                    # print(attribut1)
                                    cle.append(attribut1)
                                    print(type(attribut1))
                                for valeur in attribut.values():
                                    # print(valeur)
                                    val.append(valeur)
                        clas.append(Classes(typerela[i],cle,val))
                        cle=[]
                        val=[]
                        i+=1

        return clas
def Classse(clas):
    clases=[]
    attr=[]
    valeur=[]
    for cl in clas:
        for n in range(0,len(cl.attribut)):
            if n<cl.attribut.index("otherclasse"):
                attr.append(cl.attribut[n])
                valeur.append(cl.valeur[n])
        clases.append(Classes(cl.classe,attr,valeur))
        attr=[]
        valeur=[]
    return clases
def ExtractionRelation(clas):
    clases=[]
    attr=[]
    valeur=[]
    other=[]
    for cl in clas:
        print("------------------------------")
        print(cl.classe)
        print("------------------------------")
        for n in range(0,len(cl.attribut)):
            if n>=cl.attribut.index("otherclasse"):
                if cl.attribut[n]=="otherclasse1":

                            other.append(cl.valeur[n])
                            attr.append(cl.attribut[n])
                            print(cl.attribut[n],":",cl.valeur[n])
                            print(n)
                else:
                    if n==cl.attribut.index("otherclasse"):
                            other.append(cl.valeur[n])
                            attr.append(cl.attribut[n])
                            print(cl.attribut[n],":",cl.valeur[n])

                    else:
                        attr.append(cl.attribut[n])
                        valeur.append(cl.valeur[n])
                        print(cl.attribut[n],":",cl.valeur[n])

        clases.append(Relations(cl.classe,other,attr,valeur))
        print(len(attr))
        attr=[]
        valeur=[]
        other=[]
    return clases
def AssociationLine(rel,coord,a,b,declage):
    CoordOther=[]
    CoordClass=[]
    nomrelation="Nom de la classe"
    for cord in coord:
        if rel.classes==cord.nomclasse:
            print(cord.cx,":",cord.cy)
            print(rel.otherclass)
            CoordClass.append(cord.cx)
            CoordClass.append(cord.cy)

    for rela in relations:
        if len(rela.relationstype)>3:
            if rela.classes==rel.classes:
                other1=rel.otherclass[0]
                other2=rel.otherclass[1]
                print(other1,"je suis la")
                i=0
                for cord in coord:
                        if other1==cord.nomclasse:
                            # print(cord.cx,":",cord.cy)
                            CoordOther.append(cord.cx)
                            CoordOther.append(cord.cy)
                            print(cord.cx,":",cord.cy)
                            nomrelation=rela.nomrelations[0]
                        if other2==cord.nomclasse:
                            CoordOther.append(cord.cx)
                            CoordOther.append(cord.cy)
                            print(cord.cx,":je suis la",cord.cy)
        else:
            if rela.classes==rel.classes:
                other=rel.otherclass[0]
                print("je suis dans ce boucle ",other)
                for cord in coord:
                    if other==cord.nomclasse:
                        # print(cord.cx,":",cord.cy)
                        CoordOther.append(cord.cx)
                        CoordOther.append(cord.cy)
                        print(cord.cx,":",cord.cy)
                        nomrelation=rela.nomrelations[0]
    print("la taille du des autres ",len(CoordOther))
    if len(CoordOther)==2:

        print(CoordClass[0],":",CoordClass[1])
        print(CoordOther[0],":",CoordOther[1])

        x=CoordClass[0]
        y=CoordClass[1]
        z=CoordOther[0]
        t=CoordOther[1]
        if y==t:
            if x>z:
                y+=200
                t+=200
                z+=100
            else:
                y+=100
                x+=200
                # z+=200
                t+=100
        elif x==z:
            if y>t:
                x+=100
                t+=200
                z+=100
            else:
                x+=100
                z+=100
                y+=200
        else:
            if x>z:
                if y>t :
                    t+=200
                    z+=200
                else:
                    y+=200
                    z+=200
            else:
                if y>t :
                    x+=200
                    t+=200
                else:
                    x+=200
                    y+=200
        svg_document.add(svgwrite.shapes.Line(start=(x,y),
                                            end=(z,t),
                                            stroke = "black",
                                            stroke_width = "3"
                                            ))
        svg_document.add(svg_document.text(nomrelation,
                                        insert = ((x+z)/2+15, (y+t)/2+15)))
    else:
        print(CoordClass[0],":",CoordClass[1])
        print(CoordOther[0],":",CoordOther[1])
        print(CoordOther[2],":",CoordOther[3])

        x=CoordClass[0]
        y=CoordClass[1]
        x1=CoordOther[0]
        y1=CoordOther[1]
        x2=CoordOther[2]
        y2=CoordOther[3]
        pointx = 340+declage
        pointy=340+declage
        if pointy>y:
            y+=200
            if pointx>x:
                x+=200
        else:
            if pointx>x:
                x+=200
        if pointy>y1:
            y1+=200
            if pointx>x1:
                x1+=200
        else:
            if pointx>x1:
                x1+=200
        if pointy>y2:
            y2+=200
            if pointx>x2:
                x2+=200
        else:
            if pointx>x2:
                x2+=200



        svg_document.add(svg_document.rect(insert = (pointx,pointy),
                                           size = (20,20),
                                           color= "black",
                                           stroke_width = "3",
                                           stroke = "black",
                                           fill = "rgb(255,255,0)"))
        svg_document.add(svgwrite.shapes.Line(start=(x,y),
                                            end=(pointx,pointy),
                                            stroke = "yellow",
                                            stroke_width = "3"
                                            ))
        svg_document.add(svgwrite.shapes.Line(start=(x1,y1),
                                            end=(pointx,pointy),
                                            stroke = "yellow",
                                            stroke_width = "3"
                                            ))
        svg_document.add(svgwrite.shapes.Line(start=(x2,y2),
                                            end=(pointx,pointy),
                                            stroke = "yellow",
                                            stroke_width = "3"
                                            ))
        svg_document.add(svg_document.text(nomrelation,
                                    insert = (pointx+25, pointy+25)))


    # svg_document.add(svgwrite.shapes.Line(start=(300+a,400+b),
    #                                     end=(z,t),
    #                                     stroke = "black",
    #                                     stroke_width = "3"
    #                                     ))
    for rel in relations:
        print(rel.nomrelations[0])
        print(rel.relationstype)

def Dessin(clas):
    y=0
    coord=[]

    for value in clas:
        # print(value.classe)
        # for value1 in value.attribut:
            # print(value1)
        # print("-------------+--------------------------------")

        if y%2 :
            CreateTable(500*(y//2),600,value.classe,value.attribut,len(value.attribut))
            coord.append(coordonnee(value.classe,500*(y//2),600))
        else:

            CreateTable(500*(y//2),100,value.classe,value.attribut,len(value.attribut))
            coord.append(coordonnee(value.classe,500*(y//2),100))
        y+=1



    AssociationLine(relations[3],coord,50,50,0)
    AssociationLine(relations[0],coord,50,50,0)
    AssociationLine(relations[1],coord,50,50,150)
    AssociationLine(relations[2],coord,50,50,200)
    print(svg_document.tostring())
    svg_document.save()
    for value in coord:
        print(value.nomclasse)
        print(value.cx)
        print(value.cy)


if __name__ == '__main__':
    i=1
    tmp=1
    tp=0
    classe=[]
    if sys.argv[i]=="-i":
        if len(sys.argv)==i:
            sys.exit()
        i+=1
        if sys.argv[i]=="xml":
            if len(sys.argv)==i:
                sys.exit()
            i+=1
            print("traitement avec un fichier xml")
            if sys.argv[i]=="-t":
                if len(sys.argv)==i:
                    sys.exit()
                i+=1
                file=sys.argv[1:]
                for arg in file:
                    for filename in glob(arg):
                        try:
                            parsefile(filename)

                        except Exception as error:
                            print (filename,"n'est pas bien formé!",error)
                            tp=1
                if tp==0:
                    print("le fichier est valide")
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
                if len(sys.argv)==i:
                    sys.exit()
                i+=1
                print("permet de désigner un input en flux http car -h est bien present"+sys.argv[i])
                creationFichierxml(sys.argv[i])
                XmlExtraction(sys.argv[i])
                i+=1
            if sys.argv[i]=="-f":

                print("permet de désigner un input de type fichier "+sys.argv[i+1]+" car le -f est présent")
                if len(sys.argv)==i:
                    sys.exit()
                i+=2
            if sys.argv[i]=="-o" :
                    if len(sys.argv)==i:
                        sys.exit()
                    print(" le -o est bien présent "+sys.argv[i+1])
                    print("Ce qui reste c'est de creer un fichier svg valide respectant les normes du MLD")

                    svg_document = svgwrite.Drawing(filename =sys.argv[i+1],

                                                            size = (1500,1500))
                    XmlExtraction(sys.argv[i-1])
            else:
                print("pas de fichier svg")



        elif sys.argv[2]=="json":
            print("traitement avec un fichier json")
            i+=1

            if sys.argv[i]=="-t":
                i+=1
                classe=ValidatorAndExtractorJson(sys.argv[sys.argv.index("-f")+1])
                print("")
                print("***** Relations *****")
                relations=ExtractionRelation(classe)
                classe=Classse(classe)
                print("")
                print("***** Classes *****")
                for cl in classe:
                    print("------------------------------")
                    print(cl.classe)
                    print("------------------------------")
                    for n in range(0,len(cl.attribut)):
                        print(cl.attribut[n],":",cl.valeur[n])
                        print("")
                print(" permet de dire si on veut les traces car -t est present ")
                if len(sys.argv)==i:
                    sys.exit()
            if sys.argv[i]=="-h":
                i+=1
                print("permet de désigner un input en flux http car -h est bien present"+sys.argv[i])
                creationFichierjson(sys.argv[i])
                i+=1
                if len(sys.argv)==i:
                    sys.exit()
            if sys.argv[i]=="-f":
                print("permet de désigner un input de type fichier "+sys.argv[i+1]+" car le -f est présent")
                i+=2
                if len(sys.argv)==i:
                    sys.exit()
            if sys.argv[i]=="-o":
                print(" le -o est bien présent")
                print("Ce qui reste c'est de creer un fichier svg valide respectant les normes du MLD")
                svg_document = svgwrite.Drawing(filename =sys.argv[i+1],
                                                size = (1500,1500))
                classe=ValidatorAndExtractorJson(sys.argv[i-1])
                classe=Classse(classe)
                Dessin(classe)
                # AssociationLine(relations[1],coord,0,0)

        else:
            print("format de fichier non prise en compte")
            print("Ce fichier doit respecter")
