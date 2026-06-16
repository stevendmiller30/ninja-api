import logging

from django.core.management.base import BaseCommand

from src.search.services.colorado_business import ColoradoBusinessService
from src.search.services.es_index import ESIndex


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

        logging.info("starting co business download.")

        # retrieve data from the Colorado Business dataset, convert to list of COBusiness
        cbs = ColoradoBusinessService()
        businesses = cbs.fetch_businesses()

        # create index and upload data to Elasticsearch
        es_index = ESIndex()
        es_index.make_index("co_business", "elastic_config/co_bus_config.json", businesses)
        logging.info("Finished co business download and Elasticsearch indexing.")
