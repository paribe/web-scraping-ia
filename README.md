# 📊 Web Scraping com IA e Streamlit

Este projeto demonstra como usar **Python, LangChain, Playwright, BeautifulSoup e OpenAI GPT-4o** para extrair dados de sites de forma inteligente e exibi-los em uma interface interativa feita com **Streamlit**.

---

## 📦 Funcionalidades

- 📈 **Scraping da Tabela do Brasileirão 2024** direto do site [GE.globo.com](https://ge.globo.com/futebol/brasileirao-serie-a/)
- 💹 **Scraping de ações Big Caps** da página [TradingView Brasil](https://br.tradingview.com/markets/stocks-brazil/market-movers-large-cap/)
- 🤖 **Agente inteligente com LangChain** que responde perguntas de forma autônoma navegando em sites via Playwright

---

## 🚀 Como usar

### 1. Clone ou baixe o projeto
Extraia o arquivo ZIP em uma pasta local.

### 2. Instale as dependências
No terminal, vá até a pasta do projeto e execute:

```bash
pip install -r requirements.txt
playwright install
```

### 3. Rode a aplicação Streamlit

```bash
streamlit run interface/app.py
```

### 4. Use a aplicação

- Insira sua `OPENAI_API_KEY` (necessária para usar o GPT-4o da OpenAI)
- Escolha uma das opções de scraping
- Veja os dados extraídos diretamente na tela

---

## 🧪 Estrutura do Projeto

```
web_scraping_ia/
├── app.py                    # ← ESTE (raiz)
├── interface/
│   └── app.py               # ← arquivo antigo
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml
├── exemplo1_brasileirao.py
├── artilharia.py
├── requirements.txt
└── .env
```

---

## 🔑 API Key da OpenAI

Crie uma conta em [platform.openai.com](https://platform.openai.com/) e gere sua chave. Insira a chave diretamente na interface quando solicitado.

---

## 📚 Tecnologias utilizadas

- [LangChain](https://www.langchain.com/)
- [Playwright](https://playwright.dev/python/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Streamlit](https://streamlit.io/)
- [OpenAI GPT-4o](https://openai.com/gpt-4o)

---

## 📬 Contribuição

Sinta-se à vontade para sugerir melhorias ou adaptar o projeto para novos sites, exportação para PDF ou deploy na nuvem.

---

It seems like I can’t do more advanced data analysis right now. Please try again later.

Mas posso te ajudar mesmo assim! Aqui está o conteúdo atualizado que você pode copiar e salvar como `README.md` em seu projeto:

---

## 🤖 Por que usar IA com LangChain e OpenAI?

A combinação de **LangChain** e **OpenAI** traz grandes vantagens ao realizar web scraping:

### 🧠 1. Extração inteligente de dados não estruturados

* Sites modernos muitas vezes usam HTML complexo, com dados misturados em blocos difíceis de interpretar.
* Com a **IA da OpenAI (GPT-4o)**, conseguimos **interpretar e extrair informações como humanos**, mesmo de textos ambíguos ou dados fora de tabelas tradicionais.

### 🧰 2. LangChain facilita a integração com navegadores e modelos

* O **LangChain** permite conectar o modelo GPT a ferramentas como **Playwright**, permitindo navegar em sites dinâmicos.
* Ele também fornece abstrações poderosas para **dividir documentos, transformar HTML em texto útil e aplicar modelos de linguagem para extração.**

### 🔄 3. Automatização com agentes inteligentes

* O exemplo do **agente com LangChain** mostra como podemos usar **um modelo para interagir com ferramentas e responder perguntas específicas**, como "Qual time está na liderança do Brasileirão?".
* Isso elimina a necessidade de código rígido e scripts manuais. Basta descrever o que quer em linguagem natural.

### 🚀 Benefícios

* 🔍 Maior precisão em scraping de páginas complexas
* 🧩 Facilidade em adaptar para novos sites sem reescrever todo o código
* 🤝 Interfaces mais inteligentes e interativas
* 🔄 Possibilidade de criar **agentes autônomos** que exploram a web com raciocínio

Essa abordagem é ideal para quem deseja ir além do scraping tradicional e construir soluções mais robustas e inteligentes.

---

Se quiser, posso agora reintegrar essa explicação ao ZIP do projeto e gerar o arquivo de download novamente. Deseja isso?


Vou explicar esse código passo a passo de forma didática! É um exemplo muito interessante de como criar um **agente inteligente** que navega na web automaticamente.

## 🤖 **O que este código faz:**

Este código cria um **agente de IA** que consegue:
1. **Abrir um navegador automaticamente**
2. **Navegar para um site específico**
3. **"Ler" o conteúdo da página**
4. **Extrair informações específicas**
5. **Responder perguntas sobre o que encontrou**

## 📚 **Explicação linha por linha:**

### **1. Importações (bibliotecas necessárias):**
```python
import os
from decouple import config
from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from langchain_openai import ChatOpenAI
```

**O que cada uma faz:**
- `os` → Gerenciar variáveis do sistema
- `decouple` → Ler configurações do arquivo .env
- `langchain.agents` → Criar agentes inteligentes
- `PlayWrightBrowserToolkit` → Ferramentas para controlar navegador
- `create_sync_playwright_browser` → Criar um navegador automatizado
- `ChatOpenAI` → Interface com o modelo GPT da OpenAI

### **2. Configuração da API:**
```python
os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')
```
**Tradução:** "Pegue a chave da API do arquivo .env e configure no sistema"

### **3. Função principal:**
```python
def executar_agente():
```

### **4. Criar o modelo de IA:**
```python
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
```
**Tradução:** 
- "Crie uma conexão com o GPT-4o-mini"
- `temperature=0` = "Seja preciso e consistente (menos criativo)"

### **5. Criar o navegador automatizado:**
```python
browser = create_sync_playwright_browser()
```
**Tradução:** "Abra um navegador que pode ser controlado por código"

### **6. Criar ferramentas de navegação:**
```python
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=browser)
tools = toolkit.get_tools()
```
**Tradução:** "Dê ao agente ferramentas para navegar: clicar, digitar, ler páginas, etc."

### **7. Criar o agente inteligente:**
```python
agent_chain = initialize_agent(
    tools, llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
```
**Tradução:** 
- "Crie um agente que combina o GPT com as ferramentas de navegação"
- `STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION` = Tipo de agente que raciocina e age
- `verbose=True` = "Mostre o que está pensando/fazendo"

### **8. Executar a tarefa:**
```python
result = agent_chain.invoke(
    input='qual time está na primeira colocação do brasileirão na tabela do site https://ge.globo.com/futebol/brasileirao-serie-a/? E o último colocado?'
)
```
**Tradução:** "Execute esta pergunta usando navegação inteligente"

## 🧠 **Como o agente "pensa":**

O agente segue este processo:

1. **Pensamento:** "Preciso acessar o site do Globo Esporte"
2. **Ação:** Navegar para https://ge.globo.com/futebol/brasileirao-serie-a/
3. **Observação:** "Vejo uma tabela de classificação"
4. **Pensamento:** "Preciso identificar o primeiro e último colocado"
5. **Ação:** Extrair dados da tabela
6. **Resposta:** "O primeiro colocado é [Time X] e o último é [Time Y]"

## 🆚 **Diferença dos outros métodos:**

| Método | Como funciona |
|--------|---------------|
| **Scraping tradicional** | Código específico para cada site |
| **LangChain com schema** | IA extrai dados seguindo um padrão |
| **Agente inteligente** | IA navega e raciocina como humano |

## 🎯 **Vantagens do agente:**

- ✅ **Flexível:** Funciona mesmo se o site mudar
- ✅ **Inteligente:** Pode responder perguntas complexas
- ✅ **Adaptável:** Consegue navegar por diferentes layouts
- ✅ **Natural:** Entende linguagem humana

## ⚠️ **Desvantagens:**

- ❌ **Mais lento:** Precisa "pensar" a cada passo
- ❌ **Mais caro:** Usa mais tokens da API
- ❌ **Imprevisível:** Pode tomar caminhos diferentes

**Resumo:** É como ter um assistente virtual que você pode mandar "vá neste site e me traga essa informação" e ele faz tudo sozinho! 🤖✨