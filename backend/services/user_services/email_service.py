from base64 import urlsafe_b64encode
from smtplib import SMTPException

import yagmail

import config
from models.models import User
from results import Result
from schemas.payloads import EmailPayload
from services import util_service
from services.user_services.token_generator import TokenGenerator

EMAIL_VERIFICATION_TOKEN_GENERATOR = TokenGenerator()


def send_activation_email(url: str, user: User) -> Result:
    subject = "Account activation"
    email_path = config.ACTIVATION_EMAIL_PATH
    email_payload = EmailPayload(
        url_prefix=url,
        subject=subject,
        template_path=email_path,
        user=user,
        token_generator=EMAIL_VERIFICATION_TOKEN_GENERATOR,
    )
    try:
        __send_email(email_payload)
        return Result()
    except (SMTPException, ValueError) as ex:
        return Result(False, str(ex))


def __send_email(payload: EmailPayload) -> None:
    uid = util_service.urlsafe_base64_encode(util_service.force_bytes(payload.user.id))
    token = payload.token_generator.make_token(payload.user)
    url = f"{payload.url_prefix}/{uid}/{token}"
    yag = yagmail.SMTP(config.EMAIL_USER)
    body = __read_email_template(payload.template_path, payload.user.username, url)
    yag.send(to=payload.user.email, subject=payload.subject, contents=body)


def __read_email_template(template_path: str, username: str, url: str) -> str:
    with open(template_path) as f:
        return "\n".join(f.readlines()).replace("{username}", username).replace("{url}", url)
