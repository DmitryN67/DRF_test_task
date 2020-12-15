def token_to_int(token, n):
    """
        Convert token to integer value length of n
    """
    import hashlib
    return str(int(hashlib.sha256(token.encode('utf-8')).hexdigest(), 16))[:n]
 