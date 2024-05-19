from cooker import CodeCooker
import logging


def setup_logger(ai_type):
    """ログファイルをセットアップする関数"""
    logger = logging.getLogger(ai_type)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(f'./tests/{ai_type}.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


def run_cooker(ai_type):
    """指定されたAIタイプでcookerを実行し、結果をログに記録する関数"""
    logger = setup_logger(ai_type)
    logger.info("Start processing.")

    cooker = CodeCooker(ai_type=ai_type, config_path="./cooker/.config")
    cooker.set_ai_type(ai_type=ai_type)
    cooker.operation(operation="new")
    cooker.input_prompt("Kaggleのtaitanicの分析をしてください")

    response, python_code, output_stream = cooker.code_cook()

    logger.info("AI Type: %s", ai_type)
    logger.info("Response: %s", response)
    logger.info("Python Code: %s", python_code)
    logger.info("Output Stream: %s", output_stream)
    logger.info("End processing.")

    # ロガーのハンドラをクリーンアップ
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)


ai_type_choices = ['Claude 3 Opus', 'GPT-4', 'GPT-4o', 'Gemini 1.5 Pro', 'Gemini 1.5 Flash']

for ai_type in ai_type_choices:
    run_cooker(ai_type)
