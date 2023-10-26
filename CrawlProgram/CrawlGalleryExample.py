from bs4 import BeautifulSoup
import requests
import json

json_file_path = '../crawled_links/crawled_gallery_links.json'

with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

gallery_example = []
i, idx = 0, 0
for entry in data[i:536]:
    url = entry['url']
    r = requests.get(url)  # Demo网址
    demo = r.text

    each_gallery_example = {}
    soup = BeautifulSoup(demo, "html.parser")
    element = soup.find('section', class_='sphx-glr-example-title')
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
            each_gallery_example.update({'h1': heading.text.strip('#')})
        if heading.name == 'p':
            text_buffer.append(heading.text)
        if heading.name == 'pre':
            # each_gallery_example.update({"text" + str(i): text_buffer})
            # each_gallery_example.update({'code' + str(i): heading.text})
            code_buffer.append(heading.text)

    if len(code_buffer) > 1:
        print("Progress: " + str(i))
        i = i + 1
        continue
    else:
        each_gallery_example.update({"text": str(text_buffer)[:str(text_buffer).find("Download") - 4].replace('\\n', '\n').strip("['").strip("']").replace(
            "', '", ' ').replace('[\"', '').replace('\"]', '').strip('\"')})
        each_gallery_example.update({'code': str(code_buffer).replace('\\n', '\n').strip("['").strip("']").strip('\"').replace(
            "', '", ' ').replace("\\'", "'").replace('\\"', '"').replace('\"', "'")})
        each_gallery_example.update({'id': idx})
        idx += 1

    with open('../crawled_examples/crawled_gallery_examples_1_code_block_url_links.json', 'a') as json_file:
        json_obj = json.dumps({"gallery_example_url_link": url}, indent=4) + ',\n'
        json_file.write(json_obj)
    print("Progress: " + str(i))
    i = i + 1
