from Crypto.Cipher import AES as _AES
import binascii
from .keys import wbKey

# Padding for the input string --not
# related to encryption itself.
BLOCK_SIZE = 16  # Bytes
IV = b'\x00' * BLOCK_SIZE


MODE_CBC = _AES.MODE_CBC


def pad(s):
    return (
        s +
        (BLOCK_SIZE - len(s) % BLOCK_SIZE) *
        chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
    )


def unpad(s):
    return s[:-ord(s[len(s) - 1:])]


class AES:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key, mode=_AES.MODE_ECB, *args):
        try:
            self.key = binascii.unhexlify(key)
        except (TypeError, binascii.Error):
            self.key = key

        self._mode = mode
        self._args = args

    @property
    def _cipher(self):
        if self._mode == MODE_CBC:
            cipher = _AES.new(self.key, self._mode, IV)
        else:
            cipher = _AES.new(self.key, self._mode, *self._args)

        return cipher

    def decrypt(self, enc, remove_padding=True, unhexlify=binascii.unhexlify):
        if unhexlify is not None:
            data = unhexlify(enc)
        else:
            data = enc

        data = self._cipher.decrypt(data)

        if remove_padding:
            return unpad(data)
        else:
            return data

    def encrypt(self, raw, add_padding=True, encoding="utf8"):
        if add_padding:
            data = pad(raw)
        else:
            data = raw

        if encoding is not None:
            data = data.encode(encoding)

        return self._cipher.encrypt(data)


AES_CIPHER = AES(wbKey, MODE_CBC)
