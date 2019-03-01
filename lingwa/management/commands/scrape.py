from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from urlparse import urlparse
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from lingwa.models import Url, Image, Utterence, UtterenceUrl, UtterenceImage, Keyword, Language

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
    utterence.save()

    return utterence

def save_utterance_to_url(language, text, url):
    utterence = save_utterance(language, text)

    utterence_url = UtterenceUrl(utterence=utterence, url=url)
    utterence_url.save()

    return utterence_url

def save_utterance_to_image(language, text, image):
    utterence = save_utterance(language, text)

    utterence_image = UtterenceImage(utterence=utterence, image=image)
    utterence_image.save()

    return utterence_image

def get_responce():
    url = Url.objects.all().filter(last_read__isnull=True, active=True).first()
    if url is not None:
        response = simple_get(url.url)

        if response is not None:
            soup = BeautifulSoup(response, 'html.parser')
            parse_url = urlparse(url.url)

            html = soup.find('html')
            language = Language.objects.all().filter(iso2letter=html['lang']).first()

            title = soup.find('title')
            save_utterance_to_url(language, title.get_text().strip(), url)

            for img in soup.find_all('img', src=True, alt=True):
                if img['src'].strip():
                    img_parse_url = urlparse(img['src'])
                    if not img_parse_url.scheme:
                        img_parse_url = img_parse_url._replace(scheme=parse_url.scheme)
                    if not img_parse_url.netloc:
                        img_parse_url = img_parse_url._replace(netloc=parse_url.netloc)

                    image = Image.objects.all().filter(src=img_parse_url.geturl()).first()
                    if not image:
                        image = Image(src=img_parse_url.geturl())
                        image.save()

                    if img['alt'].strip():
                        save_utterance_to_image(language, img['alt'], image)

            heading_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
            for heading_tag in heading_tags:
                for heading in soup.find_all(heading_tag):
                    if heading.get_text().strip():
                        save_utterance_to_url(language, heading.get_text(), url)

            for p in soup.find_all('p'):
                if p.get_text().strip():
                    save_utterance_to_url(language, p.get_text(), url)

            for li in soup.find_all('li'):
                if li.get_text().strip():
                    save_utterance_to_url(language, li.get_text(), url)

            for a in soup.find_all('a', href=True):
                if a['href'].strip():
                    link_parse_url = urlparse(a['href'])
                    if not link_parse_url.scheme:
                        link_parse_url = link_parse_url._replace(scheme=parse_url.scheme)
                    if not link_parse_url.netloc:
                        link_parse_url = link_parse_url._replace(netloc=parse_url.netloc)

                    link_url = Url.objects.all().filter(url=link_parse_url.geturl()).first()
                    if not link_url:
                        link_url = Url(url=link_parse_url.geturl())
                        link_url.save()

                    if a.get_text().strip():
                        save_utterance_to_url(language, a.get_text(), url)

            url.language = language
            url.last_read = datetime.now()
            url.save()

class Command(BaseCommand):
    help = 'Read those sites'

    def add_argument(self, parser):
        pass

    def handle(self, *args, **options):
        get_responce()
