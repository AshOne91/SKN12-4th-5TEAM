from fastapi import FastAPI
from contextlib import asynccontextmanager
from application.drug_server.routers import drug
from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.drug.drug_template_impl import DrugTemplateImpl

@asynccontextmanager
async def lifespan(app: FastAPI):
    drug_template_instance = DrugTemplateImpl()
    drug_template_instance.init(config=None)
    # TemplateType을 DRUG로 정확하게 지정합니다.
    TemplateContext.add_template(TemplateType.DRUG, drug_template_instance)
    yield    

app = FastAPI(lifespan=lifespan)

app.include_router(drug.router, prefix="/drug", tags=["drug"])
# app.include_router(drug.router, prefix="/drug_server", tags=["drug"])

@app.get("/")
def root():
    return {"message": "Drug Server is running"} 