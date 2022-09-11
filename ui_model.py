from bs4 import BeautifulSoup

class Form:
    def __init__(self, input_form):
        self.form = input_form

    def get_form(self):
        form = BeautifulSoup().new_tag('form')
        form['class'] = self.form['class']

        for item in self.form['fields']:
            html = self.get_field(self.form['fields'][item])
            form.append(html)

        return form

    def get_field(self, field) -> BeautifulSoup:
        div = BeautifulSoup().new_tag('div')
        div['class'] = field['class']

        label = BeautifulSoup().new_tag('label')
        label['for'] = field['id']
        label['class'] = "form-label"
        label.string = field['label']

        _input = BeautifulSoup().new_tag('input')
        _input['type'] = field['type']
        _input['class'] = "form-control"
        _input['id'] = field['id']

        div.append(label)
        div.append(_input)
        return div