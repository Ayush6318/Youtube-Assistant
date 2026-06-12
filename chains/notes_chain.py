from config.llm import get_llm

from prompts.notes_prompt import (
    notes_prompt
)

llm = get_llm()


def generate_notes(
    docs
):

    full_text = "\n".join(
        doc.page_content
        for doc in docs
    )

    chain = (
        notes_prompt
        |
        llm
    )

    response = chain.invoke(
        {
            "content": full_text
        }
    )

    return response.content