def token_to_int(token, n):
    import hashlib
    return str(int(hashlib.sha256(token.encode('utf-8')).hexdigest(), 16))[:n]
 