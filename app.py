import streamlit as st
import google.generativeai as genai
import google.api_core.exceptions
import urllib.parse

# --- 1. 初期設定 ---
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# あきとさんの環境で唯一「404」にならない最強のモデル
model = genai.GenerativeModel('models/gemini-2.0-flash')

# --- 2. 画面UI ---
st.title("推し詠み 🌸")
sender = st.text_input("詠み手", value="")
recipient = st.text_input("宛て先", value="")
relationship = st.text_area("関係性", value="")

# --- 3. 実行処理 ---
if st.button("短歌を詠む"):
    if not sender or not recipient:
        st.warning("⚠️ 詠み手と宛て先を入力してください！")
    else:
        with st.spinner("想いを短歌に紡いでいます..."):
            try:
                prompt = f"{sender}から{recipient}へ。関係は{relationship}。これに基づいた短歌と解説を出力して。"
                response = model.generate_content(prompt)
                
                # 結果表示
                st.success("完成しました！")
                st.write(response.text)
                
                # シェアボタン
                share_text = f"【推し詠み】\n{sender}から{recipient}への短歌\n\n#推し詠み"
                share_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(share_text)}"
                st.markdown(f'[Xでシェアする]({share_url})')

            except google.api_core.exceptions.ResourceExhausted:
                st.error("⏳ Googleの無料枠制限です。新しいAPIキーを『新しいプロジェクト』で作るか、少し時間を置いてください。")
            except Exception as e:
                st.error(f"⚠️ エラーが発生しました: {e}")
