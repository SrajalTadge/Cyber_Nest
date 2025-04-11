
from PIL import Image
from PIL.ExifTags import TAGS
from PyPDF2 import PdfReader

def extract_metadata(file_path):
    metadata = {}
    try:
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            img = Image.open(file_path)
            info = img._getexif()
            if info:
                for tag, val in info.items():
                    decoded = TAGS.get(tag, tag)
                    metadata[decoded] = str(val)
        elif file_path.lower().endswith('.pdf'):
            reader = PdfReader(file_path)
            if reader.metadata:
                for key, value in reader.metadata.items():
                    metadata[key] = str(value)
    except Exception as e:
        metadata["error"] = str(e)
    return metadata if metadata else {"info": "No metadata found"}
