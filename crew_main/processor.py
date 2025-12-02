# # # crew_engine/processor.py
# # from crew_engine.crew_main import build_email_crew

# # def generate_response(email_content, predicted_category):
# #     crew = build_email_crew(email_content, predicted_category)

# #     result = crew.kickoff()

# #     # Return final task's raw output (the email text)
# #     try:
# #         return result.tasks_output[-1].raw
# #     except:
# #         return str(result)

# ########################################################################################################
# # crew_engine/processor.py
# import json
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from crew_engine.crew_main import build_email_crew

# def generate_pdf(json_data, output_path):
#     c = canvas.Canvas(output_path, pagesize=letter)
#     y = 750

#     c.setFont("Helvetica-Bold", 14)
#     c.drawString(50, y, json_data["title"])
#     y -= 40

#     c.setFont("Helvetica", 11)
#     for key, value in json_data.items():
#         if key == "title":
#             continue
#         c.drawString(50, y, f"{key}: {value}")
#         y -= 20

#     c.save()

# def generate_response(email_content, predicted_category):
#     crew = build_email_crew(email_content, predicted_category)
#     result = crew.kickoff()

#     final_reply = result.tasks_output[1].raw        # compose_task output
#     attachment_decision = json.loads(result.tasks_output[2].raw)
#     attachment_json = None
#     attachment_path = None

#     if attachment_decision.get("attachment_required"):
#         attachment_json = json.loads(result.tasks_output[3].raw)
#         attachment_path = "generated_attachment.pdf"
#         generate_pdf(attachment_json, attachment_path)

#     return {
#         "email_body": final_reply,
#         "attachment_path": attachment_path
#     }
# ########################################################################################################

# # processor.py
# import json
# import re
# from crew_engine.crew_main import build_email_crew

# from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors

# # --------------------------
# # SAFE JSON extraction
# # --------------------------
# def safe_json_extract(raw_text):
#     """
#     Extract the FIRST valid JSON object from an LLM response.
#     """
#     match = re.search(r'\{.*\}', raw_text, flags=re.DOTALL)
#     if not match:
#         raise ValueError("No JSON object found in LLM output")
#     return json.loads(match.group(0))


# # --------------------------
# # PDF Generator
# # --------------------------
# def generate_pdf(json_data, output_path):

#     doc = SimpleDocTemplate(output_path, pagesize=letter)
#     styles = getSampleStyleSheet()
#     flow = []

#     # Title
#     flow.append(Paragraph(f"<b>{json_data['title']}</b>", styles["Title"]))
#     flow.append(Spacer(1, 20))

#     # Summary paragraph
#     flow.append(Paragraph(json_data.get("summary", ""), styles["BodyText"]))
#     flow.append(Spacer(1, 20))

#     # HOLDINGS TABLE
#     holdings = json_data.get("holdings", [])
#     if holdings:
#         table_data = [["Date", "Units", "NAV"]]
#         for row in holdings:
#             table_data.append([row["date"], row["units"], row["nav"]])

#         t = Table(table_data)
#         t.setStyle([
#             ("BACKGROUND", (0,0), (-1,0), colors.lightblue),
#             ("GRID", (0,0), (-1,-1), 1, colors.black),
#         ])
#         flow.append(t)
#         flow.append(Spacer(1, 20))

#     # TRANSACTIONS TABLE
#     transactions = json_data.get("transactions", [])
#     if transactions:
#         table_data = [["Type", "Date", "Amount"]]
#         for row in transactions:
#             table_data.append([row["type"], row["date"], row["amount"]])

#         t = Table(table_data)
#         t.setStyle([
#             ("BACKGROUND", (0,0), (-1,0), colors.lightgreen),
#             ("GRID", (0,0), (-1,-1), 1, colors.black),
#         ])
#         flow.append(t)

#     doc.build(flow)


# # --------------------------
# # MAIN EXECUTION
# # --------------------------
# def generate_response(email_content, predicted_category):

#     crew = build_email_crew(email_content, predicted_category)
#     result = crew.kickoff()

#     # 1. Email reply
#     final_reply = result.tasks_output[1].raw

#     # 2. Attachment decision (Strict JSON)
#     attachment_decision = safe_json_extract(result.tasks_output[2].raw)

#     attachment_path = None

#     # 3. If attachment needed → build JSON + PDF
#     if attachment_decision.get("attachment_required"):

#         pdf_json = safe_json_extract(result.tasks_output[3].raw)
#         attachment_path = "generated_attachment.pdf"

#         generate_pdf(pdf_json, attachment_path)

#     return {
#         "email_body": final_reply,
#         "attachment_path": attachment_path
#     }

########################################################################################################

# # processor.py
# import json
# import re
# from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.pagesizes import letter
# from reportlab.lib import colors

# from crew_engine.crew_main import build_email_crew


# def safe_json_extract(raw_text):
#     match = re.search(r'\{.*\}', raw_text, flags=re.DOTALL)
#     if not match:
#         raise ValueError("No JSON found")
#     return json.loads(match.group(0))


# def pdf_statement(data, doc, flow, styles):
#     flow.append(Paragraph("<b>Account Statement</b>", styles["Title"]))
#     flow.append(Spacer(1, 20))

#     flow.append(Paragraph(data.get("summary", ""), styles["BodyText"]))
#     flow.append(Spacer(1, 20))

#     # Holdings Table
#     holdings = data.get("holdings", [])
#     if holdings:
#         table_data = [["Date", "Units", "NAV"]]
#         for row in holdings:
#             table_data.append([row["date"], row["units"], row["nav"]])
#         t = Table(table_data)
#         t.setStyle([("GRID", (0,0), (-1,-1), 1, colors.black)])
#         flow.append(t)
#         flow.append(Spacer(1, 20))

#     # Transactions Table
#     transactions = data.get("transactions", [])
#     if transactions:
#         table_data = [["Type", "Date", "Amount"]]
#         for row in transactions:
#             table_data.append([row["type"], row["date"], row["amount"]])
#         t = Table(table_data)
#         t.setStyle([("GRID", (0,0), (-1,-1), 1, colors.black)])
#         flow.append(t)

#     doc.build(flow)


# def pdf_performance(data, doc, flow, styles):
#     flow.append(Paragraph("<b>Fund Performance Report</b>", styles["Title"]))
#     flow.append(Spacer(1, 20))

#     returns = data.get("returns", {})
#     table_data = [["Period", "Return"]]
#     for k, v in returns.items():
#         table_data.append([k, v])

#     t = Table(table_data)
#     t.setStyle([("GRID", (0,0), (-1,-1), 1, colors.black)])
#     flow.append(t)
#     flow.append(Spacer(1, 20))


# def pdf_kyc(data, doc, flow, styles):
#     flow.append(Paragraph("<b>KYC Compliance Summary</b>", styles["Title"]))
#     flow.append(Spacer(1, 20))

#     info = [
#         f"Investor Name: {data.get('investor_name','')}",
#         f"PAN: {data.get('pan','')}",
#         f"Email: {data.get('email','')}",
#         f"Phone: {data.get('phone','')}",
#         f"KYC Status: {data.get('kyc_status','')}",
#         f"Last Updated: {data.get('last_updated','')}"
#     ]

#     for line in info:
#         flow.append(Paragraph(line, styles["BodyText"]))
#         flow.append(Spacer(1, 10))

#     doc.build(flow)


# def generate_pdf(json_data, output_path):

#     doc = SimpleDocTemplate(output_path, pagesize=letter)
#     styles = getSampleStyleSheet()
#     flow = []

#     atype = json_data.get("type")

#     if atype == "statement":
#         pdf_statement(json_data, doc, flow, styles)

#     elif atype == "performance":
#         pdf_performance(json_data, doc, flow, styles)

#     elif atype == "kyc":
#         pdf_kyc(json_data, doc, flow, styles)


# def generate_response(email_content, predicted_category):

#     crew = build_email_crew(email_content, predicted_category)
#     result = crew.kickoff()

#     final_reply = result.tasks_output[1].raw
#     decision = safe_json_extract(result.tasks_output[2].raw)

#     attachment_path = None

#     if decision.get("attachment_required"):
#         json_data = safe_json_extract(result.tasks_output[3].raw)
#         attachment_path = "generated_attachment.pdf"
#         generate_pdf(json_data, attachment_path)

#     return {
#         "email_body": final_reply,
#         "attachment_path": attachment_path
#     }

###################################################################################################

# processor.py
import json
import re
from crew_engine.crew_main import build_email_crew

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors


# --------------------------
# Extract JSON safely
# --------------------------
def safe_json_extract(raw_text):
    match = re.search(r'\{.*\}', raw_text, flags=re.DOTALL)
    if not match:
        raise ValueError("No JSON found")
    return json.loads(match.group(0))


# --------------------------
# PDF GENERATOR
# --------------------------
def generate_pdf(json_data, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    flow = []

    # Title
    flow.append(Paragraph(f"<b>{json_data.get('title','Document')}</b>", styles["Title"]))
    flow.append(Spacer(1, 20))

    # Summary / Description
    if json_data.get("summary"):
        flow.append(Paragraph(json_data["summary"], styles["BodyText"]))
        flow.append(Spacer(1, 20))

    # ACCOUNT STATEMENT tables
    if "holdings" in json_data:
        data = [["Date", "Units", "NAV"]]
        for h in json_data["holdings"]:
            data.append([h["date"], h["units"], h["nav"]])
        t = Table(data)
        t.setStyle([("GRID", (0,0), (-1,-1), 1, colors.black)])
        flow.append(t)
        flow.append(Spacer(1, 20))

    if "transactions" in json_data:
        data = [["Type", "Date", "Amount"]]
        for tx in json_data["transactions"]:
            data.append([tx["type"], tx["date"], tx["amount"]])
        t = Table(data)
        t.setStyle([("GRID", (0,0), (-1,-1), 1, colors.black)])
        flow.append(t)
        flow.append(Spacer(1, 20))

    # PERFORMANCE REPORT tables
    if "portfolio" in json_data:
        data = [["Sector", "Allocation"]]
        for row in json_data["portfolio"]:
            data.append([row["sector"], row["allocation"]])
        t = Table(data)
        t.setStyle([("GRID", (0,0), (-1,-1), 1, colors.black)])
        flow.append(t)
        flow.append(Spacer(1, 20))

    # KYC fields printed as bullet list
    if json_data.get("kyc_status"):
        for key in ["investor_name", "pan", "dob", "email", "phone", "address", "kyc_status", "verification_date"]:
            if json_data.get(key):
                flow.append(Paragraph(f"<b>{key.replace('_',' ').title()}:</b> {json_data[key]}", styles["BodyText"]))
                flow.append(Spacer(1, 10))

    doc.build(flow)


# --------------------------
# MAIN PIPELINE
# --------------------------
def generate_response(email_content, predicted_category):

    crew = build_email_crew(email_content, predicted_category)
    result = crew.kickoff()

    # Reply text
    reply = result.tasks_output[1].raw

    # Attachment decision
    decision = safe_json_extract(result.tasks_output[2].raw)
    attachment_path = None

    if decision.get("attachment_required"):
        pdf_json = safe_json_extract(result.tasks_output[3].raw)
        attachment_path = "generated_attachment.pdf"
        generate_pdf(pdf_json, attachment_path)

    return {
        "email_body": reply,
        "attachment_path": attachment_path
    }
