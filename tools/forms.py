from django.forms import ModelForm,Textarea
from tools.models import blastModel

class blastForm(ModelForm):
    class Meta:
        model = blastModel
        widgets = {
            'querySeq': Textarea(attrs={'cols': 80, 'rows': 8}),
        }
