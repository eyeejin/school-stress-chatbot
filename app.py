import streamlit as st
import re
import pandas as pd

df = pd.read_excel('자동응답시스템 개발.xlsx')
answer_dict = {}
for i in range(len(df)):
    answer = df.loc[i, '응답']
    answer_dict[i] = answer

rule_dict = {
    0: ['어려움', '어렵', '힘들'],
    1: ['하기', '싫어'],
    2: ['오랫동안', '집중', '안됨'],
    3: ['사이', '갈등'],
    4: ['소음', '방해'],
    5: ['선생님', '의견', '말하기'],
    6: ['화장실', '악취', '심해'],
    7: ['교복', '불편'],
    8: ['커서', '미래', '고민'],
    9: ['남자친구', '여자친구', '사귈'],
    10: ['좋아하는', '사람', '말', '못', '걸기']
}

def tokenize(text):
    text = re.sub('[^가-힣\s]', '', text)
    return text.split()

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

st.title("학교 스트레스 상담 챗봇")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 입력창은 항상 보여줘야 함! 조건문 밖에 둠
user_input = st.text_input("요즘 어떤 고민이 있어?", value="", key="input")

if user_input:
    matched = match_rule(user_input)
    if matched is not None and matched in answer_dict:
        response = answer_dict[matched]
    else:
        response = "미안 ㅜ 잘 이해가 안 가는데 다시 입력해줘. 예를 들어 {'공부가 어려워'/ '공부 하기 싫어'/ '집중이 안돼'/ '친구랑 사이가 안 좋아졌어'/ '공사 소음이 너무 심해서 방해가 돼'/ '선생님에게 내 의견을 못 말하겠어.'/ '화장실 악취가 너무 심해', '교복 입기가 불편해'/ '난 커서 뭐가 될까'/ '내가 남자친구/여자친구를 사귈 수 있을까?'/ '좋아하는 사람이 있는데 말을 못 걸겠어'} 라고 입력하면 더 정확하게 대답해 줄 수 있어."

    # 대화 기록 저장
    st.session_state.chat_history.append(("나", user_input))
    st.session_state.chat_history.append(("챗봇", response))

    # 입력칸 초기화하려면 아래 코드를 쓰면 안됨 (Streamlit 제한)
    # 대신 사용자가 직접 입력창을 지우고 새로 입력해야 함

# 이전 대화 내용 출력
for speaker, text in st.session_state.chat_history:
    if speaker == "나":
        st.markdown(f"**나:** {text}")
    else:
        st.markdown(f"**챗봇:** {text}")