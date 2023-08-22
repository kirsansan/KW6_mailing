from django import forms

from main.models import MailingList, MailingMessage


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-container'
            else:
                field.widget.attrs['class'] = 'form-control'


class MailingListCreationForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingList
        # fields = '__all__'
        exclude = ('creator',)

    def clean_finish(self):
        finish = self.cleaned_data['finish']
        start = self.cleaned_data['start']
        if start > finish:
            raise forms.ValidationError('Attention! Finish time cannot be less then start')
        if start == finish:
            raise forms.ValidationError('Attention! Finish time need to be more then start at least 5 min')

        return finish


class MessageCreationForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingMessage
        exclude = ('creator',)
