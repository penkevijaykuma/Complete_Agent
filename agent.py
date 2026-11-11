import os
from dotenv import load_dotenv
from groq import Groq

# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()


class ResearchAgent:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )

        # Store conversation memory
        self.chat_history = []

    # ==========================================
    # Answer from Website Chunks (FAISS)
    # ==========================================

    def answer_question(
        self,
        question,
        chunks
    ):

        context = "\n\n".join(
            chunks
        )

        history = "\n".join(
            self.chat_history[-10:]
        )

        prompt = f"""
You are an Advanced AI Research Agent.

PREVIOUS CONVERSATION:

{history}

CONTEXT:

{context}

QUESTION:

{question}

Rules:

1. Use conversation history if required.
2. Answer only from context.
3. Do not hallucinate.
4. If answer unavailable:
   Information not found.
5. Keep answer concise.
"""

        response = (
            self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )
        )

        answer = (
            response
            .choices[0]
            .message
            .content
        )

        self.chat_history.append(
            f"User: {question}"
        )

        self.chat_history.append(
            f"Assistant: {answer}"
        )

        return answer

    # ==========================================
    # Answer using Web Search Results
    # ==========================================

    def answer_from_web(
        self,
        question,
        search_results
    ):

        context = ""

        for result in search_results:

            context += f"""

TITLE:
{result['title']}

CONTENT:
{result['body']}

SOURCE:
{result['href']}

--------------------------------
"""

        history = "\n".join(
            self.chat_history[-10:]
        )

        prompt = f"""
You are an Advanced AI Research Agent.

PREVIOUS CONVERSATION:

{history}

QUESTION:

{question}

SEARCH RESULTS:

{context}

Instructions:

1. Give direct answer.
2. Brief explanation.
3. Mention sources.
4. Keep answer factual.
"""

        response = (
            self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )
        )

        answer = (
            response
            .choices[0]
            .message
            .content
        )

        self.chat_history.append(
            f"User: {question}"
        )

        self.chat_history.append(
            f"Assistant: {answer}"
        )

        return answer

        # ==========================================
    # Generate Research Report
    # ==========================================

    def generate_report(
        self,
        topic,
        chunks
    ):

        context = "\n\n".join(
            chunks
        )

        history = "\n".join(
            self.chat_history[-10:]
        )

        prompt = f"""
You are a Senior Research Analyst.

PREVIOUS CONVERSATION:

{history}

Create a detailed research report on:

{topic}

Using the following context:

{context}

Report Format:

# Overview

# Key Information

# Important Facts

# Timeline

# Interesting Insights

# Summary

Write a professional report.
"""

        response = (
            self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )
        )

        report = (
            response
            .choices[0]
            .message
            .content
        )

        self.chat_history.append(
            f"User: research {topic}"
        )

        self.chat_history.append(
            f"Assistant: {report[:500]}"
        )

        return report