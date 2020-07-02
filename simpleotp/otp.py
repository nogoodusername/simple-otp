import hashlib
import hmac
import random
from datetime import datetime, timedelta
from typing import Any, Sequence, Tuple, Optional


class OTP(object):
    """
    OTP Generations and Verification class
    """

    def __init__(self,
                 secret: str,
                 length: int = 7,
                 otp_chars: Sequence[str] = None,
                 digest: Any = hashlib.sha256,
                 expires_after: int = 15,
                 user_identifier: Optional[str] = None):
        """
        :param secret          : secret key used for hashing.
        :param length          : length of otp.
        :param otp_chars       : list of characters to be used to generate otp. by default setup to send numeric otp
        :param digest          : digest function to use for hashing.
        :param expires_after   : otp expiry in minutes
        :param user_identifier : user identifier can be phone number, email, user-id, username
        """
        self.secret = secret
        self.length = length
        self.digest = digest
        self.expires_after = expires_after
        self.user_identifier = user_identifier or 'Secret'
        self.otp_chars = otp_chars or list('0123456789')

    def generate(self) -> Tuple[str, str]:
        """
        Generate OTP
        :return: OTP, signature
        """

        otp = self.__generate_otp()
        expiry = int((datetime.utcnow() + timedelta(minutes=self.expires_after)).timestamp())

        hash_string = self.__generate_hash_string(otp, expiry)

        dig = self.__hmac(hash_string)
        signature = f"{dig}.{expiry}"

        return otp, signature

    def verify(self,
               otp: str,
               signature: str) -> bool:
        """
        Verify OTP using signature matching
        :param otp       : otp input from client
        :param signature : signature generated along with otp
        :return          : verified boolean
        """

        if signature.find('.') == -1 or len(signature.split('.')) != 2:
            return False

        dig, expiry = signature.split('.')

        if int(datetime.utcnow().timestamp()) > int(expiry):
            return False

        hash_string = self.__generate_hash_string(otp, expiry)
        n_dig = self.__hmac(hash_string)

        if dig == n_dig:
            return True

        return False

    def __generate_otp(self) -> str:
        """
        Generate OTP of length self.length
        :return: X character long otp
        """

        return ''.join(
            random.choice(self.otp_chars)
            for _ in range(self.length)
        )

    def __generate_hash_string(self,
                               otp: str,
                               expiry: int) -> str:
        """
        Generate string to be used for hashing
        :param otp     : otp string
        :param expiry  : expiry timestamp (seconds)
        :return        : string
        """

        return f"{self.user_identifier}.{otp}.{expiry}"

    def __hmac(self, hash_string: str) -> str:
        """
        Hashing method
        :param hash_string  : message to be hashed
        :return             : hexadecimal string
        """

        return hmac.new(self.secret.encode(), hash_string.encode(), digestmod=self.digest).hexdigest()
