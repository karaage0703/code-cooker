import gradio as gr
import os

from cooker.cooker import CodeCooker

cooker = CodeCooker(ai_type="ANTHROPIC", config_path="./cooker/.config")


# def respond(ai_type, operation, prompt):
def respond(operation, prompt):
    print(operation)
    if operation == "new":
        print("unko")
        cooker.initialize_images()
        cooker.initialize_prompt()

    cooker.input_prompt(prompt)
    response, python_code, output_stream = cooker.code_cook()

    image_files = cooker.get_image_files()
    return response, python_code, output_stream, image_files


iface = gr.Interface(
    fn=respond,
    inputs=[
        # gr.Dropdown(choices=['CLAUDE_3_OPUS', 'GPT4'], label="AIタイプを選択"),
        gr.Radio(["new", "continue"]),
        gr.Textbox(lines=2, placeholder="ここにプロンプトを入力してください", label="プロンプト")
    ],
    outputs=[
        gr.Textbox(lines=1, placeholder="ここに応答が表示されます", label="応答"),
        gr.Textbox(lines=1, placeholder="ここに実行するコードが表示されます", label="コード"),
        gr.Textbox(lines=1, placeholder="ここにコードの実行結果が表示されます", label="結果"),
        gr.Gallery(label="画像ギャラリー")
    ],
    title="Code Cooker",
    description="面倒なことはLLMにやらせよう"
)

iface.launch()
