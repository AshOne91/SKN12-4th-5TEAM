# ------------------------------------------------------------
from fastapi import FastAPI
from contextlib import asynccontextmanager
from application.internal_external_server.routers import internal_external
from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.internal_external.internal_external_template_impl import InternalExternalTemplateImpl

@asynccontextmanager
async def lifespan(app: FastAPI):
    # TemplateContext.add_template(TemplateType.EMERGENCY_SUPPORT, EmergencySupportTemplateImpl())
    internal_external_template_instance = InternalExternalTemplateImpl()
    # config 인자는 현재 init 메서드에서 사용되지 않으므로 None을 전달합니다.
    internal_external_template_instance.init(config=None)
    TemplateContext.add_template(TemplateType.INTERNAL_EXTERNAL, internal_external_template_instance)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(internal_external.router, prefix="/internal-external", tags=["internal-external"])

@app.get("/")
def root():
    return {"message": "Internal & External Server is running"} 







# ------------------------------------------------------------