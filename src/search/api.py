from ninja import Query, Router

from src.search.schemas.co_business_schemas import COBusinessDataList
from src.search.schemas.us_senator_schemas import SenatorFilterSchema, USSenatorDataList
from src.search.services.colorado_business import ColoradoBusinessService
from src.search.services.us_senators import USSenatorService

router = Router()


@router.get("businesses", url_name="business-search", response=COBusinessDataList)
def co_business_name_search(request, business_name: str):

    cbs = ColoradoBusinessService()
    colorado_businesses = cbs.search_businesses_by_name(business_name)

    return colorado_businesses


@router.get("senators", url_name="senator-state-search", response=USSenatorDataList)
def us_senator_by_state_search(request, filters: SenatorFilterSchema = Query(...)):

    uss = USSenatorService()
    us_senators = uss.search_us_senators_by_state(filters)

    return us_senators
