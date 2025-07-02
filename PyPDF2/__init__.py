class Page:
    def __init__(self, text: str):
        self._text = text
    def extract_text(self):
        return self._text

class PdfReader:
    def __init__(self, stream):
        if hasattr(stream, 'read'):
            data = stream.read()
        else:
            with open(stream, 'rb') as f:
                data = f.read()
        text = data.decode('utf-8', errors='ignore')
        self.pages = [Page(text)]
