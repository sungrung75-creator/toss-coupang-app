import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="토스&쿠팡 AI 특가 생성기", page_icon="🛍️", layout="centered")

st.title("🛍️ AI 링크 분석 특가 문구 생성기")
st.write("토스나 쿠팡 링크를 넣으면 AI가 상품을 분석해서 플랫폼별 맞춤 홍보글을 뚝딱 만들어줍니다!")

with st.sidebar:
    st.header("🔑 설정")
    api_key_input = st.text_input("Gemini API 키 입력", type="password", placeholder="AI 키를 입력하세요")
    st.markdown("---")
    st.markdown("💡 Google AI Studio에서 무료 API 키를 발급받아 입력해 주세요.")

platform = st.radio("1. 제휴 플랫폼 선택", ["토스쇼핑", "쿠팡 파트너스"], horizontal=True)
link = st.text_input("2. 상품 링크(URL)를 붙여넣으세요", placeholder="https://...")
tone = st.selectbox("3. 문구 분위기 선택", [
    "🔥 단가 쪼개기 / 가성비 강조 (인기)", 
    "😱 '와 이거 미쳤다' 탄성형", 
    "💡 실생활 꿀템 / 필수 쟁여두기"
])

generate_btn = st.button("✨ AI 맞춤 홍보 문구 생성하기")

if generate_btn:
    if not api_key_input:
        st.warning("⚠️ 왼쪽 사이드바에 Gemini API 키를 먼저 입력해 주세요!")
    elif not link:
        st.warning("⚠️ 상품 링크를 입력해 주세요!")
    else:
        try:
            genai.configure(api_key=api_key_input)
            model = genai.GenerativeModel('gemini-3.8-flash
            ')
            
            prompt = f"""
            당신은 유능한 쇼핑 마케터이자 제휴 마케팅 전문가입니다.
            사용자가 제공한 쇼핑 링크와 분위기를 바탕으로 SNS 홍보 문구를 작성해주세요.
            
            - 플랫폼: {platform}
            - 상품 링크: {link}
            - 선택한 분위기: {tone}
            
            반드시 아래 3가지 양식으로 나누어서 결과를 출력해줘. 각 양식에는 입력된 링크({link})가 필수로 포함되어야 해.
            
            [양식 1: 스레드/인스타용]
            [양식 2: 카카오톡 오픈채팅방용]
            [양식 3: 블로그/카페용]
            """
            
            with st.spinner("🤖 AI가 링크와 상품 정보를 분석하여 글을 작성 중입니다..."):
                response = model.generate_content(prompt)
                result_text = response.text
            
            st.success("🎉 맞춤 홍보 문구가 성공적으로 생성되었습니다!")
            
            tab1, tab2, tab3 = st.tabs(["🧵 스레드/인스타용", "💬 카카오톡 오픈채팅방용", "📝 블로그/카페용"])
            
            with tab1:
                st.text_area("스레드/인스타용 문구", result_text, height=200)
            with tab2:
                st.text_area("카카오톡 오픈채팅방용 문구", result_text, height=200)
            with tab3:
                st.text_area("블로그/카페용 문구", result_text, height=200)
                
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
