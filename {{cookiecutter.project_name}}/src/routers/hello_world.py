from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
async def landing():

    output = {
        "msg": "{{ cookiecutter.project_name }}"
    }

    return JSONResponse(
        content=output,
        status_code=200
    )