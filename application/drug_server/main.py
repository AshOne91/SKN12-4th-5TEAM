from fastapi import FastAPI
from contextlib import asynccontextmanager
from application.drug_server.routers import drug
from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.drug.drug_template_impl import DrugTemplateImpl

@asynccontextmanager
async def lifespan(app: FastAPI):
    drog_template_instance = DrugTemplateImpl()
    drog_template_instance.init(config=None)
    TemplateContext.add_template(TemplateType.EMERGENCY_SUPPORT, drog_template_instance)
    yield    

app = FastAPI(lifespan=lifespan)

# 등록
TemplateContext.add_template(TemplateType.DRUG, DrugTemplateImpl())

app.include_router(drug.router, prefix="/drug", tags=["drug"])

@app.get("/")
def root():
    return {"message": "Drug Server is running"} 