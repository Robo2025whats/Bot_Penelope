# Bot Penélope - Assistente de Contas a Pagar e Receber

Penélope é um chatbot para WhatsApp que ajuda a gerenciar contas a pagar e receber, permitindo cadastrar, visualizar, editar e monitorar seus compromissos financeiros.

## 📋 Recursos

- Cadastro de contas a pagar e receber
- Visualização de contas por mês, data, status ou método de pagamento
- Marcar contas como pagas/recebidas
- Cancelar ou adiar compromissos
- Editar informações de contas
- Busca por nome da conta
- Interface amigável via WhatsApp

## 🛠️ Tecnologias Utilizadas

- **Python**: Processamento principal e lógica de negócios
- **JavaScript**: Integração com WhatsApp
- **Supabase**: Banco de dados PostgreSQL
- **WhatsApp-web.js**: Biblioteca para integração com WhatsApp

## 🚀 Instalação

### Pré-requisitos

- Node.js (v14 ou superior)
- Python 3.8+
- NPM ou Yarn
- Conta no WhatsApp para o bot

### Passos de Instalação

1. **Clone o repositório**:
   ```
   git clone <seu-repositorio>
   cd bot_contas
   ```

2. **Instale as dependências do Node.js**:
   ```
   npm install
   ```

3. **Instale as dependências do Python**:
   ```
   pip install -r requirements.txt
   ```

4. **Configure o arquivo config.json**:
   O arquivo já está configurado com suas credenciais do Supabase.

5. **Inicie o bot**:
   ```
   npm start
   ```

6. **Escaneie o QR Code**:
   Quando o bot iniciar, será exibido um QR Code no terminal. Escaneie-o com seu WhatsApp seguindo estas etapas:
   - Abra o WhatsApp no seu celular
   - Toque nos três pontos ⋮ no canto superior direito
   - Selecione "WhatsApp Web"
   - Aponte a câmera para o QR Code no terminal

## 💬 Como usar o bot

Uma vez conectado, qualquer pessoa que enviar uma mensagem para o número do WhatsApp vinculado ao bot receberá uma resposta automática da Penélope, que guiará sobre como utilizar o serviço.

### Comandos iniciais:

1. A Penélope se apresentará e pedirá seu nome na primeira interação
2. Após o cadastro, você poderá escolher entre:
   - Cadastrar contas a pagar
   - Cadastrar contas a receber
   - Visualizar suas contas
   - Gerenciar contas existentes

## 📌 Estrutura do Projeto

- `whatsapp_bot.js`: Integração com WhatsApp
- `main.py`: Código principal para gerenciamento do bot
- `database.py`: Comunicação com Supabase
- `message_handler.py`: Processamento das mensagens
- `config.json`: Configurações e credenciais
- `requirements.txt`: Dependências Python
- `package.json`: Dependências Node.js

## 🔒 Segurança

- As credenciais do Supabase estão no arquivo config.json
- O bot armazena a sessão localmente no diretório './session_data'
- Não compartilhe seu QR Code com ninguém

## 📋 Resolução de Problemas

1. **QR Code expirou**:
   - Reinicie o bot com `npm start`

2. **Erro de conexão com o Supabase**:
   - Verifique se as credenciais no arquivo config.json estão corretas

3. **Erro de dependências**:
   - Verifique se todas as dependências foram instaladas corretamente

4. **Bot não responde**:
   - Verifique se o WhatsApp do bot está conectado
   - Verifique logs de erro no terminal

## 🤝 Suporte

Para problemas, dúvidas ou sugestões, entre em contato pelo WhatsApp ou crie uma issue no repositório.
