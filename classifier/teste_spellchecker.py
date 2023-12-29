from spellchecker import SpellChecker

spell = SpellChecker(language='pt')

texto = "Este é um exemmplo de arvore algumms erros."
palavras_erradas = spell.unknown(texto.split())

for palavra in palavras_erradas:
    correcao = spell.correction(palavra)
    print(f"Palavra errada: {palavra}, Correção: {correcao}")
