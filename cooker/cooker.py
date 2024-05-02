import configparser
import os
import io
import matplotlib.pyplot as plt
import japanize_matplotlib
from contextlib import redirect_stdout
import anthropic
import time
from .system_prompt import system_prompt


class CodeCooker:
    """
    CodeCookerクラスは、AIを使用してコードを生成し、実行するためのクラスです。
    """

    def __init__(self, ai_type, config_path):
        """
        CodeCookerクラスのインスタンスを初期化します。

        Args:
            ai_type (str): 使用するAIのタイプ。
        """
        self._max_retry_count = 3
        self._retry_count = 0

        self._config = configparser.ConfigParser()
        self._config.read(config_path)
        self._anthropic_api_key = self._config.get('claude_api_key', 'key')
        self.set_ai_type(ai_type)
        self.initialize_prompt()

    def initialize_prompt(self):
        self._prompt_w_history = []

    def set_ai_type(self, ai_type):
        self._ai_type = ai_type

        if self._ai_type == "ANTHROPIC":
            self._client_anthropic = anthropic.Anthropic(
                api_key=self._anthropic_api_key
            )

    def _chat_claude(self, prompt_w_history):
        """
        Anthropic APIを使用してClaude AIとチャットを行います。

        Args:
            prompt_w_history (list): チャット履歴を含むプロンプト。
            system_prompt (str): システムプロンプト。

        Returns:
            response: Anthropic APIからの応答。
        """
        print("I am Claude")
        response = self._client_anthropic.messages.create(
            max_tokens=2048,
            messages=prompt_w_history,
            model="claude-3-opus-20240229",
            system=system_prompt
        )

        return response

    def input_prompt(self, user_prompt):
        if self._ai_type == "ANTHROPIC":
            messages = [
                {"role": "user", "content": user_prompt},
            ]

        self._prompt_w_history.extend(messages)

    def code_cook(self):
        """
        与えられたプロンプトに基づいてコードを生成し、実行します。
        """
        output_stream = ""

        if self._retry_count < self._max_retry_count:
            try:
                if self._ai_type == "ANTHROPIC":
                    response = self._chat_claude(
                        self._prompt_w_history
                    )

            except Exception as e:
                print(e)

            if self._ai_type == "ANTHROPIC":
                assistant_response = response.content[0].text

            print("APIからの応答:", assistant_response)

            python_code = ""
            if "```python" in assistant_response and "```" in assistant_response:
                python_code = assistant_response.split("```python")[1].split("```")[0]

            try:
                stream = io.StringIO()

                with redirect_stdout(stream):
                    exec(python_code)

                output_stream = stream.getvalue()

                print("Result:")
                print(output_stream)

                self._prompt_w_history.append({
                    "role": "assistant",
                    "content": str(assistant_response) + 'result:' + output_stream
                })
                print("コードの実行が完了しました。")
                self._retry_count = 0
            except Exception as e:
                print(f"エラーが発生しました: {e}")
                self._prompt_w_history.append({
                    "role": "assistant",
                    "content": str(assistant_response)
                })
                self._retry_count += 1
                if self._retry_count < self._max_retry_count:
                    self._prompt_w_history.append({
                        "role": "user",
                        "content": f"エラーが発生しました。エラーメッセージ: {e}\nコードを修正して再度実行してください。"
                    })
        else:
            print("コードの修正に失敗しました。再実行回数が上限に達しました。")
            self._retry_count = 0

        return assistant_response+python_code+output_stream
