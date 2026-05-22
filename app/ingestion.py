from pypdf import PdfReader
from pathlib import Path


def load_pdfs(documents_path="documents"):
    """
    Load all PDF files from the documents folder.

    Returns:
        List of dictionaries containing:
        - text
        - metadata (source file + page number)
    """

    documents = []

    # Find all PDF files
    pdf_files = Path(documents_path).glob("*.pdf")

    for pdf_file in pdf_files:
        try:
            reader = PdfReader(pdf_file)

            print(f"\nProcessing: {pdf_file.name}")

            for page_number, page in enumerate(reader.pages):
                try:
                    text = page.extract_text()

                    if text and text.strip():
                        documents.append({
                            "text": text.strip(),
                            "metadata": {
                                "source": pdf_file.name,
                                "page": page_number + 1
                            }
                        })

                except Exception as page_error:
                    print(
                        f"Skipping page {page_number + 1} "
                        f"from {pdf_file.name}: {page_error}"
                    )
                    continue

        except Exception as pdf_error:
            print(f"Error loading {pdf_file.name}: {pdf_error}")

    print(f"\nTotal pages loaded: {len(documents)}")

    return documents


if __name__ == "__main__":
    docs = load_pdfs()

    # Preview first loaded document
    if docs:
        print("\nSample Document:\n")
        print(docs[0]["text"][:500])

        print("\nMetadata:")
        print(docs[0]["metadata"])