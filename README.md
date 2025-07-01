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
