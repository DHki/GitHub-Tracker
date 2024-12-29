FROM ubuntu:22.04

COPY ./src /app
WORKDIR /app

RUN apt update
RUN apt install python3 python3-pip -y
RUN pip install -r requirements.txt

ENV GITHUB_API_TOKEN=your_github_token
ENV DISCORD_BOT_TOKEN=your_discord_bot_token
ENV DISCORD_GUILD_ID=your_discord_guild_id

CMD [ "python3", "app.py" ]