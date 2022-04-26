from smtplib import SMTPException

import aioyagmail

import config
from models.models import User
from results import Result
from schemas.payloads import EmailPayload
from services import util_service
from services.user_services.token_generator import TokenGenerator

EMAIL_VERIFICATION_TOKEN_GENERATOR = TokenGenerator()


async def send_activation_email(url: str, user: User) -> Result:
    subject = "Email verification"
    email_path = config.ACTIVATION_EMAIL_PATH
    email_payload = __create_payload(url, subject, email_path, user)
    try:
        await __send_email(email_payload)
        return Result()
    except (SMTPException, ValueError) as ex:
        return Result(False, str(ex))


async def send_password_reset_email(url: str, user: User) -> Result:
    subject = "Password reset"
    email_path = config.PASSWORD_RESET_EMAIL_PATH
    email_payload = __create_payload(url, subject, email_path, user)
    try:
        await __send_email(email_payload)
        return Result()
    except (SMTPException, ValueError) as ex:
        return Result(False, str(ex))


async def __send_email(payload: EmailPayload) -> None:
    uid = util_service.urlsafe_base64_encode(util_service.force_bytes(payload.user.id))
    token = payload.token_generator.make_token(payload.user)
    url = f"{payload.url_prefix}/{uid}/{token}"
    body = __read_email_template(payload.template_path, payload.user.username, url)
    async with aioyagmail.AIOSMTP(
        user=config.EMAIL_USER,
        password=config.EMAIL_PASSWORD,
    ) as yag:
        await yag.send(to=payload.user.email, subject=payload.subject, contents=body)


def __read_email_template(template_path: str, username: str, url: str) -> str:
    with open(template_path) as f:
        return "\n".join(f.readlines()).replace("{username}", username).replace("{url}", url)


def __create_payload(url: str, subject: str, template_path: str, user: User) -> EmailPayload:
    return EmailPayload(
        url_prefix=url,
        subject=subject,
        template_path=template_path,
        user=user,
        token_generator=EMAIL_VERIFICATION_TOKEN_GENERATOR,
    )
