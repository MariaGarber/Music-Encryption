from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import ast

def decrypt(encr,privatekey):
    key = RSA.importKey(privatekey)
    decryptor = PKCS1_OAEP.new(key)
    decrypted = decryptor.decrypt(ast.literal_eval(str(encr)))
    print ("decrypted:", decrypted.decode())


def main():
    t='-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQCh3NC0Qj+YY379Z+C5ZWGLEQKI2XXP0U+vtBD/wy8HpsgCkKQV\nMbBohmrssOcGrYlmp5Os6eT65rfy1A2ww97XRflMuiAJWvPiQ4539W75iOGFBwUk\ne67n/2xZhxJtGppa1Iv6MOw+eTITMGYyKI8FNGE5xDXaxZAE0uUfDauFNwIDAQAB\nAoGABb7cha7dql91xYb8xM1NeMNCJMYbVs97laVoU7vY8oZADp9Abnl/ZTvIQIid\nsBtUMkRRNfpuJLMwj7ppQKoN7JCD+Psyp3DAon8hcjNB4AAF6Aa4rF1c08yM594Q\nGdTyygVIlAdEjD4wtGKRxbuiYt3kRxXLxkdBspTJS5ZsaxECQQDCPhAHZOIlYVqT\nxGTQgJpmM1c2Z4rOjax2lHTiw6kKdi4ovrkQ6tzAGXSWZXsO7ifRmyqYZiZS8IqM\nVrlHCIlvAkEA1VNDifHZLgH6RMu5yL4IptqhqMajLD8lmBlADjXoTIYndE9nEhOO\nZKlDv4K3wJbedKiIgV40R3z6bJJkMWEMuQJAfMgL2gQn9yV8X5L5xKvpBCCVNSD9\nHcYLdb3W/Nn+3PagnpIvJzwJheqUaA1XKXc64z9P9Mkic4ONLayEp6pHRwJBAJ5s\nLXYeM2llcpTwrtITvp0bNH8AtWFArAyeg+GJyzA5WMeZyDO2bkL3KSbqTsgpwp7k\nIivg5/ZHLDrBJMM/DZECQHm9STFmp758f4VQKNg5CduOm+DFcSQJdEFsyGOF2vat\n8DzXNMR420mQ4sblHb/VFeI7ol3wuU97NsjZhUDQeZ0=\n-----END RSA PRIVATE KEY-----'
    z=b"\x0c\xaa\xaaJ\xb6\xadV:\xc5\xea\r\xed\xbf\x14TN\x97\xbc;\xa8:d\xef\x01\x86U\xe9-\x80yl2\x1995\x86.\x84/\xfd!o?L?\x90\x9c\xe7\r\xe5\xb95\\C\xcc\x92\x14\x00\\'0gF7)\xf8\xd0Z:\xbe\xbd\xec\x15?U\x88$v\xf2_\xb6\xa1h\xdb\xdc\x05\xa6\xcfm_\x14\xf30\xd2\x9f\n\xe8\xbb\x9bVp\x16\x184\xb4\xaev\x84\xffI\x08_]GJ'g9c]-\x07\xa8\xb1\xf1\xc7\xd7K"
    decrypt(z,t)


main()