import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def refinar_dados_com_ia(produto: dict):
    """Refina os dados do produto com IA"""
    prompt = f"""
    O produto "{produto['nome']}" precisa de uma descrição detalhada e otimizada para SEO.
    
    **Especificações**:
    - GTIN: {produto.get('gtin', 'Desconhecido')}
    - Peso: {produto.get('peso', 'Desconhecido')} kg
    - Dimensões: {produto.get('dimensoes', 'Desconhecido')}
    - Categoria: {produto.get('categoria', 'Desconhecida')}
    - Marca: {produto.get('marca', 'Desconhecida')}

    **Descrição esperada**:
    Gere uma descrição detalhada para marketplaces, explicando os benefícios do produto.
    """

    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Você é um especialista em e-commerce."},
                  {"role": "user", "content": prompt}]
    )
    
    return resposta['choices'][0]['message']['content']

def gerar_sugestao_ncm(descricao: str) -> str:
    """Utiliza a OpenAI para sugerir um NCM baseado na descrição do produto"""
    prompt = f"""
    Baseado na seguinte descrição de produto: "{descricao}", sugira um código NCM válido.
    O código deve ser compatível com a classificação fiscal brasileira e coerente com produtos similares.
    Retorne apenas o código NCM no formato XXXXXXXX (8 dígitos).
    """

    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Você é um especialista em classificação fiscal de produtos."},
                  {"role": "user", "content": prompt}]
    )

    return resposta['choices'][0]['message']['content'].strip()