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
        email = self.cleaned_data.get("email")
        # Usaremos el email como username también
        if User.objects.filter(username=email).exists():
            raise ValidationError("Ya existe un usuario registrado con este correo.")
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
        """Crea el User y el Cliente asociado. Devuelve el user."""
        nombre = self.cleaned_data["nombre"]
        apellido = self.cleaned_data["apellido"]
        email = self.cleaned_data["email"]
        direccion = self.cleaned_data.get("direccion", "")
        telefono = self.cleaned_data.get("telefono", "")
        password = self.cleaned_data["password1"]

        # Usamos el email como username para no pedir username aparte
        user = User(
            username=email,
            email=email,
            first_name=nombre,
            last_name=apellido,
        )
        user.set_password(password)
        user.save()

        Cliente.objects.create(
            user=user,
            nombre=nombre,
            apellido=apellido,
            direccion=direccion,
            telefono=telefono,
        )

        return user
