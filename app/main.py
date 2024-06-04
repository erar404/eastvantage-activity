import logging
from logger import LogHandler
from fastapi import FastAPI
from api.routes.address import address_router
from tortoise.contrib.fastapi import register_tortoise


LogHandler('activity-logs')
logger = logging.getLogger('activity-logs')

try:
    logger.info('Start Address Book Api')
    app = FastAPI(title="Eastvantage Application Exam")
    app.include_router(address_router)
    register_tortoise(
        app=app,
        db_url="sqlite://activity.db",
        add_exception_handlers=True,
        generate_schemas=True,
        modules={"models": ["api.models.address"]}
    )
    logger.info('Initialization Complete')
except Exception as e:
    logger.error('Error on Initializing program. Details:{}'.format(e))


@app.get("/index")
def index():
    return {"status": "Api is running"}
