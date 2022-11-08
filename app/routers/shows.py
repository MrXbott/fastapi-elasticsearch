from fastapi import APIRouter, Depends, HTTPException, Request
from http import HTTPStatus
from services.show_service import NetflixShowService
from models.model import NetflixShow


router = APIRouter(
    prefix="/shows",
    tags=["shows"],
    responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=list[NetflixShow], response_model_exclude_unset=True)
async def get_all_shows() -> list[NetflixShow]:
    '''
    Returns all shows with details
    '''
    shows = await NetflixShowService.find_all_shows()
    if not shows:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return shows


@router.get("/search", response_model=list[NetflixShow], response_model_exclude_unset=True)
async def get_shows_by_params(request: Request) -> list[NetflixShow]:
    '''
    Returns a list of shows found by the given parameters. 
    Parameters must be specified as a key value pair, where key is the search field and 
    value is the value of this field. 
    \nExample: ?country=india&type=movie
    '''
    params = dict(request.query_params)
    shows = await NetflixShowService.execute_search_query(params)
    if not shows:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return shows


@router.get("/multi_search", response_model=list[NetflixShow], response_model_exclude_unset=True)
async def get_shows_by_string(request: Request) -> list[NetflixShow]:
    '''
    Returns a list of shows found by the given parameters. 
    Two parameters must be given here: "search_str" and "fields".
    Parameters must be specified as a key value pair.
    \n"search_str" is a string that should be found.
    \n"fields" is a list of fields where the search should be performed.
    \nExample: ?search_str=cat&fields=title,description
    '''
    params = dict(request.query_params)
    if 'search_str' in params.keys() and 'fields' in params.keys():
        params['fields'] = params['fields'].split(',')
        shows = await NetflixShowService.execute_search_query(search_params=params, multi=True)
    else:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    if not shows:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return shows


@router.get('/{show_id}', response_model=NetflixShow, response_model_exclude_unset=True)
async def get_show_by_id(show_id: str) -> NetflixShow:
    '''
    Returns a show by the given show id
    '''
    show = await NetflixShowService.find_show_by_id(show_id)
    if not show:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return show

