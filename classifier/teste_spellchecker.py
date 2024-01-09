from spellchecker import SpellChecker

spell = SpellChecker(language='pt')

texto = "eaa vmorunsa sisgee espato saa ein re aga ernsnraro"


print(texto.split())
palavras_erradas = spell.unknown(texto.split())

for palavra in palavras_erradas:
    correcao = spell.correction(palavra)
    print(f"Palavra errada: {palavra}, Correção: {correcao}")
