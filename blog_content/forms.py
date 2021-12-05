from django.forms import ModelForm
from .models import Comentaries
import re


class FormComentario(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormComentario, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2'
            visible.field.widget.attrs['style'] = 'resize: none;'

    def Clean(self):
        cleaned_data = self.cleaned_data
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        title = cleaned_data.get('comment_title')
        message = cleaned_data.get('message')

        if len(name) < 5:
            self.add_error(
                'name',
                'Nome precisa ter mais do que 5 carácteres.'
            )

        if len(title) < 5:
            self.add_error(
                'title',
                'Título precisa ter mais do que 5 carácteres.'
            )

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if not (re.match(regex, email)):
            self.add_error(
                'email',
                'E-mail inválido.'
            )

        if message == '':
            self.add_error(
                'message',
                'Campo comentário não pode ficar vazio.'
            )

    class Meta:
        model = Comentaries
        fields = ('name', 'email', 'comment_title', 'message')
