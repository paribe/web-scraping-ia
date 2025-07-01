import os, json
from decouple import config
from pprint import pprint
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

schema = {
    'properties': {
        'simbolo_empresa': {'type': 'string'},
        'nome_empresa': {'type': 'string'},
        'setor_empresa': {'type': 'string'},
        'valor_mercado': {'type': 'string'},
        'div_yield': {'type': 'string'},
        'preco': {'type': 'string'},
        'variacao': {'type': 'string'},
        'volume': {'type': 'string'},
        'classificacao_analistas': {'type': 'string'},
    },
}

def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).invoke(content).get('text')

def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(documents=docs, tags_to_extract=['table'])
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=2000, chunk_overlap=0)
    splits = splitter.split_documents(documents=docs_transformed)
    extracted_content = []
    for split in splits:
        extracted_content.extend(extract(schema=schema, content=split.page_content))
    return extracted_content

def main():
    urls = ['https://br.tradingview.com/markets/stocks-brazil/market-movers-large-cap/']
    extracted_content = scrape_with_playwright(urls=urls, schema=schema)
    pprint(extracted_content)
    with open('data_acoes.json', 'w') as fp:
        json.dump(extracted_content, fp, ensure_ascii=False, indent=4)


schema = schema
scrape_with_playwright = scrape_with_playwright