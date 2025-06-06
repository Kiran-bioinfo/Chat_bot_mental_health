import pdfplumber
import re
import os
import nltk
from nltk.tokenize import sent_tokenize
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    nltk.download('punkt')

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces/newlines with a single space
    text = text.strip()
    return text

def split_into_chunks(text, max_tokens=300, sentences_per_chunk=(2, 3)):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk_sentences = []
    current_chunk_tokens = 0

    for sentence in sentences:
        sentence_tokens = len(sentence.split())
        
        # If adding the sentence exceeds max_tokens, or if we have enough sentences for a chunk
        if (current_chunk_tokens + sentence_tokens > max_tokens and current_chunk_sentences) or \
           (len(current_chunk_sentences) >= sentences_per_chunk[1]):
            chunks.append(" ".join(current_chunk_sentences))
            current_chunk_sentences = [sentence]
            current_chunk_tokens = sentence_tokens
        else:
            current_chunk_sentences.append(sentence)
            current_chunk_tokens += sentence_tokens

    if current_chunk_sentences:
        chunks.append(" ".join(current_chunk_sentences))
    return chunks

def process_pdf_directory(directory_path, output_file='chunks.txt'):
    all_chunks = []
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith('.pdf'):
                pdf_path = os.path.join(root, file_name)
                print(f"Processing {pdf_path}...")
                try:
                    with pdfplumber.open(pdf_path) as pdf:
                        pdf_text = ""
                        for page in pdf.pages:
                            pdf_text += page.extract_text() or ""
                        
                        cleaned_pdf_text = clean_text(pdf_text)
                        chunks = split_into_chunks(cleaned_pdf_text)
                        all_chunks.extend(chunks)
                except Exception as e:
                    print(f"Error processing {pdf_path}: {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        for chunk in all_chunks:
            f.write(chunk + '\n')
    print(f"Extracted {len(all_chunks)} chunks and saved to {output_file}")
    return all_chunks

if __name__ == "__main__":
    pdf_data_path = 'c:/Users/MSI/Desktop/chat_t_bot_hackathon/book_data_hackathon/'
    chunks_file = 'chunks.txt'
    faiss_index_file = 'faiss_index.bin'
    chunks_pickle_file = 'chunks.pkl'

    # Step 1: Process PDFs and create chunks.txt (if not already done)
    if not os.path.exists(chunks_file) or os.path.getsize(chunks_file) == 0:
        print("chunks.txt not found or empty. Processing PDFs...")
        all_extracted_chunks = process_pdf_directory(pdf_data_path, chunks_file)
    else:
        print("chunks.txt already exists. Loading chunks from file...")
        with open(chunks_file, 'r', encoding='utf-8') as f:
            all_extracted_chunks = [line.strip() for line in f if line.strip()]
    
    if not all_extracted_chunks:
        print("No chunks found. Exiting.")
        exit()

    # Step 2: Generate embeddings
    print("Loading SentenceTransformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print(f"Generating embeddings for {len(all_extracted_chunks)} chunks...")
    chunk_embeddings = model.encode(all_extracted_chunks, show_progress_bar=True)
    print("Embeddings generated.")

    # Step 3: Build FAISS index
    dimension = chunk_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity search
    index.add(np.array(chunk_embeddings).astype('float32'))
    print(f"FAISS index built with {index.ntotal} vectors.")

    # Step 4: Save FAISS index and original chunks
    faiss.write_index(index, faiss_index_file)
    print(f"FAISS index saved to {faiss_index_file}")

    with open(chunks_pickle_file, 'wb') as f:
        pickle.dump(all_extracted_chunks, f)
    print(f"Original chunks saved to {chunks_pickle_file}")

    print("Knowledge base creation complete.")