# message_manager.py
"""
message_manager.py
Gerencia as mensagens e interações com o banco de dados
"""
import json
import re

class MessageManager:
    """Classe para gerenciar as mensagens e interações do bot Penélope"""
    
    def __init__(self):
        """Inicializa o gerenciador de mensagens"""
        from database import SupabaseManager  # Mover a importação aqui
        from message_templates import MESSAGES
        from state_manager import StateManager  # Mover a importação aqui

        self.db = SupabaseManager()
        self.state_manager = StateManager()
        self.temp_data = {}
        self.user_states = {}
        self.load_message_templates()

    def load_message_templates(self):
        """Carrega as mensagens pré-definidas do bot"""
        self.messages = MESSAGES

    # Resto do código...
# message_manager.py
"""
message_manager.py
Gerencia as mensagens e interações com o banco de dados
"""
import json
import re
from database import SupabaseManager
from message_templates import MESSAGES
from state_manager import StateManager

class MessageManager:
    """Classe para gerenciar as mensagens e interações do bot Penélope"""
    
    def __init__(self):
        """Inicializa o gerenciador de mensagens"""
        self.db = SupabaseManager()
        self.state_manager = StateManager()
        self.temp_data = {}
        self.user_states = {}
        self.load_message_templates()

    def load_message_templates(self):
        """Carrega as mensagens pré-definidas do bot"""
        self.messages = MESSAGES

    def process_message(self, phone_number, message_text):
        """
        Processa uma mensagem recebida e retorna a resposta
        Retorna uma tupla (resposta, mídia, tipo_de_mídia)
        """
        try:
            # Verifica se o usuário já está cadastrado
            exists, user_data = self.db.check_cliente_exists(phone_number)
            if not exists:
                return self._handle_new_user(phone_number, message_text)

            user_id = user_data['id']
            user_name = user_data['nome']
            user_state = self.state_manager.get_user_state(phone_number)
            current_state = user_state.get('state', 'main_menu')

            response = self._handle_state(phone_number, user_id, user_name, current_state, message_text)
            self.state_manager.save_user_state(phone_number, current_state, None, {'name': user_name, 'id': user_id}, self.temp_data.get(phone_number, {}))
            return response
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.", None, None

    def _handle_new_user(self, phone_number, message_text):
        """Gerencia a interação com novos usuários"""
        if not message_text or message_text.strip() == '':
            return self.messages['greeting_new'], None, None
        
        name = message_text.strip()
        success, user_data = self.db.create_cliente(name, phone_number)
        
        if not success or not user_data:
            return "Desculpe, ocorreu um erro ao cadastrar seu usuário. Por favor, tente novamente mais tarde.", None, None
        
        user_id = user_data['id']
        self.state_manager.save_new_user_state(phone_number, name, user_id)
        return self.messages['welcome_new'].format(name=name), None, None

    def _handle_state(self, phone_number, user_id, user_name, current_state, message_text):
        """Processa a mensagem com base no estado atual do usuário"""
        if current_state == 'main_menu':
            return self._handle_main_menu(phone_number, user_id, user_name, message_text)
        # Adicione outros estados conforme necessário
        return "Estado não reconhecido.", None, None

    def _handle_main_menu(self, phone_number, user_id, user_name, message_text):
        """Gerencia interações no menu principal"""
        if message_text == '1':
            self.temp_data[phone_number] = {}
            return "📝 *Nome da conta:* (Ex: Aluguel, Energia, Internet)", None, None
        elif message_text == '2':
            self.temp_data[phone_number] = {}
            return "💰 *Nome do recebível:* (Ex: Salário, Freelance, Aluguel)", None, None
        # Adicione outras opções do menu principal
        return "Opção inválida. Escolha um número entre as opções disponíveis.", None, None

# Função principal para testar o gerenciador de mensagens
if __name__ == "__main__":
    manager = MessageManager()
    # Teste com um número de telefone e uma mensagem
    response = manager.process_message("+5511999999999", "João")
    print(response)