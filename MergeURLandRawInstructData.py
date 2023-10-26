import pandas as pd
import json

df_url = pd.read_json("crawled_examples/crawled_gallery_examples_1_code_block_url_links.json", orient="records")
df_raw_ins = pd.read_json("raw_instruction_tuning_data_prepared_by_gpt-3.5-turbo.json", orient="records")

result = pd.concat([df_raw_ins, df_url], axis=1)

out = result.to_json(orient='records', force_ascii=False, indent=4)[1:-1].replace('\\/', '/').replace('},{', '},\n{')
json_object = json.dumps(out, ensure_ascii=False)

with open('gpt-3.5-turbo_raw_instruction_tuning_data.json', 'w', encoding='utf8') as f:
    f.write(out)