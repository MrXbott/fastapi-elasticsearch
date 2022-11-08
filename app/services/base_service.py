

class BaseService:
    @classmethod
    def _create_query_string(cls, search_params:dict, multi:bool) -> dict:
        if not search_params:
            query = {
                'match_all': {}
            }
            return query

        if multi == True:
            query = {
                'query': {
                    'multi_match': {
                    'query':  search_params['search_str'], 
                    'type': 'most_fields',
                    'fields': search_params['fields']
                    }
                }
            }
        else:
            must = [{'match':{k: v}} for k, v in search_params.items()]
            query = {
                'bool': {
                    'must': must
                }
            }
        return query