"""
database.py
Gerencia a conexão e operações com o banco de dados Supabase
"""
import sys
import json
import os
from datetime import datetime, date
from supabase import create_client, Client

class SupabaseManager:
    """Classe para gerenciar a conexão e operações com o Supabase"""
    
    def __init__(self):
        """Inicializa o cliente Supabase com as credenciais do arquivo config.json"""
        # 1. Carrega as configurações do arquivo config.json
        try:
            with open('config.json', 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
                self.url = config['supabase']['url']
                self.key = config['supabase']['key']
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}", file=sys.stderr)
            raise
        
        # 2. Inicializa o cliente Supabase
        try:
            self.supabase: Client = create_client(self.url, self.key)
            print("Conexão com o Supabase estabelecida com sucesso!", file=sys.stderr)
        except Exception as e:
            print(f"Erro ao conectar ao Supabase: {e}", file=sys.stderr)
            raise
    
    # GERENCIAMENTO DE CLIENTES
    
    def check_cliente_exists(self, celular):
        """Verifica se um cliente existe pelo número de celular"""
        # 3. Consulta na tabela clientes
        try:
            response = self.supabase.table('clientes').select('*').eq('celular', celular).execute()
            return len(response.data) > 0, response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao verificar cliente: {e}", file=sys.stderr)
            return False, None
    
    def create_cliente(self, nome, celular, email=''):
        """Cria um novo cliente no banco de dados"""
        # 4. Insere um novo cliente
        try:
            data = {
                'nome': nome,
                'celular': celular,
                'email': email
            }
            response = self.supabase.table('clientes').insert(data).execute()
            return True, response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao criar cliente: {e}", file=sys.stderr)
            return False, None
    
    # GERENCIAMENTO DE CONTAS A PAGAR
    
    def add_conta_pagar(self, cliente_id, nome, valor, data_vencimento, 
                       tipo_conta_id, sazonalidade_id, metodo_pagamento_id, observacao=''):
        """Adiciona uma nova conta a pagar"""
        # 5. Insere uma nova conta a pagar
        try:
            # Converter data_vencimento para objeto date se for string
            if isinstance(data_vencimento, str):
                # Verifica o formato (DD ou DD/MM)
                if '/' in data_vencimento:
                    day, month = map(int, data_vencimento.split('/'))
                    year = datetime.now().year
                    # Se o mês for anterior ao mês atual, assumimos que é para o próximo ano
                    if month < datetime.now().month:
                        year += 1
                    data_vencimento = date(year, month, day)
                else:
                    # Apenas o dia foi fornecido, usamos o mês atual
                    day = int(data_vencimento)
                    month = datetime.now().month
                    year = datetime.now().year
                    # Se o dia for anterior ao dia atual, assumimos que é para o próximo mês
                    if day < datetime.now().day:
                        month += 1
                        if month > 12:
                            month = 1
                            year += 1
                    data_vencimento = date(year, month, day)
            
            # Status inicial é sempre pendente (id=1)
            status_id = 1
            
            data = {
                'nome': nome,
                'valor': float(valor),
                'data_vencimento': data_vencimento.isoformat() if isinstance(data_vencimento, date) else data_vencimento,
                'status_id': status_id,
                'tipo_conta_id': tipo_conta_id,
                'sazonalidade_id': sazonalidade_id,
                'metodo_pagamento_id': metodo_pagamento_id,
                'observacao': observacao,
                'cliente_id': cliente_id,
                'criado_por': cliente_id
            }
            
            response = self.supabase.table('contas_pagar').insert(data).execute()
            return True, response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao adicionar conta a pagar: {e}", file=sys.stderr)
            return False, str(e)
    
    def add_conta_receber(self, cliente_id, nome, valor, data_vencimento, 
                         tipo_conta_id, sazonalidade_id, metodo_pagamento_id, observacao=''):
        """Adiciona uma nova conta a receber"""
        # 6. Insere uma nova conta a receber
        try:
            # Converter data_vencimento para objeto date se for string (mesmo tratamento da função anterior)
            if isinstance(data_vencimento, str):
                if '/' in data_vencimento:
                    day, month = map(int, data_vencimento.split('/'))
                    year = datetime.now().year
                    if month < datetime.now().month:
                        year += 1
                    data_vencimento = date(year, month, day)
                else:
                    day = int(data_vencimento)
                    month = datetime.now().month
                    year = datetime.now().year
                    if day < datetime.now().day:
                        month += 1
                        if month > 12:
                            month = 1
                            year += 1
                    data_vencimento = date(year, month, day)
            
            # Status inicial é sempre pendente (id=1)
            status_id = 1
            
            data = {
                'nome': nome,
                'valor': float(valor),
                'data_vencimento': data_vencimento.isoformat() if isinstance(data_vencimento, date) else data_vencimento,
                'status_id': status_id,
                'tipo_conta_id': tipo_conta_id,
                'sazonalidade_id': sazonalidade_id,
                'metodo_pagamento_id': metodo_pagamento_id,
                'observacao': observacao,
                'cliente_id': cliente_id,
                'criado_por': cliente_id
            }
            
            response = self.supabase.table('contas_receber').insert(data).execute()
            return True, response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao adicionar conta a receber: {e}", file=sys.stderr)
            return False, str(e)
    
    # CONSULTA DE CONTAS
    
    def get_contas_pagar(self, cliente_id, filtro='mes_atual'):
        """Obtém as contas a pagar com filtro específico"""
        # 7. Consulta contas a pagar com diferentes filtros
        try:
            query = self.supabase.table('contas_pagar').select(
                'id, nome, valor, data_vencimento, status_id, tipo_conta_id, sazonalidade_id, metodo_pagamento_id, observacao'
            ).eq('cliente_id', cliente_id)
            
            hoje = datetime.now().date()
            primeiro_dia_mes = date(hoje.year, hoje.month, 1)
            
            # Aplicar o filtro selecionado
            if filtro == 'mes_atual':
                # Contas do mês atual
                proximo_mes = hoje.month + 1
                proximo_ano = hoje.year
                if proximo_mes > 12:
                    proximo_mes = 1
                    proximo_ano += 1
                ultimo_dia_mes = date(proximo_ano, proximo_mes, 1)
                query = query.gte('data_vencimento', primeiro_dia_mes.isoformat())
                query = query.lt('data_vencimento', ultimo_dia_mes.isoformat())
            elif filtro == 'vencimento_hoje':
                # Contas com vencimento hoje
                query = query.eq('data_vencimento', hoje.isoformat())
            elif filtro == 'pendentes':
                # Todas pendentes (status_id = 1)
                query = query.eq('status_id', 1)
            elif filtro == 'status':
                # Filtro por status será aplicado na chamada da função
                pass
            elif filtro == 'metodo_pagamento':
                # Filtro por método de pagamento será aplicado na chamada da função
                pass
                
            response = query.execute()
            
            # Buscar informações adicionais para cada conta
            result = []
            for conta in response.data:
                # Obter nome do status
                status_response = self.supabase.table('status_conta').select('nome').eq('id', conta['status_id']).execute()
                status_nome = status_response.data[0]['nome'] if status_response.data else 'desconhecido'
                
                # Obter nome do tipo de conta
                tipo_response = self.supabase.table('tipo_conta').select('nome').eq('id', conta['tipo_conta_id']).execute()
                tipo_nome = tipo_response.data[0]['nome'] if tipo_response.data else 'desconhecido'
                
                # Obter nome da sazonalidade
                sazonalidade_response = self.supabase.table('sazonalidade').select('nome').eq('id', conta['sazonalidade_id']).execute()
                sazonalidade_nome = sazonalidade_response.data[0]['nome'] if sazonalidade_response.data else 'desconhecido'
                
                # Obter nome do método de pagamento
                metodo_response = self.supabase.table('metodos_pagamento').select('nome').eq('id', conta['metodo_pagamento_id']).execute()
                metodo_nome = metodo_response.data[0]['nome'] if metodo_response.data else 'desconhecido'
                
                # Adicionar esses campos ao resultado
                conta['status_nome'] = status_nome
                conta['tipo_nome'] = tipo_nome
                conta['sazonalidade_nome'] = sazonalidade_nome
                conta['metodo_nome'] = metodo_nome
                
                result.append(conta)
                
            return True, result
        except Exception as e:
            print(f"Erro ao consultar contas a pagar: {e}", file=sys.stderr)
            return False, str(e)
    
    def get_contas_receber(self, cliente_id, filtro='mes_atual'):
        """Obtém as contas a receber com filtro específico"""
        # 8. Consulta contas a receber com diferentes filtros
        try:
            query = self.supabase.table('contas_receber').select(
                'id, nome, valor, data_vencimento, status_id, tipo_conta_id, sazonalidade_id, metodo_pagamento_id, observacao'
            ).eq('cliente_id', cliente_id)
            
            hoje = datetime.now().date()
            primeiro_dia_mes = date(hoje.year, hoje.month, 1)
            
            # Aplicar o filtro selecionado (mesmo tratamento da função anterior)
            if filtro == 'mes_atual':
                proximo_mes = hoje.month + 1
                proximo_ano = hoje.year
                if proximo_mes > 12:
                    proximo_mes = 1
                    proximo_ano += 1
                ultimo_dia_mes = date(proximo_ano, proximo_mes, 1)
                query = query.gte('data_vencimento', primeiro_dia_mes.isoformat())
                query = query.lt('data_vencimento', ultimo_dia_mes.isoformat())
            elif filtro == 'vencimento_hoje':
                query = query.eq('data_vencimento', hoje.isoformat())
            elif filtro == 'pendentes':
                query = query.eq('status_id', 1)
            elif filtro == 'status':
                pass
            elif filtro == 'metodo_pagamento':
                pass
                
            response = query.execute()
            
            # Buscar informações adicionais para cada conta
            result = []
            for conta in response.data:
                # Buscar nomes de status, tipo, sazonalidade e método (mesmo tratamento da função anterior)
                status_response = self.supabase.table('status_conta').select('nome').eq('id', conta['status_id']).execute()
                status_nome = status_response.data[0]['nome'] if status_response.data else 'desconhecido'
                
                tipo_response = self.supabase.table('tipo_conta').select('nome').eq('id', conta['tipo_conta_id']).execute()
                tipo_nome = tipo_response.data[0]['nome'] if tipo_response.data else 'desconhecido'
                
                sazonalidade_response = self.supabase.table('sazonalidade').select('nome').eq('id', conta['sazonalidade_id']).execute()
                sazonalidade_nome = sazonalidade_response.data[0]['nome'] if sazonalidade_response.data else 'desconhecido'
                
                metodo_response = self.supabase.table('metodos_pagamento').select('nome').eq('id', conta['metodo_pagamento_id']).execute()
                metodo_nome = metodo_response.data[0]['nome'] if metodo_response.data else 'desconhecido'
                
                conta['status_nome'] = status_nome
                conta['tipo_nome'] = tipo_nome
                conta['sazonalidade_nome'] = sazonalidade_nome
                conta['metodo_nome'] = metodo_nome
                
                result.append(conta)
                
            return True, result
        except Exception as e:
            print(f"Erro ao consultar contas a receber: {e}", file=sys.stderr)
            return False, str(e)
    
    # ATUALIZAÇÃO DE STATUS DE CONTAS
    
    def _atualizar_status_conta(self, tabela, conta_id, novo_status_id, cliente_id):
        """Função interna para atualizar o status de uma conta"""
        # 9. Atualização genérica de status
        try:
            # Primeiro obter o status atual
            response = self.supabase.table(tabela).select('status_id').eq('id', conta_id).execute()
            if not response.data:
                return False, "Conta não encontrada"
            
            status_anterior = response.data[0]['status_id']
            
            # Atualizar o status
            self.supabase.table(tabela).update({'status_id': novo_status_id}).eq('id', conta_id).execute()
            
            # Registrar no histórico
            tipo_conta = 'pagar' if tabela == 'contas_pagar' else 'receber'
            historico = {
                'conta_tipo': tipo_conta,
                'conta_id': conta_id,
                'status_anterior': status_anterior,
                'status_novo': novo_status_id,
                'usuario_id': cliente_id,
                'observacao': f"Status alterado de {status_anterior} para {novo_status_id}"
            }
            self.supabase.table('historico_status').insert(historico).execute()
            
            return True, None
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
            return False, str(e)
    
    def marcar_como_paga(self, conta_id, cliente_id):
        """Marca uma conta a pagar como paga (status_id=2)"""
        # 10. Marca conta como paga
        return self._atualizar_status_conta('contas_pagar', conta_id, 2, cliente_id)
    
    def marcar_como_recebida(self, conta_id, cliente_id):
        """Marca uma conta a receber como recebida (status_id=2)"""
        # 11. Marca conta como recebida
        return self._atualizar_status_conta('contas_receber', conta_id, 2, cliente_id)
    
    def cancelar_conta_pagar(self, conta_id, cliente_id):
        """Cancela uma conta a pagar (status_id=4)"""
        # 12. Cancela conta a pagar
        return self._atualizar_status_conta('contas_pagar', conta_id, 4, cliente_id)
    
    def cancelar_conta_receber(self, conta_id, cliente_id):
        """Cancela uma conta a receber (status_id=4)"""
        # 13. Cancela conta a receber
        return self._atualizar_status_conta('contas_receber', conta_id, 4, cliente_id)
    
    def adiar_conta_pagar(self, conta_id, nova_data, cliente_id):
        """Adia uma conta a pagar (status_id=5) e atualiza a data"""
        # 14. Adia conta a pagar
        try:
            # Converter nova_data para formato ISO se for string
            if isinstance(nova_data, str):
                if '/' in nova_data:
                    day, month = map(int, nova_data.split('/'))
                    year = datetime.now().year
                    if month < datetime.now().month:
                        year += 1
                    nova_data = date(year, month, day).isoformat()
                else:
                    day = int(nova_data)
                    month = datetime.now().month
                    year = datetime.now().year
                    if day < datetime.now().day:
                        month += 1
                        if month > 12:
                            month = 1
                            year += 1
                    nova_data = date(year, month, day).isoformat()
            
            # Primeiro obter o status atual e a data atual
            response = self.supabase.table('contas_pagar').select('status_id, data_vencimento').eq('id', conta_id).execute()
            if not response.data:
                return False, "Conta não encontrada"
            
            status_anterior = response.data[0]['status_id']
            data_anterior = response.data[0]['data_vencimento']
            
            # Atualizar o status e a data
            self.supabase.table('contas_pagar').update({
                'status_id': 5,  # Status de adiada
                'data_vencimento': nova_data
            }).eq('id', conta_id).execute()
            
            # Registrar no histórico
            historico = {
                'conta_tipo': 'pagar',
                'conta_id': conta_id,
                'status_anterior': status_anterior,
                'status_novo': 5,
                'usuario_id': cliente_id,
                'observacao': f"Conta adiada de {data_anterior} para {nova_data}"
            }
            self.supabase.table('historico_status').insert(historico).execute()
            
            return True, None
        except Exception as e:
            print(f"Erro ao adiar conta: {e}")
            return False, str(e)
    
    def adiar_conta_receber(self, conta_id, nova_data, cliente_id):
        """Adia uma conta a receber (status_id=5) e atualiza a data"""
        # 15. Adia conta a receber
        try:
            # Converter nova_data para formato ISO se for string (mesmo tratamento da função anterior)
            if isinstance(nova_data, str):
                if '/' in nova_data:
                    day, month = map(int, nova_data.split('/'))
                    year = datetime.now().year
                    if month < datetime.now().month:
                        year += 1
                    nova_data = date(year, month, day).isoformat()
                else:
                    day = int(nova_data)
                    month = datetime.now().month
                    year = datetime.now().year
                    if day < datetime.now().day:
                        month += 1
                        if month > 12:
                            month = 1
                            year += 1
                    nova_data = date(year, month, day).isoformat()
            
            # Primeiro obter o status atual e a data atual
            response = self.supabase.table('contas_receber').select('status_id, data_vencimento').eq('id', conta_id).execute()
            if not response.data:
                return False, "Conta não encontrada"
            
            status_anterior = response.data[0]['status_id']
            data_anterior = response.data[0]['data_vencimento']
            
            # Atualizar o status e a data
            self.supabase.table('contas_receber').update({
                'status_id': 5,  # Status de adiada
                'data_vencimento': nova_data
            }).eq('id', conta_id).execute()
            
            # Registrar no histórico
            historico = {
                'conta_tipo': 'receber',
                'conta_id': conta_id,
                'status_anterior': status_anterior,
                'status_novo': 5,
                'usuario_id': cliente_id,
                'observacao': f"Conta adiada de {data_anterior} para {nova_data}"
            }
            self.supabase.table('historico_status').insert(historico).execute()
            
            return True, None
        except Exception as e:
            print(f"Erro ao adiar conta: {e}")
            return False, str(e)
    
    # FUNÇÕES DE BUSCA E EDIÇÃO
    
    def buscar_conta_por_nome(self, cliente_id, tipo_conta, termo_busca):
        """Busca contas por nome"""
        # 16. Busca conta por nome/termo
        try:
            tabela = 'contas_pagar' if tipo_conta == 'pagar' else 'contas_receber'
            
            # Usamos o operador ilike para busca case-insensitive
            response = self.supabase.table(tabela).select(
                'id, nome, valor, data_vencimento, status_id, tipo_conta_id, sazonalidade_id, metodo_pagamento_id, observacao'
            ).eq('cliente_id', cliente_id).ilike('nome', f'%{termo_busca}%').execute()
            
            # Buscar informações adicionais para cada conta
            result = []
            for conta in response.data:
                # Buscar nomes de status, tipo, sazonalidade e método
                status_response = self.supabase.table('status_conta').select('nome').eq('id', conta['status_id']).execute()
                status_nome = status_response.data[0]['nome'] if status_response.data else 'desconhecido'
                
                tipo_response = self.supabase.table('tipo_conta').select('nome').eq('id', conta['tipo_conta_id']).execute()
                tipo_nome = tipo_response.data[0]['nome'] if tipo_response.data else 'desconhecido'
                
                sazonalidade_response = self.supabase.table('sazonalidade').select('nome').eq('id', conta['sazonalidade_id']).execute()
                sazonalidade_nome = sazonalidade_response.data[0]['nome'] if sazonalidade_response.data else 'desconhecido'
                
                metodo_response = self.supabase.table('metodos_pagamento').select('nome').eq('id', conta['metodo_pagamento_id']).execute()
                metodo_nome = metodo_response.data[0]['nome'] if metodo_response.data else 'desconhecido'
                
                conta['status_nome'] = status_nome
                conta['tipo_nome'] = tipo_nome
                conta['sazonalidade_nome'] = sazonalidade_nome
                conta['metodo_nome'] = metodo_nome
                
                result.append(conta)
                
            return True, result
        except Exception as e:
            print(f"Erro ao buscar conta: {e}")
            return False, str(e)
    
    def editar_campo_conta(self, tipo_conta, conta_id, campo, novo_valor, cliente_id):
        """Edita um campo específico de uma conta"""
        # 17. Edita campo de conta
        try:
            tabela = 'contas_pagar' if tipo_conta == 'pagar' else 'contas_receber'
            
            # Primeiro obter o valor atual do campo
            response = self.supabase.table(tabela).select(campo).eq('id', conta_id).execute()
            if not response.data:
                return False, "Conta não encontrada"
            
            valor_anterior = response.data[0][campo]
            
            # Preparar o valor para atualização
            if campo == 'valor' and isinstance(novo_valor, str):
                novo_valor = float(novo_valor.replace(',', '.'))
            
            if campo == 'data_vencimento' and isinstance(novo_valor, str):
                if '/' in novo_valor:
                    day, month = map(int, novo_valor.split('/'))
                    year = datetime.now().year
                    if month < datetime.now().month:
                        year += 1
                    novo_valor = date(year, month, day).isoformat()
                else:
                    day = int(novo_valor)
                    month = datetime.now().month
                    year = datetime.now().year
                    if day < datetime.now().day:
                        month += 1
                        if month > 12:
                            month = 1
                            year += 1
                    novo_valor = date(year, month, day).isoformat()
            
            # Atualizar o campo
            self.supabase.table(tabela).update({campo: novo_valor}).eq('id', conta_id).execute()
            
            # Registrar no histórico se for uma alteração de status
            if campo == 'status_id':
                historico = {
                    'conta_tipo': tipo_conta,
                    'conta_id': conta_id,
                    'status_anterior': valor_anterior,
                    'status_novo': novo_valor,
                    'usuario_id': cliente_id,
                    'observacao': f"Status alterado de {valor_anterior} para {novo_valor}"
                }
                self.supabase.table('historico_status').insert(historico).execute()
            
            return True, None
        except Exception as e:
            print(f"Erro ao editar conta: {e}")
            return False, str(e)
    
    # FUNÇÕES DE UTILIDADE
    
    def get_all_categorias(self):
        """Obtém todas as categorias disponíveis (tipo, sazonalidade, método de pagamento)"""
        # 18. Obtém todas as categorias para o cadastro de contas
        try:
            tipos = self.supabase.table('tipo_conta').select('id, nome').execute()
            sazonalidades = self.supabase.table('sazonalidade').select('id, nome').execute()
            metodos = self.supabase.table('metodos_pagamento').select('id, nome').execute()
            status = self.supabase.table('status_conta').select('id, nome').execute()
            
            return {
                'tipos': tipos.data,
                'sazonalidades': sazonalidades.data,
                'metodos': metodos.data,
                'status': status.data
            }
        except Exception as e:
            print(f"Erro ao obter categorias: {e}")
            return {}

    # ATUALIZAÇÃO DE STATUS DE CONTAS