import json
import re

# Load KJV and Strong's data
with open("kjv.json", "r", encoding="utf-8") as kjv_file:
    kjv_data = json.load(kjv_file)["verses"]

with open("kjv_strongs.json", "r", encoding="utf-8") as strongs_file:
    strongs_data = json.load(strongs_file)["verses"]

# Function to merge KJV and Strong's texts
def merge_texts(kjv_text, strongs_text):
    # Split KJV and Strong's texts into words
    kjv_words = kjv_text.split()
    strongs_words = strongs_text.split()

    # Merged result
    merged_text = []
    strongs_index = 0

    # Match words and insert Strong's numbers
    for word in kjv_words:
        clean_word = re.sub(r"[^\w']", "", word)  # Remove punctuation
        merged_text.append(word)  # Always add KJV word

        # If there's a matching Strong's word, append it
        if strongs_index < len(strongs_words) and clean_word in strongs_words[strongs_index]:
            merged_text.append(f"[strong]{strongs_words[strongs_index]}[/strong]")
            strongs_index += 1

    # Append remaining Strong's words (if any)
    while strongs_index < len(strongs_words):
        merged_text.append(f"[strong]{strongs_words[strongs_index]}[/strong]")
        strongs_index += 1

    return " ".join(merged_text)

# Function to format text with tags
def format_text(text, chapter, verse):
    # Replace '<>' with [color=red][/color]
    text = text.replace("<", "[color=red]").replace(">", "[/color]")
    # Replace '[]' with [i][/i]
    text = re.sub(r"\[([^\]]+)\]", r"[i]\1[/i]", text)
    # Replace '¶' with [p]
    text = text.replace("¶", "[p]")
    # Add [color=red] tags for chapter 1, verses 8 and 11
    if chapter == 1 and verse in [8, 11]:
        text = f"[color=red]{text}[/color]"
    return text

# Create the result list
result = []

for kjv_verse, strongs_verse in zip(kjv_data, strongs_data):
    if (
        kjv_verse.get("book") == strongs_verse.get("book")
        and kjv_verse.get("chapter") == strongs_verse.get("chapter")
        and kjv_verse.get("verse") == strongs_verse.get("verse")
    ):
        # Format KJV and Strong's texts
        formatted_kjv = format_text(kjv_verse.get("text", ""), kjv_verse.get("chapter"), kjv_verse.get("verse"))
        formatted_strongs = strongs_verse.get("text", "")

        # Merge KJV and Strong's texts
        combined_text = merge_texts(formatted_kjv, formatted_strongs)

        # Append to result
        result.append({
            "book_name": kjv_verse.get("book_name", ""),
            "book": kjv_verse.get("book", ""),
            "chapter": kjv_verse.get("chapter", ""),
            "verse": kjv_verse.get("verse", ""),
            "text": combined_text
        })

# Save the result to result.json
with open("result.json", "w", encoding="utf-8") as result_file:
    json.dump(result, result_file, indent=4, ensure_ascii=False)

print("Result successfully created in result.json")