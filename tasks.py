# import os
# import requests

# domain = os.getenv("MAILGUN_DOMAIN")
# api_key = os.getenv("MAILGUN_API_KEY")

# def send_simple_message(to, subject, body):
#     print("1")
#     return requests.post(
#         "https://api.mailgun.net/v3/{0}/messages".format(domain),
#         auth=("api", "{0}".format(api_key)),
#         data={
#             "from": "Excited User <mailgun@{0}>".format(domain),
#             "to": [to, "YOU@{0}".format(domain)],
#             "subject": subject,
#             "text": body
#         }
#     )

# def send_user_registration_email(email, username):
#     print("2")
#     return send_simple_message(
#         email,
#         "Successfully signed up",
#         f"Hi {username}! You have successfully signed up to the Stores REST API.",
#     )