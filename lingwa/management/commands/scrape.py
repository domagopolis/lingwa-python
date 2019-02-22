from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from urlparse import urlparse

from django.core.management.base import BaseCommand, CommandError
from lingwa.models import Url, Image, Utterence, Keyword, Language

def log_error(e):
    print(e)

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None and content_type.find('html') > -1)

def save_utterance(language, text):
    utterence = Utterence.objects.all().filter(language=language, utterence=text).first()
    if utterence:
        utterence.count += 1;
    else:
        utterence = Utterence(language=language, utterence=text)

    return utterence.save()

def get_responce():
    url = Url.objects.all().filter(active=True).first()
    if url is not None:
        response = simple_get(url.url)

        if response is not None:
            soup = BeautifulSoup(response, 'html.parser')

            html = soup.find('html')
            language = Language.objects.all().filter(iso2letter=html['lang']).first()

            title = soup.find('title')
            save_utterance(language, title.get_text().strip())

            for img in soup.find_all('img', src=True):
                if img['src'].strip():
                    parse_url = urlparse(img['src'])
                    if parse_url.scheme is None:
                        parse_url.scheme = 'https'
                    image = Image(src=img['src'])
                    image.save()
                if img['alt'].strip():
                    save_utterance(language, img['alt'])

            heading_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
            for heading_tag in heading_tags:
                for heading in soup.find_all(heading_tag):
                    if heading.get_text().strip():
                        save_utterance(language, heading.get_text())

            for p in soup.find_all('p'):
                if p.get_text().strip():
                    save_utterance(language, p.get_text())

            links = set()
            for a in soup.find_all('a', href=True):
                links.add(a['href'])
                if a.get_text().strip():
                    save_utterance(language, a.get_text())

            #url.last_read = date
            #url.save()

            return list(links)

class Command(BaseCommand):
    help = 'Read those sites'

    def add_argument(self, parser):
        pass

    def handle(self, *args, **options):
        links = get_responce()

        if links is not None:
            results = []
            for link in links:
                try:
                    print(link)
                except:
                    log_error('Skipping:'.format(link))
