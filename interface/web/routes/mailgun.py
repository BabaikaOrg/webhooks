import logging
import re

from fastapi import APIRouter, Request

router = APIRouter()
log = logging.getLogger(__name__)


@router.post("/webhook")
async def webhook(request: Request):
    email_pattern = r"\[via Relay\]\" <(.+)>"
    otp_pattern = r"Verification code:\D+(\d{4})"

    form = await request.form()

    if not form:
        log.warning("No form data received")
        return None

    stripped_text = str(form.get("stripped-text"))
    from_field = str(form.get("from"))

    if not stripped_text or not from_field:
        log.error("No stripped-text or from field")
        return None

    match = re.search(email_pattern, from_field)
    if match:
        email = match.group(1)
        log.debug(f"From field: {email}")
    else:
        log.error(f"Could not find email in from field: {from_field}")
        return None

    match = re.search(otp_pattern, stripped_text)
    if match:
        otp = match.group(1)
        log.debug(f"OTP: {otp}")
    else:
        log.error(f"Could not find OTP in stripped text: {stripped_text}")
        return None

    # Todo: put into DB

    return {"message": "Success"}
