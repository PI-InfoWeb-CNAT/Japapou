# Projeto Japapou

## Especificação do caso de uso - Confirmar entrega

### Histórico da Revisão

| Data       | Versão   | Descrição     | Autor           |
| :--------- | :------- | :------------ | :-------------- |
| 17/05/25 | **1.00** | Versão modelo | Danilo Dantas |
| 24/05/25 | **1.01** | Modificação do fluxo de exceção | Pedro Lucas |

### 1. Resumo

Este casos de uso permite que um motoboy confirme a entrega de um pedido com o pagamento sendo automatico com o saldo do cliente no sistema. 

### 2. Atores

-   Motoboy
-   Cliente

### 3. Pré-condições

São pré-condições para iniciar este caso de uso:

-   O motoboy estar logado no sistema
-   O motoboy estar com um pedido para ser entregue

### 4. Pós-condições

Após a execução deste casos de uso, espera que o sistema:

-   O sistema deve descontar o saldo do cliente que o pedido foi feito.
-   Editar o pedido e definir como entregue.

### 5. Fluxos de evento

#### 5.1. Fluxo Principal
| Ator | Sistema |
|:-------|:------- |
| 1. Na página de pedido atual, o motoboy clica em "confirmar entrega". | --- |
| --- | 2. O sistema verifica o saldo do cliente. |
| --- | 3. O sistema desconta o saldo do cliente que o pedido foi feito. |
| --- | 4. O sistema modifica o pedido com as informações da entrega. |
| 5. O motoboy visualiza uma confirmação do pagamento. | --- |

#### 5.2.1 Fluxo de excessão 
| Ator | Sistema |
|:-------|:------- |
| 1. Na página de pedido atual, o motoboy clica em "confirmar entrega". | --- |
| --- | 2. O sistema verifica o saldo do cliente. |
| --- | 3. (EXCEÇÃO) O sistema detecta que o cliente não possui saldo suficiente. |
| --- | 4. O sistema exibe uma mensagem de alerta para o motoboy: "Saldo insuficiente. Pagamento automático falhou. Por favor, solicite o pagamento diretamente ao cliente." |
| 5. O motoboy visualiza o alerta e pede o pagamento ao cliente. | --- |
| 6. O cliente diz que vai pagar em dinheiro. | --- |
| 7. O motoboy confirma o pagamento em dinheiro. | --- |
| --- | 8. O sistema confirma o pedido com as informações da entrega.

#### 5.2.2 Fluxo de excessão 
| Ator | Sistema |
|:-------|:------- |
| 1. Na página de pedido atual, o motoboy clica em "confirmar entrega". | --- |
| --- | 2. O sistema verifica o saldo do cliente. |
| --- | 3. (EXCEÇÃO) O sistema detecta que o cliente não possui saldo suficiente. |
| --- | 4. O sistema exibe uma mensagem de alerta para o motoboy: "Saldo insuficiente. Pagamento |automático falhou. Por favor, solicite o pagamento diretamente ao cliente." |
| 5. O motoboy visualiza o alerta e pede o pagamento ao cliente. | --- |
| 6. (EXCEÇÃO) O cliente diz que vai pagar em pix. | --- |
| 7. O motoboy aperta no botão "pagamento via pix". | --- |
| --- | 8. O sistema gera um QR code para o pagamento. |
| 9. O cliente paga. | --- |
| --- | 10. O sistema confirma o pagamento. |
| --- | 11. O sistema confirma o pedido como entregue. |

### 6. Prototipos de Interface

`A ser desenvolvido pela equipe.`

### 7. Diagrama de classe de domínio usados neste caso de uso

`A ser desenvolvido pela equipe.`
