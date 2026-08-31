import streamlit as st
import google.generativeai as genai
import os

# 1. Configuração da API e do Modelo
# Certifique-se de configurar sua API_KEY nas variáveis de ambiente do seu sistema
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# 2. Injeção do System Prompt (Passo 3) e Base de Conhecimento (Passo 2)
# Em um projeto avançado, a base de conhecimento seria lida de arquivos .txt ou .md na pasta /knowledge
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

# 4. Inicialização do Histórico do Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

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
        # Em um cenário real, aqui você enviaria o histórico completo (chat.send_message)
        response = model.generate_content(prompt)
        st.markdown(response.text)
    
    # Salva a resposta da IA no histórico
    st.session_state.messages.append({"role": "assistant", "content": response.text})
