"""Testing the {% formfield %} template tag. The bits of {% formfield %} that
are related to defining forms in templates forms are contained in
`tests.test_templateformdefinition`."""

from django.test import TestCase
from django.template import Context

from otree.forms.modelforms import TemplateFormDefinition

from .test_templateformdefinition import FormDefinitionTestMixin


class TemplateFormRenderingTest(FormDefinitionTestMixin, TestCase):
    def test_fields_are_displayed(self):
        template = self.get_template_nodes(
            '''
            {% formfield player.name %}
            ''')

        context = Context({'player': self.SimplePlayer(name='initial')})

        definition = TemplateFormDefinition(template, context)
        form = definition.get_form()
        definition.apply_to_context(context, form)

        # We use the formfield.html as entry point.
        with self.assertTemplateUsed('otree/forms/formfield.html'):
            rendered = template.render(context)

        self.assertTrue('<input' in rendered, rendered)
        self.assertTrue('name="name"' in rendered, rendered)
        self.assertTrue('value="initial"' in rendered, rendered)

    def test_custom_labels(self):
        template = self.get_template_nodes(
            '''
            {% formfield player.name with label="My custom label" %}
            ''')

        context = Context({'player': self.SimplePlayer(name='initial')})

        definition = TemplateFormDefinition(template, context)
        form = definition.get_form()
        definition.apply_to_context(context, form)

        rendered = template.render(context)
        self.assertInHTML(
            '<label for="id_name">My custom label:</label>',
            rendered)
