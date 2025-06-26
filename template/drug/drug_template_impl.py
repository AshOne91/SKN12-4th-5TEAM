from template.base.template.drug_template import DrugTemplate
from template.drug.common.drug_serialize import DrugAskRequest, DrugAskResponse
from service.lang_chain.drug_lang_chain import Vector_store
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

INDEX_PATH = os.getenv('DRUG_VECTORDB_INDEX')
CHUNK_PATH = os.getenv('DRUG_VECTORDB_TXT')

class DrugTemplateImpl(DrugTemplate):
    def __init__(self):
        """
        DrugTemplateImpl initializer.
        The Vector_store is loaded once here to manage resources efficiently.
        """
        super().__init__()
        print("Initializing Vector_store for DrugTemplate...")
        # The Vector_store instance is created here and stored as an attribute.
        # This instance will be reused for the entire application lifecycle.
        self.vector_store = Vector_store(
            api_key=OPENAI_API_KEY,
            chunk_path=CHUNK_PATH,
            index_path=INDEX_PATH,
        )
        print("Vector_store for DrugTemplate initialized.")

    def init(self, config):
        """Drug template initializer (for framework compatibility)"""
        # The actual initialization is done in __init__.
        print("Drug template init hook called.")
        
    def on_load_data(self, config):
        print("Drug data loaded")
        
    def on_client_create(self, db_client, client_session):
        print("Drug client created")
        
    def on_client_update(self, db_client, client_session):
        print("Drug client updated")
        
    def on_client_delete(self, db_client, user_id):
        print("Drug client deleted")

    async def on_drug_ask_req(self, client_session, request: DrugAskRequest) -> DrugAskResponse:
        question = request.question
        # Use the pre-initialized Vector_store instance and await the coroutine.
        answer = await self.vector_store.rag_answer(question)
        return DrugAskResponse(answer=answer)