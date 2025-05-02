# Documento de visão

## Comércio Eletrônico

### Histórico da Revisão 
|  Data  | Versão | Descrição | Autor |
|:-------|:-------|:----------|:------|
| 21/04/2025 | **1.00** | Versão Inicial  | George Azevedo |
| 27/04/2025 | **1.01** | Versão Inicial  | Alunos |  

## 1. Objetivo do Projeto 
**Projeto**: Sistema de comercialização de produtos de um restaurante de comida japonesa.
## 2. Descrição do problema 
| | |
|:-|:-|
| **_O problema_** | O lojista sente que o comércio que ele atua se torna menos competitivo e visibilizado diante dos concorrentes que oferecem mais praticidade | 
| **_afetando_** | A capacidade de atrair e manter clientes |
| **_cujo impacto é_** | A lucratividade e a visibilidade do comércio |
| **_uma boa solução seria_** | Implementar um sistema próprio de pedidos online para aumentar a competitividade e melhorar a experiência do cliente |
| | |

## 3. Descrição dos usuários
| Nome | Descrição | Responsabilidades |
|:- |:- |:- |
| Gerente | O gerente é o responsável por administrar as vendas. | Ver relatórios das vendas; Montar cardápio; Visualizar os pedidos; Alterar o status dos pedidos |
| Cliente | O cliente é o responsável por reservar uma mesa e visualizar o menu do dia. |  Visualizar o cardápio; Fazer pedido; Visualizar horários de atendimento; Visualizar informações sobre o restaurante; |
| Visitante | O visitante é o responsável por visualizar as informações do estabelecimento. | Visualizar o cardápio; Visualizar horários de atendimento; Visualizar informações sobre o restaurante; Registrar uma conta |

## 4. Descrição do ambiente dos usuários 
O sistema tem três tipos de usuários. Um deles é o responsável por receber os pedidos feitos via aplicação, o outro usuário é o cliente cadastrado e o terceiro é o cliente não cadastrado, chamado de visitante.

O gerente acessará o site a partir do ambiente físico da loja, ver relatórios por meio de gráficos montar/atualizar o cardápio, visualizar os pedidos e alterar seus status.

O usuário cliente irá acessar o site utilizando  um computador ou celular e visualizar o cardápio do dia e fazer o pedido.

O usuário visitante irá acessar o site utilizando um computador ou celular e registrar/entrar em uma conta, visualizar o cardápio do dia,  visualizar informações sobre o restaurante.

## 5. Principais necessidades dos usuários
Considerando o ponto de vista do gerente, sua principal necessidade é aumentar a eficiência de sua loja para que possa ter um melhor controle dela por meio de uma gestão inteligente de todas as funções do sistema.

Considerando o ponto de vista do cliente, ele deseja ter acesso a um site com interface amigável que permita obter informações sobre o restaurante e sobre os seus pratos, sendo, posteriormente, capaz de realizar o seu pedido.

## 6. Alternativas concorrentes
Uma alternativa para concorrentes do sistema são o [Crumbl](https://crumblcookies.com/order/carry_out) e o [Brooki Bakehouse](https://www.brookibakehouse.com/).



## 7.	Visão geral do produto
O sistema desenvolvido é uma aplicação web que tem como objetivo auxiliar no gerenciamento de um restaurante, permitindo que os funcionários possam gerenciar os ingredientes, receitas e o menu, além de permitir que os clientes possam visualizar as mesas disponíveis e reservar uma, visualizar o menu do dia e visualizar as informações sobre o restaurante.

## 8. Requisitos funcionais

| Código | Nome | Descrição |
|:---  |:--- |:--- |
| F01 | Cadastrar, visualizar, alterar ou excluir ingredientes | Permite a gestão de ingredientes no sistema, incluindo operações de criação, visualização, atualização e exclusão. |
| F02 | Cadastrar, visualizar, alterar ou excluir lotes | Facilita o controle de lotes de ingredientes, permitindo operações de cadastro, visualização, modificação e remoção. |
| F03 | Pesquisar e filtrar o estoque | Oferece funcionalidades para busca e filtragem do estoque, auxiliando na localização rápida de itens. |
| F04 | Cadastrar funcionário | Possibilita o registro de novos funcionários no sistema, com seus respectivos dados pessoais e profissionais. |
| F05 | Alterar dados de funcionário | Permite a atualização das informações dos funcionários já cadastrados no sistema. |
| F06 | Remover funcionário | Disponibiliza a opção de excluir o cadastro de funcionários quando necessário. |
| F07 | Visualizar relatórios do sistema | Fornece acesso a relatórios detalhados sobre o funcionamento e dados do sistema. |
| F08 | Cadastrar, visualizar, alterar ou excluir receitas | Gerencia as receitas do restaurante, permitindo operações de criação, visualização, alteração e exclusão. |
| F09 | Pesquisar e filtrar receitas | Permite buscar e filtrar receitas armazenadas no sistema para fácil acesso. |
| F10 | Montar menu do dia | Facilita a criação do menu diário com base nas receitas disponíveis. |
| F11 | Alterar menu do dia | Oferece a possibilidade de modificar o menu do dia conforme necessário. |
| F12 | Visualizar menu do dia | Permite que usuários visualizem o menu diário disponibilizado pelo restaurante. |
| F13 | Cadastrar pedido | Habilita o registro de novos pedidos feitos pelos clientes. |
| F14 | Confirmar pedido | Permite a confirmação dos pedidos registrados pelos clientes. |
| F15 | Visualizar pedidos pendentes | Exibe uma lista atualizada dos pedidos pendentes de processamento. |
| F16 | Fechar conta | Facilita o fechamento da conta de um cliente após a conclusão de um pedido. |
| F17 | Visualizar mesas | Oferece uma visão geral das mesas disponíveis e ocupadas no restaurante. |
| F18 | Reservar mesa | Permite a reserva de mesas por parte dos clientes e do recepcionista, garantindo a disponibilidade. |
| F19 | Confirmar reserva | Confirma as reservas feitas, assegurando a alocação de mesas. |
| F20 | Realizar o cadastro e login no site | Permite que usuários se cadastrem e façam login no sistema para acesso personalizado. |
| F21 | Visualizar informações do restaurante | Disponibiliza informações gerais sobre o restaurante aos visitantes e clientes. |
| F22 | Visualizar horários de atendimento | Exibe os horários em que o restaurante está aberto para o público. |

## 9.	Requisitos não-funcionais
| Código | Nome | Descrição | Categoria | Classificação |
|:---  |:--- |:--- |:--- |:--- |
| NF01 | Design responsivo | O site apresentará responsividade, deixando-o mais confortável para o usuário | Usabilidade | Obrigatório |
| NF02 | Acesso somente com internet | É necessário um acesso contínuo à Internet para poder acessar os dados do site e suas funcionalidades. | Disponibilidade | Obrigatório |
| NF03 | Criptografia das informações sensíveis aos usuários | Senhas do usuário devem ser gravadas de forma criptografada no banco de dados | Segurança | Obrigatório |
| NF04 | Organização do conteúdo de forma objetiva | O site apresentará o conteúdo de forma objetiva, de modo que o usuário encontre o desejado com facilidade. | Usabilidade | Obrigatório |
| NF05 | Tecnologias utilizadas no desenvolvimento | O site deverá ser feito utilizando HTML, CSS e JS no front-end. No back-end deverá ser utilizado Python com Django e o banco de dados será o MySQL. | Desempenho | Obrigatório |
