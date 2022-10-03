from time import sleep

from simpleotp import OTP, generate_secret


def test_generate_secret():
    secret_key = generate_secret()

    assert (
        type(secret_key) == str
    ), f"secret_key was not a string, secret_key value was {secret_key} of type {type(secret_key)}"


def test_otp_generate():
    secret_key = generate_secret()
    length = 4

    otp_handler = OTP(
        secret_key, length=length, expires_after=1, user_identifier="test_user"
    )

    otp, sig = otp_handler.generate()

    assert (
        type(otp) == str
    ), f"otp was not a string, otp value was {otp} of type {type(otp)}"
    assert (
        type(sig) == str
    ), f"signature was not a string, signature value was {sig} of type {type(sig)}"
    assert len(otp) == length, f"otp length was {len(otp)}, it should be {length}"


def test_otp_verification():
    secret_key = generate_secret()
    length = 4
    expires_after = 1

    otp_handler = OTP(
        secret_key,
        length=length,
        expires_after=expires_after,
        user_identifier="test_user",
    )
    otp, sig = otp_handler.generate()

    is_verified = otp_handler.verify(otp, sig)
    assert is_verified is True

    is_not_verified_otp = otp_handler.verify(otp + ".", sig)
    assert is_not_verified_otp is False, "otp should not be verified"

    is_not_verified_sig = otp_handler.verify(otp, sig + ".")
    assert (
        is_not_verified_sig is False
    ), "otp should not be verified as signature is mismatched"

    sleep(expires_after * 60 + 1)

    is_not_verified_time = otp_handler.verify(otp, sig)
    assert is_not_verified_time is False, "otp should not be verified as it is expired"
