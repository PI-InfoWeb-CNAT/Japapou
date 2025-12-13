from django.db import models  # type: ignore
from django.conf import settings # type: ignore # Importar settings
from japapou.models.adress import Endereco

class Order(models.Model):

    class Status(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente (Aguardando Confirmação)'
        PROCESSANDO = 'PROCESSANDO', 'Em Preparo'
        PRONTO_PARA_RETIRADA = 'PRONTO_PARA_RETIRADA', 'Pronto para Retirada'
        A_CAMINHO = 'A_CAMINHO', 'A Caminho'
        ENTREGUE = 'ENTREGUE', 'Entregue'
        CONCLUIDO = 'CONCLUIDO', 'Concluído'
        CANCELADO = 'CANCELADO', 'Cancelado'
        FALHA = 'FALHA', 'Falha no Pagamento/Entrega'

    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.PENDENTE, # Todos os pedidos novos começam como Pendente
        verbose_name="Status do Pedido"
    )

    # apenas se a opção de pagamento for dinheiro
    troco_para = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Troco para o valor"
    )

    class MetodoPagamento(models.TextChoices):
        DINHEIRO = 'DINHEIRO', 'Dinheiro'
        CARTAO = 'CARTAO', 'Cartão'
        PIX = 'PIX', 'Pix'

    metodo_pagamento = models.CharField(
        max_length=10, 
        choices=MetodoPagamento.choices, 
        default=MetodoPagamento.PIX, 
        verbose_name="Método de Pagamento"
    )

    class TipoPedido(models.TextChoices):
        RETIRADA = 'RETIRADA', 'retirada'
        ENTREGA = 'ENTREGA', 'entrega'

    tipo_pedido = models.CharField(max_length=10, choices=TipoPedido.choices, default=TipoPedido.ENTREGA, verbose_name='tipo de pedido')

    date = models.DateField(auto_now_add=True) # Alterado para auto_now_add
    estimate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Permitir nulo
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    altered_at = models.DateTimeField(auto_now=True)


    endereco_entrega = models.ForeignKey(
        Endereco,
        on_delete=models.SET_NULL, 
        null=True,                 
        blank=True,                
        related_name="pedidos_neste_endereco"
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, 
        related_name="Pedidos"
    )

    # Campos de 'Pickup'
    data_retirada = models.DateTimeField(null=True, blank=True, verbose_name="Data de Retirada")

    # Campos de 'Delivery'
    taxa_entrega = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, # Deve ser nulo se for 'PICKUP'
        verbose_name="Taxa de Entrega"
    )
    data_saida = models.DateTimeField(null=True, blank=True, verbose_name="Data de Saída")
    data_entrega = models.DateTimeField(null=True, blank=True, verbose_name="Data de Entrega")
    
    entregador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'tipo_usuario': 'DELIVERY_MAN'},
        related_name='pedidos_entregues'
    )

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-date"]

    def __str__(self):
        #data_formatada = self.date.strftime('%d/%m/%Y')
        id_pedido = f"Pedido #{self.id}"

        if self.tipo_pedido == self.TipoPedido.RETIRADA:
            tipo = self.get_tipo_pedido_display()
            return f"[{tipo}] {id_pedido} (Retirado) - R$ {self.total} - Cliente {self.usuario}"
        if self.tipo_pedido == self.TipoPedido.ENTREGA:
            tipo = self.get_tipo_pedido_display()
            return f"[{tipo}] {id_pedido} (Entregue) - R$ {self.total}"
            
    


    