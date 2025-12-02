# # # crew_engine/tasks.py
# # from crewai import Task

# # def build_tasks(email_interpreter, response_writer, email_content, predicted_category):

# #     interpret_task = Task(
# #         description=(
# #             f"Analyze the following investor email:\n\n"
# #             f"{email_content}\n\n"
# #             "Extract ALL useful details — even if email is short or unclear. "
# #             "NEVER say the email is missing. If a field is absent, set it to null "
# #             "but infer meaning where possible.\n\n"
# #             "Return a structured output (dictionary-like) with fields:\n"
# #             "- action\n"
# #             "- folio\n"
# #             "- fund_name\n"
# #             "- scheme\n"
# #             "- amount\n"
# #             "- dates\n"
# #             "- investor_name\n"
# #             "- pan\n"
# #             "- email_address\n"
# #             "- phone\n"
# #             "- tone\n"
# #             "- urgency\n"
# #             "- summary\n"
# #         ),
# #         expected_output="A structured dictionary-like output containing extracted and inferred details.",
# #         agent=email_interpreter
# #     )

# #     compose_task = Task(
# #         description=(
# #             f"Using the extracted information below, write a CAMS-ready professional reply.\n\n"
# #             f"Extracted details:\n{{{{ interpret_task.output }}}}\n\n"
# #             f"Predicted Category: {predicted_category}\n\n"
# #             "Rules:\n"
# #             "- If Category == 'Account Statement Requests' AND folio exists → reply with Statement-of-Account email.\n"
# #             "- If investor explicitly asks for anything → respond accordingly.\n"
# #             "- If action unclear → ask EXACTLY ONE clarifying question.\n"
# #             "- ALWAYS use professional CAMS tone.\n"
# #             "- NEVER say the email content was missing.\n"
# #             "- Output ONLY the final email body (no meta text).\n"
# #         ),
# #         expected_output="A professionally written email ready to send.",
# #         agent=response_writer
# #     )

# #     return interpret_task, compose_task


# ########################################################################################################
# # crew_engine/tasks.py
# from crewai import Task

# def build_tasks(email_interpreter, response_writer, attachment_selector,
#                 attachment_generator, email_content, predicted_category):

#     # --- Existing interpret and compose tasks ---
#     interpret_task = Task(
#         description=(
#             f"Analyze the following investor email:\n\n"
#             f"{email_content}\n\n"
#             "Extract all useful fields. Never say email is missing."
#         ),
#         expected_output="dictionary-like structured extraction",
#         agent=email_interpreter
#     )

#     compose_task = Task(
#         description=(
#             f"Write a professional CAMS reply.\n"
#             f"Email details:\n{{{{ interpret_task.output }}}}\n"
#             f"Category: {predicted_category}"
#         ),
#         expected_output="ready-to-send email body",
#         agent=response_writer
#     )

#     # --- NEW: Attachment selection task ---
#     decide_attachment_task = Task(
#         description=(
#             "Based on the extracted info, decide if an attachment is needed.\n\n"
#             "Input:\n{{ interpret_task.output }}\n"
#             f"Category: {predicted_category}\n\n"
#             "Output MUST be valid JSON with:\n"
#             "{\n"
#             "  'attachment_required': true/false,\n"
#             "  'attachment_type': 'statement' | 'kyc' | 'performance' | null\n"
#             "}"
#         ),
#         expected_output="JSON selecting attachment type",
#         agent=attachment_selector
#     )

#     # --- NEW: Attachment content generator ---
#     create_attachment_task = Task(
#         description=(
#             "Generate structured data for the attachment.\n"
#             "ONLY if attachment_required is true.\n\n"
#             "Inputs:\n"
#             "- Extracted details: {{ interpret_task.output }}\n"
#             "- Attachment decision: {{ decide_attachment_task.output }}\n\n"
#             "Output VALID JSON with fields needed for PDF creation:\n"
#             "{\n"
#             "  'title': '...',\n"
#             "  'folio': '...',\n"
#             "  'fund_name': '...',\n"
#             "  'investor_name': '...',\n"
#             "  'pan': '...',\n"
#             "  'email': '...',\n"
#             "  'amount': '...',\n"
#             "  'date_range': '...',\n"
#             "  'body': '...'  # text body for the PDF\n"
#             "}"
#         ),
#         expected_output="JSON describing PDF content",
#         agent=attachment_generator
#     )

#     return interpret_task, compose_task, decide_attachment_task, create_attachment_task
# ########################################################################################################

# # tasks.py
# from crewai import Task

# def build_tasks(
#     email_interpreter,
#     response_writer,
#     attachment_selector,
#     attachment_generator,
#     email_content,
#     predicted_category
# ):

#     # 1️⃣ Interpret email
#     interpret_task = Task(
#         description=(
#             f"Analyze the following investor email:\n\n"
#             f"{email_content}\n\n"
#             "Extract ALL possible fields (action, folio, fund name, PAN, dates, amount, etc.) "
#             "Never say the email content is missing."
#         ),
#         expected_output="dictionary-like structured extraction",
#         agent=email_interpreter
#     )

#     # 2️⃣ Write reply email
#     compose_task = Task(
#         description=(
#             "Write a professional CAMS reply email.\n\n"
#             "Use these extracted details:\n{{ interpret_task.output }}\n\n"
#             f"Predicted category: {predicted_category}\n\n"
#             "Rules:\n"
#             "- If action is explicit, respond accordingly.\n"
#             "- If unclear, ask ONE clarifying question.\n"
#             "- Do NOT mention attachments being prepared — because the PDF will already be attached.\n"
#             "- Output ONLY the final email body."
#         ),
#         expected_output="ready-to-send email body",
#         agent=response_writer
#     )

#     # 3️⃣ Decide if attachment is needed
#     decide_attachment_task = Task(
#         description=(
#             "Based on extracted details, decide if an attachment is required.\n\n"
#             "Inputs:\n"
#             "{{ interpret_task.output }}\n"
#             f"Category: {predicted_category}\n\n"
#             "Rules:\n"
#             "- Account Statement Requests → attachment_required=true, attachment_type=\"statement\".\n"
#             "- Fund Performance Queries → attachment_required=true, attachment_type=\"performance\".\n"
#             "- KYC/Compliance Issues → attachment_required=true, attachment_type=\"kyc\".\n"
#             "- Otherwise → attachment_required=false.\n\n"
#             "OUTPUT STRICT JSON ONLY:\n"
#             "{\n"
#             "  \"attachment_required\": true/false,\n"
#             "  \"attachment_type\": \"statement\" | \"performance\" | \"kyc\" | null\n"
#             "}"
#         ),
#         expected_output="Strict JSON selecting attachment type",
#         agent=attachment_selector
#     )

#     # 4️⃣ Generate structured PDF content
#     create_attachment_task = Task(
#         description=(
#             "Generate structured JSON for a CAMS PDF attachment.\n"
#             "You MUST output pure JSON with NO extra text.\n\n"
#             "Inputs:\n"
#             "- Extracted details: {{ interpret_task.output }}\n"
#             "- Attachment decision: {{ decide_attachment_task.output }}\n\n"
#             "If attachment_required=false, output:\n"
#             "{\"attachment_required\": false}\n\n"

#             "If true, output EXACT JSON format:\n"
#             "{\n"
#             "  \"title\": \"Account Statement\",\n"
#             "  \"investor_name\": \"...\",\n"
#             "  \"folio\": \"...\",\n"
#             "  \"fund_name\": \"...\",\n"
#             "  \"pan\": \"...\",\n"
#             "  \"email\": \"...\",\n"
#             "  \"amount\": \"...\",\n"
#             "  \"date_range\": \"2024-01-01 to 2024-12-31\",\n"
#             "  \"summary\": \"One paragraph describing the folio performance...\",\n"
#             "  \"holdings\": [\n"
#             "      {\"date\": \"YYYY-MM-DD\", \"units\": 0, \"nav\": 0.0}\n"
#             "  ],\n"
#             "  \"transactions\": [\n"
#             "      {\"type\": \"Purchase\", \"date\": \"YYYY-MM-DD\", \"amount\": 0}\n"
#             "  ]\n"
#             "}"
#         ),
#         expected_output="Strict JSON describing PDF content",
#         agent=attachment_generator
#     )

#     return interpret_task, compose_task, decide_attachment_task, create_attachment_task



#######################################################################################################

# tasks.py
from crewai import Task

def build_tasks(
    email_interpreter,
    response_writer,
    attachment_selector,
    attachment_generator,
    email_content,
    predicted_category
):

    # 1️⃣ Extract details
    interpret_task = Task(
        description=(
            f"Analyze the following investor email:\n\n"
            f"{email_content}\n\n"
            "Extract ALL useful fields such as: action, folio, fund_name, scheme, amount, "
            "dates, investor_name, pan, email_address, phone, tone, urgency, summary.\n"
            "Never say email content is missing."
        ),
        expected_output="Structured dictionary-like extraction.",
        agent=email_interpreter
    )

    # 2️⃣ Write email reply
    compose_task = Task(
        description=(
            "Write a polite CAMS reply email.\n\n"
            "Use extracted details:\n{{ interpret_task.output }}\n\n"
            f"Predicted category: {predicted_category}\n\n"
            "Rules:\n"
            "- If action is clear → respond directly.\n"
            "- If unclear → ask ONE clarifying question.\n"
            "- Do NOT mention attachments.\n"
            "- Output ONLY the final email body."
        ),
        expected_output="Professional final email body.",
        agent=response_writer
    )

    # 3️⃣ Decide attachment type
    decide_attachment_task = Task(
        description=(
            "Decide if a PDF attachment is required.\n\n"
            "Inputs:\n{{ interpret_task.output }}\n"
            f"Category: {predicted_category}\n\n"
            "Rules:\n"
            "- Account Statement Requests → statement\n"
            "- Fund Performance Queries → performance\n"
            "- KYC/Compliance Issues → kyc\n"
            "- Else → no attachment\n\n"
            "Output STRICT JSON:\n"
            "{\n"
            "  \"attachment_required\": true/false,\n"
            "  \"attachment_type\": \"statement\" | \"performance\" | \"kyc\" | null\n"
            "}"
        ),
        expected_output="Strict JSON attachment decision.",
        agent=attachment_selector
    )

    # 4️⃣ Generate JSON for PDF content
    create_attachment_task = Task(
        description=(
            "Generate STRICT JSON for a PDF attachment.\n\n"
            "Inputs:\n"
            "- Extracted: {{ interpret_task.output }}\n"
            "- Attachment decision: {{ decide_attachment_task.output }}\n\n"

            "If attachment_required=false, output exactly:\n"
            "{\"attachment_required\": false}\n\n"

            "If statement attachment:\n"
            "{\n"
            "  \"title\": \"Account Statement\",\n"
            "  \"investor_name\": \"...\",\n"
            "  \"folio\": \"...\",\n"
            "  \"fund_name\": \"...\",\n"
            "  \"pan\": \"...\",\n"
            "  \"email\": \"...\",\n"
            "  \"amount\": \"...\",\n"
            "  \"date_range\": \"2024-01-01 to 2024-12-31\",\n"
            "  \"summary\": \"...\",\n"
            "  \"holdings\": [{\"date\": \"YYYY-MM-DD\", \"units\": 0, \"nav\": 0.0}],\n"
            "  \"transactions\": [{\"type\": \"Purchase\", \"date\": \"YYYY-MM-DD\", \"amount\": 0}]\n"
            "}\n\n"

            "If performance attachment:\n"
            "{\n"
            "  \"title\": \"Fund Performance Report\",\n"
            "  \"investor_name\": \"...\",\n"
            "  \"folio\": \"...\",\n"
            "  \"fund_name\": \"...\",\n"
            "  \"pan\": \"...\",\n"
            "  \"returns\": {\"1Y\": \"...\", \"3Y\": \"...\", \"5Y\": \"...\"},\n"
            "  \"benchmark\": \"...\"," 
            "  \"risk_rating\": \"Low/Medium/High\",\n"
            "  \"summary\": \"1–2 line summary...\",\n"
            "  \"portfolio\": [\n"
            "      {\"sector\": \"...\", \"allocation\": \"...%\"}\n"
            "  ]\n"
            "}\n\n"

            "If kyc attachment:\n"
            "{\n"
            "  \"title\": \"KYC Information Document\",\n"
            "  \"investor_name\": \"...\",\n"
            "  \"pan\": \"...\",\n"
            "  \"dob\": \"YYYY-MM-DD\",\n"
            "  \"email\": \"...\",\n"
            "  \"phone\": \"...\",\n"
            "  \"address\": \"...\",\n"
            "  \"kyc_status\": \"Verified/Pending\",\n"
            "  \"verification_date\": \"YYYY-MM-DD\"\n"
            "}"
        ),
        expected_output="Strict JSON describing PDF structure.",
        agent=attachment_generator
    )

    return interpret_task, compose_task, decide_attachment_task, create_attachment_task
