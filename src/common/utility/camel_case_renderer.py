import json
from typing import Any, Mapping, Type

import humps
import orjson
from ninja.renderers import BaseRenderer
from ninja.responses import NinjaJSONEncoder


class CamelCaseRenderer(BaseRenderer):
    media_type = "application/json"
    encoder_class: Type[json.JSONEncoder] = NinjaJSONEncoder
    json_dumps_params: Mapping[str, Any] = {}

    def render(self, request, data, *, response_status):
        # Convert Pydantic models (v2: model_dump, v1: dict) to native Python types recursively
        def _to_primitive(obj):
            if hasattr(obj, "model_dump") and callable(obj.model_dump):
                return _to_primitive(obj.model_dump())
            if hasattr(obj, "dict") and callable(obj.dict):
                return _to_primitive(obj.dict())
            if isinstance(obj, list):
                return [_to_primitive(item) for item in obj]
            if isinstance(obj, dict):
                return {k: _to_primitive(v) for k, v in obj.items()}
            return obj

        data = _to_primitive(data)

        return orjson.dumps(humps.camelize(data))
