import os
import sendgrid

sg = sendgrid.SendGridAPIClient(api_key='YOUR_API_KEY_HERE')

# Your email must be authenticated on SendGrid, within Setting -> Sender Identity,
# or you will get an Unauthorized error.
sender_email = 'SENDER_EMAIL'
sender_name = "COMPANY_NAME"


class EmailService:

    @staticmethod
    def generic_email(user, subject, message, template_id, optional_template_data=None):
        data = {
            "personalizations": [
                {
                    "to": [user],
                    "dynamic_template_data": {
                        "name": user['name'],
                        "message": message,
                        "subject": subject
                    },
                }
            ],
            "from": {
                "email": sender_email,
                "name": sender_name
            },
            "reply_to": {
                "email": sender_email,
                "name": sender_name,
                'subject': 'email-reply'
            },
            "template_id": template_id
        }

        # Add any additional fields passed to the template data
        if optional_template_data:
            for key in optional_template_data:

                # I know, this part needs an upgrade, feel free to suggest one!
                dynamic_template_data = data["personalizations"][0]["dynamic_template_data"]
                dynamic_template_data[key] = optional_template_data[key]

        try:
            response = sg.client.mail.send.post(request_body=data)
            print(response.status_code)
            print(response.body)
            print(response.headers)

        except Exception as e:
            print(e)

    @staticmethod
    def send_welcome_email(user, **optional_args):

        subject = "Welcome to MyCompany!"
        message = "SOME_MESSAGE_TEMPLATE"

        # Standard template (without button or image)
        template_id = "TEMPLATE_ID"

        # In here I checked which template I would use.
        # Its very trivial but gets the job done as there are only two optional fields

        if optional_args:
            if 'button_text' in optional_args:
                # Button only template
                template_id = "TEMPLATE_ID"

                if 'img_src' in optional_args:

                    # Template with button and image
                    template_id = "TEMPLATE_ID"

            elif 'img_src' in optional_args:
                # Image only template
                template_id = "TEMPLATE_ID"

        EmailService.generic_email(user=user, subject=subject, message=message, template_id=template_id,
                                   optional_template_data=optional_args)


users = [{
    "name": "John",
    "email": "john@mail.com"
}]

for u in users:

    # Mandatory args(1): user.
    # Optional args(n): any variables used by the template you are passing.

    # In my case, I needed templates with a button and an image,
    # so i specified the template_id based on the args passed within the function.

    EmailService.send_welcome_email(user=u, button_text='Click here!', img_src='SOME_IMG_URL')

