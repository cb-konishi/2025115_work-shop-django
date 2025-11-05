# Django Workshop - Issue Driven Development & GitHub Copilot

このリポジトリは、**Issue Driven Development（イシュー駆動開発）** と **GitHub Copilot の活用** を学ぶためのワークショッププロジェクトです。

## 📋 プロジェクト概要

Django 5とMySQLを使用したシンプルな商品管理Webアプリケーションを通じて、以下を実践的に学びます：

- **Issue Driven Development**: GitHubのIssueを起点とした開発フロー
- **Assigning Copilot**: GitHub Copilotを活用した効率的なコーディング
- **ベストプラクティス**: Djangoプロジェクトの標準的な構成と管理方法

## 🛠️ 技術スタック

- **言語**: Python 3.12
- **フレームワーク**: Django 5.x
- **データベース**: MySQL 8.0
- **コンテナ**: Docker & Docker Compose
- **その他**: 
  - Shell（エントリーポイントスクリプト）
  - HTML（テンプレート）

## 🚀 セットアップ手順

### 前提条件

以下がインストールされていることを確認してください：

- Docker
- Docker Compose

### 起動方法

1. **リポジトリのクローン**

```bash
git clone https://github.com/cb-konishi/2025115_work-shop-django.git
cd 2025115_work-shop-django
```

2. **Docker Composeで環境を起動**

```bash
docker-compose up -d
```

初回起動時、以下が自動的に実行されます：
- MySQL データベースの初期化
- Django マイグレーションの実行
- スーパーユーザーの作成（username: `admin`, password: `admin`）

3. **起動確認**

ログを確認：
```bash
docker-compose logs -f web
```

`[entrypoint] Starting Django dev server on 0.0.0.0:8000 ...` と表示されれば起動成功です。

## 💻 利用方法

### アプリケーションへのアクセス

- **商品一覧ページ**: http://localhost:8000/products/
- **管理画面**: http://localhost:8000/admin/
  - ユーザー名: `admin`
  - パスワード: `admin`

### 商品の追加

1. 管理画面にログイン
2. 「Products」セクションから商品を追加
3. 商品一覧ページで確認

### コンテナの停止

```bash
docker-compose down
```

データベースも削除する場合：
```bash
docker-compose down -v
```

## 📁 プロジェクト構成

```
.
├── config/              # Djangoプロジェクト設定
│   ├── settings.py      # 設定ファイル
│   ├── urls.py          # URLルーティング
│   └── wsgi.py          # WSGIエントリーポイント
├── store/               # 商品管理アプリケーション
│   ├── migrations/      # データベースマイグレーション
│   ├── templates/       # HTMLテンプレート
│   ├── models.py        # データモデル（Product）
│   ├── views.py         # ビュー関数
│   ├── urls.py          # URLパターン
│   └── admin.py         # 管理画面設定
├── .github/             # GitHub関連設定
│   ├── agents/          # GitHub Copilot Agent設定
│   └── prompts/         # プロンプトテンプレート
├── Dockerfile           # Dockerイメージ定義
├── docker-compose.yml   # Docker Compose設定
├── entrypoint.sh        # コンテナ起動スクリプト
├── manage.py            # Django管理コマンド
└── requirements.txt     # Python依存パッケージ
```

## 🎯 ワークショップの趣旨

### Issue Driven Development

このプロジェクトでは、以下のワークフローを実践します：

1. **Issue作成**: 機能追加やバグ修正をIssueとして起票
2. **ブランチ作成**: Issueに紐づくブランチを作成
3. **実装**: GitHub Copilotを活用してコードを実装
4. **プルリクエスト**: レビューとマージ
5. **Issue完了**: PRマージ後、Issueをクローズ

このフローにより、開発の透明性と追跡可能性が向上します。

### Assigning Copilot

GitHub Copilotの以下の機能を活用します：

- **コード補完**: 文脈に応じた適切なコード提案
- **チャット機能**: 実装方針の相談や質問
- **コメントからのコード生成**: 自然言語での指示からコード生成
- **リファクタリング支援**: 既存コードの改善提案

## 🔧 開発コマンド

コンテナ内でDjangoコマンドを実行する場合：

```bash
# マイグレーション作成
docker-compose exec web python manage.py makemigrations

# マイグレーション実行
docker-compose exec web python manage.py migrate

# スーパーユーザー作成
docker-compose exec web python manage.py createsuperuser

# シェル起動
docker-compose exec web python manage.py shell

# テスト実行
docker-compose exec web python manage.py test
```

## 📚 参考資料

- [Django公式ドキュメント](https://docs.djangoproject.com/)
- [GitHub Copilot ドキュメント](https://docs.github.com/ja/copilot)
- [Docker Compose ドキュメント](https://docs.docker.com/compose/)
- [MySQL 8.0 リファレンスマニュアル](https://dev.mysql.com/doc/refman/8.0/ja/)

## 📝 ライセンス

このプロジェクトはワークショップ教材として提供されています。

## 🤝 コントリビューション

Issue・Pull Requestは歓迎です。Issue Driven Developmentの実践の場としてご活用ください。
