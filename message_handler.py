"""
message_handler.py
Gerencia as mensagens e interações com o WhatsApp
"""
import json
import re
import os
from datetime import datetime
from database import SupabaseManager
from message_templates import MESSAGES
from state_manager import StateManager

class MessageHandler:
    """Classe para gerenciar as mensagens e estados de conversa do bot Penélope"""
    
    def __init__(self):
        """Inicializa o handler de mensagens"""
        # 1. Inicializar o gerenciador do banco de dados
        self.db = SupabaseManager()
        
        # 2. Carregar mensagens pré-definidas
        self.load_message_templates()
        
        # 3. Inicializar o gerenciador de estados
        self.state_manager = StateManager()
        
        # 4. Dicionário para armazenar dados temporários durante o cadastro
        self.temp_data = {}
        
        # Inicializar o dicionário de estados de usuários
        self.user_states = {}
    
    def load_message_templates(self):
        """Carrega as mensagens pré-definidas do bot"""
        # 5. Carrega as mensagens do módulo message_templates
        self.messages = MESSAGES
    
    def process_message(self, phone_number, message_text):
        """
        Processa uma mensagem recebida e retorna a resposta
        Retorna uma tupla (resposta, mídia, tipo_de_mídia)
        """
        try:
            # 6. Verificar se o usuário já está cadastrado
            exists, user_data = 
def check_cliente_exists(self, celular):
    """Verifica se um cliente existe pelo número de celular"""
    try:
        response = self.supabase.table('clientes').select('*').eq('celular', celular).execute()
        return len(response.data) > 0, response.data[0] if response.data else None
    except Exception as e:
        print(f"Erro ao verificar cliente: {e}", file=sys.stderr)
        return False, None
            
            # 7. Se não existir, iniciar fluxo de cadastro
            if not exists:
                return self._handle_new_user(phone_number, message_text)
            
            # 8. Se existir, processar conforme o estado atual
            user_id = user_data['id']
            user_name = user_data['nome']
            
            # 9. Carregar estado do usuário do arquivo
            user_state = self.state_manager.get_user_state(phone_number)
            
            # Atualizar o dicionário de estados de usuários
            self.user_states[phone_number] = user_state
            
            # 10. Obter estado atual
            current_state = user_state.get('state', 'main_menu')
            current_step = user_state.get('step')
            
            # Carregar dados temporários do estado
            if 'temp_data' in user_state and user_state['temp_data']:
                self.temp_data[phone_number] = user_state['temp_data']
            
            # 11. Processar com base no estado atual
            response = None
            if current_state == 'main_menu':
                response = self._handle_main_menu(phone_number, user_id, user_name, message_text)
            elif current_state == 'welcome_new':
                response = self._handle_welcome_new(phone_number, user_id, user_name, message_text)
            elif current_state == 'new_bill':
                response = self._handle_new_bill(phone_number, user_id, user_name, message_text)
            elif current_state == 'new_receivable':
                response = self._handle_new_receivable(phone_number, user_id, user_name, message_text)
            elif current_state == 'view_bills':
                response = self._handle_view_bills(phone_number, user_id, user_name, message_text)
            elif current_state == 'view_receivables':
                response = self._handle_view_receivables(phone_number, user_id, user_name, message_text)
            elif current_state == 'mark_as_paid':
                response = self._handle_mark_as_paid(phone_number, user_id, user_name, message_text)
            elif current_state == 'cancel_bill':
                response = self._handle_cancel_bill(phone_number, user_id, user_name, message_text)
            elif current_state == 'postpone_bill':
                response = self._handle_postpone_bill(phone_number, user_id, user_name, message_text)
            elif current_state == 'edit_bill':
                response = self._handle_edit_bill(phone_number, user_id, user_name, message_text)
            elif current_state == 'search_bill':
                response = self._handle_search_bill(phone_number, user_id, user_name, message_text)
            elif current_state == 'help':
                response = self._handle_help(phone_number, user_id, user_name, message_text)
            elif current_state == 'confirm_exit':
                response = self._handle_confirm_exit(phone_number, user_id, user_name, message_text)
            else:
                # Estado desconhecido, retornar para o menu principal
                current_state = 'main_menu'
                current_step = None
                response = (self.messages['welcome_return'].format(name=user_name) + "\n" + self.messages['main_menu'], None, None)
            
            # 12. Salvar o estado atual no arquivo
            temp_data = self.temp_data.get(phone_number, {})
            user_data = {'name': user_name, 'id': user_id}
            self.state_manager.save_user_state(
                phone_number, 
                current_state,
                current_step,
                user_data,
                temp_data
            )
            
            return response
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.", None, None
    
    def _handle_new_user(self, phone_number, message_text):
        """Gerencia interação com novos usuários"""
        # 13. Carregar estado do arquivo (se existir)
        user_state = self.state_manager.get_user_state(phone_number)
        current_state = user_state.get('state', 'new_user_get_name')
        
        # 14. Se estamos esperando o nome
        if current_state == 'new_user_get_name':
            # Se é a primeira mensagem, apenas perguntar o nome
            if message_text is None or message_text.strip() == '':
                # Salvar estado inicial
                self.state_manager.save_user_state(
                    phone_number,
                    'new_user_get_name',
                    None,
                    {},
                    {}
                )
                return self.messages['greeting_new'], None, None
            
            # Verificar se o nome foi fornecido
            if message_text.strip() == '':
                return self.messages['error_invalid_input'] + "\n\n" + self.messages['greeting_new'], None, None
            
            # Armazenar o nome fornecido
            name = message_text.strip()
            
            # 15. Criar o usuário no banco de dados
            success, user_data = self.db.create_cliente(name, phone_number)
            
            if not success or not user_data:
                return "Desculpe, ocorreu um erro ao cadastrar seu usuário. Por favor, tente novamente mais tarde.", None, None
            
            user_id = user_data['id']
            
            # 16. Salvar o estado inicial ('welcome_new') no arquivo
            self.state_manager.save_new_user_state(phone_number, name, user_id)
            
            # Enviar boas-vindas
            return self.messages['welcome_new'].format(name=name), None, None
        
        # Se por algum motivo o estado for inválido, resetar
        self.state_manager.save_user_state(
            phone_number,
            'new_user_get_name',
            None,
            {},
            {}
        )
        return self.messages['greeting_new'], None, None
    
    def _handle_welcome_new(self, phone_number, user_id, user_name, message_text):
        """Gerencia o estado de boas-vindas para novos usuários"""
        # Processar a opção selecionada
        if message_text == '1':
            # Iniciar cadastro de conta
            new_state = 'new_bill'
            new_step = 'name'
            self.temp_data[phone_number] = {}  # Limpar dados temporários
            self.state_manager.save_user_state(
                phone_number,
                new_state,
                new_step,
                {'name': user_name, 'id': user_id},
                {}
            )
            return self.messages['new_bill_header'] + "\n\n" + self.messages['bill_name'], None, None
        elif message_text == '2':
            # Ver menu principal
            new_state = 'main_menu'
            new_step = None
            self.state_manager.save_user_state(
                phone_number,
                new_state,
                new_step,
                {'name': user_name, 'id': user_id},
                {}
            )
            return self.messages['welcome_return'].format(name=user_name) + "\n" + self.messages['main_menu'], None, None
        elif message_text == '3':
            # Encerrar conversa
            new_state = 'confirm_exit'
            new_step = None
            self.state_manager.save_user_state(
                phone_number,
                new_state,
                new_step,
                {'name': user_name, 'id': user_id},
                {}
            )
            return self.messages['confirm_exit'], None, None
        else:
            return self.messages['error_invalid_option'] + "\n\n" + self.messages['welcome_new'].format(name=user_name), None, None

    def _handle_main_menu(self, phone_number, user_id, user_name, message_text):
        """Gerencia interações no menu principal"""
        # 18. Processar opção do menu principal
        if message_text == '1':
            # Cadastrar conta a pagar
            self.state_manager.save_user_state(
                phone_number,
                'new_bill',
                'name',
                {'name': user_name, 'id': user_id},
                {}
            )
            return self.messages['new_bill_header'] + "\n\n" + self.messages['bill_name'], None, None
        elif message_text == '2':
            # Cadastrar conta a receber
            self.state_manager.save_user_state(
                phone_number,
                'new_receivable',
                'name',
                {'name': user_name, 'id': user_id},
                {}
            )
            return self.messages['new_receivable_header'] + "\n\n" + self.messages['receivable_name'], None, None
        elif message_text == '3':
            # Visualizar contas a pagar
            self.state_manager.save_user_state(
                phone_number,
                'view_bills',
                'select_filter',
                {'name': user_name, 'id': user_id},
                {}
            )
            return self.messages['view_bills'], None, None
        elif message_text == '4':
            # Visualizar contas a receber
            self.state_manager.save_user_state(
                phone_number,
                'view_receivables',
                'select_filter',
                {'name': user_name, 'id': user_id},
                {}
            )
            return self.messages['view_receivables'], None, None
        elif message_text == '5':
            # Marcar como paga/recebida
            self.state_manager.save_user_state(
                phone_number,
                'mark_as_paid',
                'select_type',
                {'name': user_name, 'id': user_id},
                {}
            )
            return "Qual tipo de conta deseja marcar?\n1 💰 Contas a Pagar\n2 💸 Contas a Receber\n0 👈 Voltar", None, None
        elif message_text == '6':
            # Cancelar conta
            self.state_manager.save_user_state(
                phone_number,
                'cancel_bill',
                'select_type',
                {'name': user_name, 'id': user_id},
                {}
            )
            return "Qual tipo de conta deseja cancelar?\n1 💰 Contas a Pagar\n2 💸 Contas a Receber\n0 👈 Voltar", None, None
        elif message_text == '7':
            # Adiar conta
            self.state_manager.save_user_state(
                phone_number,
                'postpone_bill',
                'select_type',
                {'name': user_name, 'id': user_id},
                {}
            )
            return "Qual tipo de conta deseja adiar?\n1 💰 Contas a Pagar\n2 💸 Contas a Receber\n0 👈 Voltar", None, None
        elif message_text == '8':
            # Editar conta
            self.state_manager.save_user_state(
                phone_number,
                'edit_bill',
                'select_type',
                {'name': user_name, 'id': user_id},
                {}
            )
            return "Qual tipo de conta deseja editar?\n1 💰 Contas a Pagar\n2 💸 Contas a Receber\n0 👈 Voltar", None, None
        elif message_text == '9':
            # Buscar conta
            self.state_manager.save_user_state(
                phone_number,
                'search_bill',
                'get_keyword',
                {'name': user_name, 'id': user_id},
                {}
            )
            return self.messages['search_bill'], None, None
        elif message_text == '0':
            # Ajuda
            self.state_manager.save_user_state(
                phone_number,
                'help',
                None,
                {'name': user_name, 'id': user_id},
                {}
            )
            return self.messages['help'], None, None
        elif message_text == '#':
            # Encerrar conversa
            self.state_manager.save_user_state(
                phone_number,
                'confirm_exit',
                None,
                {'name': user_name, 'id': user_id},
                {}
            )
            return self.messages['confirm_exit'], None, None
        else:
            # Opção inválida
            return self.messages['error_invalid_option'] + "\n\n" + self.messages['main_menu'], None, None

    def _handle_new_bill(self, phone_number, user_id, user_name, message_text):
        """Gerencia o fluxo de cadastro de conta a pagar"""
        # Carregar estado do usuário
        user_state = self.state_manager.get_user_state(phone_number)
        current_step = user_state.get('step')
        
        # 19. Cancelamento
        if message_text == '0':
            self.state_manager.save_user_state(
                phone_number,
                'main_menu',
                None,
                {'name': user_name, 'id': user_id},
                {}
            )
            return self.messages['welcome_return'].format(name=user_name) + "\n" + self.messages['main_menu'], None, None
        
        # 20. Processar cada etapa do cadastro
        if current_step == 'name':
            if not message_text or message_text.strip() == '':
                return self.messages['error_invalid_input'], None, None
            
            temp_data = {'name': message_text.strip()}
            self.temp_data[phone_number] = temp_data
            
            self.state_manager.save_user_state(
                phone_number,
                'new_bill',
                'value',
                {'name': user_name, 'id': user_id},
                temp_data
            )
            return self.messages['bill_value'], None, None
        
        elif current_step == 'value':
            try:
                # Remover qualquer caractere não numérico exceto ponto ou vírgula
                clean_value = ''.join(c for c in message_text if c.isdigit() or c in ['.', ','])
                # Substituir vírgula por ponto para conversão correta
                clean_value = clean_value.replace(',', '.')
                # Converter para float
                value = float(clean_value)
                
                if value <= 0:
                    return self.messages['error_invalid_input'] + "\n\n" + self.messages['bill_value'], None, None
                
                temp_data = self.temp_data.get(phone_number, {})
                temp_data['value'] = value
                self.temp_data[phone_number] = temp_data
                
                self.state_manager.save_user_state(
                    phone_number,
                    'new_bill',
                    'due_date',
                    {'name': user_name, 'id': user_id},
                    temp_data
                )
                return self.messages['bill_due_date'], None, None
            except Exception as e:
                print(f"Erro ao processar valor: {e}")
                return self.messages['error_invalid_input'] + "\n\n" + self.messages['bill_value'], None, None
        
        elif current_step == 'due_date':
            # Validar data (simples por enquanto)
            date_match = re.match(r'^(\d{1,2})(?:/(\d{1,2}))?$', message_text)
            if not date_match:
                return self.messages['error_invalid_date'] + "\n\n" + self.messages['bill_due_date'], None, None
            
            day = int(date_match.group(1))
            month = int(date_match.group(2)) if date_match.group(2) else datetime.now().month
            year = datetime.now().year
            
            # Validação básica do dia/mês
            try:
                # Tenta criar um objeto datetime para validar
                valid_date = datetime(year, month, day)
                # Formata a data para dd/mm/yyyy
                formatted_date = valid_date.strftime('%d/%m/%Y') 
            except ValueError:
                return self.messages['error_invalid_date'] + "\n\n" + self.messages['bill_due_date'], None, None

            temp_data = self.temp_data.get(phone_number, {})
            temp_data['due_date'] = formatted_date
            self.temp_data[phone_number] = temp_data
            
            self.state_manager.save_user_state(
                phone_number,
                'new_bill',
                'type',
                {'name': user_name, 'id': user_id},
                temp_data
            )
            return self.messages['bill_type'], None, None
        
        # Implementar os outros passos do fluxo de cadastro de conta a pagar
        # ...
        
        # Fallback para estado desconhecido
        self.state_manager.save_user_state(
            phone_number,
            'main_menu',
            None,
            {'name': user_name, 'id': user_id},
            {}
        )
        return self.messages['welcome_return'].format(name=user_name) + "\n" + self.messages['main_menu'], None, None
    
    # Implementar os outros métodos de manipulação de estados
    def _handle_new_receivable(self, phone_number, user_id, user_name, message_text):
        # Implementação similar ao _handle_new_bill
        return "Função não implementada completamente", None, None
    
    def _handle_view_bills(self, phone_number, user_id, user_name, message_text):
        # Implementação para visualizar contas a pagar
        return "Função não implementada completamente", None, None
    
    def _handle_view_receivables(self, phone_number, user_id, user_name, message_text):
        # Implementação para visualizar contas a receber
        return "Função não implementada completamente", None, None
    
    def _handle_mark_as_paid(self, phone_number, user_id, user_name, message_text):
        # Implementação para marcar conta como paga/recebida
        return "Função não implementada completamente", None, None
    
    def _handle_cancel_bill(self, phone_number, user_id, user_name, message_text):
        # Implementação para cancelar conta
        return "Função não implementada completamente", None, None
    
    def _handle_postpone_bill(self, phone_number, user_id, user_name, message_text):
        # Implementação para adiar conta
        return "Função não implementada completamente", None, None
    
    def _handle_edit_bill(self, phone_number, user_id, user_name, message_text):
        # Implementação para editar conta
        return "Função não implementada completamente", None, None
    
    def _handle_search_bill(self, phone_number, user_id, user_name, message_text):
        # Implementação para buscar conta
        return "Função não implementada completamente", None, None
    
    def _handle_help(self, phone_number, user_id, user_name, message_text):
        # Implementação para ajuda
        if message_text == '0':
            self.state_manager.save_user_state(
                phone_number,
                'main_menu',
                None,
                {'name': user_name, 'id': user_id},
                {}
            )
            return self.messages['welcome_return'].format(name=user_name) + "\n" + self.messages['main_menu'], None, None
        return self.messages['help'], None, None
    
    def _handle_confirm_exit(self, phone_number, user_id, user_name, message_text):
        # Implementação para confirmar saída
        if message_text == '1':
            self.state_manager.save_user_state(
                phone_number,
                'main_menu',  # Voltamos para o menu principal na próxima interação
                None,
                {'name': user_name, 'id': user_id},
                {}
            )
            return self.messages['goodbye'].format(name=user_name), None, None
        elif message_text == '2':
            self.state_manager.save_user_state(
                phone_number,
                'main_menu',
                None,
                {'name': user_name, 'id': user_id},
                {}
            )
            return self.messages['welcome_return'].format(name=user_name) + "\n" + self.messages['main_menu'], None, None
        else:
            return self.messages['error_invalid_option'] + "\n\n"