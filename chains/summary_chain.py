from config.llm import get_llm
from prompts.summary_prompt import map_prompt
from prompts.summary_prompt import reduce_prompt

def batch_list(items, batch_size):

    batches = []

    for i in range(
        0,
        len(items),
        batch_size
    ):
        batches.append(
            items[i:i + batch_size]
        )

    return batches


def generate_summary(docs):
    
    print('Inside the function')

    print("DOCS TYPE:", type(docs))
    print("FIRST ITEM TYPE:", type(docs[0]))

    llm = get_llm()

    map_chain = map_prompt | llm

    chunk_summaries = []

    for i, doc in enumerate(docs):

        print(f"Processing chunk {i}")
        print(type(doc))

        response = map_chain.invoke(
            {"chunk": doc.page_content}
        )

        chunk_summaries.append(
            response.content
        )

    reduce_chain = reduce_prompt | llm

    batches = batch_list(
     chunk_summaries,
     3
    )

    intermediate_summaries = []

    for batch in batches:

     batch_text = "\n".join(
        batch
    )

    response = reduce_chain.invoke(
        {
            "summaries": batch_text
        }
    )

    intermediate_summaries.append(
        response.content
    )

    final_text = "\n".join(
     intermediate_summaries
    )

    final_summary = reduce_chain.invoke(
    {
        "summaries": final_text
    }
    )

    return final_summary.content