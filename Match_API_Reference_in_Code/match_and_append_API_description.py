import ast
import json
from collections import defaultdict

from tqdm import tqdm


class MethodVisitor(ast.NodeVisitor):
    def __init__(self):
        self.methods = set()

    def visit_Attribute(self, node):
        # Identify method calls and add them to the set
        self.methods.add(node.attr)
        self.generic_visit(node)


def merge_duplicate_values(ref_dict):
    result = {}
    for key, value_list in ref_dict.items():
        seen = defaultdict(list)
        for item in value_list:
            api_description = item["API description"]
            seen[api_description].append(item["API name"])

        merged_list = []
        for desc, names in seen.items():
            merged_dict = {
                "API name": ", ".join(names),
                "API description": desc
            }
            merged_list.append(merged_dict)

        result[key] = merged_list
    return result


def find_string_info(search_strings, f_ref):
    results = {}
    merged_ref = []
    for search_string in search_strings:
        same_name_api = []
        for item in f_ref:
            for key, value in item.items():
                if value == search_string:
                    same_name_api.append({
                        "API name": item['name'],
                        "API description": item['text']
                    })
                    results[search_string] = same_name_api
                    merged_ref = merge_duplicate_values(results)

    return merged_ref


# Simulating the content of methods.json
with open('flattened_API_reference.json', 'r') as f:
    flat_ref = json.load(f)
methods_from_json = []
for data_item in flat_ref:
    if data_item.get('leaf_class_name', []):
        methods_from_json.append(data_item['leaf_class_name'])
    if data_item.get('leaf_method_name', []):
        methods_from_json.append(data_item['leaf_method_name'])
    if data_item.get('leaf_attribute_name', []):
        methods_from_json.append(data_item['leaf_attribute_name'])
    if data_item.get('leaf_property_name', []):
        methods_from_json.append(data_item['leaf_property_name'])
    if data_item.get('leaf_function_name', []):
        methods_from_json.append(data_item['leaf_function_name'])
    if data_item.get('leaf_exception_name', []):
        methods_from_json.append(data_item['leaf_exception_name'])

code_file = []
# Provided code
with open('filter_code_2lib.jsonl', 'r', encoding='utf8') as f:
    for line in f:
        code_line = json.loads(line)
        code_file.append(code_line)
    # code_file = json.load(f)

filtered_API_doc_appended_code = []
for code_dict in tqdm(code_file):
    # Parse the provided code using ast to extract all the method calls.
    tree = ast.parse(code_dict['output'])
    visitor = MethodVisitor()
    visitor.visit(tree)

    # Compare the extracted method calls with the list from the JSON file.
    called_methods = set(visitor.methods) & set(methods_from_json)

    # print("Methods called from the JSON list:", called_methods)
    extracted_info = find_string_info(called_methods, flat_ref)
    if 'show' in extracted_info:
        filtered_API_doc_appended_code.append({
            # 'instruction': code_dict['instruction_annotation'],
            'code': code_dict['output'],
            'API info': extracted_info,
        })

with open('filtered_code_2lib_with_API_doc.json', 'w') as f:
    json.dump(filtered_API_doc_appended_code, f, indent=4)

'''for string, info in extracted_info.items():
    print(f"For string '{string}', found in key '{info['key']}':")
    print(info['info'])
    print("----------")'''