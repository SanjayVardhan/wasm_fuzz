import re

class NaiveTokenizer:
    def __init__(self):
        # Regex for comments in WebAssembly (typically starts with ;; or (; ;))
        self.comment_re = re.compile(r"(;;.*?$)|(\(;[\s\S]*?;\))", re.MULTILINE)
        # Regex for string literals (anything inside quotation marks)
        self.string_re = re.compile(r'"[^"]*"')
        # Regex for identifiers (variable names, keywords, etc.)
        self.ident_re = re.compile(r"[^\s\"()]+")
        
    def tokenize(self, text):
        tokens = []
        # Remove comments
        text = self.comment_re.sub("", text)
        # Preserve positions to handle text outside string literals
        last_pos = 0
        # Find all string literals
        matches = list(self.string_re.finditer(text))
        
        for match in matches:
            # Process text before the string literal
            non_string_section = text[last_pos:match.start()]
            # Extract non-string tokens by splitting on whitespace and using ident_re to further split
            for token in self.ident_re.findall(non_string_section):
                tokens.append(token)
            # Add the entire string literal as a token
            tokens.append(match.group(0))
            # Update the last position to the end of the current match
            last_pos = match.end()
        
        # Handle any remaining text after the last string literal
        non_string_section = text[last_pos:]
        for token in self.ident_re.findall(non_string_section):
            tokens.append(token)

        return tokens

if __name__ == "__main__":
    tokenizer = NaiveTokenizer()
    with open("test.wat", "r") as file:
        wat_content = file.read()
    tokens = tokenizer.tokenize(wat_content)
    print(tokens)
