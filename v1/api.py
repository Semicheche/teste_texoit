from fastapi import APIRouter
from fastapi.responses import JSONResponse
from core.models import Movie

router = APIRouter()

@router.get('/best-producers')
def best_producers():
    mv = Movie()
    res = mv.get_producer_ordered()
    return JSONResponse(res, status_code=200)

@router.get('/movies/all')
def get_all():
    mv = Movie()
    res = mv.get_all()
    return JSONResponse(res, status_code=200)