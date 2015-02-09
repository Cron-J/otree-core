"""Tags related to form rendering.

To load these in the template use {% load otree_tags %}."""

from django import template
from django.template.base import token_kwargs


class FormFieldNode(template.Node):
    """Render form fields in a template. It also contains helping mechanisms to
    define model forms in the template."""

    is_form_field_marker = True
    template_name = 'otree/forms/formfield.html'

    class Identifier(object):
        def __init__(self, variable, node):
            self.variable = variable
            self.node = node

        def __str__(self):
            return str(self.node)

        def __unicode__(self):
            return unicode(self.node)

        def is_valid(self):
            # The variable name is valid if it contains at least one dot.
            return '.' in self.variable

        def get_variable_name(self):
            return self.variable

        def get_instance_name(self):
            """Returns everything until the last dot.

            That will be the name of the variable which should contain the
            model instance.
            """
            return self.variable.split('.', -1)[0]

        def get_field_name(self):
            """Returns everything after the last dot.

            That will be the modelfield's name.
            """
            return self.variable.split('.', -1)[1]

    def __init__(self, tokens, variable, with_arguments):
        self.tokens = tokens
        self.identifiers = [self.Identifier(variable, self)]
        self.template = template.loader.get_template(self.template_name)
        self.with_arguments = with_arguments

    def get_identifiers(self):
        return self.identifiers

    def get_form_instance(self, context):
        return context['form']

    def get_bound_fields(self, context):
        form = self.get_form_instance(context)
        fields = []
        for identifier in self.get_identifiers():
            bound_field = form[identifier.get_field_name()]
            fields.append(bound_field)
        return fields

    def get_context(self, context):
        fields = self.get_bound_fields(context)
        extra_context = {
            'form': self.get_form_instance(context),
            'field': fields[0],
            'fields': fields,
        }
        with_context = dict([
            (name, var.resolve(context))
            for name, var in self.with_arguments.items()])
        extra_context.update(with_context)
        return context.new(extra_context)

    def render(self, context):
        field_context = self.get_context(context)
        return self.template.render(field_context)

    def get_tag_definition(self):
        tokens = ' '.join(self.tokens)
        return '{% ' + tokens + ' %}'

    @classmethod
    def parse(cls, parser, token):
        tokens = token.split_contents()
        bits = list(tokens)
        # That's the tag name (formfield).
        tagname = bits.pop(0)
        if len(bits) == 0:
            raise template.TemplateSyntaxError(
                "'{tagname}' tag expects at least one argument.".format(
                    tagname=tagname))
        variable = bits.pop(0)
        if variable == 'with':
            raise template.TemplateSyntaxError(
                "First argument of '{tagname}' tag must be a "
                "model field.".format(tagname=tagname))
        if bits:
            with_ = bits.pop(0)
            if with_ != 'with':
                raise template.TemplateSyntaxError(
                    "'{tagname}' tag must be in the form of "
                    "{{% {tagname} <model-field> "
                    "[with key=value key=value ...] %}}".format(
                        tagname=tagname))
            with_arguments = token_kwargs(bits, parser, support_legacy=False)
        else:
            with_arguments = {}
        return cls(tokens, variable, with_arguments)
