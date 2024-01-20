# slack_bot

```
git clone https://github.com/lejelly/slack_bot.git
```
```
cd slack_bot
```

```
docker build -t lejelly/slack_bot:20240121 .
```

開発用
```
docker run -it -v /Users/jeong/Dev:/Dev --name jeong_slack_bot lejelly/slack_bot:20240121 /bin/bash
```
git setting
```
git config --global user.email j.seongcheol118@gmail.com;git config --global user.name lejelly
```
push時にアカウントとパス聞かれなくする
```
git remote set-url origin https://lejelly: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@github.com
/lejelly/slack_bot.git/
```

デプロイ用
```
docker run -d --name jeong_slack_bot lejelly/slack_bot:20240121
```


