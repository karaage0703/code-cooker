from cooker import CodeCooker

cooker = CodeCooker(ai_type="ANTHROPIC", config_path="./cooker/.config")
cooker.input_prompt("Kaggleのtaitanicの分析をしてください")

response, python_code, output_stream = cooker.code_cook()

print("response-------------")
print(response)

print("python_code-------------")
print(python_code)

print("output_stream-------------")
print(output_stream)
