import json

with open('../crawled_examples/crawled_API_reference_raw.json', 'r') as f:
    data = json.load(f)


def flatten_module(data):
    flattened = []
    for data_item in data:
        module_name = data_item.get('module name')
        for cls in data_item.get('class', []):
            if cls.get('class name', []):
                cls_name = cls['class name'].replace('class ', '')
                flattened.append({
                    'name': cls_name,
                    'text': cls['class text']
                })
                class_name = cls['class name'].split("(")[0].strip().replace('class ', '')
            for method in cls.get('class method', []):
                method_name = method['method name']
                full_name = f"{class_name}.{method_name}"
                flattened.append({
                    'name': full_name,
                    'text': method['method text']
                })

            # If 'class property' and 'class attribute' exist, you can handle them similarly:
            for prop in cls.get('class property', []):
                prop_name = prop['property name'].replace('property ', '')
                full_name = f"{class_name}.{prop_name}"
                flattened.append({
                    'name': full_name,
                    'text': prop['property text']
                })

            for attr in cls.get('class attribute', []):
                attr_name = attr['attribute name']
                full_name = f"{class_name}.{attr_name}"
                flattened.append({
                    'name': full_name,
                    'text': attr['attribute text']
                })

        for func in data_item.get('function', []):
            func_name = func['function name']
            full_name = f"{module_name}.{func_name}"
            flattened.append({
                'name': full_name,
                'text': func['function text']
            })

        for exc in data_item.get('exception', []):
            exc_name = exc['exception name']
            full_name = f"{module_name}.{exc_name}"
            flattened.append({
                'name': full_name,
                'text': exc['exception text']
            })

    return flattened


flattened_data = flatten_module(data)

# Saving the flattened data to a JSON file
with open('flattened_API_reference.json', 'w') as f:
    json.dump(flattened_data, f, indent=4)
