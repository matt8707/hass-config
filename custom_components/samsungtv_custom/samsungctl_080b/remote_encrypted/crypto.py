from __future__ import print_function
from . import keys

import hashlib
import struct
import logging
import binascii
from Crypto.Cipher import AES as _AES
from .rijndael import Rijndael
from .keys import PUBLIC_KEY, BN_PRIVATE_KEY, BN_PRIME, TRANS_KEY
from ..utils import LogItWithReturn


logger = logging.getLogger('samsungctl')


BLOCK_SIZE = 16
SHA_DIGEST_LENGTH = 20
USER_ID_POS = 15
USER_ID_LEN_POS = 11
GX_SIZE = 0x80
IV = b"\x00" * BLOCK_SIZE


try:
    # noinspection PyShadowingBuiltins
    unicode = unicode
except NameError:
    # noinspection PyShadowingBuiltins
    unicode = bytes


def bytes2str(data):
    data = binascii.hexlify(data)
    if isinstance(data, unicode):
        return data.decode('utf-8')
    else:
        return data


def debug(label, data):
    logging.debug('(' + label + ') ' + bytes2str(data))


def pack(data):
    return struct.pack('>I', data)


def unpack(data):
    return struct.unpack('>I', data)


@LogItWithReturn
def encrypt_parameter_data_with_aes(data):
    output = b""
    for num in range(0, 128, 16):
        cipher = _AES.new(binascii.unhexlify(keys.wbKey), _AES.MODE_CBC, IV)
        output += cipher.encrypt(data[num:num + 16])
    return output


@LogItWithReturn
def decrypt_parameter_data_with_aes(data):
    output = b""
    for num in range(0, 128, 16):
        cipher = _AES.new(binascii.unhexlify(keys.wbKey), _AES.MODE_CBC, IV)
        output += cipher.decrypt(data[num:num + 16])
    return output


def apply_samy_go_key_transform(data):
    r = Rijndael(TRANS_KEY)
    return r.encrypt(data)


@LogItWithReturn
def generate_server_hello(user_id, pin):
    pin_hash = generate_sha1(pin.encode('utf-8'))
    aes_key = pin_hash[:16]
    debug("AES key", aes_key)

    cipher = _AES.new(aes_key, _AES.MODE_CBC, IV)
    encrypted = cipher.encrypt(PUBLIC_KEY)
    debug("AES encrypted", encrypted)

    swapped = encrypt_parameter_data_with_aes(encrypted)
    debug("AES swapped", swapped)

    data = pack(len(user_id)) + user_id.encode('utf-8') + swapped
    debug("data buffer", data.upper())

    data_hash = generate_sha1(data)
    debug("hash", data_hash)

    server_hello = (
        b'\x01\x02\x00\x00\x00\x00\x00' +
        pack(len(user_id) + 132) +
        data +
        b'\x00\x00\x00\x00\x00'
    )
    return {"serverHello": server_hello, "hash": data_hash, "AES_key": aes_key}


@LogItWithReturn
def parse_client_hello(client_hello, aes_key, g_user_id):
    data = binascii.unhexlify(client_hello)
    debug('client_hello', data)

    user_id_len = unpack(data[11:15])[0]

    start = USER_ID_POS
    stop = user_id_len + USER_ID_POS

    user_id = data[start:stop]
    logger.debug('(user_id) ' + user_id.decode('utf-8'))

    start = stop
    stop += GX_SIZE

    p_enc_wbgx = data[start:stop]
    debug('pEncWBGx', p_enc_wbgx)

    p_enc_gx = decrypt_parameter_data_with_aes(p_enc_wbgx)
    debug('pEncGx', p_enc_gx)

    cipher = _AES.new(aes_key, _AES.MODE_CBC, IV)
    p_gx = cipher.decrypt(p_enc_gx)
    debug('pGx', p_gx)

    bn_pgx = int(bytes2str(p_gx), 16)
    secret_int = pow(bn_pgx, BN_PRIVATE_KEY, BN_PRIME)
    secret = hex(secret_int).upper().rstrip('L').lstrip('0X')
    secret = ((len(secret) % 2) * '0') + secret
    secret = binascii.unhexlify(secret)
    debug('secret', secret)

    if not check_pin_validity(
        user_id,
        data,
        stop,
        secret
    ):
        return False

    final_buffer = (
        user_id +
        g_user_id.encode('utf-8') +
        p_gx +
        PUBLIC_KEY +
        secret
    )

    sk_prime = generate_sha1(final_buffer)
    debug('sk_prime', sk_prime)

    sk_prime_hash = generate_sha1(sk_prime + b'\x00')
    debug('sk_prime_hash', sk_prime_hash)

    ctx = apply_samy_go_key_transform(sk_prime_hash[:16])

    return dict(ctx=ctx, SKPrime=sk_prime)


@LogItWithReturn
def check_pin_validity(user_id, data, start, secret):
    stop = start + SHA_DIGEST_LENGTH

    data_hash_2 = data[start:stop]
    debug('data_hash_2', data_hash_2)

    secret2 = user_id + secret
    debug("secret2", secret2)

    data_hash_3 = generate_sha1(secret2)
    debug("data_hash_3", data_hash_3)

    if data_hash_2 != data_hash_3:
        logger.debug('pin error!!!')
        return False

    start = stop
    stop += 1
    if ord(data[start:stop]):
        logger.debug('first flag error!!!')
        return False

    start = stop
    stop += 4
    if unpack(data[start:stop])[0]:
        logger.debug('second flag error!!!')
        return False

    return True


def generate_sha1(data):
    sha1 = hashlib.sha1()
    sha1.update(data)
    return sha1.digest()


@LogItWithReturn
def generate_server_acknowledge(sk_prime):
    sk_prime_hash = generate_sha1(sk_prime + b'\x01')

    return (
        '0103000000000000000014' +
        bytes2str(sk_prime_hash).upper() +
        '0000000000'
    )


@LogItWithReturn
def parse_client_acknowledge(client_ack, sk_prime):
    sk_prime_hash = generate_sha1(sk_prime + b'\x02')

    tmp_client_ack = (
        '0104000000000000000014' +
        bytes2str(sk_prime_hash).upper() +
        '0000000000'
    )

    return client_ack == tmp_client_ack
