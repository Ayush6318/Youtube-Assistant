import json

from config.llm import get_llm

from prompts.quiz_prompt import (
    quiz_prompt
)

llm = get_llm()


def generate_quiz(
    docs
):

    full_text = "\n".join(
        doc.page_content
        for doc in docs
    )

    chain = (
        quiz_prompt
        |
        llm
    )

    response = chain.invoke(
        {
            "content": full_text
        }
    )

    content = response.content

    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )

    quiz = json.loads(
        content
    )

    return quiz