# # from crewai import Agent, LLM
# # from langchain_groq import ChatGroq
# # import streamlit as st


# # llm = LLM(model="groq/llama-3.3-70b-versatile")


# # def build_agents():
# #     email_interpreter = Agent(
# #         role="Content Analyst",
# #         goal=(
# #             "Extract as many useful details as possible from ANY type of Content. "
# #             "Even if the Content is a single sentence or incomplete, "
# #             "never claim the Content is missing. "
# #             "Infer the user's intention whenever possible."
# #         ),
# #         backstory=(
# #             "You are an expert CAMS communication analyst. "
# #             "You handle well written, and poorly written, short, vague, and incomplete investor Contents daily. "
# #             "You ALWAYS extract whatever is available."
# #         ),
# #         llm=llm   # ✅ direct, no wrapper
# #     )

# #     response_writer = Agent(
# #         role="Response Writer",
# #         goal=(
# #             "Write a precise, polite, professional CAMS reply to the investor. "
# #             "If action is unclear, write a clarifying response. "
# #             "Always produce a clean final email body."
# #         ),
# #         backstory=(
# #             "You are a CAMS customer support representative. "
# #             "You generate high-quality investor communication emails."
# #         ),
# #         llm=llm   # ✅ direct, no wrapper
# #     )

# #     return email_interpreter, response_writer

# ########################################################################################################
# # crew_engine/agents.py
# from crewai import Agent, LLM

# llm = LLM(model="groq/llama-3.3-70b-versatile")

# def build_agents():
#     email_interpreter = Agent(
#         role="Content Analyst",
#         goal="Extract all useful information from any investor email.",
#         backstory="CAMS email analyst.",
#         llm=llm
#     )

#     response_writer = Agent(
#         role="Response Writer",
#         goal="Write a professional CAMS-ready reply.",
#         backstory="CAMS support representative.",
#         llm=llm
#     )

#     attachment_selector = Agent(
#         role="Attachment Selector",
#         goal=(
#             "Decide if the reply should include an attachment and determine what type (statement, KYC, performance, etc)."
#         ),
#         backstory="Expert at selecting which official CAMS document is required for each query.",
#         llm=llm
#     )

#     attachment_generator = Agent(
#         role="Attachment Generator",
#         goal=(
#             "Prepare structured content for a PDF attachment using extracted details. "
#             "Output pure JSON with fields the PDF builder will use."
#         ),
#         backstory="Specialist in preparing formal CAMS document contents.",
#         llm=llm
#     )

#     return email_interpreter, response_writer, attachment_selector, attachment_generator
# ########################################################################################################

# # agents.py
# from crewai import Agent, LLM

# llm = LLM(model="groq/llama-3.3-70b-versatile")

# def build_agents():
#     email_interpreter = Agent(
#         role="Content Analyst",
#         goal="Extract all useful information from any investor email.",
#         backstory="CAMS email analyst.",
#         llm=llm
#     )

#     response_writer = Agent(
#         role="Response Writer",
#         goal="Write a professional CAMS-ready reply.",
#         backstory="CAMS support representative.",
#         llm=llm
#     )

#     attachment_selector = Agent(
#         role="Attachment Selector",
#         goal=(
#             "Decide if the reply should include an attachment and determine what type "
#             "(statement, performance, KYC, etc.). Output ONLY JSON."
#         ),
#         backstory="Expert at choosing CAMS document requirements.",
#         llm=llm
#     )

#     attachment_generator = Agent(
#         role="Attachment Generator",
#         goal=(
#             "Prepare structured JSON content for a PDF attachment using extracted details. "
#             "Must output STRICT JSON only, no text outside the object."
#         ),
#         backstory="Specialist in preparing formal CAMS document contents.",
#         llm=llm
#     )

#     return email_interpreter, response_writer, attachment_selector, attachment_generator

########################################################################################################

# agents.py
from crewai import Agent, LLM

llm = LLM(model="groq/llama-3.3-70b-versatile")

def build_agents():
    email_interpreter = Agent(
        role="Content Analyst",
        goal="Extract all useful information from any investor email.",
        backstory="CAMS email analyst.",
        llm=llm
    )

    response_writer = Agent(
        role="Response Writer",
        goal="Write a professional CAMS-ready reply.",
        backstory="CAMS support representative.",
        llm=llm
    )

    attachment_selector = Agent(
        role="Attachment Selector",
        goal=(
            "Decide if an attachment is required and choose what type "
            "(statement, performance, kyc). Output STRICT JSON only."
        ),
        backstory="Expert in determining CAMS document requirements.",
        llm=llm
    )

    attachment_generator = Agent(
        role="Attachment Generator",
        goal=(
            "Generate STRICT JSON content for the PDF attachment. "
            "Must follow the exact template required by attachment_type."
        ),
        backstory="Specialist in preparing CAMS PDF document content.",
        llm=llm
    )

    return email_interpreter, response_writer, attachment_selector, attachment_generator
