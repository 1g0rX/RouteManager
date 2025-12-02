# ÍNDICE

1. Versão em Português
   1.1 Como iniciar / terminar o sistema
   1.2 Opções oferecidas pelo sistema
   1.3 Menu Principal
   1.4 Gerenciamento de linhas
       1.4.1 Cadastrar uma nova linha
       1.4.2 Editar uma linha existente
       1.4.3 Remover uma linha existente
       1.4.4 Listar todas as linhas cadastradas
   1.5 Sistema de vendas de passagens
       1.5.1 Vender passagens (uma por vez)
       1.5.2 Exibir passagens disponíveis
       1.5.3 Carregar dados em lote
   1.6 Relatórios
       1.6.1 Receita mensal
       1.6.2 Matriz de ocupação semanal
   1.7 Conclusão
   1.8 Limitações
   1.9 Avisos

2. English Version
   2.1 How to start / exit the system
   2.2 System options
   2.3 Main Menu
   2.4 Line Management
       2.4.1 Register a new line
       2.4.2 Edit an existing line
       2.4.3 Remove an existing line
       2.4.4 List all registered lines
   2.5 Ticket Sales System
       2.5.1 Sell tickets (one at a time)
       2.5.2 Show available tickets
       2.5.3 Batch import
   2.6 Reports
       2.6.1 Monthly Revenue
       2.6.2 Weekly Occupancy Matrix
   2.7 Conclusion
   2.8 Limitations
   2.9 Warnings and cautions


# 1. VERSÃO EM PORTUGUÊS

## 1.1 Como iniciar / terminar o sistema

Para iniciar o sistema, abra o terminal na pasta raiz do projeto e execute:

    python3 main.py

Após a execução, o usuário será encaminhado à **tela principal**, onde poderá escolher entre as opções digitando o número correspondente.

O sistema pode ser encerrado a qualquer momento escolhendo a opção:

    0 - Sair

Todas as telas do sistema possuem o mesmo funcionamento: o usuário deve selecionar um número e em seguida pressionar **ENTER**.


## 1.2 Opções oferecidas pelo sistema


# 1.3 Menu Principal

![Main Menu - RouteManager](.assets/route_manager.png)

1. Gerenciar Linhas

   Abre o menu de gerenciamento de linhas (criação, edição, etc.).

2. Venda de bilhetes

   Abre o menu de venda de bilhetes.

3. Relatórios

   Abre o menu de relatórios do sistema.

4. Sair

   Encerra o sistema.


# 1.4 Gerenciamento de linhas

![Manage Line](.assets/manage_lines.jpeg)

### 1.4.1 Cadastrar uma nova linha

A primeira ação é cadastrar uma nova linha; caso contrário, as outras opções ficarão indisponíveis ou não retornarão dados.  
Será solicitado um ID para a linha, a cidade de origem, a cidade de destino, o horário e o preço da passagem.

![Create Line](.assets/create_line.png)

### 1.4.2 Editar uma linha existente

Se uma informação foi digitada incorretamente ou precisa ser atualizada, esta opção permite editar os dados.  
Serão solicitadas novamente todas as perguntas do item anterior; para manter o valor atual, basta pressionar **ENTER**.

![edit line 1](.assets/edit_line_1.png)
-------
![edit line 2](.assets/edit_line_2.png)

### 1.4.3 Remover uma linha existente

Caso seja necessário excluir uma linha, o sistema listará todas e o usuário precisa digitar o ID correspondente para removê-la.

![remove line](.assets/remove_line.png)

### 1.4.4 Listar todas as linhas cadastradas

Exibe todas as linhas cadastradas no sistema.

![list lines](.assets/list_lines.png)

0. Voltar ao menu principal

Retorna ao menu principal para escolher outra opção ou encerrar o programa.


# 1.5 Sistema de vendas de passagens

![tickets manager](.assets/tickets_menu.jpeg)

### 1.5.1 Vender passagens (uma por vez)

O sistema exibirá todas as linhas cadastradas. O usuário seleciona o ID da linha desejada, informa a data e o horário, e então será mostrado, de forma organizada (como um mapa), os assentos do ônibus.  
Assentos marcados com "X" já foram comprados.

![buy ticket](.assets/buy_a_ticket.png)

### 1.5.2 Exibir passagens disponíveis

Esta opção lista todas as linhas disponíveis; em seguida o usuário informa a cidade de destino e o horário desejado. O sistema exibirá os assentos disponíveis para essa configuração (se existirem).  
Após listar os assentos, será perguntado se o usuário deseja comprar; se sim, serão solicitadas informações e a compra será concluída; caso contrário, retorna ao menu de bilhetes.

![available system](.assets/available_seats.png)

### 1.5.3 Carregar dados em lote (arquivo)

Há uma função que carrega passagens a partir de um arquivo — cada linha do arquivo representa uma passagem diferente. Como o arquivo contém apenas uma cidade, a estratégia foi: verificar se essa cidade corresponde à origem ou ao destino de alguma linha cadastrada e, em conjunto com data e horário, se houver correspondência, adicionar a passagem a essa linha.

0. Voltar ao menu principal

Volta ao menu principal para selecionar outra opção ou sair do programa.


# 1.6 Relatórios

Calcula o faturamento total de uma linha no mês vigente, considerando o número de assentos vendidos e o preço da passagem.

![reports menu](.assets/reports_menu.png)


## 1.6.1 Receita mensal

Gera um relatório com todas as compras efetuadas no mês vigente.

![montly 1](.assets/monthy_1.png)

---

## 1.6.2 Matriz de ocupação semanal

Calcula e exibe a porcentagem média de ocupação de cada linha em cada dia da semana (segunda a domingo), considerando o número de viagens registradas e a capacidade total (20 passageiros).

![weekly](.assets/weekly.png)


# 1.7 Conclusão

O programa **RouteManager** cumpre, de forma simples, o objetivo de criação e gerenciamento de linhas e passagens de ônibus, oferecendo funcionalidades que vão desde a criação e edição de linhas até a venda de passagens, processamento em lote e relatórios de receitas e ocupação.


# 1.8 Limitações

- O programa funciona apenas por linha de comando (sem interface gráfica).
- O sistema considera ônibus com capacidade fixa de 20 assentos.
- Importações em lote podem gerar erros quando os dados do arquivo não corresponderem exatamente às linhas cadastradas.


# 1.9 Avisos

> [!WARNING]  
> Devido ao formato de entrada do processamento em lote, muitas importações de passagens podem gerar erros, pois nesse modo o arquivo apresenta apenas uma cidade, enquanto o programa utiliza duas cidades (cidade de partida e destino). Assim, sem a segunda variável (cidade), o programa não sabe o que fazer. **O programa atualmente verifica se a cidade está entre os destinos ou origens já cadastrados no sistema; se for positivo, confere data e horário, e se esses baterem, então adiciona a passagem.**

> [!CAUTION]  
> Se qualquer uma das variáveis enunciadas anteriormente não for satisfeita, será gerado um erro, que será escrito no arquivo de erros, e a passagem não será adicionada.


# 2. ENGLISH VERSION

## 2.1 How to start / exit the system

To start the system, open a terminal in the project root folder and run:

    python3 main.py

After launching, the user will be taken to the **main screen**, where they can choose options by typing the corresponding number.

The system can be closed at any time by selecting:

    0 - Exit

All screens work the same way: the user must select a number and then press **ENTER**.


## 2.2 System options


# 2.3 Main Menu

![Main Menu - RouteManager](.assets/route_manager.png)

1. Manage Lines

   Opens the line management menu (create, edit, etc.).

2. Ticket Sales

   Opens the ticket sales menu.

3. Reports

   Opens the reports menu.

4. Exit

   Closes the system.


# 2.4 Line Management

![Manage Line](.assets/manage_lines.jpeg)

### 2.4.1 Register a new line

The first action is to register a new line; otherwise other options will be unavailable or return no data.  
The user must provide an ID, origin city, destination city, schedule, and ticket price.

![Create Line](.assets/create_line.png)

### 2.4.2 Edit an existing line

If a field was entered incorrectly or needs updating, this option allows editing the information.  
All questions from the previous item will be asked again; press **ENTER** to keep the current value.

![edit line 1](.assets/edit_line_1.png)
-------
![edit line 2](.assets/edit_line_2.png)

### 2.4.3 Remove an existing line

If you need to delete a line, the system will list all lines and you enter the corresponding ID to remove it.

![remove line](.assets/remove_line.png)

### 2.4.4 List all registered lines

Displays all lines registered in the system.

![list lines](.assets/list_lines.png)

0. Return to main menu

Returns to the main menu to select another option or exit the program.


# 2.5 Ticket Sales System

![tickets manager](.assets/tickets_menu.jpeg)

### 2.5.1 Sell tickets (one at a time)

The system will show all registered lines. The user selects the desired line ID, provides date and time, and then a seat map is shown. Seats marked with "X" are already sold.

![buy ticket](.assets/buy_a_ticket.png)

### 2.5.2 Show available tickets

This option lists all available lines; then the user provides the destination city and desired schedule, and the system shows available seats for that configuration (if any). After listing seats, the user is asked if they want to purchase; if yes, required information is requested and the purchase is completed; otherwise it returns to the tickets menu.

![available system](.assets/available_seats.png)

### 2.5.3 Batch import (from file)

There is a function that loads multiple tickets from a file — each line of the file represents a ticket. Since the file contains only one city, the system checks if that city matches the origin or destination of any registered line and, together with date and time, if there is a match, adds the ticket to that line.

0. Return to main menu

Return to the main menu to choose another option or exit the program.


# 2.6 Reports

Calculates total revenue per line for the current month, considering seats sold and ticket price.

![reports menu](.assets/reports_menu.png)


## 2.6.1 Monthly Revenue

Generates a report from all purchases made in the current month.

![montly 1](.assets/monthy_1.png)

---

## 2.6.2 Weekly Occupancy Matrix

Calculates and displays the average occupancy percentage for each line on each weekday (Monday to Sunday), considering the number of registered trips and total capacity (20 passengers).

![weekly](.assets/weekly.png)


# 2.7 Conclusion

The RouteManager program fulfills the goal of creating and managing routes and bus tickets, offering functions from route creation and management to ticket sales, batch processing of tickets from a file, and reporting on generated revenue and occupancy.


# 2.8 Limitations

- The program is command-line only (no GUI).
- The system assumes buses with a fixed capacity of 20 seats.
- Batch imports may fail when file data do not match registered lines.


# 2.9 Warnings and cautions

> [!WARNING]  
> Due to the input format for batch processing, many ticket imports may cause errors because the file presents only one city while the program uses two cities (departure and destination). Without the second city, the program cannot determine which line to assign. **The program currently checks whether the city matches any registered origin or destination; if it does, it checks date and time, and if these match, it adds the ticket.**

> [!CAUTION]  
> If any of the variables mentioned above is not satisfied, an error will be generated, written to the error log file, and the ticket will not be added.
