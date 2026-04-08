import streamlit as st
import google.generativeai as genai
import google.api_core.exceptions
import urllib.parse

# --- 1. 初期設定 ---
# APIキーの読み込み (Streamlit CloudのSecretsから)
api_key = st.secrets.get("GEMINI_API_KEY") or "あなたのAPIキー"
genai.configure(api_key=api_key)

# --- 2. 画面UI（入力欄） ---
st.title("推し詠み 🌸")
st.write("キャラクターの関係性に寄り添った短歌を生成します")

sender = st.text_input("詠み手（誰が）", value="")
recipient = st.text_input("宛て先（誰に）", value="")
relationship = st.text_area("関係性・背景", value="")

# --- 3. ボタン実行処理 ---
if st.button("短歌を詠む"):
    if sender == "" or recipient == "":
        st.warning("⚠️ 詠み手と宛て先を入力してください！")
    else:
        with st.spinner("想いを短歌に紡いでいます...（数秒かかります）"):
            
            prompt = f"""
            あなたは繊細で表現豊かな現代歌人です。以下の情報を解釈し、1首の短歌（5・7・5・7・7）と解説を出力してください。
            ・詠み手：{sender}
            ・宛て先：{recipient}
            ・関係性：{relationship}
            
            【出力フォーマット】
            短歌：
            [短歌]
            
            解説：
            [解説]
            """
            
            # モデルの候補（2.0が混んでいたら1.5、それもダメなら8bへ自動切り替え）
            models_to_try = [
                'gemini-2.0-flash', 
                'gemini-1.5-flash', 
                'gemini-1.5-flash-8b'
            ]
            
            response = None
            last_error = None

            # --- モデルの自動フォールバック処理 ---
            for m_name in models_to_try:
                try:
                    temp_model = genai.GenerativeModel(m_name)
                    response = temp_model.generate_content(prompt)
                    if response:
                        break # 成功したらループを抜ける
                except Exception as e:
                    last_error = e
                    continue # 失敗したら次のモデルを試す

            # --- 結果の表示 ---
            if response:
                try:
                    st.success("完成しました！")
                    result_text = response.text
                    
                    # テキストの分割処理
                    tanka_part = result_text.split('解説：')[0].replace('短歌：', '').strip()
                    kaisetsu_part = result_text.split('解説：')[-1].strip() if '解説：' in result_text else ""
                    
                    # デザイン枠で表示
                    st.markdown(f"""
                    <div style="background-color: #fdfcf0; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 20px;">
                        <h3 style="color: #31333f; margin-top: 0;">詠みあげられた一首</h3>
                        <p style="font-size: 24px; font-weight: bold; line-height: 1.6;">{tanka_part}</p>
                        <hr>
                        <p style="font-size: 14px; color: #555;">{kaisetsu_part}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # SNSシェア
                    share_text = f"【推し詠み】\n{sender}から{recipient}へ贈る短歌：\n\n{tanka_part}\n\n#推し詠み #生成AI"
                    share_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(share_text)}&url={urllib.parse.quote('https://oshi-yomi.streamlit.app/')}"
                    st.markdown(f'<a href="{share_url}" target="_blank"><button style="background-color: #1DA1F2; color: white; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer;">X(Twitter)でシェアする</button></a>', unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"⚠️ 表示処理でエラーが発生しました: {e}")
            
            else:
                # すべてのモデルで失敗した場合
                if isinstance(last_error, google.api_core.exceptions.ResourceExhausted):
                    st.error("⏳ 現在、すべてのAIモデルが混み合っています。数分待ってからお試しください。")
                else:
                    st.error(f"⚠️ 予期せぬエラーが発生しました: {last_error}")
