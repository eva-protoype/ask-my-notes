from pypdf import PdfReader
##the functions begin
##Extract text from notes PDFs, keeping track of which page each piece of text came from
def pdf_pages(pdf_path:str):
    reader = PdfReader(pdf_path)
    return [(i+1, page.extract_text()) for i, page in enumerate(reader.pages)]

##chunking up the pdf (it remembers its page number)
def chunk_pages(pages, chunk_size=400):
    chunks = []
    for page_num, text in pages:##this is the list of tuples created by our pdf_pages function
        ##check for blank pages (skip if stumbled upon) (pages with images and no text layer get skipped)
        if not text:
            continue
        words = text.split()##list of words in the text of that page number
        for i in range(0, len(words), chunk_size):
            chunks.append({"page": page_num, "text": " ".join(words[i:i+chunk_size])})
    return chunks