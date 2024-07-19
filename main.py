import os
import streamlit as st
import openai

# 환경 변수에서 OpenAI API 키 가져오기
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

# 페이지 제목
st.header("AIDT와 관련하여 사회정서학습(SEL) 연결을 도와주는 챗봇")
st.write('학생 맥락과 AIDT 기능, 그리고 AI 기반 지원 방안을 단계적으로 입력해주세요.', divider='rainbow')

# Step 1: 학생 맥락 입력
st.subheader("STEP 1. 학생 맥락")

# session_state를 이용하여 student_context 상태 관리
if "student_context" not in st.session_state:
    st.session_state.student_context = ""

def generate_context():
    prompt1 = """
    학생의 맥락을 한문장으로 적어줘. 학생의 맥락이란 학생을 둘러싼 여러가지 상황을 말해. 학생의 맥락의 예시는 아래와 같아.
    학생의 학업 성취도가 낮은 상황.
    학업성취도는 높으나 정신적으로 어려움이 있는 상황.
    학업성취도는 중간이고, 교우관계는 좋은 상황.
    주의: 자기관리역량, 협력적 소통역량, 공동체 역량, 정신건강 중 한가지와 학업성취도를 섞어서 적어줘.
    """
    
    try:
        client = OpenAI()
        response = client.chat.completions.create(    
            model="text-davinci-003",
            prompt=prompt1,
            max_tokens=500,
            temperature=0.3
        )
        generated_context = response.choices[0].text.strip()
        st.session_state.student_context = generated_context
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

# 텍스트 상자
student_context = st.text_area("이 학생의 맥락을 자세히 작성해주세요.", value=st.session_state.student_context)

# 학생 맥락 생성을 위한 버튼
if st.button("학생 맥락 생성"):
    with st.spinner('여러분~ 잠시만 기다려주세요'):
        generate_context()

# Step 2: AIDT 기능 선택
st.subheader("STEP 2. AIDT 기능 선택")
aidt_functions = {
    "학습진단": ["성취수준 진단", "학습현황 분석"],
    "학습추천": ["학습경로 추천", "학습 처방"],
    "맞춤형 콘텐츠": ["다양한 콘텐츠 제공", "학습처방 콘텐츠 제공", "피드백 및 도움말 제공"],
    "대시보드": ["학습 참여도 정보 제공", "학습 이력 정보 제공", "학습 분석 정보 제공"],
    "AI튜터": ["질의응답", "추가학습자료 제공", "학습 전략 제안", "학습진도 모니터링", "피드백 및 성취도 평가", "오답노트 제공"],
    "AI 보조교사": ["수업설계 지원", "피드백 설계 지원", "평가 지원", "학생 모니터링 지원"],
    "교사 재구성 기능": ["학습 활동 재구성 대시보드 구성", "학습 관리", "학습자 관리"]
}

selected_aidt_functions = st.multiselect("AIDT 기능을 2개 선택해주세요.", list(aidt_functions.keys()))

# Step 3: AI 기반 지원 방안 입력
st.subheader("STEP 3. AI 기반 지원 방안")
cognitive_emotional_support = st.text_area("이 학생에게는 어떤 인지적 및 정서적 지원이 필요할까요?")
customized_support = st.text_area("이 학생에게 필요한 맞춤형 지원은 또 무엇이 있을까요?")
data_needed = st.text_area("이 학생의 배움 상황을 평가하고 개선하기 위해 어떤 데이터가 필요할까요?")



st.subheader("STEP 4. 교사의 하이터치")
high_touch = st.text_area("교사의 하이터치 전략을 적어주세요.")

# 프롬프트 생성
full_prompt = f"""
학생 맥락:
{student_context}

AIDT 기능:
{', '.join(selected_aidt_functions)}

인지적 및 정서적 지원:
{cognitive_emotional_support}

맞춤형 지원:
{customized_support}

필요한 데이터:
{data_needed}

하이터치 전략:
{high_touch}

당신은 선생님의 하이터치 전략 수립을 평가해주는 챗봇입니다.
학생 맥락, AIDT 기능, 인지적 및 정서적 지원, 맞춤형 지원, 필요한 데이터 등을 종합하여 하이터치 전략이 우수한지 평가해주세요.
```은 좋은 하이터치 전략의 예시입니다.

```
학생의 성취도가 낮은 상황
AI 디지털교과서의 대시보드를 통한 학습이력 분석을 통하여 학생의 성향을 분석함.
학생의 정의적 데이터를 보니 실수가 잦음을 파악함. 기록된 풀이를 찾아보니 문제를 두 번 푼 흔적을 찾음. 또한 해당문제를 찾아보니 문제풀이 시간이 다른 학생보다 긴것을 파악함.
학생이 평소에 성급하고 주의가 산만한 학생임.
다양한 것에 관심이 많아 한가지에 집중을 못하는 특성을 확인함.

하이테크 전략: 매번 시간에 쫓겨 문제를 푸는 학생에게 차분하게 문제를 풀어도 시간이 그리 오래 걸리지 않음을 실제로 보여줌. 또한 문제를 조건과 구하는 것을 명백히 구분하고 한 줄, 한 줄 문제를 분석하는 과정을 지도함.

```



"""

if st.button("평가하기"):
    with st.spinner('여러분~ 잠시만 기다려주세요'):
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt1},
            ],
            max_tokens=500,
            temperature=0.3
        )

        st.write(response.choices[0].message.content)