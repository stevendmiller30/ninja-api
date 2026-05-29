from django.db import transaction

from src.business.models import Business, BusinessContact
from src.business.schemas.business_schemas import (
    BusinessDataCreationResponseSchema,
    BusinessDataListResponseSchema,
    BusinessDataResponseSchema,
    BusinessSchema,
    BusinessSchemaResponse,
)


def get_businesses():
    businesses = list(Business.objects.all())

    return BusinessDataListResponseSchema(data=businesses)


def get_business_by_id(business_id: int) -> BusinessDataResponseSchema:
    business = Business.objects.get(id=business_id)

    return BusinessDataResponseSchema(data=BusinessSchema.from_orm(business))


def save_business(new_business: BusinessSchema) -> BusinessDataCreationResponseSchema:

    with transaction.atomic():
        business = Business.objects.create(business_name=new_business.business_name)

        for contact in new_business.contacts:
            BusinessContact.objects.create(business=business, **contact.dict(exclude_none=True))

    return BusinessDataCreationResponseSchema(data=BusinessSchemaResponse(id=business.id))
