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

sender = st.text_input("詠み手（誰が）", "五条悟")
recipient = st.text_input("宛て先（誰に）", "夏油傑")
relationship = st.text_area("関係性・背景", "かつて最強の二人だったが、道を違えた。戻らない青い春への決別。")

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
    st.write(response.text)