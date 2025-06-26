from fastapi import FastAPI
from contextlib import asynccontextmanager
# from fastapi_base_server.application.emergency_support_server.routers import emergency_support
from . routers import emergency_support
# from . import chatbot
from fastapi.middleware.cors import CORSMiddleware
from template.base.template_context import TemplateContext
from template.base.template_type import TemplateType
from template.emergency_support.emergency_support_template_impl import EmergencySupportTemplateImpl

@asynccontextmanager
async def lifespan(app: FastAPI):
    # TemplateContext.add_template(TemplateType.EMERGENCY_SUPPORT, EmergencySupportTemplateImpl())
    emergency_template_instance = EmergencySupportTemplateImpl()
    # config 인자는 현재 init 메서드에서 사용되지 않으므로 None을 전달합니다.
    emergency_template_instance.init(config=None)
    TemplateContext.add_template(TemplateType.EMERGENCY_SUPPORT, emergency_template_instance)
    yield

app = FastAPI(lifespan=lifespan)

# React 앱의 주소(http://localhost:3000)를 허용해야 합니다.
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(emergency_support.router, prefix="/emergency-support", tags=["emergency-support"])

@app.get("/")
def root():
    return {"message": "Emergency & Support Server is running"} 