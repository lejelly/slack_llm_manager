FROM python:3

ENV SLACK_APP_TOKEN xapp-1-A06EU7D33H9-6497725125238-9ecf4518a8637dc704c80a98279e185a744bfb6329b96dac4a34ac1a51be7d45
ENV SLACK_BOT_TOKEN xoxb-3286178968-6497726610246-nf15Q6YC7HaEd87oiqgE4V1q
ENV OPENAI_API_KEY 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
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git
RUN mkdir src
COPY src src/
RUN pip install -r ./src/requirements.txt
WORKDIR ./src/
#ENTRYPOINT [ "python", "app.py" ]