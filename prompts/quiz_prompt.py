from langchain_core.prompts import ChatPromptTemplate

quiz_prompt = ChatPromptTemplate.from_template(
"""
Generate 10 multiple choice questions.

Return ONLY valid JSON.

Format:

[
    {{
        "question":"...",
        "options":[
            "...",
            "...",
            "...",
            "..."
        ],
        "answer":"..."
    }}
]

Content:

{content}
"""
)