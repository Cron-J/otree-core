from django.template import Template
from django.test import TestCase

from otree.forms.modelforms import TemplateFormDefinition
import otree.db.models


class SimplePlayer(otree.db.models.Model):
    name = otree.db.models.CharField(max_length=50)
    age = otree.db.models.IntegerField(default=30)


class TemplateFormDefinitionTest(TestCase):
    def test_extract_form(self):
        template = Template(
            '''
            {% load otree_tags %}

            {% formfield player.name %}
            {% if true_value %}
                {% formfield player.age %}
            {% endif %}
            ''')

        instance = SimplePlayer.objects.create(name='Foo', age=20)
        context = {
            'player': instance,
            'true_value': True
        }

        form_helper = TemplateFormDefinition(template, context)
        form_helper._bootstrap()

        self.assertEqual(form_helper.get_field_identifiers(),
                         ['player.name', 'player.age'])
        self.assertEqual(form_helper.get_model_class(), SimplePlayer)
        self.assertEqual(form_helper.get_model_instance(), instance)

        modelform = form_helper.get_form_class()

        self.assertEqual(modelform._meta.model, SimplePlayer)
        self.assertEqual(len(modelform.base_fields), 2)
        self.assertEqual(modelform.base_fields.keys(), ['name', 'age'])

        name_field = modelform.base_fields['name']
        age_field = modelform.base_fields['age']

        self.assertEqual(name_field.__class__, otree.forms.CharField)
        self.assertEqual(age_field.__class__, otree.forms.IntegerField)
