import logging
import os

import requests
from elasticsearch import Elasticsearch
from elasticsearch.dsl import Q

from src.search.models.us_senator_es_model import USSenator
from src.search.schemas.us_senator_schemas import SenatorFilterSchema, USSenatorDataList, USSenatorList

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ES_HOST_URL = os.getenv("ES_HOST_URL", "http://localhost:9200")

_US_SENATOR_URL = "https://www.govtrack.us/api/v2/role?current=true&role_type=senator"


class USSenatorService:
    def fetch_senators(self):

        response = requests.get(_US_SENATOR_URL)

        response.raise_for_status()
        senate_dataset = response.json()["objects"]
        logger.info(f"Fetched {len(senate_dataset)} senators")

        # convert raw dataset to list of Pydantic models.
        # maps dataset field names to python Pydantic model field names
        # removes any fields from the dataset that are not defined in the Pydantic model
        senator_list = USSenatorList(root=senate_dataset)

        return senator_list.model_dump()

    def build_elasticsearch_query(self, filters: SenatorFilterSchema):
        must_queries = []

        if filters.state:
            must_queries.append(Q("match", **{"state": filters.state}))

        if filters.first_name:
            must_queries.append(Q("match", **{"person.first_name": filters.first_name}))

        if filters.last_name:
            must_queries.append(Q("match", **{"person.last_name": filters.last_name}))

        final_query = Q("bool", must=must_queries)

        return final_query

    # search elasticsearch for businesses matching the provided business name
    def search_us_senators_by_state(self, filters: SenatorFilterSchema) -> USSenatorDataList:
        """
        Search for senators by state in the Elasticsearch US Senator index.
        """

        logger.info("starting search for senators with filters: %s", filters)

        q = self.build_elasticsearch_query(filters)

        with Elasticsearch(ES_HOST_URL) as es_conn:
            dsl_query = USSenator.search().using(es_conn).query(q)
            logger.info(f"dsl query: {dsl_query.to_dict()}")
            results = dsl_query.execute()

        senator_list = []

        for senator in results:
            senator_dict = senator.to_dict()
            logger.info(f"found senator: {senator_dict}")
            senator_list.append(senator_dict)

        return USSenatorDataList(data=senator_list)
