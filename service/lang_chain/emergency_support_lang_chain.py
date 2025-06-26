import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# ---- 리소스 로딩 함수 ----

def load_embedding_model():
    """SentenceTransformer 모델을 로드합니다."""
    print("임베딩 모델 로딩...")
    return SentenceTransformer("jhgan/ko-sroberta-multitask")

def load_faiss_index(index_path: str):
    """지정된 경로의 FAISS 인덱스 파일을 로드합니다."""
    print(f"FAISS 인덱스 로딩: {index_path}")
    return faiss.read_index(index_path)

def load_chunks(chunk_path: str):
    """지정된 경로의 텍스트 청크 파일을 로드합니다."""
    print(f"텍스트 청크 로딩: {chunk_path}")
    with open(chunk_path, "r", encoding="utf-8") as f:
        return [c.strip() for c in f.read().split("\n\n") if c.strip()]

# ---- RAG 파이프라인 함수 ----

def build_rag_chain(openai_api_key: str):
    """LangChain RAG 체인을 빌드합니다."""
    print("RAG 체인 빌드...")
    prompt = PromptTemplate.from_template(
        "당신은 의학전공을 하여 저희의 질문에 대답을 잘 해주는 챗봇입니다"
        "만약 진료혹은 약, 의학과 관련이 없는 질문이면 질문이 주제와 다르다고 하면 됩니다"
        "다음은 사용자의 질문에 답하기 위한 참고 문서입니다:\n\n"
        "{context}\n\n"
        "---\n\n"
        "질문: {question}\n"
        "답변:"
    )
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=openai_api_key)
    return prompt | llm | StrOutputParser()

def search_similar_chunks(question: str, index, chunks, model, top_k=3):
    """FAISS 인덱스를 사용해 질문과 유사한 청크를 검색합니다."""
    embedding = model.encode([question])
    _, indices = index.search(np.array(embedding).astype("float32"), top_k)
    return [chunks[i] for i in indices[0]]

async def get_rag_answer_async(question: str, index, chunks, embed_model, rag_chain):
    """
    비동기적으로 RAG 파이프라인 전체를 실행하여 최종 답변을 생성합니다.
    """
    # 1. 관련 문서 검색 (Retrieval)
    top_chunks = search_similar_chunks(question, index, chunks, embed_model)
    context = "\n".join(top_chunks)

    # 2. LLM을 통한 답변 생성 (Generation) - 비동기(ainvoke) 사용
    answer = await rag_chain.ainvoke({"context": context, "question": question})
    return answer