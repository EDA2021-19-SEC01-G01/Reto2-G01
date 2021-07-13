"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Ordenar los n videos con más views para una categoría específica")
    print("3- Requerimiento 1")
    print("4- Requerimiento 2")
    print("5- Requerimiento 3")
    print("6- Requerimiento 4")
    print("0- Salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.initCatalog()
        #measure = controller.loadData(catalog)
        controller.loadData(catalog)
        print ("La cantidad de videos cargados son: " + str(lt.size(catalog['videos'])))
        print ("La cantidad de categorías cargadas son: " + str(mp.size(catalog['categorias'])))
        #print ("Tiempo [ms]: ", f"{measure[0]:.3f}", "  ||  ",
        #      "Memoria [kB]: ", f"{measure[1]:.3f}")
    elif int(inputs) == 2:
        n = int(input("Ingrese el número de videos: "))
        cate = input("Ingrese el id de la categoría a filtrar: ")
        print(controller.reqCero(catalog,n,cate))
    elif int(inputs) == 3:
        categoria = input("Ingrese el id de la categoría a consultar: ")
        pais = input("Ingrese el país filtro: ")
        n = int(input("Ingrese el número de videos: "))
        print(controller.reqUno(catalog,n,categoria,pais))
    elif int(inputs)== 4:
        pais = input("Ingrese el país filtro: ")
        gold = (controller.reqDos(catalog,pais))['elements']
        if gold == "No hay ningún video con ese ratio de likes/dislikes":
            print(gold)
        else:
            for ind in range(1,lt.size(gold)+1):
               print(lt.getElement(gold,ind))
    elif int(inputs) == 5:
        category = input("Ingrese la categoría a consultar: ")
        silver = (controller.reqTres(catalog,category))['elements']
        if silver == "No hay ningún video con ese ratio de likes/dislikes":
            print(silver)
        else:
            for ind in range(1,lt.size(silver)+1):
               print(lt.getElement(silver,ind))
    elif int(inputs) == 6:
        pais = input("Ingrese el filtro por país: ")
        n = int(input("Ingrese el número de videos a listar: "))
        tag = input("Ingrese la etiqueta del video: ")
        rtas = controller.reqCuatro(catalog,pais,n,tag)
        print(rtas)
    elif int(inputs) == 0:
        sys.exit(0)
    else:
        sys.exit(0)
sys.exit(0)
