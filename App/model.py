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
               'categorias': None}

    catalog['videos'] = lt.newList('ARRAY_LIST')
    catalog['categorias'] = mp.newMap(18,maptype='PROBING',loadfactor=0.5)
    return catalog
# Funciones para agregar informacion al catalogo
def addCategory(catalog, id):
    """
    Adiciona una categoría a la lista de categorias.
    """
    mp.put(catalog['categorias'],id,lt.newList('ARRAY_LIST'))

def addVideo(catalog, video):
    lt.addLast(catalog['videos'],video)

def addVideoPerCat(catalog,video,id):
    lista = (mp.get(catalog['categorias'],id))['value']
    lt.addLast(lista,video)

# Funciones para creacion de datos

# Funciones de consulta
def reqCero (catalog, n, cate):
    dataCat = (mp.get(catalog['categorias'],cate))['value']
    return (sortVideos(dataCat,4,cmpVideosByViews,n))

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpVideosByViews(video1, video2):
    """
    Devuelve verdadero (True) si los Views de video1 son mayores que los del video2
    Args:
    video1: informacion del primer video que incluye su valor 'views'
    video2: informacion del segundo video que incluye su valor 'views'
    """
    return (int(video1['views']) > int(video2['views']))
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

def sortVideos (listaO,ordAlg,cmp,n):
    sorted_list = comoOrdenar(listaO,cmp,ordAlg)
    subList = lt.subList(sorted_list,1,n)
    return subList
