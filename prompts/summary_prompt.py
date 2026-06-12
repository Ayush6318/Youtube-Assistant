from langchain_core.prompts import ChatPromptTemplate

map_prompt = ChatPromptTemplate.from_template(
"""
You are an expert educational content summarizer.

Analyze the transcript below.

Transcript:
{chunk}

Generate:

1. Executive Summary
2. Key Concepts
3. Important Insights
4. Final Takeaways

Keep response clear and structured.
"""
)

reduce_prompt = ChatPromptTemplate.from_template("""
Combine these summaries into one final summary:

{summaries}
""")