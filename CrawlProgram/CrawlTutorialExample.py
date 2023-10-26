from bs4 import BeautifulSoup
import requests
import json

json_file_path = '../crawled_links/crawled_tutorial_links.json'

with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

gallery_example = []
i, idx = 0, 0
for entry in data[i:54]:
    url = entry['url']
    r = requests.get(url)  # Demo网址
    demo = r.text

    each_gallery_example = {}
    soup = BeautifulSoup(demo, "html.parser")
    element = soup.find('article', class_='bd-article')
    try:
        headings = element.find_all(['h1', 'h2', 'h3', 'p', 'pre'])
    except AttributeError:
        print("Progress: " + str(i))
        i = i + 1
        continue

    text_buffer = []
    code_buffer = []
    for heading in headings:
        if heading.name == 'h1':
            text_buffer.append({'h1': heading.text.strip('#')})
        if heading.name == 'h2':
            text_buffer.append({'h2': heading.text.strip('#')})
        if heading.name == 'h3':
            text_buffer.append({'h3': heading.text.strip('#')})
        if heading.name == 'p':
            text_buffer.append({'text': heading.text})
        if heading.name == 'pre':
            # each_gallery_example.update({"text" + str(i): text_buffer})
            # each_gallery_example.update({'code' + str(i): heading.text})
            text_buffer.append({'code': heading.text})

    if text_buffer[0].__contains__('text'):
        text_buffer = text_buffer[2:]
    each_gallery_example.update({"raw_page": str(text_buffer).replace('\\n', '\n').strip("['").strip("']").replace(
            "', '", ' ').replace('[\"', '').replace('\"]', '').strip('\"').replace("\\'", "'").replace('\\"', '"').replace('\"', "'")})

    each_gallery_example.update({'id': idx})
    idx += 1

    with open('../crawled_examples/crawled_tutorial_raw_data.json', 'a') as json_file:
        json_obj = json.dumps(each_gallery_example, indent=4) + ',\n'
        json_file.write(json_obj)
    print("Progress: " + str(i))
    i = i + 1
