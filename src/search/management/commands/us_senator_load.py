import logging

from django.core.management.base import BaseCommand

from src.search.services.es_index import ESIndex
from src.search.services.us_senators import USSenatorService


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

        logging.info("starting us senator download.")

        # download data from data source
        us_sen = USSenatorService()
        senators = us_sen.fetch_senators()

        # create Elasticsearch index
        es_index = ESIndex()
        es_index.make_index("us_senator", "elastic_config/us_senator_config.json", senators)

        logging.info("Finished us senator download and Elasticsearch index")
