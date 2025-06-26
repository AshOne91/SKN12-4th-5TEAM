
from template.base.template.clicnic_template import ClinicTemplate
from template.clinic.common.clinic_serialize import ClinicAskRequest, ClinicAskResponse
from sentence_transformers import SentenceTransformer
import os
import faiss
import json
import numpy as np

class ClinicTemplateImpl(ClinicTemplate):
    def init(self, config):
        print("Clinic template initialized")

        # 경로 설정
        base_path = "resources/vectordb/treatment/RAG_Output/faiss_medical"
        self.index = faiss.read_index(os.path.join(base_path, "faiss_index", "index.faiss"))
        with open(os.path.join(base_path, "doc_ids.json"), "r", encoding="utf-8") as f:
            self.doc_ids = json.load(f)
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.processed_docs_path = "resources/vectordb/treatment/RAG_Output/processed_docs"

    async def on_clinic_ask_req(self, client_session, request: ClinicAskRequest) -> ClinicAskResponse:
        question = request.question

        # 1. 질문 임베딩
        q_vector = self.embedding_model.encode(question)
        q_vector = np.array([q_vector]).astype("float32")

        # 2. FAISS 검색 (top 3)
        D, I = self.index.search(q_vector, k=3)

        # 3. 검색된 문서 chunk 로드
        retrieved_texts = []
        for idx in I[0]:
            if idx < len(self.doc_ids):
                doc_filename = self.doc_ids[idx]
                if not doc_filename.endswith(".txt"):
                    doc_filename += ".txt"
                doc_path = os.path.join(self.processed_docs_path, doc_filename)
                if os.path.exists(doc_path):
                    with open(doc_path, "r", encoding="utf-8") as f:
                        retrieved_texts.append(f.read())

        # 4. context 구성
        context = "\n\n".join(retrieved_texts)
        answer = f"{context}"
        return ClinicAskResponse(answer=answer)
