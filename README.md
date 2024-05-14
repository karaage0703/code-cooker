# code-cooker
Simple data analysis software like Advanced Data Analysis(Code Interpreter).

## Setup

```sh
$ cd && git clone https://github.com/karaage0703/code-cooker
```

Edit `./cooker/.config` and input api key which you use.

Setup Docker.

## Usage

### GUI

Execute following commands:

```sh
$ cd ~/code-cooker
$ docker compose up -d base
$ docker exec -it code-cooker-base python3 app.py
```

Access `http://localhost:7860/` with web browser.

Execute following command for shutdown docker:

```sh
$ docker compose down
```

### Google Colab

Open [colab-notebooks/code_cooker_on_colab.ipynb](colab-notebooks/code_cooker_on_colab.ipynb).

## VS Code Editor(For development)

### Preparation

1. Launch VS Code Editor
1. Install Visual Studio Code Dev Containers.
1. Press F1 key.
1. Select "Dev Containers: Open Folder in Container..." and choose folder "container-base"

In container, execute following command:

```sh
root@hostname:~# pip install -e .
```

### launch GUI

In container, execute following command:

```sh
root@hostname:~# python3 app.py
```

Access `http://localhost:7860/` with web browser.

### Test

In container, execute following command:

```sh
root@hostname:~# python3 tests/test_cooker.py
```
