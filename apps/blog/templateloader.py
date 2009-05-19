theme_template_dirs = None

def load_template_source(template_name, template_dirs=None):
    """ Configurable template directories for custom theme templates.
    Just set the theme_template_dirs during the request.
    """
    if template_dirs is None:
        template_dirs = theme_template_dirs
    from django.template.loaders.filesystem import load_template_source
    return load_template_source(template_name, template_dirs)
load_template_source.is_usable = True