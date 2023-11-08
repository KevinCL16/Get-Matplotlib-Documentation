import pandas as pd
import json

df_annotation = pd.read_csv("Gallery_annotation_1006_pre_final.csv", header=1)
condition = df_annotation['是否已标注'] == '是'
df_filtered = df_annotation[condition]
df_crawled = pd.read_json("crawled_examples/crawled_gallery_examples_1_code_block_better_quality.json", orient="records")

result = pd.merge(df_crawled, df_filtered, on='id', how='inner')
result = result.drop('extracted_data', axis=1).drop('是否已标注', axis=1).drop('文本', axis=1).drop('gallery_example_url_link', axis=1)

out = result.to_json(orient='records', force_ascii=False, indent=4)[1:-1].replace('\\/', '/').replace('},{', '},\n{').replace(u'\xa0', u' ')
json_object = json.dumps(out, ensure_ascii=False)

with open('crawled_examples/Annotated_gallery_examples_1_code_block_better_quality.json', 'w', encoding='utf8') as f:
    f.write(out)