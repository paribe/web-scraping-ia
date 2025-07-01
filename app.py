import streamlit as st
import json
import os
import sys
import pandas as pd

# PRIMEIRO: Configurar página (deve ser a primeira linha Streamlit)
st.set_page_config(
    page_title="Web Scraping com IA", 
    layout="wide",
    page_icon="⚽"
)

# Configurar o caminho para encontrar os módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) if 'interface' in current_dir else current_dir
exemplos_dir = os.path.join(parent_dir, 'exemplos')

# Adicionar diretórios ao sys.path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if exemplos_dir not in sys.path:
    sys.path.insert(0, exemplos_dir)

# Configurar a API key usando st.secrets (para Streamlit Cloud)
def carregar_api_key():
    """Carrega a API key usando st.secrets ou arquivo .env local"""
    
    # Método 1: Streamlit Secrets (produção)
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        if api_key and len(api_key) > 20:
            return api_key
    except:
        pass
    
    # Método 2: Arquivo .env (desenvolvimento local)
    caminhos_env = [
        os.path.join(parent_dir, '.env'),
        os.path.join(current_dir, '.env'),
        os.path.join(os.getcwd(), '.env'),
        '.env'
    ]
    
    # Tentar decouple config primeiro
    try:
        from decouple import config
        api_key = config('OPENAI_API_KEY', default=None)
        if api_key and len(api_key) > 20:
            return api_key
    except:
        pass
    
    # Ler arquivo .env manualmente
    for caminho in caminhos_env:
        if os.path.exists(caminho):
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    for linha in f:
                        linha = linha.strip()
                        if linha.startswith('OPENAI_API_KEY='):
                            api_key = linha.split('=', 1)[1].strip().strip('"\'')
                            if len(api_key) > 20:
                                return api_key
            except Exception:
                continue
    
    return None

# Carregar API key
api_key = carregar_api_key()
if api_key:
    os.environ['OPENAI_API_KEY'] = api_key
    api_key_configurada = True
else:
    api_key_configurada = False

st.title("⚽ Web Scraping com IA usando LangChain")

opcao = st.selectbox(
    "Escolha o tipo de scraping:",
    ("Tabela do Brasileirão", "Ações (Big Caps)", "Agente inteligente")
)

def formatar_tabela_brasileirao(resultado):
    """Formatar dados do Brasileirão PRESERVANDO a ordem original"""
    if not resultado:
        return None
    
    # Filtrar apenas dados válidos de times
    dados_validos = []
    for item in resultado:
        if isinstance(item, dict) and item.get('time') and item.get('time') != 'nan' and item.get('time').strip():
            dados_validos.append(item)
    
    if not dados_validos:
        return None
    
    # Converter para DataFrame SEM alterar a ordem
    df = pd.DataFrame(dados_validos)
    
    # Garantir que as colunas existam e tenham valores padrão
    colunas_esperadas = {
        'posicao': 0,
        'time': 'N/A',
        'jogos': 0,
        'vitorias': 0,
        'empates': 0,
        'derrotas': 0,
        'gols_pro': 0,
        'gols_contra': 0,
        'saldo_gols': 0,
        'pontos': 0
    }
    
    for col, default_value in colunas_esperadas.items():
        if col not in df.columns:
            df[col] = default_value
        else:
            # Limpar valores nan e inválidos
            df[col] = df[col].fillna(default_value)
            if col != 'time':
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    
    # Reordenar colunas
    df = df[list(colunas_esperadas.keys())]
    
    # Remover linhas com time inválido
    df = df[df['time'].str.len() > 2]
    df = df[df['time'] != 'N/A']
    
    # PRESERVAR A ORDEM ORIGINAL - apenas resetar o índice
    df = df.reset_index(drop=True)
    
    # Renomear colunas para exibição
    df.columns = ['Pos', 'Time', 'J', 'V', 'E', 'D', 'GP', 'GC', 'SG', 'Pts']
    
    return df

def formatar_tabela_acoes(resultado):
    """Formatar dados de ações"""
    if not resultado:
        return None
    
    # Filtrar apenas dados válidos
    dados_validos = []
    for item in resultado:
        if isinstance(item, dict) and (item.get('simbolo_empresa') or item.get('nome_empresa')):
            dados_validos.append(item)
    
    if not dados_validos:
        return None
    
    df = pd.DataFrame(dados_validos)
    
    # Renomear colunas para exibição
    column_mapping = {
        'simbolo_empresa': 'Símbolo',
        'nome_empresa': 'Empresa',
        'setor_empresa': 'Setor',
        'valor_mercado': 'Valor de Mercado',
        'div_yield': 'Div. Yield',
        'preco': 'Preço',
        'variacao': 'Variação',
        'volume': 'Volume',
        'classificacao_analistas': 'Classificação'
    }
    
    # Renomear apenas as colunas que existem
    df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
    
    return df

def formatar_artilharia(resultado):
    """Formatar dados de artilharia usando extração específica"""
    try:
        # Importar o módulo de artilharia
        artilharia_path = os.path.join(parent_dir, 'artilharia.py')
        
        # Se o arquivo não existir, retornar None
        if not os.path.exists(artilharia_path):
            return None
        
        # Importar e usar a função de artilharia
        import sys
        sys.path.append(parent_dir)
        import artilharia
        
        urls = ['https://ge.globo.com/futebol/brasileirao-serie-a/']
        dados_artilharia = artilharia.scrape_artilharia(urls)
        
        if dados_artilharia and len(dados_artilharia) > 0:
            df = pd.DataFrame(dados_artilharia)
            # Renomear colunas para melhor exibição
            if 'jogador' in df.columns:
                df = df.rename(columns={
                    'posicao': 'Pos',
                    'jogador': 'Jogador', 
                    'time': 'Time',
                    'gols': 'Gols',
                    'posicao_campo': 'Posição'
                })
            return df
    except Exception as e:
        print(f"Erro ao carregar artilharia: {e}")
    
    return None

# REMOVIDO o parâmetro type="primary" para compatibilidade
executar = st.button("🚀 Executar")

if executar:
    if not api_key_configurada:
        st.error("❌ API Key não encontrada")
        st.info("**Para desenvolvimento local:** Crie um arquivo .env com OPENAI_API_KEY=sua_chave")
        st.info("**Para produção:** Configure a API key nos Secrets do Streamlit Cloud")
        
    else:
        try:
            if opcao == "Tabela do Brasileirão":
                with st.spinner("Fazendo scraping da tabela do Brasileirão..."):
                    # Fazer scraping
                    import exemplo1_brasileirao
                    urls = ['https://ge.globo.com/futebol/brasileirao-serie-a/']
                    resultado = exemplo1_brasileirao.scrape_with_playwright(urls=urls, schema=exemplo1_brasileirao.schema)
                    
                    if resultado:
                        st.success("✅ Scraping concluído com sucesso!")
                        
                        # Criar duas colunas
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.subheader("📊 TABELA DE CLASSIFICAÇÃO")
                            
                            # Tentar formatar como tabela do Brasileirão
                            df_tabela = formatar_tabela_brasileirao(resultado)
                            
                            if df_tabela is not None and not df_tabela.empty:
                                # Aplicar estilos na tabela (versão compatível)
                                def colorir_posicoes(row):
                                    if row['Pos'] <= 4:
                                        return ['background-color: #d4edda'] * len(row)  # Verde claro - Libertadores
                                    elif row['Pos'] <= 6:
                                        return ['background-color: #fff3cd'] * len(row)  # Amarelo claro - Sul-Americana
                                    elif row['Pos'] >= 17:
                                        return ['background-color: #f8d7da'] * len(row)  # Vermelho claro - Rebaixamento
                                    else:
                                        return [''] * len(row)
                                
                                # Mostrar tabela estilizada (versão compatível)
                                try:
                                    st.dataframe(
                                        df_tabela.style.apply(colorir_posicoes, axis=1),
                                        height=600
                                    )
                                except:
                                    # Fallback para versões mais antigas do Streamlit
                                    st.dataframe(df_tabela, height=600)
                                
                                # Legenda
                                st.markdown("""
                                **Legenda:**
                                - 🟢 **Posições 1-4**: Classificação para Libertadores
                                - 🟡 **Posições 5-6**: Classificação para Sul-Americana  
                                - 🔴 **Posições 17-20**: Zona de rebaixamento
                                """)
                                
                            else:
                                st.warning("⚠️ Não foi possível formatar os dados como tabela de classificação")
                                st.json(resultado)
                        
                        with col2:
                            st.subheader("🥅 ARTILHARIA")
                            
                            # Tentar extrair dados de artilharia
                            df_artilharia = formatar_artilharia(resultado)
                            
                            if df_artilharia is not None and not df_artilharia.empty:
                                st.dataframe(df_artilharia)
                            else:
                                st.info("ℹ️ Dados de artilharia não encontrados nesta extração")
                        
                        # Seção expandível com dados brutos
                        with st.expander("🔍 Ver dados brutos (JSON)"):
                            st.json(resultado)
                            
                    else:
                        st.warning("⚠️ Nenhum dado foi extraído. Verifique a URL ou o schema.")
                    
            elif opcao == "Ações (Big Caps)":
                with st.spinner("Fazendo scraping das ações..."):
                    try:
                        # Importar o módulo de ações
                        import exemplo2_acoes
                        
                        urls = ['https://br.tradingview.com/markets/stocks-brazil/market-movers-large-cap/']
                        resultado = exemplo2_acoes.scrape_with_playwright(urls=urls, schema=exemplo2_acoes.schema)
                        
                        if resultado:
                            st.success("✅ Scraping de ações concluído com sucesso!")
                            
                            st.subheader("📈 AÇÕES - BIG CAPS")
                            
                            # Formatar dados de ações
                            df_acoes = formatar_tabela_acoes(resultado)
                            
                            if df_acoes is not None and not df_acoes.empty:
                                st.dataframe(df_acoes, height=600)
                                
                                # Estatísticas básicas
                                st.subheader("📊 Estatísticas")
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric("Total de Empresas", len(df_acoes))
                                
                                with col2:
                                    if 'Setor' in df_acoes.columns:
                                        setores_unicos = df_acoes['Setor'].nunique()
                                        st.metric("Setores Diferentes", setores_unicos)
                                
                                with col3:
                                    st.metric("Dados Extraídos", "Em tempo real")
                                
                            else:
                                st.warning("⚠️ Não foi possível formatar os dados das ações")
                                st.json(resultado)
                            
                            # Seção expandível com dados brutos
                            with st.expander("🔍 Ver dados brutos (JSON)"):
                                st.json(resultado)
                                
                        else:
                            st.warning("⚠️ Nenhum dado de ações foi extraído. Verifique a URL ou o schema.")
                            
                    except Exception as e:
                        st.error(f"❌ Erro ao processar ações: {str(e)}")
                    
            elif opcao == "Agente inteligente":
                with st.spinner("Executando agente inteligente... (pode demorar alguns minutos)"):
                    try:
                        # Importar o módulo do agente
                        import exemplo3_agente
                        
                        resultado = exemplo3_agente.executar_agente()
                        
                        if resultado:
                            st.success("✅ Agente inteligente executado com sucesso!")
                            
                            st.subheader("🤖 RESULTADO DO AGENTE INTELIGENTE")
                            
                            # Exibir resultado do agente
                            if isinstance(resultado, dict):
                                if 'output' in resultado:
                                    st.write("**Resposta do Agente:**")
                                    st.info(resultado['output'])
                                else:
                                    st.json(resultado)
                            else:
                                st.write("**Resposta do Agente:**")
                                st.info(str(resultado))
                            
                            # Seção expandível com dados brutos
                            with st.expander("🔍 Ver resposta completa (JSON)"):
                                st.json(resultado)
                                
                        else:
                            st.warning("⚠️ O agente não retornou nenhum resultado.")
                            
                    except Exception as e:
                        st.error(f"❌ Erro ao executar agente: {str(e)}")
                        st.info("💡 **Nota:** O agente inteligente requer bibliotecas adicionais que podem não estar disponíveis no deploy.")
                    
        except ImportError as e:
            st.error(f"❌ Erro de importação: {str(e)}")
            st.info("💡 Verifique se todos os módulos estão presentes no repositório.")
            
        except Exception as e:
            st.error(f"❌ Erro durante a execução: {str(e)}")

# Sidebar dinâmica baseada na opção selecionada
with st.sidebar:
    st.header("ℹ️ Informações")
    
    if opcao == "Tabela do Brasileirão":
        st.write("**Brasileirão Série A**")
        st.write("- Classificação em tempo real")
        st.write("- Dados extraídos do Globo Esporte")
        st.write("  [https://ge.globo.com/futebol/brasileirao-serie-a/](https://ge.globo.com/futebol/brasileirao-serie-a/)")
        st.write("- Powered by LangChain + OpenAI")
        
    elif opcao == "Ações (Big Caps)":
        st.write("**Ações - Big Caps**")
        st.write("- Dados extraídos da fonte:")
        st.write("  [https://br.tradingview.com/markets/stocks-brazil/market-movers-large-cap/](https://br.tradingview.com/markets/stocks-brazil/market-movers-large-cap/)")
        st.write("- Powered by LangChain + OpenAI")
        
    elif opcao == "Agente inteligente":
        st.write("**Agente Inteligente**")
        st.write("- Análise automatizada com IA")
        st.write("- Pergunta: Qual time está na primeira colocação do brasileirão na tabela do site:")
        st.write("  [https://ge.globo.com/futebol/brasileirao-serie-a/](https://ge.globo.com/futebol/brasileirao-serie-a/)")
        st.write("- E o último colocado?")
        st.write("- Powered by LangChain + OpenAI + Playwright")
    
    # Informações do deploy
    st.markdown("---")
    st.caption("🚀 Deploy: Streamlit Cloud")
    st.caption("🔧 GitHub: paribe/web-scraping-ia")