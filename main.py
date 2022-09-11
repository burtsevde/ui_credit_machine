import json
import webbrowser
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup

# тестовый json schema
# тестовый набор данных под схему
# тестовый json | yaml для описания UI
class UI:
    def __init__(self, json_schema: str, data: str, ui_yaml: str):
        self.json_schema = json.load(open(json_schema, 'r', encoding="utf-8"))
        self.data = json.load(open(data, 'r', encoding="utf-8"))
        self.ui_yaml = yaml.safe_load(open(ui_yaml, 'r', encoding="utf-8"))
        self.ui_json = ''

    def conver_yaml_to_json(self):
        self.ui_json = json.dumps(self.ui_yaml)

    def validate(self):
        from jsonschema import validate
        return validate(self.data, self.json_schema)

    def get_content(self) -> str:
        import markdown
        from markdown.extensions.tables import TableExtension
        from bs4 import BeautifulSoup
        extensions = [TableExtension(use_align_attribute=True)]
        soup = BeautifulSoup()
        # изучаем ui_layout
        for item in self.ui_yaml:
            div = BeautifulSoup().new_tag('div')

            if self.ui_yaml[item]['type'] == 'form':
                soup.append(Form(self.ui_yaml[item]).get_form())
                continue

            div['name'] = item
            div['id'] = self.ui_yaml[item]['id']
            div['class'] = self.ui_yaml[item]['class']

            description = self.ui_yaml[item]['description'] if 'description' in self.ui_yaml[item] else ''
            html = markdown.markdown(description, extensions=extensions)
            div.append(BeautifulSoup(html))

            soup.append(div)

        return str(soup)



if __name__ == '__main__':
    ui_test = UI(json_schema=Path('data/json_schema.json'),
                 data=Path('data/data.json'),
                 ui_yaml=Path('data/ui_layout.yaml'))

    env = Environment(loader=FileSystemLoader('./template'))
    template = env.get_template('baseTamplate.html')

    with open('./template/test_template.html', 'w', encoding='utf-8') as f:
        f.write(template.render(content=ui_test.get_content()))

    webbrowser.open('test_template.html')

    print('Done!')