import requests
import json

###  todo Variables Globales
FILE_JSON = 'data_company.json'
OBJECT_JSON = []
RANGE_ARRAY = list(range( 1 , 1000 ))


### * Funcion que se llama en forma de bucle
def function_for_connect( id_url ):
    #*  Abriendo las sessiones y enviando el get para traer datos nuevos
    session_explorer = requests.Session()
    session_explorer.trust_env = False

    #*  Convirtiendo el id en un string para poder concatenarlo con la URL que es un string
    id_url = str( id_url )

    #*  Haciendo un GET a la API de themoviedb
    resp_explorer = session_explorer.get( 'https://api.themoviedb.org/3/company/' + id_url + '?api_key=834059cb24bc11be719c241a12f537f4&language=es' )

    #*  Retornando lo que TheMovieDB devolvio en el GET
    return resp_explorer



### * El script inicia aqui
if __name__ == '__main__':
    # * For con el que
    for i in RANGE_ARRAY:
        #*  Annadiendo a este objeto el JSON que me devulve esta funcion
        json_devolver = function_for_connect( i )

        #*  Formateando el JSON que me devuelve la anterio funcion de la API
        data = json.loads(json_devolver.text)

        #*  Almacenando en el Objeto el item - 2 para que coincidan los rangos de las listas
        #OBJECT_JSON[ i - 2 ] = { 'data': data }
        OBJECT_JSON.append( { 'data': data } )

        #* Imprimir a modo de log la respuesta en la consola
        print( data )

    #*  Borrar lo que ya esta escrito en el archivo
    filew = open( FILE_JSON , 'w')
    filew.write('')

    #*  Abrir el archivo para escribir a partir de la ultima linea
    json.dump( OBJECT_JSON , filew , indent=4 )
    filew.close()
