FROM python:3

ENV SLACK_APP_TOKEN 'your-slack-app-token'
ENV SLACK_BOT_TOKEN 'your-slack-bot-token'
ENV OPENAI_API_KEY 'your-openai-api-key'
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git
RUN mkdir src
COPY src src/
RUN pip install -r ./src/requirements.txt
WORKDIR /Dev
#ENTRYPOINT [ "python", "app.py" ]
