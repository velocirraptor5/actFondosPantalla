import argparse
import datetime
import csv
import logging
logging.basicConfig(level=logging.INFO)
import re

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError


import  Movies_page_objects as Movies
from common import config

logger=logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$')# https://example.com/hello
is_root_path = re.compile(r'^/.+$')# /some-text


def _movies_scraper(movies_site_uid):
    host= config()['movies_sites'][movies_site_uid]['url']

    logging.info('Empesando scrape para {}'.format(host))
    homepage = Movies.HomePage(movies_site_uid,host)
    
    encontradas=[]
    for link in homepage.movies_links:
        movie=_fetch_movie(movies_site_uid,host,link)
        if movie:
            logger.info('se encontro pelicula')
            encontradas.append(movie)
    #_save_encontradas(movies_site_uid,encontradas)

def _save_encontradas(movies_site_uid,encontradas):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name='{movies_site_uid}_{datetime}_encontradas.csv'.format(
        movies_site_uid=movies_site_uid,
        datetime=now)
    csv_titles = list(filter(lambda  property: not property.startswith('_'),dir(encontradas[0])))

    with open(out_file_name,mode='w+') as f:
        writer = csv.writer(f)
        writer.writerow(csv_titles)

        for movie in encontradas:
            row = [str(getattr(movie,prop))for prop in csv_titles]
            writer.writerow(row)

def _fetch_movie(movies_site_uid,host,link):
    logger.info('Observando la pelicula en {}'.format(link))
    movie= None
    try:
        movie = Movies.MoviePage(movies_site_uid,_build_link(host,link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error buscando el articulo', exc_info=False)

    if movie and not movie.title:
        logger.warning('Pelicual invalidad. no tiene titulo')
        return None
    return movie
    
def _build_link(host,link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host,link)
    else:
        return '{host}/{url}'.format(host=host,url=link)

if __name__ == "__main__":
    parser= argparse.ArgumentParser()

    movies_sites_choise =(list)(config()['movies_sites'].keys())
    parser.add_argument('movies_sites',
                        help='La pagina de peliculas que quieres scrapear',
                        type=str,
                        choices=movies_sites_choise)
    args =parser.parse_args()
    _movies_scraper(args.movies_sites)
    