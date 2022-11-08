from db.elastic import EsConnection
from models.model import NetflixShow
from services.base_service import BaseService


class NetflixShowService(BaseService):
    index_name = 'netflix'

    @classmethod
    async def execute_search_query(cls, search_params:dict={}, multi:bool=False) -> list[NetflixShow]:
        '''
        This function executes search by the given params and returns the found values 
        :param search_params: a dictionary with fields and values for search, eq: {'country': 'India'}
        :param multi: bool value, if True then multi search will be performed
        '''
        query = cls._create_query_string(search_params, multi)

        if multi == False:
            results = await EsConnection.connection.search(index=cls.index_name, query=query, size=5)
        else:
            results = await EsConnection.connection.search(index=cls.index_name, body=query, size=5)
        if results['hits']['total']['value'] == 0:
            return
        shows = []
        for show in results['hits']['hits']:
            shows.append(NetflixShow(**show['_source']))
        return shows


    @classmethod
    async def find_all_shows(cls) -> list[NetflixShow]:
        '''
        Just returns all shows from the index
        '''
        results = await cls.execute_search_query({})
        return results


    @classmethod
    async def find_show_by_id(cls, show_id: str) -> NetflixShow | None:
        '''
        Return a show found by the given show id, if not found returns None
        :param show_id: the id of the show that should be found
        '''
        results = await cls.execute_search_query({'show_id': show_id})
        if not results:
            return
        return results[0]
