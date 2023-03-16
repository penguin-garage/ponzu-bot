# Ponzu Bot
Ponzu Botは、ペンギンガレージコミュニティの公式キャラクターであるポンズのロールプレイを行うChatbotです。GPT-3.5-turboを使用してSlack上でユーザーと対話を行います。

## 前提条件
Python 3.9 がインストールされていること
SlackとGoogle Cloud Functionsへのアクセス権限があること

## インストール
1. このリポジトリをクローンします。

```bash
git clone https://github.com/penguin-garage/ponzu-bot.git
cd ponzu-bot
```

2. 依存関係をインストールします。

```
poetry install
```

3. .envファイルに必要な環境変数を設定します。

```makefile
SLACK_BOT_TOKEN=<your_slack_bot_token>
SLACK_SIGNING_SECRET=<your_slack_signing_secret>
SLACK_APP_TOKEN=<your_slack_app_token>
OPENAI_API_KEY=<your_openai_api_key>
INITIAL_PROMPT=<initial_prompt>
```

## ローカルでの実行
1. アプリケーションをローカルで実行します。

```css
poetry run python main.py
```

2. ブラウザで http://localhost:3000/slack/events にアクセスして、アプリケーションが正常に動作していることを確認します。

## デプロイ
1. Google Cloud Functionsにデプロイします。

```css
gcloud functions deploy ponzu_bolt_app \
    --runtime python39 \
    --trigger-http \
    --allow-unauthenticated \
    --env-vars-file .env.yaml
```

2. デプロイが完了したら、Slackの設定で、Events APIとInteractivityをそれぞれGoogle Cloud Functionsで生成されたURLに設定します。

## 使い方
Ponzu BotがインストールされているSlackチャンネルで@Ponzuとメンションすることで、ポンズとの会話が始まります。ポンズは設定された制約条件に従って返信を行います。

## ライセンス
このプロジェクトはMITライセンスのもとで公開されています。詳細はLICENSEファイルを参照してください。