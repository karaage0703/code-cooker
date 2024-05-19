
# code-cooker

シンプルなデータ分析ソフトウェア (コードインタープリターのように)

<p align="center">
  <a href="./README.md"><img alt="README in English" src="https://img.shields.io/badge/English-d9d9d9"></a>
  <a href="./README_JA.md"><img alt="日本語のREADME" src="https://img.shields.io/badge/日本語-d9d9d9"></a>
</p>

## セットアップ

```sh
$ cd && git clone https://github.com/karaage0703/code-cooker
```

ファイル`./cooker/.config`を編集し、使用するAPIキーを入力してください。

Dockerをセットアップします。

## 使用方法

### GUI

以下のコマンドを実行します:

```sh
$ cd ~/code-cooker
$ docker compose up -d base
$ docker exec -it code-cooker-base python3 app.py
```

Webブラウザで`http://localhost:7860/`にアクセスします。

Dockerをシャットダウンするためには以下のコマンドを実行します:

```sh
$ docker compose down
```

### Google Colab

[こちらのノートブック](colab-notebooks/code_cooker_on_colab.ipynb)をオープンします。

## VS Code エディタ (開発用)

### 準備

1. VS Code エディタを起動します。
2. Visual Studio Code Dev Containersをインストールします。
3. F1キーを押します。
4. "Dev Containers: Open Folder in Container..."を選択し、フォルダ "container-base" を選択します。

コンテナー内で以下のコマンドを実行します:

```sh
root@hostname:~# pip install -e .
```

### GUIの起動

コンテナー内で以下のコマンドを実行します:

```sh
root@hostname:~# python3 app.py
```

Webブラウザで`http://localhost:7860/`にアクセスします。

### テスト

コンテナー内で以下のコマンドを実行します:

```sh
root@hostname:~# python3 tests/test_cooker.py
```
