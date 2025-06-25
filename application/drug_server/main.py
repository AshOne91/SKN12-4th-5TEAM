from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_base_server.application.drug_server.routers import drug

from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.drug.drug_template_impl import DrugTemplateImpl

@asynccontextmanager
async def lifespan(app: FastAPI):
    TemplateContext.add_template(TemplateType.DRUG, DrugTemplateImpl())
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(drug.router, prefix="/drug", tags=["drug"])

@app.get("/")
def root():
    return {"message": "Drug Server is running"} 