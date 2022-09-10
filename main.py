import json
import webbrowser
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader


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
        from bs4 import BeautifulSoup
        soup = BeautifulSoup()
        # изучаем ui_layout
        for item in self.ui_yaml:

            soup.append('<p>asd</p>')

        html = markdown.markdown('string', output_format='html')

        return soup


if __name__ == '__main__':
    ui_test = UI(json_schema=Path('data/json_schema.json'),
                 data=Path('data/data.json'),
                 ui_yaml=Path('data/ui_layout.yaml'))

    env = Environment(loader=FileSystemLoader('./template'))
    # template = env.get_template('DocVeriosn_-4591224837923658569.html')
    template = env.get_template('baseTamlate.html')

    with open('test_template.html', 'w', encoding='utf-8') as f:
        f.write(template.render(ui_test.get_content()))

    webbrowser.open('test_template.html')

    print('Done!')