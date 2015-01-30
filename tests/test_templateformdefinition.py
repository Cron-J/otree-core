from django.core.management import call_command
from django.template import Template
from django.test import TestCase

from otree.forms.modelforms import FormDefinitionError
from otree.forms.modelforms import get_modelform_from_template
from otree.forms.modelforms import TemplateFormDefinition
import otree.db.models

from tests.simple_game.models import Player
from tests.utils import capture_stdout


class SimplePlayer(otree.db.models.Model):
    name = otree.db.models.CharField(max_length=50)
    age = otree.db.models.IntegerField(default=30)


class TemplateFormDefinitionTest(TestCase):
    def setUp(self):
        with capture_stdout():
            call_command('create_session', 'simple_game', 1)
        self.player = Player.objects.first()

    def get_template_nodes(self, source):
        return Template('{% load otree_tags %}' + source)

    def test_extract_form(self):
        template = self.get_template_nodes(
            '''
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

        player_name, player_age = form_helper.get_field_identifiers()
        self.assertEqual(player_name.variable, 'player.name')
        self.assertEqual(player_age.variable, 'player.age')
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

    def test_variable_syntax_error(self):
        template = self.get_template_nodes(
            '''
            {% formfield player..name %}
            ''')

        context = {}
        with self.assertRaises(FormDefinitionError) as cm:
            get_modelform_from_template(template, context)

        self.assertEqual(cm.exception.code, 'invalid_variable_format')

    def test_variable_contains_no_dot(self):
        template = self.get_template_nodes(
            '''
            {% formfield player %}
            ''')

        context = {}
        with self.assertRaises(FormDefinitionError) as cm:
            get_modelform_from_template(template, context)

        self.assertEqual(cm.exception.code, 'invalid_variable_format')

    def test_variable_not_in_context(self):
        template = self.get_template_nodes(
            '''
            {% formfield player.name %}
            ''')

        context = {}
        with self.assertRaises(FormDefinitionError) as cm:
            get_modelform_from_template(template, context)

        self.assertEqual(cm.exception.code, 'instance_not_found')

    def test_variable_is_not_a_model_instance(self):
        # TODO
        pass

    def test_variable_is_not_a_model_field(self):
        # TODO
        pass

    def test_variable_is_unsaved_model_instance(self):
        # TODO
        pass

    def test_multiple_model_instances(self):
        # TODO
        pass

    def test_multiple_model_instances(self):
        # TODO
        pass

    def test_formfield_tag_inside_if(self):
        # TODO
        pass

    def test_formfield_tag_inside_loop(self):
        # TODO
        pass
