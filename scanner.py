import requests
import json
from bs4 import BeautifulSoup


###  Variables globales
FILE_JSON = "./data.json"
###  URLs general donde se encuentran los datos para traer los datos
URL_GENERAL = [ 'http://127.0.0.1/guflyscanner/listado_test.html' , 'https://visuales.uclv.cu/listado.html' ];
URL_GENERAL = URL_GENERAL[0]
###  Anno de las peliculas
anno_movie_test = ''

def function_for_connect( link ):
    ###  Abriendo las sessiones y enviando el get para traer datos nuevos
    session_explorer = requests.Session()
    session_explorer.trust_env = False
    resp_explorer = session_explorer.get( link )

    ###  Explorando los nuevos <a> para verficar cual de todos es el video
    soup_explorer = BeautifulSoup(resp_explorer.text, 'html.parser')
    links_explorer = soup_explorer.find_all('a')

    return links_explorer

###  Funcion para encontrar el archivo de video dentro de la carpeta del repo
def url_link_exporer(link_href_explorer):
    links_explorer = function_for_connect( link_href_explorer )

    ###  Inicializando las variables a un valor vacio para el caso en que no haya o subtitulo o video de pelicula
    ###  Si el valor no se inicia aqui la variable luego si no hay archivo de subtitulo no existiria ya que no se creario por estar detras de una condicional
    return_link_complete_video = ''
    return_link_complete_subtitle = ''

    ###  Verificando que tipo de archivo se esta analizando [video]
    ###  Recorrer la lista de <a> que quedo de BeautifulSoup
    for link_explorer in links_explorer:
        link_explorer_href = link_explorer.get('href')

        ###  Verificando cual de todos los archivos es el video analisando la extension en el final de su cadena (avi, mp4, webm, mkv ...)
        if link_explorer_href.endswith('.mkv') or link_explorer_href.endswith('.mp4') or link_explorer_href.endswith('.avi') or link_explorer_href.endswith('.webm') or link_explorer_href.endswith('.mov') or link_explorer_href.endswith('.wmv'):
            return_link_complete_video = link_href_explorer + link_explorer_href

    ###  Verificando si es un subtitulo del video
    ###  Recorrer la lista de <a> que quedo de BeautifulSoup
    for link_explorer in links_explorer:
        link_explorer_href = link_explorer.get('href')

        ###  Verificando cual de todos los archivos es el video analisando la extension en el final de su cadena (avi, mp4, webm, mkv ...)
        if link_explorer_href.endswith('.srt') or link_explorer_href.endswith('.biff') or link_explorer_href.endswith('.sub') or link_explorer_href.endswith('.usf'):
            return_link_complete_subtitle = link_href_explorer + link_explorer_href

    ###  Objeto que se le devulve con el url del video y del subtitulo
    object_return = {
        'video' : return_link_complete_video,
        'subtitulo' : return_link_complete_subtitle
    }
    return object_return


###  Funcion para sacar correctamente el nombre de la pelicula
def url_link_name( name_movie ):
    ###  Escribiendo el nombre original de la pelicula
    print( name_movie )

    ###  Separando el anno del nombre original de la pelicula en este caso (_)
    name_movie_array = name_movie.split('_')

    ###  Verificando que exista almenos el nombre de la pelicula
    if name_movie_array[1] != '':
        ###  Formateando el nombre de la pelicula. Separando los elementos del array por cada uno de los '.' que haya en el nombre de la pelicula
        name_movie_array_array = name_movie_array[1].split('.')

        ###  Recorriendo el array en este caso para mostrarlo por consola pero la realidad estaria en una varibale ocn el nombre final de la pelicula y ese seria el return de esta funcion 
        name_complete_separator = ' '

        ###  Empaquetando en la variable name siguiente el nombre completo de la pelicula
        name_complete_finali = name_complete_separator.join( name_movie_array_array )

        ###  ELiminado espacios en blanco al inicio y al final del nombre de la pelicula
        name_complete_finali = name_complete_finali.rstrip()
        name_complete_finali = name_complete_finali.lstrip()

        ###  Mostrando la salida por consola
        print( name_complete_finali + '\n' )

        return name_complete_finali


###  Funcionn para verificar el nombre del enlace para decidir si procesarlo en el JSON o no
def function_verification_name_link( name ):
    ###  Verificando si es el enlace que dice 2021
    if name == 'Subs' or ( function_verification_anno_movie( name ) ):
        return False
    else:
        return True


###  Funcion para verificar el anno de la pelicula
def function_verification_anno_movie(  anno_text ):
    if anno_text.isdigit() and len( anno_text ) == 4 and ( anno_text.find('19') != -1 or anno_text.find('20') != -1 ):
        return True
    else:
        return False



###  Punto de partida de este programa
if __name__ == '__main__':

    links = function_for_connect( URL_GENERAL )

    ### Recorrer el Array con for in
    link_peliculas = 'Peliculas/Extranjeras/2021'

    ###  Borrar lo que ya esta escrito en el archivo
    filew = open( FILE_JSON , 'w')
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
            ###  Verificador para annadir el anno a las peliculas
            if function_verification_anno_movie( link.get_text() ):
                anno_movie_test = link.get_text()

            ###  Verificar si es valido en nombre del enlace como una pelicula para procesarlo en el JSON
            if function_verification_name_link( link.get_text() ):

                ###  Se ejecuta si el <a> tiene la condicion que necesito
                name_archivo_end_url = url_link_exporer(link_href)

                ###  Sacar el nombre real de la pelicula
                nombre_real_to_show = url_link_name( link.get_text() )

                jsonObject[ index ] = {
                    'name_video': nombre_real_to_show,
                    'anno_video': anno_movie_test,
                    'url_video' : name_archivo_end_url['video'],
                    'url_subtitle' :  name_archivo_end_url['subtitulo'],
                    'url_folder' : link_href
                }

                ###  Andirle 1 al contador
                index = index + 1


    ###  Abrir el archivo para escribir a partir de la ultima linea
    json.dump( jsonObject , filew , indent=4 )
    filew.close()