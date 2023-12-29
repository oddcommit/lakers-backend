# lakers-backend

## 環境構築

- 踏み台サーバのkey設定に関しては[こちら](https://www.notion.so/trustart/57d313fbb13f4fa5a2437cc0d14fce32?pvs=4#1f6d7f791c7f4febb0e11152944ab996)の設定が完了していることが前提
- aws-aldなどのコマンドの詳細に関しては[こちら](https://www.notion.so/trustart/57d313fbb13f4fa5a2437cc0d14fce32?pvs=4#fa26642390be44e4ae8503843a45fdbe)も参照


```bash
# package install
poetry install

# pre-commit初期化
pre-commit install

# postgresqlの起動
brew services start postgresql@14

# (初回のみ必要)dev環境の踏み台サーバーのkey設定
aws-ald
set-bastion-key

# (初回のみ必要)stg環境の踏み台サーバーのkey設定
aws-als
set-bastion-key

# (初回のみ必要)prod環境の踏み台サーバーのkey設定
aws-alp
set-bastion-key

# スクリプトに実行権限の付与
chmod +x scripts/*.sh

# データベースのセットアップ
scripts/_setup_database.sh

# stg環境からdump
aws-als # AWSプロファイルを設定
bastion-ec2 # 踏み台サーバーに接続
## 踏み台サーバーとは別のターミナルで実行
aws-als # AWSプロファイルを設定
scripts/_aws_rds_dump.sh

# migrate
poetry run python manage.py migrate

# restore
scripts/_local_db_restore.sh
```

※何かしらの理由でbastion-ec2を実行し、pemを再インストールする場合には
```bash
chmod 700 ~/.ssh
```
を実行する

## 踏み台サーバーへの接続方法

### 前提条件

`set-bastion-key`が完了していること(対象となる環境のsshキーのダウンロードが完了していること)

### 手順

### AWS接続の前準備(dev環境に接続する場合)

aws-alx は接続したいAWS環境を設定する
接続先は以下の表のようになる(表の下の図も参照)

|  コマンド(aws-alxに対応)  |  接続先  |
| ---- | ---- |
|  aws-ald  |  dev環境  |
|  aws-als  |  stg環境  |
|  aws-alp  |  prod環境  |


```bash
# AWSプロファイルを設定
aws-alx

# 踏み台サーバーに接続
bastion-ec2
```

↓のようにコマンドを実行する

![aws接続プロンプト](.docs/img/connectaws.png)

コマンド実行後、下のようにAWSに接続した状態になる（このウィンドウを消すと接続は解除される)

![aws接続完了](.docs/img/hasconnectedaws.png)



## RDSのdump

### 前提条件

踏み台サーバに接続し、↓のようなプロンプトを別ウィンドウで開いている状態

![aws接続完了](.docs/img/hasconnectedaws.png)


### AWSからデータをdump

※aws-alxの箇所は接続先の踏み台サーバに対応するコマンド(bastion-ec2を実行する直前に入力したものと同じものを入力)


```bash
## 踏み台サーバーとは別のターミナルで実行
aws-alx # AWSプロファイルを設定
scripts/_aws_rds_dump.sh 
```

![別ウィンドウでデータをdumpする](.docs/img/dumpaws.png)


## ローカルデータベースのdump
```bash
scripts/_local_db_dump.sh
```

## ローカルデータベースのrestore
- `scripts/product.dump`がある状態で実行
```bash
scripts/_local_db_restore.sh
```


## Django経由でAWS環境(RDS)に接続

### 前提条件

踏み台サーバに接続し、↓のようなプロンプトを別ウィンドウで開いている状態

![aws接続完了](.docs/img/hasconnectedaws.png)

### 接続

別なタブで以下のシェルを実行
※aws-alxの箇所は接続先の踏み台サーバに対応するコマンド(bastion-ec2を実行する直前に入力したものと同じものを入力)

```bash
# AWSプロファイルを設定
aws-alx

# 踏み台サーバーとは別のターミナルで実行
. scripts/_switch_db_setting.sh 
# 以降このターミナルで任意のコマンドを実行
```

## .sqlファイルを実行する
- `RealEstateReceptionBook`テーブルに追加のデータをinsertする場合など

### ローカルのDB場合
[Notionの手順書](https://www.notion.so/trustart/90f7e31c5fa44ce0b8be53e97e6f412f?pvs=4#24835969362246588874c91fb87565a7)

### AWS環境(RDS)の場合
[Notionの手順書](https://www.notion.so/trustart/90f7e31c5fa44ce0b8be53e97e6f412f?pvs=4#f89728c9eb404f7685be4c65798ea3ec)

## postgresql
```bash
# 起動
brew services start postgresql@14

# 停止
brew services stop postgresql@14

# 再起動
brew services restart postgresql@14
```

## スクリプト
### 必要なライブラリのインストール
```bash
poetry install
```

### ライブラリの追加
```bash
poetry add xxx
```

### サーバー起動
```bash
poetry run python manage.py runserver
```

### migration状態の確認
```bash
poetry run python manage.py showmigrations
```

### migration fileの作成
```bash
poetry run python manage.py makemigrations
```

### migrate
```bash
poetry run python manage.py migrate
```

### テストの実施方法
```bash
poetry run pytest
```

## ディレクトリ構造
domain フォルダの構造:

```sh
lakers_backend/domains/awesome_domain
|
+-- application_services    # 実装を実行する
|
+-- objects                 # ドメインオブジェクトの定義
|
+-- repositories            # 実装のインターフェイス
```

application フォルダの構造:

```sh
lakers_backend/awesome_application
|
+-- urls            # url設定
|
+-- views           # RequestとResponseに対して責任を持つ
|
+-- usecases        # Serviceを実行する
|
+-- repositories    # 実際にビジネスロジックを書く
|
+-- types           # Dictionaryに型を付ける dict[str, Any]を利用しない
|
+-- serializers     # domainオブジェクトをResponseTypeに変換する
```

## linter & formatter

commit前にpre-commitによりisort/black/flake8/pylintによるチェックが行われます。  
ただし変更があったpythonファイルのみチェックの対象となります。

commit前に手動でチェックしたい場合は下記の様にします。
```sh
# 編集したものだけ。
pre-commit run
# 編集していなものも含めて全部のファイル
pre-commit run --all-files
# isortだけチェック。--all-filesも同時OK
pre-commit run isort
```
