from fastapi import FastAPI
from database import engine, Base
from routers import usuarios, laboratorios, servicios, tickets, auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Mesa de Servicios para Laboratorios",
    description="API para gestionar solicitudes de servicios usando FastAPI, PostgreSQL y JWT.",
    version="1.0.0"
)

app.include_router(auth_router.router)
app.include_router(usuarios.router)
app.include_router(laboratorios.router)
app.include_router(servicios.router)
app.include_router(tickets.router)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de Mesa de Servicios"}