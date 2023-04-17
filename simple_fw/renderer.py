import os
from jinja2 import Template


def render(template_name, folder="templates", **kwargs):
    """
    Args:
        template_name (_type_): Template name
        folder (str, optional): Folder of templates. Defaults to "templates".
    """
    file_path = os.path.join(folder, template_name)
    with open(file_path, encoding="utf-8") as f:
        template = Template(f.read())

    return template.render(**kwargs)