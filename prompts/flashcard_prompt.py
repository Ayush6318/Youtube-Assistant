from langchain_core.prompts import ChatPromptTemplate

flashcard_prompt = ChatPromptTemplate.from_template(
"""
Create 15 study flashcards from the content.

Return ONLY valid JSON.

Format:

[
    {{
        "question":"...",
        "answer":"..."
    }}
]

Content:

{content}
"""
)