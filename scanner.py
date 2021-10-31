import requests
import json
from bs4 import BeautifulSoup
import os


###  Variables globales
filejson = "./data.json"


###  Funcion para encontrar el archivo de video dentro de la carpeta del repo
def url_link_exporer(link_href_explorer):
    ###  Abriendo las sessiones y enviando el get para traer datos nuevos
    session_explorer = requests.Session()
    session_explorer.trust_env = False
    resp_explorer = session.get( link_href_explorer )

    ###  Explorando los nuevos <a> para verficar cual de todos es el video
    soup_explorer = BeautifulSoup(resp_explorer.text, 'html.parser')
    links_explorer = soup_explorer.find_all('a')

    ###  Recorrer la lista de <a> que quedo de BeautifulSoup
    for link_explorer in links_explorer:
        link_explorer_href = link_explorer.get('href')

        ###  Verificando cual de todos los archivos es el video analisando la extension en el final de su cadena (avi, mp4, webm, mkv ...)
        if link_explorer_href.endswith('.mkv') or link_explorer_href.endswith('.mp4') or link_explorer_href.endswith('.avi') or link_explorer_href.endswith('.webm') or link_explorer_href.endswith('.mov') or link_explorer_href.endswith('.wmv'):
            #print(link_href_explorer + "" + link_explorer_href)
            return link_href_explorer + link_explorer_href


###  Funcion para sacar correctamente el nombre de la pelicula
def url_link_name( name_movie ):

    ###  Verificando que no sea el <a> del ano de las pelis
    #if name_movie != '2021':
    ###  Escribiendo el nombre original de la pelicula
    print( name_movie )

    ###  Separando el anno del nombre original de la pelicula en este caso (_)
    name_movie_array = name_movie.split('_')

    ###  Verificando que exista almenos el nombre de la pelicula
    if name_movie_array[1] != '':
        ###  Formateando el nombre de la pelicula. Separando los elementos del array por cada uno de los '.' que haya en el nombre de la pelicula
        name_movie_array_array = name_movie_array[1].split('.')

        ###  Recorriendo el array en este caso para mostrarlo por consola pero la realidad estaria en una varibale ocn el nombre final de la pelicula y ese seria el return de esta funcion 
        name_complete_finali = ''
        for item in name_movie_array_array:
            ###  Empaquetando en la variable name siguiente el nombre completo de la pelicula
            name_complete_finali = item + " "
        
        print( name_complete_finali + '\n' )
        
        return name_complete_finali
        


###  Punto de partida de este programa
if __name__ == '__main__':
    ###  URLs para traer los datos
    url = [ 'http://127.0.0.1/guflyjson/listado.php' , 'http://127.0.0.1/guflyjson/listado_test.html' , 'https://visuales.uclv.cu/listado.html' ]

    ###  Creo una sesion para la conexion (evitando el proxy para python)
    session = requests.Session()
    session.trust_env = False

    ###  Haciendo el GET de la URL que se desea tratar 
    resp = session.get( url[1] )

    ###  Trabajo con el HTML ###

    ###  Creando un objeto para tratar con BeautifulSoup
    soup = BeautifulSoup(resp.text, 'html.parser')

    ###  Almacenar todas las <a> en un array
    links = soup.find_all('a')

    ### Recorrer el Array con for in
    link_peliculas = 'Peliculas/Extranjeras/2021'
    
    ###  Borrar lo que ya esta escrito en el archivo
    filew = open( filejson , 'w')
    filew.write('')
    jsonObject = {}
    index = 0

    for link in links:
        ###  Links dentro de la web
        link_href = link.get('href')
        
        ###  Indicarme con -1 si no tiene la condicion de link_peliculas
        link_href_find = link_href.find(link_peliculas)

        ###  Detectar a salido por consola para 
        if int(link_href_find) == -1:
            print('no esta ...')
        else:
            ###  Se ejecuta si el <a> tiene la condicion que necesito
            name_archivo_end_url = url_link_exporer(link_href)

            ###  Sacar el nombre real de la pelicula
            nombre_real_to_show = url_link_name( link.get_text() )
            
            jsonObject[ index ] = { 'name': nombre_real_to_show , 'name_url' : link.get_text() , 'url' : name_archivo_end_url }
            
            ###  Andirle 1 al contador
            index = index + 1


    ###  Abrir el archivo para escribir a partir de la ultima linea
    json.dump( jsonObject , filew )
    filew.close()