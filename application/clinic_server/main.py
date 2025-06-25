from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_base_server.application.clinic_server.routers import clinic

from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.clinic.clinic_template_impl import ClinicTemplateImpl

@asynccontextmanager
async def lifespan(app: FastAPI):
    TemplateContext.add_template(TemplateType.CLINIC, ClinicTemplateImpl())
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(clinic.router, prefix="/clinic", tags=["clinic"])

@app.get("/")
def root():
    return {"message": "Clinic Server is running"} 