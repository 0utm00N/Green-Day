from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Cliente

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'direccion']  # ajusta según tus campos



class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=50, label="Nombre")
    apellido = forms.CharField(max_length=50, label="Apellido")
    email = forms.EmailField(label="Correo electrónico")
    direccion = forms.CharField(
        max_length=200,
        label="Dirección",
        required=False
    )
    telefono = forms.CharField(
        max_length=20,
        label="Teléfono",
        required=False
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Repetir contraseña",
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: clases CSS para que se vea parecido a tu login
        for field in self.fields.values():
            field.widget.attrs["class"] = "auth-input"  # cámbialo si usas otra clase
            field.widget.attrs["autocomplete"] = "off"

    def clean_email(self):
        email = self.cleaned_data.get("email").lower().strip()

        # Normalizar correo
        email = email.lower().strip()

        # Revisar si existe un usuario con ese username
        if User.objects.filter(username=email).exists():
            raise ValidationError("Ya existe un usuario registrado con este correo.")

        # Revisar si existe un Cliente asociado a ese email
        if Cliente.objects.filter(user__username=email).exists():
            raise ValidationError("Este usuario ya tiene un perfil registrado.")

        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")

        if p1 and len(p1) < 8:
            self.add_error("password1", "La contraseña debe tener al menos 8 caracteres.")

        return cleaned_data

    def save(self):
        cleaned = self.cleaned_data

        user = User.objects.create_user(
            username=cleaned["email"].lower().strip(),
            email=cleaned["email"],
            password=cleaned["password1"],
            first_name=cleaned["nombre"],
            last_name=cleaned["apellido"],
        )

        Cliente.objects.create(
            user=user,
            nombre=cleaned["nombre"],
            apellido=cleaned["apellido"],
            direccion=cleaned.get("direccion") or "",
            telefono=cleaned.get("telefono") or "",
        )

        return user

