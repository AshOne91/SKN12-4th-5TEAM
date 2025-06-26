from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from sentence_transformers import SentenceTransformer
from openai import OpenAI  # OpenAI SDK
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import numpy as np
import os
import pickle
import torch
import faiss

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TEXT_PATH = os.getenv('CATEGORY_VECTORDB')
EMBEDDING_PATH = TEXT_PATH
CATEGORY_PATH = TEXT_PATH

class Category_Classifier:
    def __init__(self):
        self.category_texts, self.category_categories, self.category_embeddings = self.load_vector_db()
        self.category_embeddings_norm = self.normalize(self.category_embeddings.numpy())
        self.embedder = SentenceTransformer("jhgan/ko-sroberta-multitask")
        
        # ChatBot LLM (LangChain 용)
        self.chatbot_llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.3)
        self.chatbot_prompt = self.make_prompt()
        self.chatbot_chain = self.chatbot_prompt | self.chatbot_llm | StrOutputParser()

        # 분류 전용 LLM (OpenAI SDK)
        self.client = OpenAI(api_key=OPENAI_API_KEY)  

    def load_vector_db(self):
        texts = pickle.load(open(os.path.join(TEXT_PATH, "texts.pkl"), "rb"))
        categories = pickle.load(open(os.path.join(CATEGORY_PATH, "categories.pkl"), "rb"))
        embeddings = torch.load(os.path.join(EMBEDDING_PATH, "embeddings.pt"), map_location=torch.device('cpu'))
        return texts, categories, embeddings

    def normalize(self, v):
        return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-8)

    def make_prompt(self):
        return ChatPromptTemplate.from_messages([
            ("system", """
            당신은 의료 질문에 전문적으로 답하는 AI 상담사입니다. 
            사용자의 질문과 history, 카테고리 전용 LLM 응답을 바탕으로 최적의 답변을 생성하세요. 
            만약 사용자의 질문이 이전 질문(history)요청, 의학, 약, 진료와 관련없는 질문을 받을 시 질문이 주제와 다르다고 말하세요.
            """),
            MessagesPlaceholder(variable_name="history"),
            ("human", """[사용자 질문]
{question}

[카테고리 전용 LLM 응답]
{draft_answer}

[최종 응답]""")
        ])

    def classify_category_with_llm(self, input_text, retrieved_examples):
        fewshot = ""
        for i, (ex, cat, score) in enumerate(retrieved_examples):
            fewshot += f"예시 {i+1}:\n텍스트: \"{ex}\"\n카테고리: {cat}\n\n"

        prompt = f"""
당신은 텍스트를 아래 4가지 카테고리 중 하나로만 분류해야 하는 전문가입니다.

선택 가능한 카테고리:
- emergency_support
- internal_external
- drug
- clinic

아래는 분류된 예시들입니다:
{fewshot}

이제 입력된 텍스트를 위 카테고리 중 **하나만** 선택하여 분류하세요.
카테고리 이름만 출력하세요. 다른 설명 없이 정확히 하나의 카테고리명만 출력해야 합니다.

입력 텍스트: "{input_text}"

정답 카테고리:"""

        response = self.client.chat.completions.create( 
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()

    def return_category(self, user_input: str) -> str:
        input_emb = self.embedder.encode([user_input])[0]  # (D,)
        input_emb_norm = input_emb / (np.linalg.norm(input_emb) + 1e-8)

        sims = np.dot(self.category_embeddings_norm, input_emb_norm)  # (N,)
        top_k = 3
        top_idx = np.argsort(sims)[-top_k:][::-1]
        top_sims = sims[top_idx]
        max_sim = top_sims[0]

        if max_sim < 0.5:
            return ""

        retrieved_examples = [
            (self.category_texts[i], self.category_categories[i], float(top_sims[j]))
            for j, i in enumerate(top_idx)
            if top_sims[j] >= 0.5
        ]
        if not retrieved_examples:
            return ""

        predicted_category = self.classify_category_with_llm(user_input, retrieved_examples)
        return predicted_category