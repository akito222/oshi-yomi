import streamlit as st
import google.generativeai as genai
import os # OSの機能を使うためのライブラリを追加

# 1. APIキーの設定（公開時はStreamlitの「Secrets」から読み込むようにします）
# ローカルでテストする時は自分のキーを入れ、GitHubへ上げる時は st.secrets から読み込む設定にします
api_key = st.secrets.get("GEMINI_API_KEY") or "あなたの今のAPIキー"
genai.configure(api_key=api_key)

# 使えるモデルを探す
available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
st.write(f"利用可能なモデル: {available_models}") # 確認用（後で消してOK）

# リストの最初にあるモデルを自動で使う
if available_models:
    model = genai.GenerativeModel(available_models[0])
else:
    st.error("利用可能なモデルが見つかりませんでした。")
# --- ここまで ---


# 2. 画面のUI（タイトルと入力欄）
st.title("推し詠み 🌸")
st.write("キャラクターの関係性に寄り添った短歌を生成します")

sender = st.text_input("詠み手（誰が）", value="")
recipient = st.text_input("宛て先（誰に）", value="")
relationship = st.text_area("関係性・背景", value="")

# 3. 実行ボタンが押された時の処理
if st.button("短歌を詠む"):
    st.info("詠んでいます...")
    
    # 4. プロンプトの組み立て
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
    
   # 5. AIにリクエストを投げて結果を表示
response = model.generate_content(prompt)
st.success("完成しました！")

# 出力結果をきれいに見せる
result_text = response.text

# 短歌と解説を分けて表示する工夫（簡易版）
st.markdown(f"""
<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
    <h3 style="color: #31333f; margin-top: 0;">詠みあげられた一首</h3>
    <p style="font-size: 24px; font-family: 'Sawarabi Mincho', serif; font-weight: bold; line-height: 1.6;">
        {result_text.split('解説：')[0].replace('短歌：', '').strip()}
    </p>
    <hr>
    <p style="font-size: 14px; color: #555;">
        {result_text.split('解説：')[-1].strip() if '解説：' in result_text else ""}
    </p>
</div>
""", unsafe_allow_html=True)


import urllib.parse

# 短歌の内容をURL用に変換
tanka_only = result_text.split('解説：')[0].replace('短歌：', '').strip()
share_text = f"【推し詠み】\n{sender}から{recipient}へ贈る短歌：\n\n{tanka_only}\n\n#推し詠み #生成AI"
share_url = f"https://twitter.com/intent/tweet?text={urllib.parse.quote(share_text)}&url={urllib.parse.quote('https://oshi-yomi.streamlit.app/')}"

# シェアボタンの設置
st.markdown(f'<a href="{share_url}" target="_blank"><button style="background-color: #1DA1F2; color: white; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer;">X(Twitter)でシェアする</button></a>', unsafe_allow_html=True)
