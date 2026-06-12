from config.llm import get_llm
import json

from prompts.flashcard_prompt import (
    flashcard_prompt
)

llm = get_llm()


def generate_flashcards(
    docs
):

    full_text = "\n".join(
        doc.page_content
        for doc in docs
    )

    chain = (
        flashcard_prompt
        |
        llm
    )

    response = chain.invoke(
        {
            "content": full_text
        }
    )

    content =  response.content

    content = content.replace(
        "```json",""
    )

    content = content.replace(
        "```",""
    )

    flashcards = json.loads(content)

    return flashcards

    