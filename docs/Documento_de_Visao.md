# Documento de visão

## Comércio Eletrônico

### Histórico da Revisão 
|  Data  | Versão | Descrição | Autor |
|:-------|:-------|:----------|:------|
| 21/04/2025 | **1.00** | Versão Inicial  | George Azevedo |
| 27/04/2025 | **1.01** | Versão Inicial  | Alunos |  

## 1. Objetivo do Projeto 
**Projeto**: Sistema para um restaurante, permitindo a gestão de produtos, receitas, pedidos, mesas e reservas.
 
## 2. Descrição do problema 
| | |
|:-|:-|
| **_O problema_** | O lojista que atua no comércio convencional se sente sobrecarregado com o controle manual da loja | 
| **_afetando_** | A produtividade das vendas da loja |
| **_cujo impacto é_** | Eficiencia dos funcionários e lucratividade do comércio |
| **_uma boa solução seria_** | Incluir funcionalidades automáticas por meio do sistema |
| | |

## 3. Descrição dos usuários
| Nome | Descrição | Responsabilidades |
|:- |:- |:- |
| Gerente | O gerente é o responsável por administrar o sistema. | Cadastrar ingredientes e seus lotes; Cadastrar e manejar funcionários e suas funções; Visualizar relatórios do sistema |
| Chef | O chef é o responsável por produzir as receitas e o menu do estabelecimento. | Cadastrar ingredientes e seus lotes; Visualizar estoque de ingredientes; Cadastrar receitas com base nos ingredientes disponíveis; Montar o menu do dia; Visualizar os pedidos pendentes |
| Garçom | O garçom é o responsável por atender os clientes e realizar os pedidos. | Cadastrar o pedido de um cliente; Confirmar o pedido de um cliente; Fechar a conta de um cliente |
| Recepcionista | O recepcionista é o responsável por gerenciar as reservas e alocar os clientes em suas mesas. | Visualizar reservas; Confirmar reservas para um cliente; Alocar uma cliente para um mesa que não resevou |
| Cliente | O cliente é o responsável por reservar uma mesa e visualizar o menu do dia. | Visualizar mesas disponíveis; Reservar uma mesa; Ver o menu do dia;  |
| Visitante | O visitante é o responsável por visualizar as informações do estabelecimento. | Visualisar o menu; Visualizar horários de atendimento; Visualizar informações sobre o restaurante; Registrar uma conta |

## 4. Descrição do ambiente dos usuários 
O sistema tem cinco tipos de usuários. Quatro deles são funcionários do estabelecimento e um outro que representa o cliente, seja ele anônimo ou já cadastrado.

O gerente acessará o site a partir do ambiente físico da loja e fará o cadastro dos ingredientes e realizará a gestão dos funcionários e ver relatórios por meio de gráficos.

O chef irá acessar o site a partir do ambiente físico da loja e realizará a gestão dos ingredientes, das receitas e do menu.
O chef também poderá visualizar os pedidos pendentes por meio de uma tela na cozinha.

O garçom irá acessar o site a partir de um dispositivo móvel e realizará a gestão dos pedidos.

O recepcionista irá acessar o site a partir do ambiente físico da loja e realizará a gestão das reservas e das mesas.

O usuário cliente irá acessar o site utilizando  um computador ou celular e visualizar as mesas para reservar ou visualizar o menu do dia.

O usuário visitante irá acessar o site utilizando um computador ou celular e registrar/entrar em uma conta, visualizar o menu do dia, visualisar horários de atendimento e visualizar informações sobre o restaurante.

## 5. Principais necessidades dos usuários
Considerando o ponto de vista do gerente, sua principal necessidade é aumentar a eficiência de sua loja para que possa ter um melhor controle dela por meio de uma gestão inteligente de todas as funções do sistema.

Considerando o ponto de vista do cliente, ele deseja ter acesso a um site com interface amigável que permita obter informações sobre o restaurante, seus pratos, e as mesas disponíveis, caso identifique que estes atendam às suas necessidades, ele possa montar sua relação de agendamento reservando uma mesa.

## 6. Alternativas concorrentes
Uma alternativa para a parte de reservas do sistema é o [GetIn](https://restaurante.getinapp.com.br/), que possibilita a reserva de uma mesa no horário e local escolhido pelo cliente.

Uma alternativa para a parte do gerenciamento de ingredientes, receitas e o menu é o [SisChef](https://sischef.com/), que oferece funcionalidades para gerenciar o estoque, os usuários, o menu e o redirecionamento para o pagamento.

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
