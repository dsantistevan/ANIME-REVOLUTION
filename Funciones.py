def leerArchivoUsuario(usuario):
    f = open(usuario + ".csv", "r", encoding="utf-8-sig")
    dicNombreCodigo = {}
    f.readline()
    for lineas in f:
        lineas = lineas.strip().split(",")
        codigos = lineas[1]
        nombre = lineas[0]
        score = lineas[5]
        if codigos not in dicNombreCodigo:
            dicNombreCodigo[codigos] = {nombre: score}
        else:
            dicNombreCodigo[codigos].update({nombre: score})
    f.close()
    return dicNombreCodigo


def leerArchivoAnime(anime):
    Puntaje=(leerArchivoUsuario("UserAnimeList"))
    diccionario = {}

    archivoAnimes = open(anime + ".csv", "r", encoding='utf-8')
    archivoAnimes.readline()
    for i in archivoAnimes:
        i = i.strip().split(",")
        titulo = i[1]
        tipo = i[5]
        episodios = i[7]
        estado = i[8]
        rating = i[12]
        generos = set(i[-1].split("|"))
        codigo = i[0]
        if codigo in (Puntaje.keys()):
            userScore = Puntaje[codigo]
        else:
            userScore={}
        L = [tipo,episodios,estado,rating,generos,userScore]
        diccionario[titulo] = L
    archivoAnimes.close()

    print("\nEl diccionario ha sido creado.")
    return diccionario



def ConjuntoGeneros(diccionario):
    Conj=set()
    for i in diccionario:
        Conj.update(diccionario[i][-2])
    Conj.remove("")
    L=list(Conj)
    for i in range(len(L)):
        L[i]=L[i].title()
    Conj=set(L)
    return Conj

def ratingPorGenero(genero, diccionario):
    listaRetornar = [] #lista para los animes que están en aire en este momento
    listaDic = diccionario.items()
    for anime,datos in listaDic: #recorro la lista de animes con datos
        L = []
        total_vistos = 0
        total_rating = 0
        promedio_rating = 0
        if datos[2] == 'Currently Airing': #verifico que el anime esté al aire
            for genre in datos[4]: #ahora recorro su lista de generos
                if genre == genero: #si el género a buscar está dentro de los datos
                    if datos[5] != None:
                        for usuario,rank in datos[5].items():
                            total_vistos = total_vistos + 1
                            total_rating = total_rating + int(rank)
                        if total_vistos>0:
                            promedio_rating = total_rating/total_vistos
                        else:
                            promedio_rating=0
                    L = [anime,datos[1],total_vistos,promedio_rating]
                    listaRetornar.append(L)
    listaRetornar.sort(key=lambda x: x[:][3], reverse=True)
    if len(listaRetornar) > 15:
        return listaRetornar[:15]
    elif len(listaRetornar) > 0:
        return listaRetornar
    else:
        return "No hay"
    
def diccionarioAnimes():
    d={}
    f=open("Anime_cleaned.csv","r",encoding="utf-8-sig")
    for linea in f:
        T=linea.strip().split(",")
        L=[]
        if T[3]=="":
            L.append("Ninguno")
        else:
            L.append(T[3])
        L.append(T[4])
        L.append(T[7])
        Fechas=T[10].replace("|",",")
        Fechas=Fechas.replace("'","")
        if "None" in Fechas:
            Fechas=Fechas.replace("None","No hay fecha- - ")
        Fechas=Fechas.replace("{from: ","").replace(" to: ","").replace("}","")
        Fechas=Fechas.split(",")
        for i in range(len(Fechas)):
            Fechas[i]=Fechas[i].split("-")[0]
        Fechas=" al ".join(Fechas)
        L.append(Fechas)
        L.append(", ".join(list(set(T[-1].split("|")))))
        d[T[1]]=L
    f.close()
    return d

def UsuariosPorAnime(diccionario,Anime):
    d=diccionario[Anime][-1]
    L=sorted(d.items(),key= lambda x:int(x[1]),reverse=True)
    Usuarios=[]
    for i in range(len(L)):
        Usuarios.append(L[i][0])
    if len(Usuarios)>10:
        return "\n- ".join(Usuarios[:10])
    else:
        return "\n- ".join(Usuarios[:10])


def promedioScores(diccionario):
    A=list(diccionario.values())
    return sum(A)/len(A)


def MAnimes(diccionario):
    import pandas as pd
    diccionarioTipos = {"Movie": 1.0, "Music": 2.0, "ONA": 3.0, "OVA": 4.0, "Special": 5.0, "TV": 6.0, "Unknown": 0.0}
    diccinarioRatings = {"G - All Ages": 1.0, "PG - Children": 2.0, "PG-13 - Teens 13 or older": 3.0,
                         "R - 17+ (violence & profanity)": 4.0, "R+ - Mild Nudity": 5.0, "Rx - Hentai": 6.0,
                         "None": 0.0}
    dicMatriz = {}
    for nombre, lista in diccionario.items():
        genero = float(len(lista[4]))
        rating = diccinarioRatings[lista[3]]
        tipo = diccionarioTipos[lista[0]]
        score = 0
        longitud = len(lista[-1])
        for usuario, puntaje in lista[-1].items():
            score += float(puntaje)
        if longitud != 0:
            promedio = score / longitud
        else:
            promedio = 0.0
        episodios = float(lista[1], )
        promedio = round(promedio, 2)
        dicMatriz[nombre] = [episodios, genero, tipo, rating, promedio]
    frame = pd.DataFrame(dicMatriz)
    print("\nLa Matriz ha sido creada\n")
    print(frame.head())
    return frame

def ratings(diccionario):
    conjunto = set()
    for nombre, lista in diccionario.items():
        conjunto.add(lista[3])
    conjunto.remove("None")
    return "\n-%s\n"% "\n-".join(list(conjunto))

def AnimeRating(diccionario, rating):
    L =[]
    for nombre, lista in diccionario.items():
        if rating == lista[3]:
            L.append(nombre)
    return "\n-%s"% "\n- ".join(L)

def Tipos(diccionario):
    conjunto = set()
    for nombre, lista in diccionario.items():
        conjunto+=lista[4]
    conjunto.remove("None")
    return "\n-%s\n"% "\n-".join(list(conjunto))

def AnimeTipo(diccionario, tipo):
    L =[]
    for nombre, lista in diccionario.items():
        if tipo in lista[4]:
            L.append(nombre)
    return "\n-%s"% "\n- ".join(L)

def crearArchivo(nombre,lineas):
    c=open(nombre+".sp","w")
    for i in lineas:
        c.write(i)
    c.close()