import requests
import whois
import builtwith
from bs4 import BeautifulSoup
import csv

import gzip


def save_html_content(source_url, bs_parser_feature, file_name, extension, pages=False, headers=None, s_timeout=10):
    try:
        if pages == False:
            if headers == None:
                page = requests.get(source_url, timeout=s_timeout)
            else:
                page = requests.get(source_url, timeout=s_timeout, headers=headers)

            if page.status_code == 200:
                ruta = file_name + '.' + extension
                soup = BeautifulSoup(page.content, features=bs_parser_feature)
                output = open(ruta, "w", encoding='utf-8')
                output.write(soup.prettify())
                output.close()
            else:
                print(page.status_code)
        else:
            print('mm')

    except requests.exceptions.Timeout:
        print('error por timeout')
        pass
    except requests.exceptions.RequestException as err:
        print('error RequestException. Conexion o servidor no devuelven una respuesta HTTP útil')
        print(err)
        pass

def read_html_content(file_name, extension, bs_parser_feature):
    page = open(file_name + '.' + extension, "r", encoding='utf-8')
    soup = BeautifulSoup(page.read(),  features=bs_parser_feature)
    page.close()
    return soup;




def get_detalles(juegos):

    datos = []
    for juego in juegos:

        print('\n')

        nombre = juego.find("a", {"class": "product-item-link"})
        nombre_texto = nombre.getText().strip()

        rating = juego.find("div", {"class": "rating-result"})
        rating_texto = ''
        if rating:
            rating_texto = rating.getText().strip()
        else:
            rating_texto = 'None'

        precio = juego.find("span", {"class": "price"})
        precio_texto = ''
        if precio:
            precio_texto = precio.getText().strip()
        else:
            precio_texto = 'None'

        comentarios = juego.find("a", {"class": "action view"})
        comentarios_texto = ''
        if comentarios:
            comentarios.find('span').clear()
            if comentarios:
                comentarios_texto = comentarios.getText().strip()
            else:
                comentarios_texto = 'None'
        else:
            comentarios_texto = 'None'

        datos.append({'nombre': nombre_texto, 'rating': rating_texto, 'precio': precio_texto, 'numero_comentarios': comentarios_texto})

    return datos

def crear_csv(datos, nombre_csv):
    with open(nombre_csv, 'w', newline='') as csvfile:
        fieldnames = ['nombre', 'rating', 'precio', 'numero_comentarios']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for d in datos:
            writer.writerow({'nombre': d['nombre'], 'rating': d['rating'], 'precio': d['precio'], 'numero_comentarios': d['numero_comentarios'] })

def leer_csv(nombre_csv):
    print(nombre_csv)
    with open(nombre_csv, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        print(', '.join(row))

def get_all_game_data(soup):

    li_list = []
    games_info = []
    i = 0
    for gm in soup.findAll('li'):
        li_list.append((gm))

        li_item = li_list[i].get('class')
        if li_item != None:
            if 'product' in li_item:
                games_info.append(li_list[i])
        i = i+1

    return games_info

def save_images(soup):

    images = []
    i = 0
    for img in soup.findAll('img'):
        images.append(img.get('src'))
        if 'static' not in images[i]:
            print(images[i])
            r = requests.get(images[i], stream = True)
            if r.status_code == 200:
                print('nombre juego: ' +  img.get('alt'))
                nombre_imagen = images[i].split('/')
                nombre = nombre_imagen[(len(nombre_imagen)-1)]
                nombre_sin_extension = nombre.split('.')[0]
                ruta = "./images/" + nombre
                print(ruta)
                output = open(ruta, "wb")

                for chunk in r:
                    output.write(chunk)
                output.close()
        i = i+1

def create_header():
    headers = {
        "Accept": "text/html, application/xhtml+xml,application/xml;q=0.9,image/webp, \*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Cache-Control": "no-cache",
        "dnt": "1",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"  # no esta completo
    }
    return headers

def load_request(source_url):
    r = requests.get(source_url, stream = True)
    if r.status_code == 200:

        aSplit = source_url.split('/')
        ruta = "/" + aSplit[len(aSplit)-1]
        print(ruta)
        output = open(ruta, "wb")
        for chunk in r:
            output.write(chunk)
        output.close()

def url_tecnologies(url):
    print(builtwith.parse(url))

def web_owner(url):
    print(whois.whois(url))

# Pagina web a realizar web scraping
url = 'https://zacatrus.es/juegos-de-mesa.html'
# Nombre del archivo donde guardar la pagina web
file_name = 'pagina4'
# Se guarda html
save_html_content(url, 'html.parser', file_name, 'html', create_header())
# Se lee fichero html
soup = read_html_content(file_name, 'html', 'html.parser')
# Se estraen imagenes
#save_images(soup)
# Se extrae html de los juegos
datos_juegos = get_all_game_data(soup)
# Se extrae informacion de cada juego
datos = get_detalles(datos_juegos)
# Se guardan los datos extraidos
nombre_cvs = 'juegos.csv'
crear_csv(datos, nombre_cvs)
#leer_csv(nombre_cvs)



