from cooker import CodeCooker

cooker = CodeCooker(ai_type="ANTHROPIC", config_path="./cooker/.config")
cooker.input_prompt("Kaggleのtaitanicの分析をしてください")

response = cooker.code_cook()

print("response-------------")
print(response)

response = cooker.code_cook()

print("response-------------")
print(response)

response = cooker.code_cook()

print("response-------------")
print(response)
