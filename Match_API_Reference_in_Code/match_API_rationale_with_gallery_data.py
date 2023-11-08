import json
import pandas as pd
from tqdm import tqdm

df_api_rationale = pd.read_json('../gpt-3.5-turbo-16k_API_test.json', orient="records")
df_filtered_gallery = pd.read_json('gallery_example_precise_API.jsonl', orient="records")

df_ins_code_api_gallery = pd.concat((df_filtered_gallery["instruction"], df_filtered_gallery["code"], df_api_rationale["assistant"], df_api_rationale["id"]), axis=1)
result = df_ins_code_api_gallery.to_json(orient="records", force_ascii=False, indent=4).replace(u'\xa0', u' ')
# json_result = json.dumps(result, ensure_ascii=False)

with open("annotated_gallery_code_with_API_rationale_short.json", 'w', encoding='utf8') as f:
    f.write(result)

print("1")
