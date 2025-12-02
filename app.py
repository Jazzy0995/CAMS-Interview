# import streamlit as st
# import joblib
# import numpy as np
# import smtplib
# from email.mime.text import MIMEText
# # -------------------------
# # Load model + vectorizer
# # -------------------------
# tfidf = joblib.load("tfidf_vectorizer.pkl")
# model = joblib.load("email_classifier_lr.pkl")
# label_encoder = joblib.load("label_encoder.pkl")

# GMAIL_USER = st.secrets["gmail_user"]
# GMAIL_APP_PASSWORD = st.secrets["gmail_password"]

# CATEGORIES = [
#     'Account Statement Requests',
#     'Complaint Handling and Escalations',
#     'Distributor Commissions and Payouts',
#     'Fund Performance Queries',
#     'General Queries (Other)',
#     'KYC/Compliance Issues',
#     'Redemption Requests',
#     'SIP Modifications'
# ]

# # -------------------------
# # Session State Setup
# # -------------------------
# if "predicted_category" not in st.session_state:
#     st.session_state.predicted_category = None

# if "confidence" not in st.session_state:
#     st.session_state.confidence = None

# if "show_send_button" not in st.session_state:
#     st.session_state.show_send_button = False


# # -------------------------
# # Email Sending Function
# # -------------------------
# def send_email(to_email, subject, body):
    
#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = GMAIL_USER
#     msg["To"] = to_email

#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#         server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
#         server.sendmail(GMAIL_USER, to_email, msg.as_string())


# # -------------------------
# # UI
# # -------------------------
# st.title("📧 CAMS Email Classification Demo")

# email_text = st.text_area("Paste email content", height=200)


# # -------------------------
# # Predict Button
# # -------------------------
# if st.button("Predict Category"):
#     if email_text.strip() == "":
#         st.warning("Please paste an email first.")
#     else:
#         # Vectorize and predict
#         vec = tfidf.transform([email_text])
#         proba = model.predict_proba(vec)[0]
#         idx = np.argmax(proba)
#         label = label_encoder.inverse_transform([idx])[0]
#         conf = proba[idx]

#         # Store in session state
#         st.session_state.predicted_category = label
#         st.session_state.confidence = conf
#         st.session_state.show_send_button = True


# # -------------------------
# # Show prediction (if available)
# # -------------------------
# if st.session_state.predicted_category:
#     st.success(f"Predicted Category: **{st.session_state.predicted_category}**")
#     st.write(f"Confidence: `{st.session_state.confidence:.3f}`")

#     # Allow user to override
#     selected_category = st.selectbox(
#         "Select / override category:",
#         CATEGORIES,
#         index=CATEGORIES.index(st.session_state.predicted_category)
#     )

#     # -------------------------
#     # Send Email Button
#     # -------------------------
#     if st.session_state.show_send_button:
#         if st.button("Submit & Send Email"):
#             cat = selected_category

#             if cat == "Account Statement Requests":
#                 body = "Your request for an account statement has been received."
#             elif cat == "Redemption Requests":
#                 body = "Your redemption request has been received and is being processed."
#             elif cat == "SIP Modifications":
#                 body = "Your SIP modification request has been acknowledged."
#             elif cat == "KYC/Compliance Issues":
#                 body = "Your KYC/compliance issue is being reviewed."
#             elif cat == "Complaint Handling and Escalations":
#                 body = "Your complaint has been registered."
#             elif cat == "Fund Performance Queries":
#                 body = "Your fund performance query has been noted."
#             elif cat == "Distributor Commissions and Payouts":
#                 body = "Your distributor commission query is being reviewed."
#             else:
#                 body = "Thank you for contacting us."

#             send_email(
#                 "thejassairam95@gmail.com",
#                 subject=f"[CAMS Demo] {cat}",
#                 body=body
#             )

#             st.success("📩 Email sent successfully!")


# app.py
import streamlit as st
import joblib
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

# from langchain_openai import ChatOpenAI
from crew_engine.processor import generate_response

# -------------------------
# Load model + vectorizer
# -------------------------
tfidf = joblib.load("tfidf_vectorizer.pkl")
model = joblib.load("email_classifier_lr.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# -------------------------
# Email creds
# -------------------------
GMAIL_USER = st.secrets["gmail_user"]
GMAIL_APP_PASSWORD = st.secrets["gmail_password"]


# -------------------------
# Helpers
# -------------------------
# def send_email(to_email, subject, body):
#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = GMAIL_USER
#     msg["To"] = to_email

#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#         server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
#         server.sendmail(GMAIL_USER, to_email, msg.as_string())
def send_email(to_email, subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = to_email

    msg.attach(MIMEText(body, "plain"))

    if attachment_path:
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={attachment_path.split('/')[-1]}"
        )
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, to_email, msg.as_string())


# -------------------------
# UI
# -------------------------
st.title("📧 CAMS Email Classification + AI Reply")

email_text = st.text_area("Paste email content:", height=200)


if "predicted_category" not in st.session_state:
    st.session_state.predicted_category = None
    st.session_state.confidence = None
    st.session_state.generated_response = None

if st.button("Predict Category"):
    if not email_text.strip():
        st.warning("Please enter an email first.")
    else:
        vec = tfidf.transform([email_text])
        proba = model.predict_proba(vec)[0]
        idx = np.argmax(proba)
        label = label_encoder.inverse_transform([idx])[0]
        conf = proba[idx]

        st.session_state.predicted_category = label
        st.session_state.confidence = conf

if st.session_state.predicted_category:
    st.success(f"Predicted Category: **{st.session_state.predicted_category}**")
    st.write(f"Confidence: `{st.session_state.confidence:.3f}`")

    selected_category = st.selectbox(
        "Select / override category:",
        label_encoder.classes_,
        index=list(label_encoder.classes_).index(st.session_state.predicted_category)
    )

    # if st.button("Generate AI Response"):
    #     with st.spinner("AI is generating the response..."):
    #         response_text = generate_response(
    #             email_text=email_text,
    #             predicted_category=selected_category
    #         )
    #         st.session_state.generated_response = response_text

    if st.button("Generate AI Response"):
        with st.spinner("AI is generating the response..."):
            response = generate_response(
                email_text,
                selected_category
            )
            st.session_state.response = response
            st.session_state.generated_response = response["email_body"]
            print("-----++++++-----+++++-----",response["attachment_path"])
    if st.session_state.generated_response:
        st.subheader("AI-Generated Email")
        st.write(st.session_state.generated_response)
        

        # if st.button("Send Email"):
        #     send_email(
        #         "thejassairam95@gmail.com",
        #         subject=f"[CAMS Demo] {selected_category}",
        #         body=st.session_state.generated_response,
        #     )
        #     st.success("📩 Email sent successfully!")
        # Ensure attachment session State exists
        if "attachment" not in st.session_state:
            st.session_state.attachment = None

        # Button: Send Email
        if st.button("Send Email"):
            # Get attachment from stored response
            st.session_state.attachment = st.session_state.response.get("attachment_path")

            st.info(f"Attachment generated: {st.session_state.attachment}")

            send_email(
                "thejassairam95@gmail.com",
                subject=f"[CAMS Demo] {selected_category}",
                body=st.session_state.generated_response,
                attachment_path=st.session_state.attachment
            )

            st.success("📩 Email sent successfully!")
