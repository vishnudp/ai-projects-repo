from nlp.semantic_matcher import SemanticMatcher

matcher = SemanticMatcher()

questions = [

    "Which tickets are done?",

    "What got delivered?",

    "Show pending stories",

    "How healthy is sprint?"
]

for q in questions:

    print(q)

    print(
        matcher.classify(q)
    )

    print()