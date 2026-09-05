import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
# 1. Configuração da API e do Modelo
# Certifique-se de configurar sua API_KEY nas variáveis de ambiente do seu sistema
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# 2. Injeção do System Prompt (Passo 3) e Base de Conhecimento (Passo 2)
INSTRUCOES_SISTEMA = """
Você é um Consultor Financeiro Inteligente.
Regras:
1. Responda baseando-se estritamente nas informações financeiras oficiais (Banco Central, CVM, B3, Sicalc).
2. Nunca forneça recomendações diretas de compra ou venda de ativos.
3. Se não souber ou for uma previsão futura incerta, diga que não possui dados suficientes.
4. Mantenha tom analítico e cite as fontes (ex: InfoMoney, G1, CNN).
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=INSTRUCOES_SISTEMA
)

# 3. Configuração da Interface Visual com Streamlit
st.set_page_config(page_title="Consultor Financeiro IA", page_icon="📊")
st.title("📊 Consultor Financeiro Inteligente")
st.markdown("Tire suas dúvidas sobre mercado de capitais, indicadores econômicos e tributação brasileira.")

# 4. Inicialização do Histórico e da Sessão de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inicializa a sessão de chat do Gemini para manter a memória das mensagens
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Exibe mensagens anteriores na tela
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Captura de Entrada do Usuário e Resposta da IA
if prompt := st.chat_input("Ex: Quais as regras do Sicalc para tributação de Day Trade?"):
    # Salva e exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta do modelo e exibe na tela
    with st.chat_message("assistant"):
        try:
            # Usa send_message na sessão ativa para preservar o contexto
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
            
            # Salva a resposta da IA no histórico visual
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erro ao processar a consulta financeira: {e}")
