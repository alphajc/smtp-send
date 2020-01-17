import os
import json
from jinja2 import Template

class Tools:
    @staticmethod
    def render(template, meta_json):
        with open(template, 'r') as f:
            tpl = Template(f.read())
        with open(meta_json, 'r') as f:
            metadata = json.loads(f.read())
        configmaps = metadata['configmaps']
        model = dict(zip(configmaps.keys(), map(lambda v: os.environ.get(v), configmaps.values())))
        return tpl.render(**model)