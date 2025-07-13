import streamlit as st
import pandas as pd
import re

# 엑셀 파일 불러오기
df = pd.read_excel('자동응답시스템 개발.xlsx')

# 응답 딕셔너리 만들기
answer_dict = {}
for i in range(len(df)):
    answer = df.loc[i, '응답']
    answer_dict[i] = answer

# 룰 딕셔너리 (키워드 리스트)
rule_dict = {
    0: ['어려움', '어렵', '힘들'],
    1: ['공부', '하기', '싫어'],
    2: ['집중', '안돼', '안됨', '안돼요'],
    3: ['친구', '사이', '갈등', '싸움'],
    4: ['소음', '공사', '시끄러'],
    5: ['선생님', '의견', '말하기'],
    6: ['화장실', '악취', '냄새', '심해'],
    7: ['교복', '불편', '작아'],
    8: ['커서', '미래', '진로', '고민'],
    9: ['남자친구', '여자친구', '연애', '사귈'],
    10: ['좋아하는', '사람', '말', '못', '고백']
}

# 입력 문장을 토큰으로 나누는 함수
def tokenize(text):
    text = re.sub('[^가-힣\s]', '', text)
    return text.split()

# 입력 문장에서 키워드가 몇 개 매칭되는지 계산
def match_rule(user_input):
    user_words = set(tokenize(user_input))
    max_score = 0
    best_rule = None
    for idx, keywords in rule_dict.items():
        score = len(user_words.intersection(keywords))
        if score > max_score:
            max_score = score
            best_rule = idx
    return best_rule

# Streamlit 챗봇 UI
st.title("🎓 학교 스트레스 상담 챗봇")

# 이전 대화 기록 유지
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 사용자 입력 받기
user_input = st.text_input("요즘 어떤 고민이 있어?", value="", key="input")

if user_input:
    matched = match_rule(user_input)

    if matched is not None and matched in answer_dict:
        response = answer_dict[matched]
    else:
        response = "미안 ㅜ 잘 이해가 안 갔어. 예시처럼 입력해볼래?\n\n" \
                   "- 공부가 어려워\n- 집중이 안돼\n- 친구랑 사이가 안 좋아졌어\n- 공사 소음이 너무 심해\n" \
                   "- 선생님에게 말하기 힘들어\n- 교복이 불편해\n- 화장실이 너무 더러워\n" \
                   "- 미래가 고민돼\n- 연애 고민 있어\n- 좋아하는 사람에게 고백 못 하겠어"

    # 대화 내용 저장
    st.session_state.chat_history.append(("나", user_input))
    st.session_state.chat_history.append(("챗봇", response))

# 대화 내용 보여주기
for speaker, text in st.session_state.chat_history:
    if speaker == "나":
        st.markdown(f"**👤 나:** {text}")
    else:
        st.markdown(f"**🤖 챗봇:** {text}")
