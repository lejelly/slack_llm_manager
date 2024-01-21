# ファイルを開いて内容を読み込む
with open('/Dev/slack_bot/prompt/community_info.txt', 'r', encoding='utf-8') as file:
    file_contents = file.read()

# 特定の文字列を置換
file_contents = file_contents.replace(':チェッカーフラッグ:', '')

# 置換後の内容をファイルに書き戻す
with open('/Dev/slack_bot/prompt/community_info.txt', 'w', encoding='utf-8') as file:
    file.write(file_contents)

