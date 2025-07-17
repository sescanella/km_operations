print(">>> ESTOY EJECUTANDO EL main.py CORRECTO <<<")

from fastapi import FastAPI
from backend.app.api.v1.endpoints import excel_routes, etapa2_routes

app = FastAPI()

app.include_router(excel_routes.router)
app.include_router(etapa2_routes.router)