
'''cleans a string from special characters'''



def scrub_string(phrase):
    #growing dictionary WIP
    out = phrase
    out = out.replace(",", "")
    out = out.replace("-", " ")
    out = out.replace("(", "")
    out = out.replace(")", "")
    out = out.replace("'", "")
    out = out.replace("+", " ")
    out = out.replace("!", "")
    out = out.replace("?", "")
    out = out.replace("/", "")
    out = out.replace("’", '')
    out = out.replace("å", 'a')
    out = out.replace("$", "S")
    out = out.replace("À", "A")
    out = out.replace("ë", "e")
    out = out.replace("&", "n")
    out = out.replace("‘", "")
    out = out.replace("é", "e")
    out = phrase
    return out