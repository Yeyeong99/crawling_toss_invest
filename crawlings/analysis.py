from openai import OpenAI
from django.conf import settings
from .models import CommentAnalysis

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def analyze_comments_with_openai(comments, company_name):
    prompt = f"""
당신은 금융 투자 전문가입니다. 아래는 '{company_name}'에 대한 일반 투자자들의 댓글입니다.  
댓글 내용을 바탕으로 전체 여론을 긍정/부정/중립으로 나누고, 핵심 키워드 및 요약을 제시해주세요.
출력할 때는 꼭 존댓말을 사용해주세요.
--- 댓글 목록 ---
{chr(10).join(f"- {c}" for c in comments)}
--------------------

출력 형식은 다음과 같으며, 존댓말을 사용해야 합니다.
1. 전체 여론: (긍정/부정/중립 중 하나)
2. 긍정적 키워드:
3. 부정적 키워드:
4. 종합 분석 요약:
"""

    # GPT-4o-mini 호출
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "출력은 한국어, 존댓말로 해야합니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=500
    )

    result = response.choices[0].message.content.strip()

    # DB에 분석 결과 저장
    CommentAnalysis.objects.create(
        company_name=company_name,
        analysis_result=result
    )

    return result
