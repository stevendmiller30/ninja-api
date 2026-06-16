import json
import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

from src.common.utility.utils import load_json_file

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ESIndex:
    _BASE_ES_URL = "http://elasticsearch:9200"

    def make_index(self, alias_name: str, configuration_filename: str, load_data: list):
        current_indexes: list = self.get_current_indexes(alias_name)
        index_config: dict = self.get_index_config(configuration_filename)
        new_index_name: str = self.generate_new_index_name(alias_name)
        self.create_index(new_index_name, index_config)
        es_formatted_data = self.format_es_data(load_data)
        self.bulk_load_data(new_index_name, es_formatted_data)
        self.activate_alias(alias_name, new_index_name)
        self.remove_old_indexes(current_indexes)

    def format_es_data(self, data: list):

        bulk_data = []
        for index, value in enumerate(data):
            bulk_data.append(f'{{"index": {{"_id": "{index}"}}}}')
            bulk_data.append(json.dumps(value, default=str))

        return "\n".join(bulk_data) + "\n"

    def bulk_load_data(self, index_name: str, es_data: list):
        resp = requests.post(
            f"{self._BASE_ES_URL}/{index_name}/_bulk",
            headers={"Content-Type": "application/json"},
            data=es_data,
        )
        resp.raise_for_status()

    def get_current_indexes(self, index_name: str):
        resp = requests.get(f"{self._BASE_ES_URL}/_cat/indices?format=json")
        resp.raise_for_status()

        cur_indexes = []
        for index in resp.json():
            if index["index"].startswith(index_name):
                cur_indexes.append(index["index"])
        logger.info(f"Current indexes for {index_name}: {cur_indexes}")

        return cur_indexes

    def get_file_pathname(self, filename: str) -> str:
        return f"{os.path.dirname(__file__)}/{filename}"

    def get_index_config(self, filename):
        file_path = self.get_file_pathname(filename)
        return load_json_file(file_path)

    def generate_new_index_name(self, index_name: str) -> str:
        return f"{index_name}_{datetime.now(ZoneInfo('America/Denver')).strftime('%Y%m%d%H%M%S')}"

    def create_index(self, index_name: str, index_config: dict):
        resp = requests.put(
            f"{self._BASE_ES_URL}/{index_name}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(index_config),
        )

        resp.raise_for_status()  # Raise an exception for HTTP errors

    def remove_old_indexes(self, old_index_names: list):
        for index_name in old_index_names:
            response = requests.delete(f"{self._BASE_ES_URL}/{index_name}")
            response.raise_for_status()

    def activate_alias(self, alias_name: str, new_index_name: str):
        data = {"actions": [{"add": {"index": new_index_name, "alias": f"{alias_name}_alias"}}]}

        resp = requests.post(
            f"{self._BASE_ES_URL}/_aliases",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
        )

        resp.raise_for_status()
