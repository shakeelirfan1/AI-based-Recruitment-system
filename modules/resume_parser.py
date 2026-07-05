import fitz  # PyMuPDF


class ResumeParser:

    def extract_text(self, file):

        # If file comes from Streamlit uploader
        if hasattr(file, "read"):
            pdf = fitz.open(
                stream=file.read(),
                filetype="pdf"
            )

        # If file is a file path (from Gmail download)
        elif isinstance(file, str):
            pdf = fitz.open(file)

        else:
            raise ValueError("Unsupported file type.")

        text = ""

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return text