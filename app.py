import gradio as gr
import os

from cooker.cooker import CodeCooker

cooker = CodeCooker(ai_type="GPT-4o", config_path="./cooker/.config")

ai_type_choices = ['Claude 3.5 Sonnet', 'GPT-4', 'GPT-4o', 'Gemini 1.5 Pro', 'Gemini 1.5 Flash']
systemp_prompt_choices = ['Empty', 'Data Analysis']


def respond(ai_type, system_prompt, operation, prompt):
    cooker.set_ai_type(ai_type)
    cooker.set_system_prompt(system_prompt)
    cooker.operation(operation)
    cooker.input_prompt(prompt)
    response, python_code, output_stream = cooker.code_cook()

    image_files = cooker.get_image_files()
    return response, python_code, output_stream, image_files


iface = gr.Interface(
    fn=respond,
    inputs=[
        gr.Dropdown(choices=ai_type_choices, label="AIタイプを選択", value="GPT-4o"),
        gr.Dropdown(choices=systemp_prompt_choices, label="システムプロンプトを選択", value="Data Analysis"),
        gr.Radio(["new", "continue"], value="new"),
        gr.Textbox(lines=2, placeholder="ここにプロンプトを入力してください", label="プロンプト")
    ],
    outputs=[
        gr.Textbox(lines=1, placeholder="ここに応答が表示されます", label="応答"),
        gr.Textbox(lines=1, placeholder="ここに実行するコードが表示されます", label="コード"),
        gr.Textbox(lines=1, placeholder="ここにコードの実行結果が表示されます", label="結果"),
        gr.Gallery(label="画像")
    ],
    title="Code Cooker",
    description="面倒なことはLLMにやらせよう"
)

iface.launch(server_name="0.0.0.0")
