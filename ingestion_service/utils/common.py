def decode_bytes(content_bytes):
    try:
        return content_bytes.decode('utf-8-sig')
    except UnicodeDecodeError:
        try:
            return content_bytes.decode('cp1256')
        except UnicodeDecodeError:
            return content_bytes.decode('utf-8', errors='ignore')
