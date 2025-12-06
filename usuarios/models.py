from django.db import models
from django.utils.crypto import get_random_string

class Usuario(models.Model):
    # Lista de graduações do Exército Brasileiro
    GRADUACAO_CHOICES = [
        ('soldado', 'Soldado'),
        ('cabo', 'Cabo'),
        ('3_sargento', '3º Sargento'),
        ('2_sargento', '2º Sargento'),
        ('1_sargento', '1º Sargento'),
        ('subtenente', 'Subtenente'),
        ('aspirante', 'Aspirante'),
        ('2_tenente', '2º Tenente'),
        ('1_tenente', '1º Tenente'),
        ('capitao', 'Capitão'),
        ('major', 'Major'),
        ('tenente_coronel', 'Tenente-Coronel'),
        ('coronel', 'Coronel'),
        ('general_brigada', 'General de Brigada'),
        ('general_divisao', 'General de Divisão'),
        ('general_exercito', 'General de Exército'),
        ('marechal', 'Marechal'),
    ]

    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)  # Em produção use hashing!
    pin = models.CharField(max_length=4)  # PIN de 4 dígitos obrigatório para confirmação de retirada
    graduacao = models.CharField(max_length=20, choices=GRADUACAO_CHOICES)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} - {self.get_graduacao_display()}"


class Sessao(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=100)  # pode ser armazenada criptografada
    criador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="sessoes")
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Item(models.Model):
    sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE, related_name="itens")
    nome = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField(default=1)
    criado_em = models.DateTimeField(auto_now_add=True)

class Retirada(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="retiradas")
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    quantidade = models.PositiveIntegerField(default=1)
    data_retirada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} retirou {self.quantidade} de {self.item.nome} em {self.data_retirada:%d/%m/%Y}"