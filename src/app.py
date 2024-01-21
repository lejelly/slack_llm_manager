import os
import logging
from slack_bolt import App, Ack, Say, BoltContext, Respond
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from  openai import OpenAI

# デバッグレベルのログを有効化
logging.basicConfig(level=logging.DEBUG)
# これから、この app に処理を設定していきます
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

gpt = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

@app.command("/modal-command")
def handle_some_command(ack: Ack, body: dict, client: WebClient):
    # 受信した旨を 3 秒以内に Slack サーバーに伝えます
    ack()
    # views.open という API を呼び出すことでモーダルを開きます
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "modal-id",
            "title": {"type": "plain_text", "text": "コミュニティマネージャー"},
            "submit": {"type": "plain_text", "text": "送信"},
            "close": {"type": "plain_text", "text": "閉じる"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "question-block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "input-element",
                    },
                    "label": {"type": "plain_text", "text": "どんな人をお探しですか？"},
                },
            ],
            "notify_on_close": True,
        },
    )

@app.view_closed("modal-id")
def handle_view_closed(ack: Ack, view: dict, logger: logging.Logger):
    # 受信した旨を 3 秒以内に Slack サーバーに伝えます
    ack()
    # 処理中だったバックエンド処理を中止したり、完了通知を DM に切り替えるために
    # この閉じられたという状態を view_id と紐づけて保存しておく
    logger.info(view) 
    
# view.callback_id にマッチングする（正規表現も可能）
@app.view("modal-id")
def handle_view_events(ack: Ack, view: dict, client: WebClient):
    # まず「処理中...」である旨を伝えます
    inputs = view["state"]["values"]
    question = inputs.get("question-block", {}).get("input-element", {}).get("value")
    ack(
        response_action="update",
        view={
            "type": "modal",
            "callback_id": "modal-id",
            "title": {"type": "plain_text", "text": "コミュニティマネージャー"},
            "close": {"type": "plain_text", "text": "閉じる"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "少々お待ちください、ぴったりの人がいますよ！",
                    },
                }
            ],
        },
    )

    # LLM による応答を取得します
    responce = query_gpt_chat(question)

    # 結果を待った後 views.update API を非同期で呼び出して再度更新をかけます
    client.views_update(
        view_id=view.get("id"),
        view={
            "type": "modal",
            "callback_id": "modal-id",
            "title": {"type": "plain_text", "text": "コミュニティマネージャー"},
            "close": {"type": "plain_text", "text": "閉じる"},
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "plain_text", "text": "この人と会ってみてはどうでしょう？\n"+responce},
                }
            ],
        },
        # ここでは ^ の ack() で hash がすでに更新されているので渡さない
        # hash=view.get("hash"),
    )

def query_gpt_chat(input_str):
    try:
        f = open('/Dev/slack_bot/prompt/system.txt', 'r', encoding='UTF-8')
        system_content = f.read()
        f.close()
        f = open('/Dev/slack_bot/prompt/fewshot.txt', 'r', encoding='UTF-8')
        fewshot = f.read()
        f.close()
        f = open('/Dev/slack_bot/prompt/user.txt', 'r', encoding='UTF-8')
        user = f.read()
        f.close()
        f = open('/Dev/slack_bot/prompt/community_info.txt', 'r', encoding='UTF-8')
        community_info = f.read()
        f.close()
        
        user_content = user + fewshot + "[ユーザからの要望]"+"\n\n"+input_str+"\n\n"+community_info+"\n\n\n"+"[あなたの回答]"
        
        response = gpt.chat.completions.create(
            model="gpt-4-1106-preview",
            temperature = 0,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
        )
        result = response.choices[0].message.content
        return result
    except AttributeError as e:
        error_message = f"Error: {e}"
        print(error_message)
        result = error_message 
        return result

if __name__ == "__main__":
    # ソケットモードのコネクションを確立
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
