# coding: utf-8
import tempfile
from os.path import join

from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.backends.base import BaseEngine
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from mako import exceptions as mako_exceptions
from mako.template import Template as MakoTemplate


class MakoTemplates(BaseEngine):
    """
    Mako template backend

    :see: https://docs.djangoproject.com/fr/dev/topics/templates/#custom-backends
    :see: https://github.com/django/deps/blob/master/final/0182-multiple-template-engines.rst
    Template OPTIONS info can contain :class:`mako.Lookup.TemplateLookup` __init__ args
    as dictionary entries.
    """

    app_dirname = 'mako'
    base_template_context = {}

    def __init__(self, params):
        """
        Initializer

        :param params:
            Contents of the backend dict in the TEMPLATES setting.
            Contains DIRS, BACKEND, OPTIONS and APP_DIRS keys (at least)
        """
        params = params.copy()
        options = params.pop('OPTIONS').copy()
        super(MakoTemplates, self).__init__(params)

        environment = options.pop('environment', 'mako.lookup.TemplateLookup')
        environment_cls = import_string(environment)

        # Defaut values for initializing the TemplateLookup class
        # You can define them in the backend OPTIONS dict.
        options.setdefault('collection_size', 5000)
        options.setdefault('module_directory', tempfile.gettempdir())
        options.setdefault('output_encoding', 'utf-8')
        options.setdefault('input_encoding', 'utf-8')
        options.setdefault('encoding_errors', 'replace')
        options.setdefault('filesystem_checks', True)
        options.setdefault('directories', self.template_dirs)

        # Use context processors like Django
        context_processors = options.pop('context_processors', [])
        self.context_processors = context_processors

        # Use the configured mako template lookup class to find templates
        self.lookup = environment_cls(**options)

    @cached_property
    def template_context_processors(self):
        """ Return a tuple of the actual context processor callables """
        context_processors = tuple(self.context_processors)
        return tuple(import_string(path) for path in context_processors)

    def from_string(self, template_code):
        """ Return a template object containing the backend template and information """
        try:
            return Template(MakoTemplate(template_code, lookup=self.lookup))
        except mako_exceptions.SyntaxException as exc:
            raise TemplateSyntaxError(exc.args)

    def get_template(self, template_name):
        """ Return a template object with a found Mako template """
        try:
            # Try to initialize a Template object with a found mako template
            template = Template(self.lookup.get_template(template_name), self.template_context_processors)
            return template
        except mako_exceptions.TemplateLookupException as exc:
            tried = [(DebugInfo(join(directory, template_name), template_name), "not found") for directory in self.lookup.directories]
            raise TemplateDoesNotExist(exc.args, backend=self, tried=tried)
        except mako_exceptions.CompileException as exc:
            raise TemplateSyntaxError(exc.args)


class DebugInfo(object):
    """ A container to hold debug information as described in the template API documentation. """

    def __init__(self, name, template_name):
        self.name = name
        self.template_name = template_name


class Template(object):
    """
    Template information.

    It could have any name, but Django requires it to have the following attributes:
    - template (which is always a MakoTemplate here)
    - origin: an object with <name> and <template_name> for debug purposes
    - render(context, request)
    """

    def __init__(self, template, context_processors):
        """ Initializer """
        self.template = template
        self.origin = DebugInfo(name=template.filename, template_name=template.uri)
        self.context_processors = context_processors

    def render(self, context=None, request=None):
        """ Render the template """
        output_context = context or dict()
        output_context.update(MakoTemplates.base_template_context)

        if request is not None:
            for processor in self.context_processors:
                # noinspection PyBroadException
                try:
                    output_context.update(processor(request))
                except Exception:
                    pass

        if request is not None:
            output_context['request'] = request
            output_context['csrf_input'] = csrf_input_lazy(request)
            output_context['csrf_token'] = csrf_token_lazy(request)

        return self.template.render(**output_context)
