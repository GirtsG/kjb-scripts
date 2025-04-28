import json
import re

# Ielādē datus no kjv.json
with open("kjv.json", "r", encoding="utf-8") as kjv_file:
    kjv_data = json.load(kjv_file)

# Ielādē datus no kjv_strongs.json
with open("kjv_strongs.json", "r", encoding="utf-8") as strongs_file:
    strongs_data = json.load(strongs_file)

# Funkcija aizvieto Strong's numurus un formatē tekstu
def format_strongs(text):
    # Aizvieto {G####} ar [strong]G####[/strong]
    text = re.sub(r"\{(G\d+)\}", r"[strong]\1[/strong]", text)
    # Aizvieto {(G####)} ar [strong](G####)[/strong]
    text = re.sub(r"\{\(G(\d+)\)\}", r"[strong](G\1)[/strong]", text)
    return text

# Apvieno tekstus no kjv un strongs failiem
def merge_texts(kjv_text, strongs_text):
    # Formatē Strong's numurus
    strongs_text = format_strongs(strongs_text)
    return strongs_text

# Formatējumu piemērošana
def apply_formatting(text, chapter, verse):
    # Aizvieto paragrāfa simbolu ar [p]
    text = text.replace("¶", "[p]")

    # Pievieno [color=red] formatējumu 1. nodaļas 8. un 11. pantam
    if chapter == 1 and verse in [8, 11]:
        text = f"[color=red]{text}[/color]"

    # Precīzi aizvieto "be glory" ar [i]be glory[/i]
    text = text.replace("be glory", "[i]be glory[/i]")
    return text

# Rezultātu saraksta ģenerēšana
result = []

for kjv_verse, strongs_verse in zip(kjv_data["verses"], strongs_data["verses"]):
    if (
        kjv_verse["book"] == strongs_verse["book"]
        and kjv_verse["chapter"] == strongs_verse["chapter"]
        and kjv_verse["verse"] == strongs_verse["verse"]
    ):
        # Apvieno tekstus
        combined_text = merge_texts(kjv_verse["text"], strongs_verse["text"])
        # Pielieto papildu formatējumu
        formatted_text = apply_formatting(combined_text, kjv_verse["chapter"], kjv_verse["verse"])
        # Pievieno rezultātu
        result.append({
            "book_name": kjv_verse["book_name"],
            "book": kjv_verse["book"],
            "chapter": kjv_verse["chapter"],
            "verse": kjv_verse["verse"],
            "text": formatted_text
        })

# Saglabā rezultātu kā JSON failu
with open("result.json", "w", encoding="utf-8") as result_file:
    json.dump(result, result_file, indent=4, ensure_ascii=False)

print("Apvienotais fails izveidots: result.json")