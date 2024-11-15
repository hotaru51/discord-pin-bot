# discord-pin-bot

特定のリアクションに反応してメッセージをピン留めするbot

## Requirements

* Python 3.12
* Docker

事前に[Discord Developer Portal](https://discord.com/developers/docs/intro)でアプリを作成してtokenを取得しておく

## Setup

環境変数周り

```sh
# envファイルのサンプルを複製してDiscordのtokenを設定
cp env_sample .env

# direnvがある場合は必要に応じて.envrcを設定
echo 'dotenv .env' > .envrc
```

コンテナ

```sh
# ビルド
docker compose build

# 実行
docker compose up -d
```

pipenv (開発時のみ)

```sh
cd bot/
pipenv install

# 必要に応じて仮想環境をactivate
pipenv shell
```
