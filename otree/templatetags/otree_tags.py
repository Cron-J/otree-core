#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# DOCS
# =============================================================================

"""Template tags to for the otree template users.

"""


# =============================================================================
# IMPORTS
# =============================================================================

from django import template
from django.template.loader import render_to_string
from otree.common import Currency

# =============================================================================
# CONSTANTS
# =============================================================================

register = template.Library()


# =============================================================================
# TAGS
# =============================================================================

class NextButtonNode(template.Node):
    def render(self, context):
        context.update({})
        try:
            return render_to_string('otree/NextButton.html', context)
        finally:
            context.pop()

    @classmethod
    def parse(cls, parser, tokens):
        return cls()


register.tag('next_button', NextButtonNode.parse)


def c(val):
    return Currency(val)


register.filter('c', c)


# =============================================================================
# FORM DEFINITION TAGS
# =============================================================================

class FormFieldNode(template.Node):
    is_form_field_marker = True

    # TODO: Provide actual rendering during output phase.

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

    def __init__(self, tokens, identifier):
        self.tokens = tokens
        self.identifiers = [self.Identifier(identifier, self)]

    def get_identifiers(self):
        return self.identifiers

    def render(self, context):
        return 'field'

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
        identifier = bits.pop(0)
        return cls(tokens, identifier)


register.tag('formfield', FormFieldNode.parse)
