
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routers import clinic
from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.clinic.clinic_template_impl import ClinicTemplateImpl
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    clinic_template_instance = ClinicTemplateImpl()
    clinic_template_instance.init(config=None)
    TemplateContext.add_template(TemplateType.CLINIC, clinic_template_instance)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(clinic.router, prefix="/clinic", tags=["clinic"])
# app.include_router(clinic.router, prefix="/clinic_server", tags=["clinic"])

@app.get("/")
def root():
    return {"message": "Clinic Server is running"}

