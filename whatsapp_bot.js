/**
 * whatsapp_bot.js
 * Bot para WhatsApp usando a biblioteca whatsapp-web.js
 * Comunica-se com a camada Python para processamento de mensagens
 */

// 1. Importações necessárias
const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const { spawn } = require('child_process');
const path = require('path');

// 2. Carregar configurações
let config;
try {
    config = JSON.parse(fs.readFileSync('config.json', 'utf8'));
} catch (error) {
    console.error('Erro ao carregar arquivo de configuração:', error);
    process.exit(1);
}

// 3. Variáveis globais
let pythonProcess = null;
const botName = config.whatsapp.bot_name || 'Penélope';
const sessionDataPath = config.whatsapp.session_data_path || './session_data';
const qrTimeout = config.whatsapp.qr_timeout || 60000;
const BOT_NUMBER = ''; // Preencha com o número do bot para evitar auto-resposta

// 4. Configuração do cliente WhatsApp
const client = new Client({
    authStrategy: new LocalAuth({
        dataPath: sessionDataPath
    }),
    puppeteer: {
        headless: true, // True para produção, false para depuração
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--disable-gpu'
        ]
    }
});

// 5. Iniciar processo Python
function startPythonProcess() {
    try {
        console.log('Iniciando processo Python...');
        pythonProcess = spawn('python', ['main.py']);
        
        pythonProcess.stdout.on('data', (data) => {
            const output = data.toString().trim();
            
            // Verificar se é uma notificação de inatividade
            if (output.startsWith('INACTIVITY_NOTIFY|')) {
                const parts = output.split('|');
                if (parts.length >= 3) {
                    const phoneNumber = parts[1];
                    const message = parts.slice(2).join('|');
                    sendMessage(phoneNumber, message);
                }
            } else {
                console.log(`Python stdout: ${output}`);
            }
        });
        
        pythonProcess.stderr.on('data', (data) => {
            console.error(`Python stderr: ${data}`);
        });
        
        pythonProcess.on('close', (code) => {
            console.log(`Processo Python finalizado com código ${code}`);
            // Reiniciar processo Python se ele terminar
            if (code !== 0) {
                console.log('Tentando reiniciar o processo Python...');
                setTimeout(startPythonProcess, 5000);
            }
        });
        
        console.log('Processo Python iniciado com sucesso!');
    } catch (error) {
        console.error('Erro ao iniciar processo Python:', error);
    }
}

// 6. Comunicação com Python para processar mensagens
function processPythonMessage(phoneNumber, message) {
    return new Promise((resolve, reject) => {
        try {
            // Verificar se o processo Python está rodando
            if (!pythonProcess || pythonProcess.killed) {
                startPythonProcess();
                // Aguardar um pouco para o processo iniciar
                setTimeout(() => {
                    callPythonFunction(phoneNumber, message, resolve, reject);
                }, 1000);
            } else {
                callPythonFunction(phoneNumber, message, resolve, reject);
            }
        } catch (error) {
            reject(`Erro ao processar mensagem com Python: ${error}`);
        }
    });
}

// 7. Chamar a função Python para processar a mensagem
function callPythonFunction(phoneNumber, message, resolve, reject) {
    try {
        // Criar um processo separado para cada chamada
        // Corrigir barras invertidas para compatibilidade com Windows
        const correctedDirname = __dirname.replace(/\\/g, '/');
        const pythonCall = spawn('python', ['-c', 
            `import sys; sys.path.append('${correctedDirname}'); import main; print(main.process_message('${phoneNumber}', """${message}"""))`
        ]);
        
        let responseData = '';
        
        pythonCall.stdout.on('data', (data) => {
            responseData += data.toString();
        });
        
        pythonCall.stderr.on('data', (data) => {
            console.log(`Log Python: ${data}`);
        });
        
        pythonCall.on('close', (code) => {
            if (code === 0) {
                try {
                    // Limpar e processar a resposta JSON
                    responseData = responseData.trim();
                    const jsonResponse = JSON.parse(responseData);
                    resolve(jsonResponse);
                } catch (error) {
                    console.error('Erro ao processar resposta JSON:', error, 'Resposta:', responseData);
                    reject('Erro ao processar resposta do servidor');
                }
            } else {
                reject(`Processo Python encerrou com código ${code}`);
            }
        });
    } catch (error) {
        reject(`Erro ao chamar função Python: ${error}`);
    }
}

// 8. Enviar mensagem para o WhatsApp
async function sendMessage(to, text, media = null, mediaType = null) {
    try {
        // Normalizar número de telefone (remover espaços, traços, etc.)
        const normalizedNumber = normalizePhoneNumber(to);
        
        // Verificar se o chat existe
        const chat = await client.getChatById(`${normalizedNumber}@c.us`);
        
        // Se tiver mídia, enviar como arquivo ou imagem
        if (media && mediaType) {
            // Converter mídia para formato WhatsApp
            const attachMedia = new MessageMedia(mediaType, media, 'attachment');
            await chat.sendMessage(attachMedia, { caption: text });
        } else {
            // Enviar apenas texto
            await chat.sendMessage(text);
        }
        
        console.log(`Mensagem enviada para ${normalizedNumber}: ${text.substring(0, 50)}...`);
        return true;
    } catch (error) {
        console.error(`Erro ao enviar mensagem para ${to}:`, error);
        return false;
    }
}

// 9. Normalizar número de telefone
function normalizePhoneNumber(number) {
    // Remover qualquer caractere não numérico
    let normalized = number.replace(/\D/g, '');
    
    // Verificar se tem código de país
    if (!normalized.startsWith('55')) {
        normalized = '55' + normalized;
    }
    
    return normalized;
}

// 10. Eventos do WhatsApp Web Client

// Evento: QR Code gerado
client.on('qr', (qr) => {
    console.log('QR CODE GERADO. Escaneie com seu telefone:');
    qrcode.generate(qr, { small: true });
    
    // Definir timeout para QR Code
    setTimeout(() => {
        if (!client.info) {
            console.log('Tempo limite para escanear o QR Code excedido.');
            process.exit(1);
        }
    }, qrTimeout);
});

// Evento: Cliente pronto
client.on('ready', () => {
    console.log(`Bot ${botName} está pronto e conectado ao WhatsApp!`);
    // Iniciar o processo Python quando o bot estiver pronto
    startPythonProcess();
});

// Evento: Cliente autenticado
client.on('authenticated', () => {
    console.log('Autenticação bem-sucedida!');
});

// Evento: Falha na autenticação
client.on('auth_failure', (error) => {
    console.error('Falha na autenticação:', error);
    process.exit(1);
});

// Evento: Desconectado
client.on('disconnected', (reason) => {
    console.log('Cliente desconectado:', reason);
    // Encerrar processo e reiniciar
    process.exit(1);
});

// Evento: Nova mensagem
client.on('message', async (message) => {
    try {
        // Ignorar mensagens enviadas pelo próprio bot
        if (message.from === BOT_NUMBER) return;
        
        // Ignorar mensagens de grupos
        if (message.from.includes('-')) return;
        
        // Extrair número e texto da mensagem
        const phoneNumber = message.from.split('@')[0];
        const messageText = message.body;
        
        console.log(`Nova mensagem de ${phoneNumber}: ${messageText}`);
        
        // Processar a mensagem com Python
        const response = await processPythonMessage(phoneNumber, messageText);
        
        // Enviar resposta
        await sendMessage(phoneNumber, response.text, response.media, response.media_type);
        
    } catch (error) {
        console.error('Erro ao processar mensagem:', error);
        // Tentar enviar mensagem de erro para o usuário
        try {
            const phoneNumber = message.from.split('@')[0];
            await sendMessage(phoneNumber, 'Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente mais tarde.');
        } catch (e) {
            console.error('Erro ao enviar mensagem de erro:', e);
        }
    }
});

// 11. Inicializar o cliente
console.log(`Iniciando Bot ${botName} para WhatsApp...`);
client.initialize();

// 12. Manipuladores de processo para encerramento gracioso
process.on('SIGINT', async () => {
    console.log('Recebido SIGINT. Encerrando bot...');
    await client.destroy();
    if (pythonProcess) {
        pythonProcess.kill('SIGINT');
    }
    process.exit(0);
});

process.on('SIGTERM', async () => {
    console.log('Recebido SIGTERM. Encerrando bot...');
    await client.destroy();
    if (pythonProcess) {
        pythonProcess.kill('SIGTERM');
    }
    process.exit(0);
});

// Tratamento de erros não capturados
process.on('uncaughtException', (error) => {
    console.error('Erro não capturado:', error);
    // Tentar encerrar graciosamente
    client.destroy().then(() => {
        if (pythonProcess) {
            pythonProcess.kill('SIGTERM');
        }
        process.exit(1);
    });
});

console.log(`Bot ${botName} iniciado. Aguardando QR Code...`);
