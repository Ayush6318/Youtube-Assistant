from langchain_core.prompts import ChatPromptTemplate

notes_prompt = ChatPromptTemplate.from_template(
    """
You are an expert note maker.

Create structured study notes from
the provided content.

Format:

# Overview

# Key Concepts

# Important Definitions

# Examples

# Key Takeaways

Content:

{content}
"""
)