from pypdf import PdfReader


def extract_text_from_pdf(file_path):

    reader = PdfReader(
        str(file_path)
    )

    pages = []


    for page in reader.pages:

        text = page.extract_text()

        if text is None:

            text = ""

        pages.append(text)


    return "\n".join(pages)