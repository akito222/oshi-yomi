import streamlit as st
import google.generativeai as genai
import google.api_core.exceptions
import urllib.parse

# --- 1. 初期設定 ---
# APIキーの読み込み (Streamlit CloudのSecretsから)
api_key = st.secrets.get("GEMINI_API_KEY") or "AIzaSyBu3QEQw4P6t20zbhQQpi21dIyeLg_p3qQ"
genai.configure(api_key=api_key)

# これに戻します（あきとさんが最初に書いていた最新モデル！）
model = genai.GenerativeModel('gemini-2.0-flash')

# --- 2. 画面UI（入力欄） ---
st.title("推し詠み 🌸")
st.write("キャラクターの関係性に寄り添った短歌を生成します")

# value="" で初期値を空にし、placeholderでヒントを表示
sender = st.text_input("詠み手（誰が）", value="")
recipient = st.text_input("宛て先（誰に）", value="")
relationship = st.text_area("関係性・背景", value="")

# --- 3. ボタン実行処理 ---
if st.button("短歌を詠む"):
    # 空欄のまま押された時のブロック
    if sender == "" or recipient == "":
        st.warning("⚠️ 詠み手と宛て先を入力してください！")
    else:
        # 処理中のぐるぐるアニメーション
        with st.spinner("想いを短歌に紡いでいます...（数秒かかります）"):
            
            # プロンプトの組み立て
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
            
            # 【プロの裏技】エラーが起きるかもしれない処理を「try」で囲む
            try:
                # AIにリクエストを投げて結果を取得
                response = model.generate_content(prompt)
                result_text = response.text
                
                # --- 4. 結果の装飾と表示 ---
                # 「短歌：」と「解説：」の文字を基準にテキストを分割
                tanka_part = result_text.split('解説：')[0].replace('短歌：', '').strip()
                kaisetsu_part = result_text.split('解説：')[-1].strip() if '解説：' in result_text else ""
                
                # 和風でエモいデザインの枠
                st.markdown(f"""
                <div style="background-color: #fdfcf0; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 20px;">
                    <h3 style="color: #31333f; margin-top: 0;">詠みあげられた一首</h3>
                    <p style="font-size: 24px; font-family: 'Sawarabi Mincho', serif; font-weight: bold; line-height: 1.6;">
                        {tanka_part}
                    </p>
                    <hr>
                    <p style="font-size: 14px; color: #555;">
                        {kaisetsu_part}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # --- 5. SNSシェアボタン ---
                share_text = f"【推し詠み】\n{sender}から{recipient}へ贈る短歌：\n\n{tanka_part}\n\n#推し詠み #生成AI"
                share_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(share_text)}&url={urllib.parse.quote('https://oshi-yomi.streamlit.app/')}"
                
                st.markdown(f'<a href="{share_url}" target="_blank"><button style="background-color: #1DA1F2; color: white; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer;">X(Twitter)でシェアする</button></a>', unsafe_allow_html=True)

            # もし「通信制限（429）」が起きたら、こっちの処理に逃がす
            except google.api_core.exceptions.ResourceExhausted:
                st.error("⏳ 現在、AIの利用リクエストが混み合っています。（無料枠の制限）\n1分ほど待ってから、もう一度ボタンを押してみてください。")
            
            # それ以外の予期せぬエラーが起きた場合
            except Exception as e:
                st.error(f"⚠️ エラーの正体: {e}")
