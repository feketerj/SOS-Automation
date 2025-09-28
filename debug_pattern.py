import re

text = 'Any vendor who can provide 8130-3 documentation is eligible'

patterns = [
    r'\b(?:any|all)[\s\-]*(?:vendor|supplier|contractor|source|one|entity|company|firm)s?[\s\-]*(?:who|that|which)?[\s\-]*can[\s\-]*provide[\s\-]*8130[\s\-]*3',
    r'\b(?:can|able[\s\-]*to|capable[\s\-]*of)[\s\-]*provid\w*[\s\-]*8130[\s\-]*3[\s\-]*(?:documentation|certificate|form|tag)?',
    r'vendor.*who.*can.*provide.*8130',
    r'can\s+provide\s+8130'
]

print('Text:', text)
print()

for i, p in enumerate(patterns):
    match = re.search(p, text, re.IGNORECASE)
    print(f'Pattern {i}: {bool(match)}')
    if match:
        print(f'  Matched: "{match.group()}"')
    else:
        print(f'  Pattern: {p}')