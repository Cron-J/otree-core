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

    def __init__(self, tokens, identifier):
        self.tokens = tokens
        self.identifier = identifier

    def get_identifiers(self):
        return [self.identifier]

    def render(self, context):
        return 'field'

    def get_tag_definition(self):
        return '{% {tokens} %}'.format(tokens=' '.join(self.tokens))

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
