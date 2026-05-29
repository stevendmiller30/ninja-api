from typing import Annotated

from ninja import Path, Router

router = Router()

PositiveInteger = Annotated[int, Path(gt=0)]


@router.get("", url_name="health-check")
def health_check(request):
    return {"status": "ok"}
