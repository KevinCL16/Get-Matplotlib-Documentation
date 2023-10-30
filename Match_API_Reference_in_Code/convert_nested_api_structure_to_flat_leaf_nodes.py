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
                leaf_cls_name = cls_name.split('.')[-1].split('(')[0]
                flattened.append({
                    'name': cls_name,
                    'leaf_class_name': leaf_cls_name,
                    'text': cls['class text']
                })
                class_name = cls['class name'].split("(")[0].strip().replace('class ', '')
            for method in cls.get('class method', []):
                method_name = method['method name']
                full_name = f"{class_name}.{method_name}"
                leaf_method_name = full_name.split('.')[-1].split('(')[0]
                flattened.append({
                    'name': full_name,
                    'leaf_method_name': leaf_method_name,
                    'text': method['method text']
                })

            # If 'class property' and 'class attribute' exist, you can handle them similarly:
            for prop in cls.get('class property', []):
                prop_name = prop['property name'].replace('property ', '').strip('#')
                full_name = f"{class_name}.{prop_name}"
                leaf_property_name = full_name.split('.')[-1].split('(')[0]
                flattened.append({
                    'name': full_name,
                    'leaf_property_name': leaf_property_name,
                    'text': prop['property text']
                })

            for attr in cls.get('class attribute', []):
                attr_name = attr['attribute name']
                full_name = f"{class_name}.{attr_name}"
                leaf_attribute_name = full_name.split('.')[-1].split('(')[0]
                flattened.append({
                    'name': full_name,
                    'leaf_attribute_name': leaf_attribute_name,
                    'text': attr['attribute text']
                })

        for func in data_item.get('function', []):
            func_name = func['function name']
            full_name = f"{func_name}"
            leaf_function_name = full_name.split('.')[-1].split('(')[0]
            flattened.append({
                'name': full_name,
                'leaf_function_name': leaf_function_name,
                'text': func['function text']
            })

        for exc in data_item.get('exception', []):
            exc_name = exc['exception name']
            full_name = f"{exc_name}"
            leaf_exception_name = full_name.split('.')[-1].split('(')[0]
            flattened.append({
                'name': full_name,
                'leaf_exception_name': leaf_exception_name,
                'text': exc['exception text']
            })

    return flattened


flattened_data = flatten_module(data)

# Saving the flattened data to a JSON file
with open('flattened_API_reference.json', 'w') as f:
    json.dump(flattened_data, f, indent=4)
