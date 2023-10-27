import requests
from bs4 import BeautifulSoup
import json

link_file_path = '../crawled_links/crawled_api_reference_links.json'

with open(link_file_path, 'r') as json_file:
    link = json.load(json_file)

i, idx = 410, 0
for entry in link[i:940]:
    url = entry['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting the main title
    title = soup.select_one('h1').text

    # Extracting the class definition and description
    class_text = []
    func_text = []
    except_text = []
    method_text = []
    property_text = []
    attribute_text = []

    all_targets = soup.select('dl.py')
    all_targets_list = [elem for elem in all_targets]
    iter_all_targets = iter(all_targets_list)
    filtered_targets = [elem for elem in all_targets if not elem.find_parent(attrs={"class": 'py'}, recursive=False)]

    for item in filtered_targets:
        if item.attrs['class'][1] == 'class':
            method_text = []
            property_text = []
            attribute_text = []

            c_text = item.contents[3].text
            class_dict = {
                'class name': item.contents[1].text.replace('[source]#', '').strip('\n'),
                'class text': c_text

            }
            class_text.append(class_dict)

            methods_attributes_in_class = item.select('dl.py')
            for it in methods_attributes_in_class:
                if it.attrs['class'][1] == 'function':
                    class_dict = {
                        'function name': it.contents[1].text.replace('[source]#', '').strip('\n'),
                        'function text': it.contents[3].text
                    }
                    func_text.append(class_dict)

                elif it.attrs['class'][1] == 'exception':
                    class_dict = {
                        'exception name': it.contents[1].text.replace('[source]#', '').strip('\n'),
                        'exception text': it.contents[3].text
                    }
                    except_text.append(class_dict)

                elif it.attrs['class'][1] == 'method':
                    class_dict = {
                        'method name': it.contents[1].text.replace('[source]#', '').strip('\n'),
                        'method text': it.contents[3].text
                    }
                    method_text.append(class_dict)
                    class_text[-1].update({'class method': method_text})

                elif it.attrs['class'][1] == 'property':
                    class_dict = {
                        'property name': it.contents[1].text.replace('[source]#', '').strip('\n'),
                        'property text': it.contents[3].text
                    }
                    property_text.append(class_dict)
                    class_text[-1].update({'class property': property_text})

                elif it.attrs['class'][1] == 'attribute':
                    class_dict = {
                        'attribute name': it.contents[1].text.replace('#', '').strip('\n'),
                        'attribute text': it.contents[3].text
                    }
                    attribute_text.append(class_dict)
                    class_text[-1].update({'class attribute': attribute_text})

        elif item.attrs['class'][1] == 'function':
            class_dict = {
                'function name': item.contents[1].text.replace('[source]#', '').strip('\n'),
                'function text': item.contents[3].text
            }
            func_text.append(class_dict)

        elif item.attrs['class'][1] == 'exception':
            class_dict = {
                'exception name': item.contents[1].text.replace('[source]#', '').strip('\n'),
                'exception text': item.contents[3].text
            }
            except_text.append(class_dict)

        elif item.attrs['class'][1] == 'method':
            class_dict = {
                'method name': item.contents[1].text.replace('[source]#', '').strip('\n'),
                'method text': item.contents[3].text
            }
            method_text.append(class_dict)
            class_text = [{'class method': method_text}]

        elif item.attrs['class'][1] == 'property':
            class_dict = {
                'property name': item.contents[1].text.replace('[source]#', '').strip('\n'),
                'property text': item.contents[3].text
            }
            property_text.append(class_dict)
            class_text = [{'class property': property_text}]

        elif item.attrs['class'][1] == 'attribute':
            class_dict = {
                'attribute name': item.contents[1].text.replace('#', '').strip('\n'),
                'attribute text': item.contents[3].text
            }
            attribute_text.append(class_dict)
            class_text = [{'class attribute': attribute_text}]

    # Storing the scraped data in a dictionary
    data = {
        'module name': title.strip('#'),
        'class': class_text,
        'function': func_text,
        'exception': except_text
    }

    with open('../crawled_examples/crawled_API_reference_raw.json', 'a') as json_file:
        json_obj = json.dumps(data, indent=4) + ',\n'
        json_file.write(json_obj)

    print("Progress: " + str(i))
    i = i + 1



