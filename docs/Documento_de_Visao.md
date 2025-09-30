# Documento de visão

## Comércio Eletrônico

### Histórico da Revisão 
|  Data  | Versão | Descrição | Autor |
|:-------|:-------|:----------|:------|
| 21/04/2025 | **1.00** | Versão Inicial | George Azevedo |
| 27/04/2025 | **1.01** | Versão Inicial | Alunos | 
| 02/05/2025 | **1.02** | Remoção de funcionalidades | Alunos |
| 05/05/2025 | **1.03** | Adição do usuário Motoboy | Alunos |
| 06/05/2025 | **1.04** | Modificações rápidas | Alunos |

## 1. Objetivo do Projeto 
**Projeto**: Sistema de comercialização de produtos de um restaurante de comida japonesa.

## 2. Descrição do problema 
| | |
|:-|:-|
| **_O problema_** | O lojista sente que o comércio que ele atua se torna menos competitivo e visibilizado diante dos concorrentes que oferecem mais praticidade | 
| **_afetando_** | A capacidade de atrair e manter clientes |
| **_cujo impacto é_** | A lucratividade e a visibilidade do comércio |
| **_uma boa solução seria_** | Implementar um sistema próprio de pedidos online para aumentar a competitividade e melhorar a experiência do cliente |

## 3. Descrição dos usuários
| Nome | Descrição | Responsabilidades |
|:- |:- |:- |
| Gerente | O gerente é o responsável por administrar as vendas. | Ver relatórios das vendas; Gerenciar Cardápio; Montar menu do dia; Visualizar pedidos pedentes; Confirmar Saída; Cadastrar Motoboys; Visualizar histórico |
| Cliente | O cliente é o responsável por visualizar o menu do dia e fazer pedidos. |  Visualizar menu do dia; Confirmar compra; Visualizar horários de atendimento; Visualizar informações sobre o restaurante; Avaliar motoboys; Avaliar pratos; Gerenciar carrinho; Visualizar histórico de pedidos; Depositar dinheiro |
| Visitante | O visitante é o responsável por visualizar as informações do estabelecimento. | Visualizar o menu do dia; Visualizar horários de atendimento; Visualizar informações sobre o restaurante; Registrar ou fazer login em uma conta |
| Motoboy | O Motoboy é o responsável por visualizar os pedidos e entregar eles. | Visualizar pedidos; Confirmar entregas |

## 4. Descrição do ambiente dos usuários 
O sistema tem quatro tipos de usuários. Um deles é o responsável por receber os pedidos feitos via aplicação, o outro usuário é o cliente cadastrado e o terceiro é o cliente não cadastrado, chamado de visitante.

O gerente acessará o site a partir do ambiente físico da loja, ver relatórios por meio de gráficos montar/atualizar o cardápio, visualizar os pedidos e alterar seus status.

O usuário cliente irá acessar o site utilizando  um computador ou celular e visualizar o cardápio do dia e fazer o pedido.

O usuário visitante irá acessar o site utilizando um computador ou celular e registrar/entrar em uma conta, visualizar o cardápio do dia,  visualizar informações sobre o restaurante.

O usuário Motoboy irá acessar o site utilizando um celular e visualizar os pedidos para ele entregar, confirmar entregas e avaliar clientes.

## 5. Principais necessidades dos usuários
Considerando o ponto de vista do gerente, sua principal necessidade é aumentar a eficiência de sua loja para que possa ter um melhor controle dela por meio de uma gestão inteligente de todas as funções do sistema.

Considerando o ponto de vista do cliente, ele deseja ter acesso a um site com interface amigável que permita obter informações sobre o restaurante e sobre os seus pratos, sendo, posteriormente, capaz de realizar o seu pedido.

Considerando o ponto de vista do Motoboy, ele deseja ter acesso a um site com interface prática de uso mobile, que permita visualizar os pedidos e confirmar eles.

## 6. Alternativas concorrentes
Uma alternativa para o sistema é o [Crumbl](https://crumblcookies.com/order/carry_out), focando no delivery: oferece escolha de filial, mostra informações sobre o carro de entrega.  

Uma outra alternativa é o [Brooki Bakehouse](https://www.brookibakehouse.com/), focando no menu: a organização de como os itens estão dispostos no site e a maneira como o pedido pode ser personalizado.

## 7.	Visão geral do produto
O sistema desenvolvido é uma aplicação web que tem como objetivo auxiliar no gerenciamento das vendas de um restaurante, permitindo que o gerente possa gerenciar os pratos, o menu e os pedidos, além de permitir que os clientes possam visualizar o cardápio e fazer pedidos.

## 8. Requisitos funcionais
| Código | Nome | Descrição | Categoria |
|:---  |:--- |:--- | :--- |
| F01 | Cadastrar, visualizar, alterar ou excluir pratos | Permite a gestão de pratos no sistema, incluindo operações de criação, visualização, atualização e exclusão. | Evidente |
| F02 | Cadastrar, visualizar, alterar ou excluir Motoboys | Permite a gestão dos Motoboys no sistema, incluindo operações de criação, visualização, atualização e exclusão. | Evidente |
| F03 | Visualizar relatórios do sistema | Fornece acesso a relatórios detalhados sobre o funcionamento e dados do sistema. | Evidente |
| F04 | Alterar menu do dia | Oferece a possibilidade de modificar o menu do dia conforme necessário. | Evidente |
| F05 | Visualizar menu do dia | Permite que usuários visualizem o menu diário disponibilizado pelo restaurante. | Evidente |
| F06 | Fazer pedido | Permite que o cliente faça pedidos de seus pratos. | Evidente |
| F07 | Realizar o cadastro e login no site | Permite que usuários se cadastrem e façam login no sistema para acesso persnalizado. | Evidente |
| F08 | Visualizar informações do restaurante | Disponibiliza informações gerais sobre o restaurante aos visitantes e clientes. | Evidente |
| F09 | Visualizar horários de atendimento | Exibe os horários em que o restaurante está aberto para o público. | Evidente |
| F10 | Avaliar Motoboy | Permite que um cliente avalie os Motoboys que entregaram seu pedido. | Evidente |
| F11 | Visualizar pedidos atuais | Permite que um Motoboy visualize os pedidos em andamento. | Evidente |
| F12 | Visualizar histórico de pedidos | Permite que um Motoboy, Cliente ou Gerente visualize o histórico de pedidos. | Evidente | 
| F13 | Confirmar entregas | Permite que um Motoboy confirme as entregas. | Evidente |
| F14 | Depositar dinheiro | Permite que um cliente deposite dinheiro em uma conta. | Evidente |
| F15 | Gerenciar carrinho | Permite que um cliente gerencie o carrinho. | Evidente |
| F16 | Descontar do saldo | Usuário utiliza o saldo depositado no aplicativo para uma compra. | Oculto |

## 9.	Requisitos não-funcionais
| Código | Nome | Descrição | Categoria | Classificação |
|:---  |:--- |:--- |:--- |:--- |
| NF01 | Acesso somente com internet | É necessário um acesso contínuo à Internet para poder acessar os dados do site e suas funcionalidades. | Disponibilidade | Obrigatório |
| NF02 | Criptografia das informações sensíveis aos usuários | Senhas do usuário devem ser gravadas de forma criptografada no banco de dados | Segurança | Obrigatório |
| NF03 | Organização do conteúdo de forma objetiva | O site apresentará o conteúdo de forma objetiva, de modo que o usuário encontre o desejado com facilidade. | Usabilidade | Obrigatório |
| NF04 | Tecnologias utilizadas no desenvolvimento | O site deverá ser feito utilizando HTML, CSS e JS no front-end. No back-end deverá ser utilizado Python com Django e o banco de dados será o MySQL. | Desempenho | Obrigatório |

## 10. Glossário

| Nome | Significado |
|:---  |:--- |
| Menu | Pratos disponpiveis para compra no período especificado |
| Cardápio | O conjunto de todos os pratos presentes no restaurante |

