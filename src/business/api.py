from typing import Annotated

from ninja import Path, Router

from src.business.schemas.business_schemas import BusinessDataCreationResponseSchema, BusinessSchema
from src.business.services import get_businesses, save_business
from src.business.services.business_services import get_business_by_id

router = Router()

PositiveInteger = Annotated[int, Path(gt=0)]


@router.get("healthcheck", url_name="health-check")
def health_check(request):
    return {"status": "ok"}


@router.get("", url_name="list-businesses")
def list_businesses(request):
    resp = get_businesses()
    return resp


@router.post("", url_name="create-business", response=BusinessDataCreationResponseSchema)
def create_business(request, payload: BusinessSchema):
    resp = save_business(payload)
    return resp


@router.get("/{business_id}", url_name="get-business-by-id")
def get_business(request, business_id: PositiveInteger):
    resp = get_business_by_id(business_id)
    return resp
