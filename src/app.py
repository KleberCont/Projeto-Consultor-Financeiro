import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
from dotenv import load_dotenv

# 1. Configuração da API e do Modelo
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Validação para evitar que a aplicação quebre se a chave não for encontrada
if not GOOGLE_API_KEY:
    st.error("Chave da API não encontrada. Verifique o arquivo .env.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# 2. Injeção do System Prompt com Guardrails e Base de Conhecimento
INSTRUCOES_SISTEMA = """
Você é um Consultor Financeiro Inteligente.
Regras de Comportamento e Segurança (Guardrails):
1. Responda baseando-se estritamente nas informações financeiras oficiais (Banco Central, CVM, B3, Sicalc e normas tributárias brasileiras).
2. NUNCA forneça recomendações diretas de compra ou venda de ativos financeiros.
3. Exija e cite fontes oficiais para fundamentar suas análises na base de conhecimento.
4. Se a informação for uma previsão futura incerta ou estiver fora da base, diga que não possui dados suficientes.
5. Mantenha um tom analítico, didático e rigoroso, adequado para a área contábil e financeira.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=INSTRUCOES_SISTEMA
)

# 3. Configuração da Interface Visual com Streamlit
st.set_page_config(page_title="Consultor Financeiro IA", page_icon="📊", layout="wide")

st.title("📊 Consultor Financeiro Inteligente")
st.markdown("Assistente virtual integrado com módulo de reconciliação bancária e análise tributária.")

# Estruturação em abas para contemplar todas as etapas do projeto
aba_chat, aba_reconciliacao = st.tabs(["💬 Chat de Consultoria", "📑 Reconciliação Contábil"])

with aba_chat:
    # 4. Inicialização do Histórico e da Sessão de Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # Exibe mensagens anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. Captura de Entrada do Usuário e Resposta da IA
    if prompt := st.chat_input("Ex: Quais as regras do Sicalc para tributação de Day Trade?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erro ao processar a consulta financeira: {e}")

with aba_reconciliacao:
    st.header("Processamento e Reconciliação")
    st.markdown("Faça o upload dos dados para automatizar as classificações contábeis e realizar o mapeamento de fornecedores e clientes.")
    
    arquivo_upload = st.file_uploader("Arquivo financeiro (CSV ou Excel)", type=["csv", "xlsx"])
    
    if arquivo_upload is not None:
        try:
            # Leitura flexível para os formatos de dados
            if arquivo_upload.name.endswith('.csv'):
                df = pd.read_csv(arquivo_upload)
            else:
                df = pd.read_excel(arquivo_upload)
            
            st.success("Base de dados carregada com sucesso!")
            st.dataframe(df.head())
            
            st.info("Aqui entram as lógicas avançadas (cruzamentos, reconciliação de diferenças de saldos e classificação contábil) antes da exportação.")
            
            # Botão para exportar resultados estruturados
            csv_export = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Exportar Planilha Estruturada",
                data=csv_export,
                file_name="dados_classificados.csv",
                mime="text/csv",
            )
        except Exception as e:
            st.error(f"Erro na leitura ou processamento do arquivo: {e}")
