"""
message_templates.py
Contém todas as mensagens pré-definidas do bot Penélope
"""

# Dicionário com todas as mensagens formatadas do bot
MESSAGES = {
    # 1. Identificação de Usuário Novo
    'greeting_new': """Que bom te ver por aqui!
Sou a *Penélope*, sua assistente de contas a pagar e receber.
Ainda não nos conhecemos, como prefere ser chamado(a)?""",

    # 2. Boas-vindas Após Identificação (Novo)
    'welcome_new': """Prazer em conhecê-lo(a), *{name}*!
Vamos começar a organizar suas finanças?

1 ➕ Cadastrar minha primeira conta
2 ◌ Ver menu principal
3 • Encerrar conversa""",

    # 3. Menu Principal (Usuário Cadastrado)
    'welcome_return': """Olá, *{name}*! Que bom te ver novamente!
Como posso te ajudar?""",
    
    'main_menu': """1 ➕ Cadastrar nova conta a pagar
2 💰 Cadastrar nova conta a receber
3 ◌ Visualizar minhas contas a pagar
4 💼 Visualizar minhas contas a receber
5 ✓ Marcar conta como paga/recebida
6 × Cancelar uma conta
7 ↻ Adiar uma conta
8 ✏ Editar uma conta
9 🔍 Buscar conta por nome
0 ❓ Ajuda / Como funciona
# • Encerrar conversa""",

    # 4. Cadastro de Conta a Pagar
    'new_bill_header': """➕ *NOVA CONTA A PAGAR*
Passo a passo:
(Cancelar: Digite 0 a qualquer momento)""",

    'bill_name': """📝 *Nome da conta:*
(Ex: Aluguel, Energia, Internet)""",

    'bill_value': """💲 *Valor:*
(Ex: 120,50)""",

    'bill_due_date': """📅 *Data de vencimento:*
(Ex: 10 ou 10/06)""",

    'bill_type': """📋 *Tipo de conta:*
1 👤 Pessoal
2 🏢 Corporativa
3 📂 Outros""",

    'bill_recurrence': """🔄 *Recorrência:*
1 ∞ Mensal
2 † Anual
3 • Avulsa
4 🗕 Trimestral""",

    'bill_payment_method': """💳 *Método de pagamento:*
1 💵 Dinheiro
2 💳 Cartão de crédito
3 💳 Cartão de débito
4 ⚡ Pix
5 🏦 Transferência
6 📃 Boleto""",

    'bill_notes': """📝 *Observação (opcional):*
Digite qualquer informação adicional ou deixe em branco.""",

    'bill_confirm': """✅ *Confirme os dados:*
Nome: {name}
Valor: R$ {value}
Vencimento: {due_date}
Tipo: {type}
Recorrência: {recurrence}
Método: {payment_method}
Obs: {notes}

1 ✓ Confirmar
2 × Cancelar""",

    # 5. Cadastro de Conta a Receber
    'new_receivable_header': """💰 *NOVA CONTA A RECEBER*
Passo a passo:
(Cancelar: Digite 0 a qualquer momento)""",

    'receivable_name': """📝 *Nome do recebível:*
(Ex: Salário, Freelance, Aluguel)""",

    'receivable_value': """💲 *Valor:*
(Ex: 120,50)""",

    'receivable_due_date': """📅 *Data prevista:*
(Ex: 10 ou 10/06)""",

    'receivable_type': """📋 *Tipo de recebível:*
1 👤 Pessoal
2 🏢 Corporativa
3 📂 Outros""",

    'receivable_recurrence': """🔄 *Recorrência:*
1 ∞ Mensal
2 † Anual
3 • Avulsa
4 🗕 Trimestral""",

    'receivable_payment_method': """💳 *Método de recebimento:*
1 💵 Dinheiro
2 💳 Cartão de crédito
3 💳 Cartão de débito
4 ⚡ Pix
5 🏦 Transferência
6 📃 Boleto""",

    'receivable_notes': """📝 *Observação (opcional):*
Digite qualquer informação adicional ou deixe em branco.""",

    'receivable_confirm': """✅ *Confirme os dados:*
Nome: {name}
Valor: R$ {value}
Data prevista: {due_date}
Tipo: {type}
Recorrência: {recurrence}
Método: {method}
Obs: {notes}

1 ✓ Confirmar
2 × Cancelar""",

    # 6. Visualizar Contas a Pagar
    'view_bills': """◌ *SUAS CONTAS A PAGAR*
Como deseja visualizar?

1 ∷ Mês atual
2 » Escolher mês
3 ◷ Vencimento hoje
4 $ Todas pendentes
5 ☑ Filtrar por status
6 💳 Filtrar por método de pagamento
7 • Voltar ao menu principal""",

    # 7. Visualizar Contas a Receber
    'view_receivables': """💼 *SUAS CONTAS A RECEBER*
Como deseja visualizar?

1 ∷ Mês atual
2 » Escolher mês
3 ◷ Previsão para hoje
4 $ Todas pendentes
5 ☑ Filtrar por status
6 💳 Filtrar por método de recebimento
7 • Voltar ao menu principal""",

    # 8. Filtrar por Status
    'filter_status': """☑ *FILTRAR POR STATUS*
Selecione o status:

1 ⊘ Pendentes
2 ✓ Pagas/Recebidas
3 ⚠ Atrasadas
4 × Canceladas
5 ↻ Adiadas
6 • Voltar""",

    # 9. Filtrar por Método de Pagamento
    'filter_payment_method': """💳 *FILTRAR POR MÉTODO*
Selecione o método:

1 💵 Dinheiro
2 💳 Cartão de crédito
3 💳 Cartão de débito
4 ⚡ Pix
5 🏦 Transferência
6 📃 Boleto
7 • Voltar""",

    # 10. Lista de Contas (Exemplo)
    'bill_list_item': """📋 *CONTAS ENCONTRADAS:*

{bill_items}

O que deseja fazer?
1 ✓ Marcar como paga
2 × Cancelar conta
3 ↻ Adiar conta
4 ✏ Editar
5 • Voltar""",

    # 11. Marcar Como Paga/Recebida
    'mark_as_paid': """✓ *MARCAR COMO PAGA/RECEBIDA*
Qual conta deseja marcar como paga/recebida?
Digite o número da conta ou 0 para voltar.""",

    'confirm_payment': """? *CONFIRMAR PAGAMENTO/RECEBIMENTO*
Você confirma o pagamento/recebimento de *{bill_name}*?

1 ✓ Sim, confirmar
2 × Não, voltar""",

    # 12. Cancelar Conta
    'cancel_bill': """× *CANCELAR CONTA*
Qual conta deseja cancelar?
Digite o número da conta ou 0 para voltar.""",

    'confirm_cancellation': """! *CONFIRMAR CANCELAMENTO*
Deseja mesmo cancelar a conta *{bill_name}*?

1 ✓ Sim
2 × Não, voltar""",

    # 13. Adiar Conta
    'postpone_bill': """↻ *ADIAR CONTA*
Qual conta deseja adiar?
Digite o número da conta ou 0 para voltar.""",

    'new_due_date': """◷ *NOVA DATA DE VENCIMENTO*
Formatos aceitos:
- Dia (Ex: 10)
- Dia/Mês (Ex: 10/09)
Digite 0 para cancelar esta operação.""",

    # 14. Editar Conta
    'edit_bill': """✏ *EDITAR CONTA*
Qual conta deseja editar?
Digite o número da conta ou 0 para voltar.""",

    'edit_bill_field': """✏ *O que deseja editar na conta {bill_name}?*
1 $ Valor
2 ◷ Data de vencimento
3 ↻ Recorrência
4 # Tipo de conta
5 💳 Método de pagamento
6 ! Observações
7 × Cancelar edição""",

    # 15. Buscar Conta por Nome
    'search_bill': """🔍 *BUSCAR CONTA*
Digite uma palavra-chave para encontrar a conta.
Digite 0 para voltar ao menu anterior.""",

    # 16. Ajuda / Como Funciona
    'help': """❓ *AJUDA - COMO FUNCIONA*
Olá! Eu posso te ajudar a:

1 ➕ Cadastrar novas contas a pagar
2 💰 Cadastrar novas contas a receber
3 ◌ Visualizar suas contas a pagar
4 💼 Visualizar suas contas a receber
5 ✓ Marcar contas como pagas/recebidas
6 × Cancelar contas
7 ↻ Adiar vencimentos
8 ✏ Editar informações de uma conta
9 🔍 Buscar contas pelo nome
0 💳 Gerenciar métodos de pagamento

Digite o número para saber mais ou 0 para voltar ao menu principal.""",

    # 17. Proteção de Encerramento
    'confirm_exit': """• *Deseja realmente encerrar a conversa?*

1 ✓ Sim, encerrar
2 • Voltar ao menu principal""",

    # 18. Mensagens de Status das Contas
    'status_pending': """⊘ *PENDENTE*
Esta conta ainda não foi paga.""",

    'status_paid': """✓ *PAGA/RECEBIDA*
Esta conta foi quitada.""",

    'status_late': """⚠ *ATRASADA*
Conta vencida sem pagamento.""",

    'status_cancelled': """× *CANCELADA*
Conta cancelada.""",

    'status_postponed': """↻ *ADIADA*
Vencimento alterado para {new_date}.""",

    # 19. Mensagens de Erro Gerais
    'error_invalid_input': """× *Ops!*
Não entendi sua resposta. Escolha uma opção disponível ou siga o formato solicitado.""",

    'error_invalid_date': """× *Data inválida!*
Informe no formato correto: Dia (10) ou Dia/Mês (10/09).""",

    'error_invalid_option': """× *Opção inválida!*
Escolha um número entre as opções disponíveis.""",

    # 20. Inatividade
    'inactivity': """? *{name}, ainda está aí?*
Nossa conversa ficou inativa. Como posso ajudar?

1 ◌ Visualizar minhas contas
2 ➕ Cadastrar nova conta
3 • Encerrar conversa por hoje""",

    # 21. Mensagem de Despedida
    'goodbye': """• *Até logo, {name}!*
Foi um prazer te ajudar hoje. Quando quiser organizar suas contas, é só me chamar!

_Penélope - Sua assistente de contas a pagar e receber_""",

    # Mensagens de sucesso
    'success_bill_added': """✅ *Conta a pagar cadastrada com sucesso!*
Deseja cadastrar outra conta?
1 ✓ Sim
2 • Não, voltar ao menu principal""",

    'success_receivable_added': """✅ *Conta a receber cadastrada com sucesso!*
Deseja cadastrar outra conta?
1 ✓ Sim
2 • Não, voltar ao menu principal""",

    'success_bill_paid': """✅ *Pagamento registrado com sucesso!*
A conta {bill_name} foi marcada como paga.""",

    'success_receivable_received': """✅ *Recebimento registrado com sucesso!*
A conta {bill_name} foi marcada como recebida.""",

    'success_bill_cancelled': """✅ *Cancelamento realizado com sucesso!*
A conta {bill_name} foi cancelada.""",

    'success_bill_postponed': """✅ *Adiamento realizado com sucesso!*
A conta {bill_name} foi adiada para {new_date}.""",

    'success_bill_edited': """✅ *Edição realizada com sucesso!*
A conta {bill_name} foi atualizada."""
}
