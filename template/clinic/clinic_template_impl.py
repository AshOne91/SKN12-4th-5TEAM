from template.base.template.clicnic_template import ClinicTemplate
from template.clinic.common.clinic_serialize import ClinicAskRequest, ClinicAskResponse
from sentence_transformers import SentenceTransformer
import os
import faiss
import json
import numpy as np
from openai import OpenAI 
from dotenv import load_dotenv
import re

load_dotenv()

class ClinicTemplateImpl(ClinicTemplate):
    def init(self, config):
        print("Clinic template initialized")

        # 경로 설정 (환경변수에서 불러오기)
        base_path = os.getenv('CLINIC_VECTORDB_BASE')
        processed_docs_path = os.getenv('CLINIC_VECTORDB_DOCS')
        if base_path is None:
            raise ValueError('CLINIC_VECTORDB_BASE_PATH 환경변수가 설정되어 있지 않습니다.')
        if processed_docs_path is None:
            raise ValueError('CLINIC_PROCESSED_DOCS_PATH 환경변수가 설정되어 있지 않습니다.')
        self.index = faiss.read_index(os.path.join(base_path, "faiss_index", "index.faiss"))
        with open(os.path.join(base_path, "doc_ids.json"), "r", encoding="utf-8") as f:
            self.doc_ids = json.load(f)
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.processed_docs_path = processed_docs_path
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        with open("resources/vectorDB/treatment/RAG_Output/faiss_medical/keyword_index.json", "r", encoding="utf-8") as f:
            self.keyword_index = json.load(f)

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
                        content = f.read()
                        if content.strip():
                            retrieved_texts.append(content)
                        else:
                            print(f"파일은 있으나 내용이 비어 있음: {doc_filename}")

        context = "\n\n".join(retrieved_texts)

        MAX_CONTEXT_CHARS = 10_000
        if len(context) > MAX_CONTEXT_CHARS:
            context = context[:MAX_CONTEXT_CHARS] + "\n\n...(생략됨)"
        
        raw_keywords = re.findall(r"[가-힣a-zA-Z]{2,}", question)
        particles = {"은", "는", "이", "가", "을", "를", "에", "의", "으로", "에서", "도", "만", "와", "과", "보다"}
        cleaned_keywords = []
        for word in raw_keywords:
            for p in particles:
                if word.endswith(p) and len(word) > len(p):
                    word = word[: -len(p)]
                    break
            cleaned_keywords.append(word)
        question_keywords = list(set(cleaned_keywords))
        indexed_keywords = [kw for kw in question_keywords if kw in self.keyword_index]

        if not any(k in context for k in question_keywords):
            added = set()
            fallback_limit = 4
            fallback_added = 0
            for kw in question_keywords:
                for fname in self.keyword_index.get(kw, []):
                    if fname not in added:
                        fpath = os.path.join(self.processed_docs_path, fname)
                        if os.path.exists(fpath):
                            with open(fpath, "r", encoding="utf-8") as f:
                                text = f.read()
                                context += "\n\n" + text
                                added.add(fname)
                                fallback_added += 1
                                break  # 키워드당 1개만 추가
                    if fallback_added >= fallback_limit:
                        break
                if fallback_added >= fallback_limit:
                    break

        # 프롬프트 구성 (GPT에 전달할 문장)
        prompt = f"""
        당신은 신뢰할 수 있는 의료 전문 상담 AI입니다.

        아래 [문서 내용]에 기반하여 [질문]에 정확하게 답변하세요.
        문서에 정보가 없으면 "문서에서 해당 질문에 대한 정보를 찾을 수 없습니다."라고 말하세요.
        절대 정보를 추측하거나 지어내지 마세요.

        [문서 내용]
        {context}

        [질문]
        {question}

        [답변]
        """

        # GPT 호출
        response = self.client.chat.completions.create(
            model="gpt-4o",  # 또는 "gpt-4o-mini"
            messages=[
                {"role": "system", "content": "너는 의료 전문 상담 AI야."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=512,
        )

        gpt_answer = response.choices[0].message.content

        return ClinicAskResponse(answer=gpt_answer)