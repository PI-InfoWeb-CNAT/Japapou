from django import forms # type: ignore
from japapou.models import Menu, Plate
from japapou.models.user import CustomUser
from django.contrib.auth.forms import UserCreationForm


class PlatesForms(forms.ModelForm):
    """
    Formulário para a classe Plate.
    """

    # Adicionamos o campo 'menus' explicitamente aqui,
    # pois ele não está diretamente na Model Plate, mas queremos exibi-lo.
    menus = forms.ModelMultipleChoiceField(
        queryset=Menu.objects.all(),  # Todos os objetos Menu disponíveis para seleção
        widget=forms.SelectMultiple(
            attrs={"class": "seu-estilo-css"}
        ),  # Adicione suas classes CSS
        required=False,  # Defina como True se a seleção de menus for obrigatória
        label="Menus Associados",  # Rótulo que aparecerá no formulário
    )

    class Meta:
        model = Plate
        # ATENÇÃO: 'menus' NÃO pode estar nos 'fields' da Meta class,
        # porque ele não é um campo direto da Model Plate.
        fields = ["price", "photo", "description"]  # Remova 'menus' daqui

        # Personaliza os widgets para os campos específicos (opcional)
        widgets = {
            "description": forms.Textarea(attrs={"rows": 8}),
            # O widget para 'menus' já foi definido no campo explícito acima
        }

        # Personaliza os rótulos (labels) para os campos (opcional)
        labels = {
            "price": "Preço",
            "photo": "Foto",
            "description": "Descrição",
            # O label para 'menus' já foi definido no campo explícito acima
        }
        def __init__(self, *args, **kwargs):
            super(PlatesForms, self).__init__(*args, **kwargs)
            self.fields['photo'].required = False
            if self.instance and self.instance.pk:
                self.fields['menus'].initial = self.instance.menu_set.all()

class PlateChoiceField(forms.ModelMultipleChoiceField):
    """
    Campo personalizado para exibir apenas o nome do prato no label.
    """
    # Sobrescrevemos o método 'label_from_instance'.
    # Este método é chamado para cada objeto no queryset.
    # O que ele retornar será usado como o label do checkbox.
    def label_from_instance(self, obj):
        return obj.name

class MenuForms(forms.ModelForm):

    # plates = forms.ModelMultipleChoiceField(
    #     queryset=Plate.objects.all(),
    #     widget=forms.CheckboxSelectMultiple, # para transformar em checkboxes
    #     required=False,
    #     label_from_instance=lambda plate: plate.name,
    # )

    plates = PlateChoiceField(
        queryset=Plate.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Pratos"
    )

    class Meta:
        model = Menu

        fields = ["name", "plates"]

class VisitorRegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'telefone', 'endereco', 'cpf', 'data_nascimento', 'first_name', 'last_name']
        widgets = {
            'password': forms.PasswordInput(),
        }



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser

        fields = ('tipo_usuario', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'telefone', 'endereco', 'cpf', 'data_nascimento', 'foto_perfil', 'cnh', 'modelo_moto')


    def clean(self):
        cleaned_data = super().clean()

        tipo_usuario = cleaned_data.get('tipo_usuario')
        cnh = cleaned_data.get('cnh')
        modelo_moto = cleaned_data.get('modelo_moto')
        email = cleaned_data.get('email')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        cpf = cleaned_data.get('cpf')
        telefone = cleaned_data.get('telefone')
        endereco = cleaned_data.get('endereco')
        foto_perfil = cleaned_data.get('foto_perfil')
        data_nascimento = cleaned_data.get('data_nascimento')

        if tipo_usuario == CustomUser.TipoUsuario.DELIVERY:
            if not cnh:
                self.add_error('cnh', 'CNH é obrigatório para entregadores.')
            if not modelo_moto:
                self.add_error('modelo_moto', 'Modelo da moto é obrigatório para entregadores.')
            if not email:
                self.add_error('email', 'Email é obrigatório para entregadores.')
            if not first_name:
                self.add_error('first_name', 'Primeiro nome é obrigatório para entregadores.')
            if not last_name:
                self.add_error('last_name', 'Sobrenome é obrigatório para entregadores.')
            if not cpf:
                self.add_error('cpf', 'CPF é obrigatório para entregadores.')
            if not telefone:
                self.add_error('telefone', 'Telefone é obrigatório para entregadores.')
            if not endereco:
                self.add_error('endereco', 'Endereço é obrigatório para entregadores.')
            if not foto_perfil:
                self.add_error('foto_perfil', 'Foto de perfil é obrigatória para entregadores.')
            if not data_nascimento:
                self.add_error('data_nascimento', 'Data de nascimento é obrigatória para entregadores.')
            

        if tipo_usuario == CustomUser.TipoUsuario.MANAGER:
            if not email:
                self.add_error('email', 'Email é obrigatório para gerentes.')
            if not first_name:
                self.add_error('first_name', 'Primeiro nome é obrigatório para gerentes.')
            if not last_name:
                self.add_error('last_name', 'Sobrenome é obrigatório para gerentes.')
            if not cpf:
                self.add_error('cpf', 'CPF é obrigatório para gerentes.')
            if not telefone:
                self.add_error('telefone', 'Telefone é obrigatório para gerentes.')
            if not endereco:
                self.add_error('endereco', 'Endereço é obrigatório para gerentes.')
            if not foto_perfil:
                self.add_error('foto_perfil', 'Foto de perfil é obrigatória para gerentes.')
            if not data_nascimento:
                self.add_error('data_nascimento', 'Data de nascimento é obrigatória para gerentes.')
        
        
        if tipo_usuario == CustomUser.TipoUsuario.CLIENT:
            if not email:
                self.add_error('email', 'Email é obrigatório para clientes.')
            if not first_name:
                self.add_error('first_name', 'Primeiro nome é obrigatório para clientes.')
            if not last_name:
                self.add_error('last_name', 'Sobrenome é obrigatório para clientes.')
            if not cpf:
                self.add_error('cpf', 'CPF é obrigatório para clientes.')
            if not telefone:
                self.add_error('telefone', 'Telefone é obrigatório para clientes.')
            if not endereco:
                self.add_error('endereco', 'Endereço é obrigatório para clientes.')
            if not foto_perfil:
                self.add_error('foto_perfil', 'Foto de perfil é obrigatória para clientes.')
            if not data_nascimento:
                self.add_error('data_nascimento', 'Data de nascimento é obrigatória para clientes.')
