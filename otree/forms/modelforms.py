import collections

from django.template import loader
from django.template import Context
from django.template import RequestContext
from django.template import Variable
from django.utils import six

import otree.forms


FORM_FIELD_MARKER_ATTRIBUTE = 'is_form_field_marker'


class TemplateFormDefinition(object):
    def __init__(self, template_names, context, request=None,
                 current_app=None):
        self.template_names = template_names
        self.context_data = context
        self._request = request
        self._current_app = current_app

    def _bootstrap(self):
        self.template = self.resolve_template(self.template_names)
        self.context = self.resolve_context(self.context_data)
        self.field_identifiers = self.get_field_identifiers()

    def resolve_template(self, template):
        "Accepts a template object, path-to-template or list of paths"
        if isinstance(template, (list, tuple)):
            return loader.select_template(template)
        elif isinstance(template, six.string_types):
            return loader.get_template(template)
        else:
            return template

    def resolve_context(self, context):
        """Converts context data into a full ``Context`` object
        (assuming it isn't already a ``Context`` object). It might return a
        ``RequestContext`` if request was passed into ``__init__``.
        """
        if isinstance(context, Context):
            return context
        if self._request is not None:
            return RequestContext(self._request, context,
                                  current_app=self._current_app)
        return Context(context)

    def get_field_identifiers(self):
        identifiers = []
        remaining_nodes = collections.deque(self.template.nodelist)

        while remaining_nodes:
            node = remaining_nodes.popleft()
            if getattr(node, FORM_FIELD_MARKER_ATTRIBUTE, False):
                identifiers.extend(node.get_identifiers())
            if hasattr(node, 'child_nodelists'):
                for nodelist_attr in node.child_nodelists:
                    # There might be nodelist attributes that are in
                    # `child_nodelists` but not defined on the nodes. So we
                    # default to empty list.
                    nodelist = getattr(node, nodelist_attr, [])
                    remaining_nodes.extend(nodelist)

        return identifiers

    def get_model_instance(self):
        identifier = self.field_identifiers[0]
        variable_name, field_name = identifier.split('.', -1)
        variable = Variable(variable_name)
        return variable.resolve(self.context)

    def get_model_class(self):
        return self.get_model_instance().__class__

    def get_form_fields(self):
        fields = []
        for identifier in self.field_identifiers:
            variable_name, field_name = identifier.split('.', -1)
            fields.append(field_name)
        return fields

    def get_base_form_class(self):
        return otree.forms.ModelForm

    def get_form_class(self):
        self._bootstrap()
        form_class = otree.forms.modelform_factory(
            self.get_model_class(),
            fields=self.get_form_fields(),
            form=self.get_base_form_class(),
            formfield_callback=otree.forms.formfield_callback)
        return form_class


def get_modelform_from_template(template, context, request=None,
                                current_app=None):
    helper = TemplateFormDefinition(template, context, request=request,
                                    current_app=current_app)
    return helper.get_form_class()
