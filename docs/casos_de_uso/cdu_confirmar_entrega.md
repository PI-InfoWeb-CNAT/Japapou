# Projeto Japapou

## Especificação do caso de uso - Confirmar entrega

### Histórico da Revisão

| Data       | Versão   | Descrição     | Autor           |
| :--------- | :------- | :------------ | :-------------- |
| 17/05/25 | **1.00** | Versão modelo | Danilo Dantas |

### 1. Resumo

Este casos de uso permite que um motoboy confirme a entrega de um pedido e receba um pagamento caso necessário. 

### 2. Atores

-   Motoboy
-   Cliente

### 3. Pré-condições

São pré-condições para iniciar este caso de uso:

-   O motoboy estar logado no sistema
-   O motoboy estar com um pedido para ser entregue

### 4. Pós-condições

Após a execução deste casos de uso, espera que o sistema:

-   Caso o pagamento seja via pix, o sistema deve gerar um código QR para o pagamento.
-   Caso o pagamento seja pelo saldo do app, deve descontar o saldo do cliente que o pedido foi feito.
-   Editar o pedido e definir como entregue.

### 5. Fluxos de evento

#### 5.1. Fluxo Principal
(Pagamento pelo saldo do app)

| Ator | Sistema |
|:-------|:------- |
| 1. Na página de pedido atual, o motoboy clica em "confirmar entrega". | --- |
| --- | 2. O sistema desconta o saldo do cliente que o pedido foi feito. |
| --- | 3. O sistema modifica o pedido com as informações da entrega. |
| 4. O motoboy visualiza uma confirmação do pagamento. | --- |

#### 5.2. Fluxo alternativo
(Pagamento via pix)

| Ator | Sistema |
|:-------|:------- |
| 1. Na página de pedido atual, o motoboy clica em "confirmar entrega". | --- |
| --- | 2. O sistema gera um código QR para o pagamento. |
| 3. O motoboy mostra o código QR para o cliente. | --- |
| 4. O cliente escanea o código QR e confirma o pagamento. | --- |
| 5. O motoboy visualiza uma confirmação do pagamento. | --- |

#### 5.3. Fluxo de excessão 
Não há excessão.

### 6. Prototipos de Interface

`A ser desenvolvido pela equipe.`

### 7. Diagrama de classe de domínio usados neste caso de uso

`A ser desenvolvido pela equipe.`
