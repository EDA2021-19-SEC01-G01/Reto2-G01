﻿"""
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
 """

import time
import tracemalloc
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog
# Funciones para la carga de datos
def loadData(catalog):
    #delta_time = -1.0
    #delta_memory = -1.0

    #tracemalloc.start()
    #start_time = getTime()
    #start_memory = getMemory()

    loadVideos(catalog)

    #stop_memory = getMemory()
    #stop_time = getTime()
    #tracemalloc.stop()

    #delta_time = stop_time - start_time
    #delta_memory = deltaMemory(start_memory, stop_memory)

    #return delta_time, delta_memory

def loadVideos(catalog):
    
    booksfile = cf.data_dir + 'videos-large.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'),delimiter=',')
    categorias = []
    paises=[]
    for video in input_file:
        id = video['category_id']
        pais=video["country"]
        if (id not in categorias):
            categorias.append(id)
            model.addCategory(catalog,id)
        model.addVideoPerCat(catalog,video,id)
        model.addVideo(catalog, video)
        if pais not in paises:
            paises.append(pais)
            model.addCountry(catalog,pais)
        model.addVideoPerC(catalog,video,pais)
        
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def reqCero(catalog,n,cate):
    return model.reqCero(catalog,n,cate)

def reqUno(catalog,n,categoria,pais):
    return model.reqUno(catalog,n,categoria,pais)

def reqDos(catalog,country):
    return model.reqDos(catalog,country)

def reqTres(catalog,category):
    return model.reqTres(catalog,category)

def reqCuatro(catalog,pais,n,tag):
    return model.reqCuatro(catalog,pais,n,tag)

# Funciones para medir tiempo y memoria

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory