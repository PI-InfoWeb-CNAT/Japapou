# Projeto Japapou

## Especificação do caso de uso - Gerenciar Menu

### Histórico da Revisão

| Data       | Versão   | Descrição     | Autor           |
| :--------- | :------- | :------------ | :-------------- |
| 17/05/25 | **1.00** | Versão modelo | Danilo Dantas |

### 1. Resumo

Este casos de uso permite que o gerente de uma filial gerencie o menu do dia com base no cardápio do restaurante.

### 2. Atores

-   Gerente

### 3. Pré-condições

São pré-condições para iniciar este caso de uso:

-   O gerente estar logado no sistema
-   Existir pratos no cardápio do restaurante

### 4. Pós-condições

Após a execução deste casos de uso, espera que o sistema:

-   Adicione ou remova pratos do menu da filial

### 5. Fluxos de evento

#### 5.1. Fluxo Principal
(Adição de prato)

| Ator | Sistema |
|:-------|:------- |
| 1. Na página de menu, o gerente clica no ícone de "+" em um prato. | --- |
| --- | 2. O sistema adiciona o prato ao menu da filial. |

#### 5.2. Fluxo alternativo
(Remoção de prato)

| Ator | Sistema |
|:-------|:------- |
| 1. Na página de menu, o gerente clica no ícone de "-" em um prato. | --- |
| --- | 2. O sistema remove o prato do menu da filial. |

#### 5.3. Fluxo de excessão 
Não há excessão.

### 6. Prototipos de Interface

`A ser desenvolvido pela equipe.`

### 7. Diagrama de classe de domínio usados neste caso de uso

`A ser desenvolvido pela equipe.`
