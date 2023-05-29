def text_to_binary(text):
    binary = ""
    for char in text:
        # Convertir chaque caractère en sa représentation binaire
        binary += format(ord(char), '08b') + " "  # Utilisez '07b' pour ignorer le bit de parité

    return binary


# Exemple d'utilisation
text = "Hello, world!"
binary_text = text_to_binary(text)
print(binary_text)
