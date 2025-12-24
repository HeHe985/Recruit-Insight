# jobs/services.py
import json
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate


# 환경변수 로드 (settings.py에서 처리했다면 생략 가능하지만 안전하게 포함)
load_dotenv()


class JobRecommendationService:
    """
    딕셔너리 형태로 반환
    """

    def __init__(self):
        # 1. 초기화 로직 (모델 설정 등)
        self.gms_key = os.getenv("GMS_KEY")
        if not os.environ.get("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = self.gms_key

        os.environ["OPENAI_API_BASE"] = "https://gms.ssafy.io/gmsapi/api.openai.com/v1"
        self.model = init_chat_model("gpt-4o-mini", model_provider="openai")
        self.parser = JsonOutputParser()

    def recommend_jobs(self, resume_data, job_list_data):
        """
        이력서와 공고 리스트를 받아 추천 결과를 반환하는 함수
        """
        system_prompt = """
            당신은 IT 전문 헤드헌터 AI입니다.
            주어진 [이력서]와 [채용공고 목록]을 분석하여, 지원자에게 가장 적합한 공고를 추천해주세요.

            다음 규칙을 반드시 따르세요:
            1. 기술 스택, 경력, 선호 지역을 종합적으로 고려하여 매칭 점수(0~100점)를 계산하세요.
            2. 매칭 점수가 높은 순서대로 정렬하세요.
            3. 추천 이유는 구체적으로 작성하세요.
            4. 반드시 아래와 같은 JSON 형식으로만 출력하세요. (마크다운 코드 블록 없이 JSON만 출력)

            [
                {{
                    "rank": 1,
                    "job_id": 1,
                    "company": "회사명",
                    "title": "공고명",
                    "score": 95,
                    "reason": "지원자의 Python 기술과 일치하며..."
                }},
                ...
            ]
        """

        # 프롬프트 생성
        prompt = ChatPromptTemplate.from_messages(
            [("system", system_prompt), ("user", "이력서: {resume}\n\n채용공고 목록: {jobs}")]
        )

        # 체인 연결
        chain = prompt | self.model | self.parser

        # AI 추천 실행
        try:
            # invoke 호출
            print("AI가 공고를 분석 중입니다.")

            result = chain.invoke(
                {
                    "resume": json.dumps(resume_data, ensure_ascii=False),
                    "jobs": json.dumps(job_list_data, ensure_ascii=False),
                }
            )
            return result

        except Exception as e:
            # 에러 발생
            print(f"AI Service Error: {e}")
            return []
