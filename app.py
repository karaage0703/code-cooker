import gradio as gr
from cooker.cooker import CodeCooker

cooker = CodeCooker(ai_type="ANTHROPIC", config_path="./cooker/.config")

def respond(ai_type, prompt):
    cooker.input_prompt(prompt)
    response = cooker.code_cook()
    return response

# UIの定義
iface = gr.Interface(
    fn=respond,
    inputs=[
        gr.Dropdown(choices=['OPENAI', 'ANTHROPIC', 'PHI3', 'LLAMA3'], label="AIタイプを選択"),
        gr.Textbox(lines=2, placeholder="ここにプロンプトを入力してください", label="プロンプト")
    ],
    outputs="text",
    title="Code Cooker",
    description="選択したAIタイプに基づいてプロンプトに応答します。"
)

iface.launch()
