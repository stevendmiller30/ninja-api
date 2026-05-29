import logging
import os

import requests
from elasticsearch import Elasticsearch
from elasticsearch.dsl import Q

from src.search.models.co_bus_es_model import COBusinesses
from src.search.schemas.co_business_schemas import COBusinessDataList, COBusinessList

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ES_HOST_URL = os.getenv("ES_HOST_URL", "http://localhost:9200")
COLORADO_BUSINESS_URL = "https://data.colorado.gov/resource/4ykn-tg5h.json"


class ColoradoBusinessService:
    def __init__(self):
        pass

    # retrieve data from the Colorado Business dataset, convert to list of COBusiness
    def fetch_businesses(self):
        """
        Fetches business data from the Colorado Business dataset.
        limit to first X records.
        """

        filter_size = 25

        # retrieve data from the Colorado Business dataset
        response = requests.get(f"{COLORADO_BUSINESS_URL}?$limit={filter_size}")
        response.raise_for_status()

        # convert data to list of COBusiness objects
        # use of Pydantic alias converts field names from CO dataset to our internal field names
        businesses = response.json()
        businesses_list = COBusinessList(root=businesses)

        return businesses_list.model_dump()

    # search elasticsearch for businesses matching the provided business name
    def search_businesses_by_name(self, business_name: str) -> COBusinessDataList:
        """
        Search for businesses by name in the Elasticsearch Colorado Business index.
        """

        q = Q("multi_match", query=business_name, fields=["business_name"])

        with Elasticsearch(ES_HOST_URL) as es_conn:
            dsl_query = COBusinesses.search().using(es_conn).query(q)
            logger.info(f"dsl query: {dsl_query.to_dict()}")
            results = dsl_query.execute()

        co_list = []

        for co_business in results:
            co_business_dict = co_business.to_dict()
            logger.info(f"found business: {co_business_dict}")
            co_list.append(co_business_dict)

        return COBusinessDataList(data=co_list)
