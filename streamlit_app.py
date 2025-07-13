import streamlit as st
import re
import pandas as pd

# 엑셀 파일에서 응답 불러오기
df = pd.read_excel('자동응답시스템 개발.xlsx')  # 파일 이름이 정확해야 함
answer_dict = {}
for i in range(len(df)):
    answer = df.loc[i, '응답']
    answer_dict[i] = answer

# 키워드 사전 (rule 기반)
rule_dict = {
    0: ['어려움', '어렵', '힘들', '힘들어'],
    1: ['하기', '싫어', '하기싫어'],
    2: ['오랫동안', '집중', '안돼', '안됨'],
    3: ['사이', '갈등', '친구'],
    4: ['소음', '방해', '시끄러'],
    5: ['선생님', '의견', '말하기', '표현'],
    6: ['화장실', '악취', '냄새', '심해'],
    7: ['교복', '불편', '입기'],
    8: ['커서', '미래', '진로', '고민'],
    9: ['남자친구', '여자친구', '사귈', '연애'],
    10: ['좋아하는', '사람', '말', '못', '고백', '걸기']
}

# 텍스트 전처리 (불필요한 문자 제거)
def tokenize(text):
    text = re.sub('[^가-힣\s]', '', text)
    return text.split()

# 입력 문장과 키워드 rule 비교 (부분 일치 방식)
def match_rule(user_input):
    user_words = tokenize(user_input)
    max_score = 0
    best_rule = None

    for idx, keywords in rule_dict.items():
        score = 0
        for word in user_words:
            for keyword in keywords:
                if keyword in word:  # 부분 일치
                    score += 1
        if score > max_score:
            max_score = score
            best_rule = idx
    return best_rule

# Streamlit 앱 UI
st.title("💬 학교 스트레스 상담 챗봇")

# 대화 내역 저장
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 입력 받기
user_input = st.text_input("요즘 어떤 고민이 있어?", value="", key="input")

# 응답 처리
if user_input:
    matched = match_rule(user_input)
    if matched is not None and matched in answer_dict:
        response = answer_dict[matched]
    else:
        response = "미안 ㅜ 잘 이해가 안 갔어. 예를 들어\n\n- 공부가 어려워\n- 집중이 안돼\n- 친구랑 사이가 안 좋아졌어\n- 선생님에게 의견을 말하기 어려워\n- 소음 때문에 힘들어\n\n이런 식으로 말해줘!"

    # 대화 기록 추가
    st.session_state.chat_history.append(("나", user_input))
    st.session_state.chat_history.append(("챗봇", response))

# 이전 대화 출력
for speaker, text in st.session_state.chat_history:
    if speaker == "나":
        st.markdown(f"**🙋 나:** {text}")
    else:
        st.markdown(f"**🤖 챗봇:** {text}")

# 다음 입력을 위한 안내
if user_input:
    st.markdown("---")
    st.markdown("다른 고민도 있어? 아래에 입력해줘 ⬇️")
