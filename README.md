
# slack_llm_manager 実行手順
参考にしたサイト：[Slack アプリでのモーダルの使い方完全ガイド](https://qiita.com/seratch/items/0b1790697281d4cf6ab3)

- 上のサイトを参考にslackのAPIを使えるようにする
- このリポジトリをcloneする
```
git clone https://github.com/lejelly/slack_llm_manager.git;cd slack_llm_manager
```
- prompt/community-info.txt に名簿と各人の情報を置いておく
- prompt/fewshot.txt に質問例とcommunity-info.txtの例と想定回答を書いておく

## 開発用
- Dockerfileの最後の行を#でコメントアウトする-> `#ENTRYPOINT [ "python", "app.py" ]`
```
docker build -t lejelly/dev_slack_llm_manager:20240121 .
```
```
docker run -it -v Path/to/your/local/dir/you/want/to/mount --name dev_slack_llm_manager lejelly/dev_slack_llm_manager:20240121 /bin/bash
```

## デプロイ用
- Dockerfileの最後の行のコメントアウトを外す-> `ENTRYPOINT [ "python", "app.py" ]`
```
docker build -t lejelly/slack_llm_manager:20240121 .
```
```
docker run -d --name slack_llm_manager lejelly/slack_llm_manager:20240121
```
コンテナの起動とともにアプリケーションがデプロイされる


