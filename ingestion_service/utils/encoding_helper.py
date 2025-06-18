def read_file_with_fallback(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(path, 'r', encoding='cp1256') as f:
                return f.read()
        except Exception as e:
            return f"⚠️ Error reading file: {str(e)}"
