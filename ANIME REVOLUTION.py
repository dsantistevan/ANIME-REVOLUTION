import Funciones as fc
import webbrowser
import numpy as np
import pandas as pd
import translate
menu1 = "\n" + "*"*25 + " ANIME REVOLUTION "+ "*"*25 +"\n"
menu2 = """1. - Crear Diccionario
2. - Consultar Información sobre un Anime.
3. - Consultar Información de animes por usuario.
4. - Crear Matriz.
5. - Reportes de Anime. 
6. - Salir \n"""

subMenu1 = "\n" + "*"*12 + " Submenú "+ "*"*12 +"\n"
subMenu2 = """a. - Animes por rating.
b. - Animes por tipo.
c. - Diferencias entre dos animes.
d. - Similitudes entre dos animes.
e. - Promedio de scores de todos los animes de un tipo.
f. - Regresar al menú principal. \n"""

opc = "a"
ListaOpc=list(map(str,range(1,7)))
genero = ""
diccionario = "No hay"
listaGenero = "No hay"
MatrizQ = "No hay"
opcSub = "a"
while opc != "6":
    print(menu1)
    print(menu2)
    opc = input("¿Que opción desea consultar?: ")
    while opc not in ListaOpc:
        opc = input("¿Que opción desea consultar?: ")
    if opc == "1":
        diccionario = fc.leerArchivoAnime("Anime_cleaned")
    elif opc == "2":
        if diccionario != "No hay":
            InfoAnime=fc.diccionarioAnimes()
            print( "\n" + '*'*30 + "\n|    Información de Anime    |\n" + '*'*30 )
            Anime=input("Ingrese el nombre del Anime: ")
            while Anime not in list(diccionario.keys()):
                Anime=input("Ingrese el nombre del Anime: ")
            print("\n"+"*"*60)
            Sinonimo=", ".join(InfoAnime[Anime][0].split("|"))
            URL=InfoAnime[Anime][1]
            Episodios=InfoAnime[Anime][2]
            Años=InfoAnime[Anime][3]
            Generos=InfoAnime[Anime][4]

            #Si al correr aparece el siguiente error:
            #requests.exceptions.HTTPError: 503 Server Error: Service Unavailable for url: https://translate.google.com/translate_a/...
            #Se debe a un exceso de tráfico hacia Google por medio de python, por lo que
            #se detecta que es un software, y Google bloquea el acceso de la
            #traducción. Si pasa esto, agregar un # antes de la siguiente línea. Caso contrario, dejarlo así.

            #Generos=(translate.translator("en","es",InfoAnime[Anime][4]))[0][0][0]

            #Esto pasa al traducir los géneros varias veces, se detecta como spam o software malicioso.
            #Sin ejecutar dicha linea, los generos se mantendrán en inglés.

            Usuarios=fc.UsuariosPorAnime(diccionario,Anime)
            print("Anime: %s\nSinónimo/s: %s\nImagen URL: %s\nEpisodios: %s\nAños al aire: %s\nGénero: %s\nTop 10 usuarios que ven la serie: \n-%s" %
                  (Anime,Sinonimo,URL,Episodios,Años,Generos,Usuarios))
            webbrowser.open(URL)
        else:
            print('\nNo se ha seleccionado la opción 1 que permite crear el diccionario.\n')
    elif opc == "3":
        if diccionario != "No hay":
            print("\n" + "*"*10 + " Animes por género "+ "*"*10 +"\n")
            print("Los generos que existen son:\n-%s" % "\n-".join(fc.ConjuntoGeneros(diccionario)))
            genero = input("Escoja el género a buscar: ").title()
            listaGenero = fc.ratingPorGenero(genero, diccionario)
            if listaGenero != "No hay":
                print ("\n" + "*"*5 + " Lista de animes del género: " + genero + " "+ "*"*5 +"\n"*2+"*"*150+"\n"+"Anime" + " "*70 + "Número episodios     Total Usuarios     Rating Promedio"+"\n"+"-"*150)
                for nombre,episodios,vistos,promedio in listaGenero:
                    val1 = len(nombre)
                    espacios1 = 75 - val1
                    val2 = len(str(episodios))
                    espacios2 = 21 - val2
                    val3 = len(str(vistos))
                    espacios3 = 19 - val3
                    print(nombre + " "*espacios1 + str(episodios) + " "*espacios2 + str(vistos) + " "*espacios3 + str(promedio))
        else:
            print('\nNo se ha seleccionado la opción 1 que permite crear el diccionario.\n')
    elif opc == "4":
        if diccionario != "No hay":
            Matriz = fc.MAnimes(diccionario)
            MatrizQ="Ya hay"
        else:
            print('\nNo se ha seleccionado la opción 1 que permite crear el diccionario.\n')
    elif opc == "5":
        if diccionario != "No hay" and MatrizQ != "No hay":
            while opcSub !="f":
                print(subMenu1)
                print(subMenu2)
                opcSub = input("Ingrese una opción de 'a'-'f': ").lower()
                if opcSub == "a":
                    ratings = fc.ratings(diccionario)
                    print("-"*20 +"\n| Anime por rating |\n" + "-"*20 +"\n\nLos Ratings existentes son: \n%s"% ratings)
                    ingresoRating = input("Ingrese un Rating: ")
                    cumplen = fc.AnimeRating(diccionario, ingresoRating)
                    print("\n" + "*" * 60)
                    print("Los animes que cumplen con el rating indicado son: %s"%cumplen)
                    if ingresoRating in ratings:
                        c=open("animeX"+ingresoRating+".fp","w")
                        c.write("Los animes que cumplen con el rating indicado son: %s"%cumplen)
                        c.close()
                        print("Su reporte ha sido guardado en el archivo "+ "animeX"+ingresoRating+".fp")
                elif opcSub == "b":
                    tipos=fc.Tipos(diccionario)
                    print("-" * 20 + "\n| Anime por tipo |\n" + "-" * 20 + "\n\nLos Ratings existentes son: \n%s" % tipos)
                    ingresoTipo=input("Ingrese un tipo")
                    cumplenTipo=fc.AnimeTipo(diccionario,ingresoTipo)
                    print("\n" + "*" * 60)
                    print("Los animes que cumplen con el tipo indicado son: %s" % cumplenTipo)
                    if ingresoTipo in tipos:
                        nombreAr="animeX"+ingresoTipo+".fp"
                        q=open(nombreAr,"w")
                        q.write("Los animes que cumplen con el tipo indicado son: %s" % cumplenTipo)
                        q.close()
                        print("Su reporte ha sido guardado en el archivo "+nombreAr)
                elif opcSub == "c":
                    print("-" * 35 + "\n| Diferencias entre dos animes |\n" + "-" * 35+"\n")
                    DosAnimes=input("Ingrese dos animes separados por (,): ").split(",")
                    while DosAnimes[0] and DosAnimes[1] not in list(diccionario.keys()):
                        DosAnimes=input("Ingrese dos animes separados por (,): ").split(",")
                    print("*"*65)
                    Conjunto=diccionario[DosAnimes[0]][4]
                    EW=0
                    LDiferencias={}
                    for i in DosAnimes:
                        print("Las características de %s son:" % i)
                        LAnime=diccionario[i]
                        MQ=Matriz[i]
                        print("\tTipo: %s"% LAnime[0])
                        if EW==0:
                            LDiferencias["Tipo"]=[LAnime[0]]
                        else:
                            LDiferencias["Tipo"].append(LAnime[0])
                        print("\tEpisodios: %s"% LAnime[1])
                        if EW==0:
                            LDiferencias["Episodios"]=[LAnime[1]]
                        else:
                            LDiferencias["Episodios"].append(LAnime[1])
                        print("\tEstado: %s" % LAnime[2])
                        if EW==0:
                            LDiferencias["Estado"]=[LAnime[2]]
                        else:
                            LDiferencias["Estado"].append(LAnime[2])
                        print("\tRating: %s" % LAnime[3])
                        if EW==0:
                            LDiferencias["Rating"]=[LAnime[3]]
                        else:
                            LDiferencias["Rating"].append(LAnime[3])
                        print("\tGeneros: %s"%", ".join(list(LAnime[4])))
                        print("\tPromedio Score: %.2f\n" % MQ[4])
                        if EW==0:
                            LDiferencias["Score"]=[MQ[4]]
                        else:
                            LDiferencias["Score"].append(MQ[4])
                        EW="dsd"
                        Conjunto2=LAnime[4]
                    ConjuntoDiferencia=Conjunto-Conjunto2
                    print("*"*60+"\n")
                    print("La diferencia entre ambos animes es: ")
                    saq=[]
                    for i in LDiferencias:
                        if LDiferencias[i][0]!=LDiferencias[i][1]:
                            saq.append(i+" "+str(LDiferencias[i][0]))
                    saq.append(", ".join(list(ConjuntoDiferencia)))
                    print(", ".join(saq))

                    nombreAr=input("Escriba el nombre de su reporte: ")
                    if len(nombreAr)==0:
                        nombreAr="SinNombre"
                    Luqa=[]
                    Luqa.append("-" * 35 + "\n| Diferencias entre dos animes |\n" + "-" * 35+"\n"*2)
                    Luqa.append("Ingrese dos animes separados por (,): %s\n" % ", ".join(DosAnimes))
                    Luqa.append("La diferencia entre ambos animes es:\n")
                    Luqa.append(", ".join(saq)+"\n")
                    fc.crearArchivo(nombreAr,Luqa)
                elif opcSub == "d":
                    print("-" * 35 + "\n| Similitudes entre dos animes |\n" + "-" * 35 + "\n")
                    DosAnimes = input("Ingrese dos animes separados por (,): ").split(",")
                    while DosAnimes[0] and DosAnimes[1] not in list(diccionario.keys()):
                        DosAnimes = input("Ingrese dos animes separados por (,): ").split(",")
                    print("*" * 65)
                    Conjunto = diccionario[DosAnimes[0]][4]
                    EW = 0
                    LDiferencias = {}
                    for i in DosAnimes:
                        print("Las características de %s son:" % i)
                        LAnime = diccionario[i]
                        MQ = Matriz[i]
                        print("\tTipo: %s" % LAnime[0])
                        if EW == 0:
                            LDiferencias["Tipo"] = [LAnime[0]]
                        else:
                            LDiferencias["Tipo"].append(LAnime[0])
                        print("\tEpisodios: %s" % LAnime[1])
                        if EW == 0:
                            LDiferencias["Episodios"] = [LAnime[1]]
                        else:
                            LDiferencias["Episodios"].append(LAnime[1])
                        print("\tEstado: %s" % LAnime[2])
                        if EW == 0:
                            LDiferencias["Estado"] = [LAnime[2]]
                        else:
                            LDiferencias["Estado"].append(LAnime[2])
                        print("\tRating: %s" % LAnime[3])
                        if EW == 0:
                            LDiferencias["Rating"] = [LAnime[3]]
                        else:
                            LDiferencias["Rating"].append(LAnime[3])
                        print("\tGeneros: %s" % ", ".join(list(LAnime[4])))
                        print("\tPromedio Score: %.2f\n" % MQ[4])
                        if EW == 0:
                            LDiferencias["Score"] = [MQ[4]]
                        else:
                            LDiferencias["Score"].append(MQ[4])
                        EW = "dsd"
                        Conjunto2 = LAnime[4]
                    ConjuntoSimilitud = Conjunto | Conjunto2
                    print("*" * 60 + "\n")
                    print("Las similitudes entre ambos animes es: ")
                    saq = []
                    for i in LDiferencias:
                        if LDiferencias[i][0] == LDiferencias[i][1]:
                            saq.append(i + " " + str(LDiferencias[i][0]))
                    saq.append(", ".join(list(ConjuntoSimilitud)))
                    print(", ".join(saq))
                    nombreAr = input("Escriba el nombre de su reporte: ")
                    if len(nombreAr) == 0:
                        nombreAr = "SinNombre"
                    Luqe=[]
                    Luqe.append("-" * 35 + "\n| Similitudes entre dos animes |\n" + "-" * 20 + "\n" * 2)
                    Luqe.append("Ingrese dos animes separados por (,): %s\n" % ", ".join(DosAnimes))
                    Luqe.append("Las similitudes entre ambos animes son:\n")
                    Luqe.append(", ".join(saq) + "\n")
                    fc.crearArchivo(nombreAr,Luqe)

                elif opcSub == "e":
                    DASQ={}
                    DTipos={"Movie":1.0,"Music":2.0,"ONA":3.0,"OVA":4.0,"Special":5.0,"TV":6.0,"Unknown":0.0}
                    for i in DTipos:
                        DASQ[DTipos[i]]=i
                    print("-" * 20 + "\n| Promedio Scores por Tipo |\n" + "-" * 20 + "\n\nLos Ratings existentes son: %s\n" % ", ".join(list(DTipos.keys())))
                    TIPO=input("Ingrese un tipo:")
                    while TIPO not in list(DTipos.keys()):
                        TIPO = input("Ingrese un tipo:")
                    Vbool= np.array(Matriz.iloc[2]==DTipos[TIPO])
                    sumatoria=Matriz.iloc[4, Vbool].mean()
                    print("*"*60)
                    print("El promedio de Scores de todos los animes de tipo %s es: %.2f" % (TIPO,sumatoria))
                    nombreAr=input("Escriba el nombre de su reporte: ")
                    Luqe=[]
                    Luqe.append("-" * 20 + "\n| Promedio Scores por Tipo |\n" + "-" * 20 + "\n\nLos Ratings existentes son: %s\n" % ", ".join(list(DTipos.keys())))
                    Luqe.append("Ingrese un tipo: %s\n" % TIPO)
                    Luqe.append("*"*60+"\n")
                    Luqe.append("El promedio de Scores de todos los animes de tipo %s es: %.2f\n" % (TIPO,sumatoria))
                    fc.crearArchivo(nombreAr, Luqe)


        else:
            print("No se han seleccionado las opciones 1 o 4 que permiten crear el diccionario y la matriz")