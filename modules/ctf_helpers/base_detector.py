
import base64

def detect_base(text):
    results = []
    try:
        base64.b64decode(text, validate=True)
        results.append("Base64")
    except Exception:
        pass
    try:
        base64.b32decode(text)
        results.append("Base32")
    except Exception:
        pass
    try:
        base64.b16decode(text)
        results.append("Base16")
    except Exception:
        pass
    try:
        int(text, 16)
        results.append("Hex")
    except Exception:
        pass
    try:
        int(text, 2)
        results.append("Binary")
    except Exception:
        pass
    return results if results else ["Unknown or custom encoding"]
