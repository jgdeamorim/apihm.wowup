import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_variacoes(produto_nome: str, descricao: str):
    """Gera variações automáticas para produtos com base em IA."""
    prompt = f"""
    O produto {produto_nome} precisa ser transformado em um produto variado.
    Sugira possíveis variações com base na descrição abaixo:

    **Descrição do produto**: {descricao}

    **Formato de resposta esperado**:
    {{
        "variacoes": [
            {{"tipo": "cor", "opcoes": ["Azul", "Vermelho", "Verde"]}},
            {{"tipo": "tamanho", "opcoes": ["P", "M", "G"]}}
        ]
    }}
    """

    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Você é um especialista em e-commerce e marketplaces."},
                  {"role": "user", "content": prompt}]
    )

    return resposta['choices'][0]['message']['content']
