from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='E-mail')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
          {'class': 'input'}
        )
        self.fields['password'].widget.attrs.update(
          {'class': 'input'}
        )


class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(
                                    attrs={
                                        "multiple": True,
                                        "id": "realFileUpload",
                                    }))

class UploadDocForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(
                                    attrs={
                                    }))

    filetype = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['file'].widget.attrs.update({
                "class": "realDocUpload realDocBrowse",
            })


        self.fields['filetype'].widget.attrs.update({
                'class': "realDocUpload realDocValue",
            })

