import uvicorn

from fastapi import FastAPI
from elasticsearch import AsyncElasticsearch
from db.elastic import EsConnection
from fastapi.responses import ORJSONResponse
from config import config
from routers import shows



app = FastAPI(
    title=config.PROJECT_NAME,
    description='Study project using FastAPI + Elasticsearch',
    docs_url='/api/docs',
    openapi_url='/api/docs.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    es = AsyncElasticsearch(
            hosts=f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}', 
            basic_auth=(config.ELASTIC_USER, config.ELASTIC_PASSWORD))
    EsConnection.init(es)

@app.on_event('shutdown')
async def shutdown():
    await EsConnection.connection.close()

@app.get('/')
async def root():
    return {'message': 'hello'}

app.include_router(shows.router)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )