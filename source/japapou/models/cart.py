# Em um novo arquivo, ex: japapou/models/cart.py
from django.db import models # type: ignore
from django.conf import settings # type: ignore
from .user import CustomUser #
from .plate import Plate #

class Cart(models.Model):
    '''
        Modelo de Carrinho de Compras.
        Cada usuário CLIENTE terá um único carrinho associado.
    '''
    usuario = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="cart",
        limit_choices_to={'tipo_usuario': 'CLIENT'} # Garante que só clientes tenham carrinho
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"

    def __str__(self):
        return f"Carrinho de {self.usuario.username}"

    def get_cart_total(self):
        """Calcula o valor total de todos os itens no carrinho."""
        # 'items' vem do related_name em CartItem
        return sum(item.get_item_total() for item in self.items.all())

class CartItem(models.Model):
    '''
        Item individual dentro do carrinho.
    '''
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items" # Permite acessar os itens com cart.items.all()
    )
    plate = models.ForeignKey(
        Plate,
        on_delete=models.CASCADE,
        related_name="in_carts"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantidade")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"
        # Garante que um prato não possa ser adicionado duas vezes ao mesmo carrinho
        # (a quantidade deve ser atualizada)
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'plate'],
                name='unique_cart_plate'
            )
        ]

    def __str__(self):
        return f"{self.quantity}x {self.plate.name} no carrinho de {self.cart.usuario.username}"

    def get_item_total(self):
        """Calcula o valor total para este item (preço * quantidade)."""
        return self.plate.price * self.quantity