from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi_base_server.application.emergency_support_server.routers import emergency_support

from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.emergency_support.emergency_support_template_impl import EmergencySupportTemplateImpl

@asynccontextmanager
async def lifespan(app: FastAPI):
    TemplateContext.add_template(TemplateType.EMERGENCY_SUPPORT, EmergencySupportTemplateImpl())
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(emergency_support.router, prefix="/emergency-support", tags=["emergency-support"])

@app.get("/")
def root():
    return {"message": "Emergency & Support Server is running"} 