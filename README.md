# slack_bot

```
git clone https://github.com/lejelly/slack_bot.git
```

```
docker build -t lejelly/slack_bot:20240121 .
```

開発用
```
docker run -it -v /Users/jeong/Dev/slack_bot:/slack_bot --name jeong_slack_bot lejelly/slack_bot:20240121 /bin/bash
```

デプロイ用
```
docker run -d --name jeong_slack_bot lejelly/slack_bot:20240121
```

push時にアカウントとパス聞かれなくする
```
git remote set-url origin https://lejelly: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@github.com
/lejelly/slack_bot.git/
```