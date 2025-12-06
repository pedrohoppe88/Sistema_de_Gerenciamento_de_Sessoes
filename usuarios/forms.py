from django import forms
from .models import Usuario, Sessao
from django.contrib.auth.hashers import make_password

class UsuarioForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)
    pin = forms.CharField(max_length=4, min_length=4, widget=forms.PasswordInput(), label="PIN (4 dígitos)", required=True)
    pin_confirm = forms.CharField(max_length=4, min_length=4, widget=forms.PasswordInput(), label="Confirmar PIN", required=True)

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha', 'graduacao']

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get('pin')
        pin_confirm = cleaned_data.get('pin_confirm')
        if pin and pin_confirm and pin != pin_confirm:
            raise forms.ValidationError("Os PINs não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        # Hash da senha antes de salvar
        usuario.senha = make_password(self.cleaned_data['senha'])
        # Salvar PIN se fornecido
        if self.cleaned_data.get('pin'):
            usuario.pin = self.cleaned_data['pin']
        if commit:
            usuario.save()
        return usuario


class LoginForm(forms.Form):
    email = forms.EmailField(label="E-mail")
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)
    
class UsuarioEditForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Deixe em branco para manter a senha atual")
    pin = forms.CharField(max_length=4, min_length=4, widget=forms.PasswordInput(), label="PIN (4 dígitos)", required=False, help_text="Deixe em branco para manter o PIN atual")

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'graduacao', 'is_admin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Se estamos editando, tornar senha e PIN opcionais
            self.fields['senha'].required = False
            self.fields['senha'].help_text = "Deixe em branco para manter a senha atual"
            self.fields['pin'].required = False
            self.fields['pin'].help_text = "Deixe em branco para manter o PIN atual"

    def save(self, commit=True):
        usuario = super().save(commit=False)
        # Só hash a senha se foi fornecida
        if self.cleaned_data.get('senha'):
            usuario.senha = make_password(self.cleaned_data['senha'])
        # Salvar PIN se fornecido
        if self.cleaned_data.get('pin'):
            usuario.pin = self.cleaned_data['pin']
        if commit:
            usuario.save()
        return usuario


class SessaoForm(forms.ModelForm):
    class Meta:
        model = Sessao
        fields = ['nome', 'senha']

    def saveSessao(self, criador):
        sessao = Sessao.objects.create(
            nome=self.cleaned_data['nome'],
            senha=self.cleaned_data['senha'],
            criador=criador
        )
        return sessao
