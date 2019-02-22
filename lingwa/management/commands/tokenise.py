from requests import get
from requests.exceptions import RequestException
from contextlib import closing

from django.core.management.base import BaseCommand, CommandError
from lingwa.models import Utterence, Keyword

class Command(BaseCommand):
    help = 'Tokenise to smaller components'

    def add_argument(self, parser):
        pass

    def handle(self, *args, **options):
        utterences = Utterence.objects.all()
        for utterence in utterences:
            for word in utterence.utterence.split(' '):
                if word.strip():
                    keyword = Keyword.objects.all().filter(language=utterence.language, keyword=word).first()
                    if keyword:
                        keyword.count += 1;
                    else:
                        keyword = Keyword(language=utterence.language, keyword=word)
                    keyword.save()
