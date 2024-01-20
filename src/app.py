import os
import logging
from slack_bolt import App, Ack, Say, BoltContext, Respond
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

# デバッグレベルのログを有効化
logging.basicConfig(level=logging.DEBUG)
# これから、この app に処理を設定していきます
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

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
                    "label": {"type": "plain_text", "text": "何らかのデータ登録"},
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
                        "text": "処理中です... このモーダルを閉じずにしばらくお待ちください :bow:",
                    },
                }
            ],
        },
    )

    # 何か時間がかかる処理をシミュレートしているだけです
    import time
    time.sleep(3.5)  # 3.5 秒かかります

    # 結果を待った後 views.update API を非同期で呼び出して再度更新をかけます
    client.views_update(
        view_id=view.get("id"),
        view={
            "type": "modal",
            "callback_id": "modal-id",
            "title": {"type": "plain_text", "text": "テストモーダル"},
            "close": {"type": "plain_text", "text": "閉じる"},
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "plain_text", "text": "正常に完了しました！"},
                }
            ],
        },
        # ここでは ^ の ack() で hash がすでに更新されているので渡さない
        # hash=view.get("hash"),
    )


if __name__ == "__main__":
    # ソケットモードのコネクションを確立
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
