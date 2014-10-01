from .models import InvalidAnswer


class InvalidAnswerModelFormMixin(object):
    def record_invalid_answers(self, user=None):
        if self.errors:
            for field_name, errors in self.errors.items():
                for error in errors:
                    self.add_invalid_answer(field_name, error, user=user)

    def get_invalid_value(self, field_name):
        return self.data.get(field_name, None)

    def add_invalid_answer(self, field_name, error, user=None):
        invalid_answer = InvalidAnswer(
            field_name=field_name,
            value=self.get_invalid_value(field_name),
            error_message=error)
        if user and user.pk:
            invalid_answer.player = user
        if self.instance.pk is not None:
            invalid_answer.content_object = self.instance
        invalid_answer.save()
