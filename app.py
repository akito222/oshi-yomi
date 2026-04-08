# 3. 実行ボタンが押された時の処理
if st.button("短歌を詠む"):
    # 空欄のまま押された時のブロック
    if sender == "" or recipient == "":
        st.warning("⚠️ 詠み手と宛て先を入力してください！")
    else:
        with st.spinner("想いを短歌に紡いでいます...（数秒かかります）"):
            
            prompt = f"""
            あなたは繊細で表現豊かな現代歌人です。以下の情報を解釈し、1首の短歌（5・7・5・7・7）と解説を出力してください。
            ・詠み手：{sender}
            ・宛て先：{recipient}
            ・関係性：{relationship}
            """
            
            # 【ここがプロの裏技】エラーが起きるかもしれない処理を「try」で囲む
            try:
                # 5. AIにリクエストを投げて結果を表示
                response = model.generate_content(prompt)
                st.success("完成しました！")
                st.write(response.text) # （もし装飾コードがあればここに書く）
                
            # もし「通信制限（429）」が起きたら、こっちの処理に逃がす
            except google.api_core.exceptions.ResourceExhausted:
                st.error("⏳ 現在、AIの利用リクエストが混み合っています。（無料枠の制限）\n1分ほど待ってから、もう一度ボタンを押してみてください。")
            
            # それ以外の予期せぬエラーが起きた場合
            except Exception as e:
                st.error("⚠️ 予期せぬエラーが発生しました。時間を置いてお試しください。")
