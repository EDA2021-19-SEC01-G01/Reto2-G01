"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as sls
from DISClib.Algorithms.Sorting import quicksort as qck
from DISClib.Algorithms.Sorting import mergesort as mrg
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    
    catalog = {'videos': None,
               'categorias': None,
                "paises" : None}

    catalog['videos'] = lt.newList('ARRAY_LIST')
    catalog['categorias'] = mp.newMap(18,maptype='PROBING',loadfactor=0.5)
    catalog["paises"]=mp.newMap(10,maptype="PROBING",loadfactor=0.5)
    return catalog
# Funciones para agregar informacion al catalogo
def addCategory(catalog, id):
    """
    Adiciona una categoría a la lista de categorias.
    """
    mp.put(catalog['categorias'],id,lt.newList('ARRAY_LIST'))

def addCountry (catalog,country):
    mp.put(catalog['paises'],country,lt.newList('ARRAY_LIST'))

def addVideo(catalog, video):
    lt.addLast(catalog['videos'],video)

def addVideoPerCat(catalog,video,id):
    lista = (mp.get(catalog['categorias'],id))['value']
    lt.addLast(lista,video)

def addVideoPerC (catalog,video,country):
    lista = (mp.get(catalog['paises'],country))['value']
    lt.addLast(lista,video)
# Funciones para creacion de datos

# Funciones de consulta
def printReq1(lista, criterios):
    listaFinalFinal = lt.newList('ARRAY_LIST')
    for j in range(1,lt.size(lista)+1):
        listaPorVideo = lt.newList('ARRAY_LIST')
        for crit in criterios:
            video = lt.getElement(lista,j)
            lt.addLast(listaPorVideo,video[crit])
        lt.addLast(listaFinalFinal,listaPorVideo['elements'])
    return listaFinalFinal['elements']

def reqCero (catalog, n, cate):
    dataCat = (mp.get(catalog['categorias'],cate))['value']
    return (lt.subList(sortVideos(dataCat,4,cmpVideosByViews),1,n))

def reqUno (catalog,n,categoria,pais):
    dataCat = (mp.get(catalog['categorias'],categoria))['value']
    catSort = sortVideos(dataCat,4,cmpVideosByLikes)
    if lt.size(catSort) >= n:
        catPais = lt.subList(filtroPais(catSort,pais),1,n)
    else:
        catPais = catSort
    listaImprimir = printReq1(catPais, ['trending_date','title','channel_title','publish_time','views','likes','dislikes'])
    return listaImprimir

def reqDos (catalog,country):
    dataPais=(mp.get(catalog['paises'],country))['value']
    soloTop = ratioLikesDislikes(dataPais,10)
    return sortVideos3(soloTop,4,cmpVideosByTrend)

def reqTres (catalog, category):
    dataCat = (mp.get(catalog['categorias'],category))['value']
    soloTop = ratioLikesDislikes(dataCat,20)
    return sortVideos3(soloTop,4,cmpVideosByTrend)

def reqCuatro(c,p,n,t):
    clas = lt.newList("ARRAY_LIST")
    ids = []
    vid = mp.get(c['paises'],p)['value']
    dicc= {}
    for i in range(1,lt.size(vid)+1):
        ele = lt.getElement(vid,i)
        id = ele['video_id']
        tag = ele["tags"]
        a2,a3=(id not in ids), (t in tag)
        if  a2 and a3 :
            ids.append(id)
            e= lt.newList("ARRAY_LIST")
            dicc[id]= e
            lt.addLast(dicc[id],ele)
        elif a3:
            lt.addLast(dicc[id],ele)
        
    for i in dicc.keys():
        if lt.size(dicc[i]) > 0:
            d= sortvideos4(dicc[i],4,cmpVideosByComments)
            lt.addLast(clas,d)
        else:
            print(dicc[i])
            lt.addLast(clas,lt.firstElement(dicc[i]))
    
    l_final= comoOrdenar(clas,cmpVideosByComments,4)
    if lt.size(l_final) >= n:
        rta = lt.subList(l_final,1,n)
    else:
        rta = l_final

    rtaF = printReq1(rta,['title', 'channel_title','publish_time','views','likes','dislikes','comment_count','tags'])
    return rtaF

def filtroPais(lista, country):
    soloCountry = lt.newList("ARRAY_LIST")
    ids = []
    vid = lista
    tamano = lt.size(vid)
    for i in range(1,tamano+1):
        ele = lt.getElement(vid,i)
        c1 = ele['country']
        id1 = ele['video_id']
        if c1 == country and (id1 in ids) == False:
            lt.addLast(soloCountry, ele)
            ids.append(id1)
    return soloCountry

def ratioLikesDislikes (lista, umbral):
    #Calcula los vídeos con un rating mayor a umbral.
    dict_id={}
    lista_id_top=lt.newList("ARRAY_LIST")
    for j in range(1,lt.size(lista)+1):
        ele=lt.getElement(lista,j)
        vid_id=ele['video_id']
        likes=int(ele["likes"])
        dislikes=int(ele["dislikes"])
        title = ele['title']
        channel_title = ele['channel_title']
        if vid_id not in dict_id:
            count=0 
            dict_id[vid_id]=[likes,dislikes,count+1,title,channel_title]
        else:
            dict_id[vid_id][0]=likes
            dict_id[vid_id][1]=dislikes
            dict_id[vid_id][2]+=1
    for i in dict_id:
        if dict_id[i][1]==0 and dict_id[i][0]>0:
            xd = lt.newList("ARRAY_LIST")
            lt.addLast(xd,dict_id[i][3])
            lt.addLast(xd,dict_id[i][4])
            lt.addLast(xd,"no tiene dislikes")
            lt.addLast(xd,dict_id[i][2])
            lt.addLast(xd,i)
            lt.addLast(lista_id_top,xd)
        elif dict_id[i][0]==0:
            pass
        else:
            ratio=dict_id[i][0]/dict_id[i][1]
            if ratio>umbral:
                xd = lt.newList("ARRAY_LIST")
                lt.addLast(xd,dict_id[i][3])
                lt.addLast(xd,dict_id[i][4])
                lt.addLast(xd,ratio)
                lt.addLast(xd,dict_id[i][2])
                lt.addLast(xd,i)
                lt.addLast(lista_id_top,xd)
    return lista_id_top

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpVideosByViews(video1, video2):
    """
    Devuelve verdadero (True) si los Views de video1 son mayores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'views'
    video2: informacion del segundo video que incluye su valor 'views'
    """
    return (int(video1['views']) > int(video2['views']))

def cmpVideosByLikes(video1, video2):
    """
    Devuelve verdadero (True) si los Likes de video1 son mayores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'likes'
    video2: informacion del segundo video que incluye su valor 'likes'
    """
    return (int(video1['likes']) > int(video2['likes']))

def cmpVideosByTrend(video1, video2):
    """
    Devuelve verdadero (True) si los TrendDays :) de video1 son menores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor días en Trend
    video2: informacion del segundo video que incluye su valor días en Trend
    """
    days1 = lt.getElement(video1,4)
    days2 = lt.getElement(video2,4)
    if days1 == days2:
        rat1 = lt.getElement(video1,3)
        rat2 = lt.getElement(video2,3)
        if type(rat1) != float or type(rat2) != float:
            rta = (days1 > days2)
        else:
            rta = (rat1 > rat2)
    else:
        rta = (days1 > days2)
    return rta

def cmpVideosByComments(video1,video2):
    return (int(video1['comment_count']) > int(video2['comment_count']))

# Funciones de ordenamiento
def comoOrdenar (sub_list,cmpF,ordAlg):
    if ordAlg == 1:
        return sa.sort(sub_list, cmpF)
    elif ordAlg == 2:
        return ins.sort(sub_list, cmpF)
    elif ordAlg == 3:
        return sls.sort(sub_list, cmpF)
    elif ordAlg == 4:
        return mrg.sort(sub_list, cmpF)
    elif ordAlg == 5:
        return qck.sort(sub_list, cmpF)

def sortVideos (listaO,ordAlg,cmp):
    sorted_list = comoOrdenar(listaO,cmp,ordAlg)
    return sorted_list

def sortVideos3 (listaFinal,ordAlg,cmp):
    sortedList=comoOrdenar(listaFinal,cmp,ordAlg)
    if lt.size(sortedList) == 0:
        return "No hay ningún video con ese ratio de likes/dislikes"
    else:
        top_trend=lt.firstElement(sortedList)
        return top_trend

def sortvideos4(lista,oa,cmp):
    sortedList=comoOrdenar(lista,cmp,oa)
    rta= lt.firstElement(sortedList)
    return rta