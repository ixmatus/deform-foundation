import colander
import deform.widget
import sys
import types

from pyramid.threadlocal import get_current_request
from pkg_resources import resource_filename
from deform import Form
from pyramid.i18n import get_localizer

from .resources import default_resources

PY3 = sys.version_info[0] == 3

if PY3: # pragma: no cover
    string_types = str,
    integer_types = int,
    class_types = type,
    text_type = str
    binary_type = bytes
    long = int
else:
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str
    long = long

@colander.deferred
def deferred_csrf_value(node, kw):
    return kw['request'].session.get_csrf_token().decode()

@colander.deferred
def deferred_csrf_validator(node, kw):
    def csrf_validate(node, value):
        if value != kw['request'].session.get_csrf_token().decode():
            raise colander.Invalid(node, 'Invalid cross-site scripting token')
    return csrf_validate

class CSRFSchema(colander.Schema):
    """
    Schema base class which generates and validates a CSRF token
    automatically.  You must use it like so:

    .. code-block:: python

      from pyramid_deform import CSRFSchema
      import colander

      class MySchema(CRSFSchema):
          my_value = colander.SchemaNode(colander.String())

      And in your application code, *bind* the schema, passing the request
      as a keyword argument:

      .. code-block:: python

        def aview(request):
            schema = MySchema().bind(request=request)

      In order for the CRSFSchema to work, you must configure a *session
      factory* in your Pyramid application.
    """
    csrf_token = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget(),
        default=deferred_csrf_value,
        validator=deferred_csrf_validator,
        )

def add_resources_to_registry():
    """Register deform_foundation widget specific requirements to
       deform's default resource registry
    """
    registry = Form.default_resource_registry
    for rqrt, versions in default_resources.items():
        for version, resources in versions.items():
            registry.set_js_resources(rqrt, version, resources.get('js'))
            registry.set_css_resources(rqrt, version, resources.get('css'))

def translator(term):
    request = get_current_request()
    if request is not None:
        return get_localizer(request).translate(term)
    else:
        return term.interpolate() if hasattr(term, 'interpolate') else term

def configure_zpt_renderer(search_path=()):
    default_paths = deform.form.Form.default_renderer.loader.search_path
    paths = []
    for path in search_path:
        pkg, resource_name = path.split(':')
        paths.append(resource_filename(pkg, resource_name))
    deform.form.Form.default_renderer = deform.ZPTRendererFactory(
        tuple(paths) + default_paths, translator=translator)

def includeme(config):
    configure_zpt_renderer(('deform_foundation:templates',))
    
    add_resources_to_registry()
    
    config.add_translation_dirs('colander:locale', 'deform:locale')
    config.add_static_view('static-deform_foundation', 'deform_foundation:static')
