"""Tags related to form rendering.

To load these in the template use {% load otree_tags %}."""
from django import template


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

    def __init__(self, tokens, variable):
        self.tokens = tokens
        self.identifiers = [self.Identifier(variable, self)]
        self.template = template.loader.get_template(self.template_name)

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
        return context.new({
            'form': self.get_form_instance(context),
            'field': fields[0],
            'fields': fields,
        })

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
        bits.pop(0)
        if len(bits) != 1:
            raise template.TemplateSyntaxError(
                "%r tag expects one argument only")
        variable = bits.pop(0)
        return cls(tokens, variable)
