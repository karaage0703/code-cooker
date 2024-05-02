from cooker import CodeCooker

cooker = CodeCooker(ai_type="ANTHROPIC", config_path="./cooker/.config")
cooker.code_cook("Kaggleのtaitanicの分析をしてください")
