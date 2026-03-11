import json


class TemplateLoader:

    def __init__(self, template_file="templates.json"):

        self.template_file = template_file

    def load(self):

        with open(self.template_file) as f:
            return json.load(f)