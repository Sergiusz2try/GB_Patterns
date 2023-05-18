from jinja2 import Environment, FileSystemLoader


def render(template_name, folder="templates", **kwargs):
    """
    Args:
        template_name (_type_): Template name
        folder (str, optional): Folder of templates. Defaults to "templates".
    """
    env = Environment()

    env.loader = FileSystemLoader(folder)

    template = env.get_template(template_name)

    return template.render(**kwargs)