from elasticsearch import AsyncElasticsearch


class EsConnection:
    __instance = None
    connection = None

    @classmethod
    def init(cls, es_obj: AsyncElasticsearch):
        if not cls.__instance:
            cls.__instance = EsConnection()
        cls.connection = es_obj
        return cls.__instance



