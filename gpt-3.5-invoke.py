import openai
import json
import pandas as pd
import random

# 个人API Key
openai.api_key = "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"
# 企业API Key
openai.organization = "org-IfPzna5SLpzIsCow27fYuPda"

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential, stop_after_delay,
)  # for exponential backoff


# 防止调用频率超过每分钟上限的等待代码######
@retry(wait=wait_random_exponential(min=0.02, max=1), stop=(stop_after_delay(60) | stop_after_attempt(500)))
# 调用OpenAI API
def completion_with_backoff(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                # 系统prompt
                "role": "system", "content": "As a coding assistant, your task is:"
                                             " Firstly, help me locate data preparation blocks in"
                                             " my matplotlib code and output the data used in the code. Output data"
                                             " should not include plot settings and function"
                                             " definitions. Secondly, help me come up with the appropriate natural"
                                             " language instruction for generating the code I provided with you."
            },
            {
                # 每次调用的输入
                "role": "user", "content": prompt
            }
        ]
    )
    # API返回回答
    result = response.choices[0]['message']
    return f"{result['content']}"
    # return f"{result['role']}:{result['content']}"


# 我之前的课题相关的处理，忽略
'''def process_table(dataframe, table_processed):
    tpt, tst, table, question, answer = DataPreprocess(dataframe).get_raw_data()
    for table_array in table:
        row_processed = []
        col = True
        for row in table_array:
            row_with_delimiter = ' | '.join([''.join(grid) for grid in row])
            if col is True:
                row_processed.append('[COL] ' + row_with_delimiter)
                col = False
            else:
                row_processed.append('[ROW] ' + row_with_delimiter)
        table_processed.append(row_processed)
    return tpt, tst, question, answer'''


if __name__ == '__main__':
    # 读数据
    df_crawled_gallery = pd.read_json('crawled_examples/crawled_gallery_examples_1_code_block.json', orient="records")
    gallery_dict = df_crawled_gallery.to_dict('records')
    # df_train = shuffle(df_train)
    # df_train = df_train.head(1000)
    # df_test = df_test.head(100)
    df_exemplar = pd.read_json('prompt_4_converting_gallery_2_instruction_tuning_data.json', orient="records")
    exemplar_dict = df_exemplar.to_dict('records')

    # 将返回的结果写进json文件
    with open('raw_instruction_tuning_data_prepared_by_gpt-3.5-turbo.json', 'a', encoding='utf-8') as f1:
        # 我在这里准备的few-shot样例，但是是通过上面注释掉的函数实现的，可以自行修改
        few_shot_examplar = exemplar_dict
        # 循环（待调用数据的长度）次
        for i in range(349, 380):
            # 准备输入
            chat_input = {
                "Example": "As an example for you to learn this task, I provide you with , \"code\": \n"
                           + str(few_shot_examplar[0]["code"]) + "and relevant context for this code snippet: "
                           + str(few_shot_examplar[0]["title"] + " " + few_shot_examplar[0]["text"])
                           + "you should output the data and desired instruction in such format: [DATA]: "
                           + str(few_shot_examplar[0]["DATA"]) + ", [INSTRUCTION]: " + str(few_shot_examplar[0]["INSTRUCTION"])
                           + "\n As the second example for you to learn this task, I provide you with , \"code\": \n"
                           + str(few_shot_examplar[1]["code"]) + "and relevant context for this code snippet: "
                           + str(few_shot_examplar[1]["title"] + " " + few_shot_examplar[1]["text"])
                           + "you should output the data and desired instruction in such format: [DATA]: "
                           + str(few_shot_examplar[1]["DATA"]) + ", [INSTRUCTION]: " + str(few_shot_examplar[1]["INSTRUCTION"])
                           + "The above code, context and instructions are only for you to understand my specific task instructions!"
                             " Please focus now on the following data waiting to be processed by you!"
                             " Please output the data and the respective instruction for"
                             " generating the following: \n",
                "code": gallery_dict[i]["code"],
                "relevant context": gallery_dict[i]["title"] + " " + gallery_dict[i]["text"],
                # "reminder:": " The information you generate should be less than 128 tokens."
            }
            prompt = str(chat_input)
            # 调用上面那个函数
            res = completion_with_backoff(prompt) + '\n'
            out = res.replace('\n', ' ').replace('},{', '}\n{')
            idx_data = out.index("[DATA]")
            idx_ins = out.index("[INSTRUCTION]")
            generated_data = out[idx_data + 7: idx_ins]
            generated_ins = out[idx_ins + 14:]

            # 输出json文件的内容格式，自定，想写什么些什么
            result = {
                "data": generated_data,
                "instruction": generated_ins,
                # "data": out,
                # "instruction": "THIS DATA SAMPLE IS UNDESIRED!!! MANUALLY ANNOTATE IT FROM SCRATCH",
                # "output": out,
                "id": i
            }
            json_object = json.dumps(result, indent=4, ensure_ascii=False) + ',\n'
            f1.write(json_object)
