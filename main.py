"""
main.py
Arquivo principal que gerencia a comunicação entre o bot do WhatsApp e o banco de dados
"""
import json
import sys
import time
from datetime import datetime
import signal
from message_handler import MessageHandler

# 1. Variáveis globais
message_handler = None
processes = {}

# 2. Inicialização e configuração
def initialize():
    """Inicializa os componentes necessários para o funcionamento do bot"""
    global message_handler
    
    print("Inicializando o Bot Penélope...", file=sys.stderr)
    
    try:
        # 3. Inicializar o handler de mensagens
        message_handler = MessageHandler()
        print("Handler de mensagens inicializado com sucesso!", file=sys.stderr)
        
        return True
    except Exception as e:
        print(f"Erro durante a inicialização: {e}", file=sys.stderr)
        return False

# 4. Função para processar mensagens recebidas do WhatsApp (chamada pelo whatsapp_bot.js)
def process_message(phone_number, message):
    """
    Processa uma mensagem recebida do WhatsApp
    Retorna a resposta a ser enviada
    """
    global message_handler
    
    try:
        if message_handler is None:
            if not initialize():
                return "Desculpe, estou temporariamente indisponível. Por favor, tente novamente mais tarde."
        
        # 5. Registrar mensagem recebida para logs
        print(f"Mensagem recebida de {phone_number}: {message}", file=sys.stderr)
        
        # 6. Processar a mensagem e obter resposta
        response, media, media_type = message_handler.process_message(phone_number, message)
        
        # 7. Retornar a resposta formatada como JSON para o bot do WhatsApp
        result = {
            "text": response,
            "media": media,
            "media_type": media_type
        }
        
        return json.dumps(result)
    
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}", file=sys.stderr)
        return json.dumps({
            "text": "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.",
            "media": None,
            "media_type": None
        })

# 8. Verificar inatividade e enviar mensagens de lembrete
def check_inactivity():
    """Verifica usuários inativos e envia mensagem de lembrete"""
    global message_handler
    
    try:
        if message_handler is None:
            return
        
        current_time = datetime.now()
        inactive_timeout = 300  # 5 minutos em segundos
        
        for phone_number, state in message_handler.user_states.items():
            last_activity = state.get('last_activity')
            if last_activity is None:
                continue
            
            # Calcular tempo de inatividade
            elapsed = (current_time - last_activity).total_seconds()
            
            # Se inativo por mais de 5 minutos e ainda não notificado
            if elapsed > inactive_timeout and not state.get('inactivity_notified', False):
                user_name = state.get('data', {}).get('name', 'Cliente')
                
                # Preparar mensagem de inatividade
                inactivity_message = message_handler.messages['inactivity'].format(name=user_name)
                
                # Marcar como notificado para não enviar múltiplas vezes
                message_handler.user_states[phone_number]['inactivity_notified'] = True
                
                # Aqui enviaria mensagem para o javascript (usando um método de comunicação como stdout)
                print(f"INACTIVITY_NOTIFY|{phone_number}|{inactivity_message}")
                sys.stdout.flush()
    
    except Exception as e:
        print(f"Erro ao verificar inatividade: {e}", file=sys.stderr)

# 9. Manipulador de sinais para encerramento gracioso
def signal_handler(sig, frame):
    """Manipula sinais de encerramento"""
    print("Encerrando o Bot Penélope...", file=sys.stderr)
    # Realizar limpeza se necessário
    sys.exit(0)

# 10. Função principal
def main():
    """Função principal"""
    # Inicializar componentes
    if not initialize():
        print("Falha na inicialização. Encerrando...", file=sys.stderr)
        sys.exit(1)
    
    # Configurar manipulador de sinais
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("Bot Penélope iniciado e pronto para processar mensagens!", file=sys.stderr)
    
    # Loop principal (apenas para verificação de inatividade)
    # O processamento real das mensagens é feito sob demanda pelo WhatsApp
    try:
        while True:
            # Verificar inatividade
            check_inactivity()
            
            # Aguardar um pouco antes da próxima verificação
            time.sleep(60)  # Verifica a cada 1 minuto
    
    except KeyboardInterrupt:
        print("Interrompido pelo usuário. Encerrando...", file=sys.stderr)
    
    except Exception as e:
        print(f"Erro no loop principal: {e}", file=sys.stderr)
    
    finally:
        print("Bot Penélope encerrado.", file=sys.stderr)

# 11. Ponto de entrada para execução direta
if __name__ == "__main__":
    main()
