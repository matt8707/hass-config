

class PaddingBase:
    def __init__(self, block_size):
        self.block_size = block_size

    def encode(self, source):
        raise NotImplementedError

    def decode(self, source):
        raise NotImplementedError


class ZeroPadding(PaddingBase):
    """
    Specified for hashes and MACs as Padding Method 1 in ISO/IEC 10118-1 and
    ISO/IEC 9797-1.
    """

    def encode(self, source):
        pad_size = (
            self.block_size -
            (
                (len(source) + self.block_size - 1) % self.block_size + 1
            )
        )
        return source + b'\0' * pad_size

    def decode(self, source):
        assert len(source) % self.block_size == 0
        offset = len(source)
        if offset == 0:
            return b''
        end = offset - self.block_size + 1

        while offset > end:
            offset -= 1
            if source[offset:offset+1] != b'\0':
                return source[:offset + 1]


class Pkcs7Padding(PaddingBase):
    """
    Technique for padding a string as defined in RFC 2315, section 10.3,
    note #2
    """

    def encode(self, source):
        amount_to_pad = self.block_size - (len(source) % self.block_size)
        amount_to_pad = (
            self.block_size if amount_to_pad == 0 else amount_to_pad
        )
        pad = chr(amount_to_pad).encode()
        return source + pad * amount_to_pad

    def decode(self, source):
        return source[:-source[-1]]
