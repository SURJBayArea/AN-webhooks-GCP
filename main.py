import json
import os

import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content


DEBUG = os.environ.get('DEBUG', False)
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SOURCE_EMAIL = 'support@surjbayarea.org'

COMMITTEES_BY_TAG = {
    # mapping of Action Network tag to email address for each committee
    'Interest_Basebuilding': 'basebuilding_notify@surjbayarea.org',
    'Communications': 'communications_notify@surjbayarea.org',
    'Fundraising': 'fundraising_notify@surjbayarea.org',
    'Mobilization': 'mobilization_notify@surjbayarea.org',
    'Queer_and_Trans': 'queertrans_notify@surjbayarea.org',
    'Youth_and_Families': 'youthandfamilies_notify@surjbayarea.org',
    'Public_Policy': 'policy_notify@surjbayarea.org',
    'Accessibility_Working_Group': 'accessibility_notify@surjbayarea.org',
}


def send_email(to_address, subject, body):
    print('SEND EMAIL', to_address, subject, body)
    if not SENDGRID_API_KEY:
        print('Sendgrid api key not found')
        return

    # in debug mode, only email myself
    if DEBUG:
        to_address = 'danajfallon@gmail.com'
        body = '[TEST] ' + body

    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    from_email = Email(SOURCE_EMAIL)
    to_email = To(to_address)
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)
    mail_json = mail.get()
    print('sending email')
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)


def http(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    print('RECEIVED REQUEST:', request)
    try:
        body = request.get_json()
    except Exception as e:
        raise e

    print('REQUEST BODY:')
    print(json.dumps(body))

    if not body:
        return 'No data received'

    if isinstance(body, list):
        body_elements = body
    else:
        body_elements = [body]
    for body_element in body_elements:
        print('checking element')
        submission = body_element.get('osdi:submission', {})
        added_tags = submission.get('add_tags', [])
        if not added_tags:
            continue
        person = submission.get('person')
        email_addresses = person.get('email_addresses')
        if not email_addresses:
            continue
        # prefer primary email address if there are multiple
        email_address = sorted(email_addresses, key=lambda x: x.get('is_primary', False))[0]['address']
        for tag in added_tags:
            if tag in COMMITTEES_BY_TAG:
                # send an email to the relevant committee
                subject = 'New committee signup'
                email_body = f'{email_address} has indicated interest in joining your committee!'
                to_address = COMMITTEES_BY_TAG[tag]
                if not to_address:
                    print('No contact email address for committee:', tag)
                    continue
                send_email(to_address, subject, email_body)

    return 'All done'
