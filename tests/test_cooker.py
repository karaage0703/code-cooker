from cooker import CodeCooker

cooker = CodeCooker(ai_type="", config_path="./cooker/.config")

ai_type_choices = ['Claude 3 Opus', 'GPT-4', 'GPT-4o', 'Gemini 1.5 Pro', 'Gemini 1.5 Flash']

for i in ai_type_choices:
    print("start-------------")
    print("AI Type:" + i)

    cooker.set_ai_type(ai_type=i)
    cooker.operation(operation="new")
    cooker.input_prompt("Kaggleのtaitanicの分析をしてください")
    response, python_code, output_stream = cooker.code_cook()

    print("AI Type:" + i)
    print("response-------------")
    print(response)

    print("python_code-------------")
    print(python_code)

    print("output_stream-------------")
    print(output_stream)
