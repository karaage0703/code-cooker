import configparser
import os
import io
import re
import shutil
import time
from contextlib import redirect_stdout

import matplotlib.pyplot as plt
import japanize_matplotlib

import anthropic
from openai import OpenAI
import google.generativeai as genai

from .system_prompt import empty_prompt
from .system_prompt import data_analysis_prompt


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
        self._image_directory_name = 'images'
        self._system_prompt = empty_prompt
        self._ai_type = ai_type
        self._previous_ai_type = ai_type

        self._config = configparser.ConfigParser()
        self._config.read(config_path)
        self.set_ai_type(ai_type)
        self._initialize_images()
        self._initialize_prompt()
        os.makedirs(self._image_directory_name, exist_ok=True)

    def operation(self, operation):
        if operation == "new" or self._previous_ai_type != self._ai_type:
            self._initialize_images()
            self._initialize_prompt()

    def _initialize_prompt(self):
        self._prompt_w_history = []

        if self._ai_type == "GPT-4" or self._ai_type == "GPT-4o":
            messages = [
                {"role": "system", "content": self._system_prompt},
            ]
            self._prompt_w_history.extend(messages)

    def _initialize_images(self):
        shutil.rmtree(self._image_directory_name, ignore_errors=True)
        os.makedirs(self._image_directory_name)

    def get_image_files(self):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        image_files = []
        for filename in os.listdir(self._image_directory_name):
            if os.path.isfile(os.path.join(self._image_directory_name, filename)) and os.path.splitext(filename)[1].lower() in image_extensions:
                image_files.append(os.path.join(self._image_directory_name, filename))

        return image_files

    def set_ai_type(self, ai_type):
        self._previous_ai_type = self._ai_type
        self._ai_type = ai_type

        if self._ai_type == "Claude 3.5 Sonnet":
            self._anthropic_api_key = self._config.get('claude_api_key', 'key')
            self._client_anthropic = anthropic.Anthropic(
                api_key=self._anthropic_api_key
            )

        if self._ai_type == "GPT-4" or self._ai_type == 'GPT-4o':
            self._openai_api_key = self._config.get('openai_api_key', 'key')
            self._client_openai = OpenAI(
                api_key=self._openai_api_key
            )

        if self._ai_type == "Gemini 1.5 Pro":
            self._gemini_api_key = self._config.get('gemini_api_key', 'key')
            genai.configure(
                api_key=self._gemini_api_key
            )
            self._client_google = genai.GenerativeModel(
                'gemini-1.5-pro-latest', system_instruction=[self._system_prompt])

        if self._ai_type == 'Gemini 1.5 Flash':
            self._gemini_api_key = self._config.get('gemini_api_key', 'key')
            genai.configure(
                api_key=self._gemini_api_key
            )
            self._client_google = genai.GenerativeModel(
                'gemini-1.5-flash-latest', system_instruction=[self._system_prompt])

    def set_system_prompt(self, system_prompt):
        if system_prompt == "Empty":
            self._system_prompt = empty_prompt

        if system_prompt == "Data Analysis":
            self._system_prompt = data_analysis_prompt

    def _chat(self, prompt_w_history):
        """
        APIを使用してAIとチャットを行います。

        Args:
            prompt_w_history (list): チャット履歴を含むプロンプト。
            system_prompt (str): システムプロンプト。

        Returns:
            response: APIからの応答。
        """

        if self._ai_type == "Claude 3.5 Sonnet":
            print("I am Claude 3.5 Sonnet")
            response = self._client_anthropic.messages.create(
                max_tokens=2048,
                messages=prompt_w_history,
                model="claude-3-5-sonnet-20240620",
                system=self._system_prompt
            )
            assistant_response = response.content[0].text

        if self._ai_type == "GPT-4":
            print("I am GPT-4")
            response = self._client_openai.chat.completions.create(
                model="gpt-4",
                messages=prompt_w_history,
            )
            assistant_response = response.choices[0].message.content

        if self._ai_type == "GPT-4o":
            print("I am GPT-4o")
            response = self._client_openai.chat.completions.create(
                model="gpt-4o",
                messages=prompt_w_history,
            )
            assistant_response = response.choices[0].message.content

        if self._ai_type == "Gemini 1.5 Pro":
            print("I am Gemini 1.5 Pro")
            response = self._client_google.generate_content(
                prompt_w_history
            )
            assistant_response = response.text

        if self._ai_type == "Gemini 1.5 Flash":
            print("I am Gemini 1.5 Flash")
            response = self._client_google.generate_content(
                prompt_w_history
            )
            assistant_response = response.text

        return assistant_response

    def input_prompt(self, user_prompt):
        if self._ai_type == "Gemini 1.5 Pro" or self._ai_type == "Gemini 1.5 Flash":
            messages = [
                {"role": "user", "parts": [user_prompt] },
            ]
        else:
            messages = [
                {"role": "user", "content": user_prompt},
            ]

        self._prompt_w_history.extend(messages)

    def _handle_error(self, assistant_response, error):
        if self._ai_type == "Gemini 1.5 Pro" or self._ai_type == "Gemini 1.5 Flash":
            self._prompt_w_history.append({
                "role": "model",
                "parts": [str(assistant_response)]
            })
        else:
            self._prompt_w_history.append({
                "role": "assistant",
                "content": str(assistant_response)
            })
        self._retry_count += 1
        if self._retry_count < self._max_retry_count:
            if self._ai_type == "Gemini 1.5 Pro" or self._ai_type == "Gemini 1.5 Flash":
                self._prompt_w_history.append({
                    "role": "user",
                    "parts": [f"エラーが発生しました。エラーメッセージ: {error}\nコードを修正して再度実行してください。"]
                })
            else:
                self._prompt_w_history.append({
                    "role": "user",
                    "content": f"エラーが発生しました。エラーメッセージ: {error}\nコードを修正して再度実行してください。"
                })

    def code_cook(self):
        """
        与えられたプロンプトに基づいてコードを生成し、実行します。
        """
        self._retry_count = 0
        output_stream = ""
        assistant_response = ""

        while self._retry_count < self._max_retry_count:
            try:
                assistant_response = self._chat(self._prompt_w_history)

            except Exception as e:
                print(e)

            print("Response:")
            print(assistant_response)

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

                if self._ai_type == "Gemini 1.5 Pro" or self._ai_type == "Gemini 1.5 Flash":
                    self._prompt_w_history.append({
                        "role": "model",
                        "parts": [str(assistant_response) + 'result:' + output_stream]
                    })
                else:
                    self._prompt_w_history.append({
                        "role": "assistant",
                        "content": str(assistant_response) + 'result:' + output_stream
                    })
                print("コードの実行が完了しました。")
                if "```python" in assistant_response and "```" in assistant_response:
                    assistant_response = re.sub(r"\`\`\`python.*?\`\`\`", "", assistant_response, flags=re.DOTALL)

                return assistant_response, python_code, output_stream

            except Exception as error:
                print(f"エラーが発生しました: {error}")
                self._handle_error(assistant_response, error)

        print("コードの修正に失敗しました。再実行回数が上限に達しました。")
        output_stream = "コードの修正に失敗しました。再実行回数が上限に達しました。"
        self._retry_count = 0

        if "```python" in assistant_response and "```" in assistant_response:
            assistant_response = re.sub(r"\`\`\`python.*?\`\`\`", "", assistant_response, flags=re.DOTALL)

        return assistant_response, python_code, output_stream
