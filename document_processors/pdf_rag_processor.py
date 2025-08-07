"""
PDF RAG Processor for handling massive government documents.
Converts gigantic PDFs into intelligent, searchable chunks optimized for SOS analysis.
"""

import os
import io
import logging
import hashlib
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import json
import time

# PDF Processing
import PyPDF2
import pdfplumber

# RAG Components
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import TokenTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import tiktoken


@dataclass
class DocumentChunk:
    """Represents a processed document chunk with metadata."""
    chunk_id: str
    content: str
    page_number: int
    section_type: str
    relevance_score: float
    keywords: List[str]
    source_file: str
    char_count: int
    token_count: int


class PDFRAGProcessor:
    """
    Advanced PDF processor that converts massive government documents into 
    intelligently chunked, searchable content optimized for SOS analysis.
    """
    
    def __init__(self, cache_dir: str = "pdf_rag_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        # Initialize embedding model (lightweight but effective)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize text splitters
        self.recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,  # Larger chunks for context
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        self.token_splitter = TokenTextSplitter(
            chunk_size=1500,
            chunk_overlap=150
        )
        
        # SOS-specific keywords for relevance scoring
        self.sos_keywords = {
            'critical': ['sar', 'source approval', 'sole source', 'security clearance', 'classified', 'itar'],
            'platform': ['f-15', 'f-16', 'f-22', 'f-35', 'b-1', 'b-2', 'b-52', 'c-130', 'kc-135', 'ch-47', 'uh-60'],
            'commercial': ['commercial', 'cots', 'far part 12', 'commercial item'],
            'technical': ['technical data', 'tdp', 'drawings', 'specifications', 'engineering'],
            'business': ['small business', 'set aside', 'hubzone', 'sdvosb', 'wosb'],
            'oem': ['oem', 'original equipment', 'authorized dealer', 'traceability'],
            'requirements': ['shall', 'must', 'required', 'mandatory', 'restriction']
        }
        
        # Initialize tokenizer for accurate token counting
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
    def get_cache_key(self, pdf_content: bytes, filename: str) -> str:
        """Generate unique cache key for PDF content."""
        content_hash = hashlib.md5(pdf_content).hexdigest()
        return f"{filename}_{content_hash}"
    
    def extract_text_with_metadata(self, pdf_content: bytes, filename: str) -> List[Dict]:
        """
        Extract text from PDF with page numbers and section detection.
        Uses both PyPDF2 and pdfplumber for maximum text extraction.
        """
        pages_data = []
        
        try:
            # Method 1: pdfplumber (better for complex layouts)
            with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        text = page.extract_text() or ""
                        
                        # Detect section type based on content
                        section_type = self.detect_section_type(text)
                        
                        pages_data.append({
                            'page_number': page_num,
                            'text': text,
                            'section_type': section_type,
                            'method': 'pdfplumber'
                        })
                        
                    except Exception as e:
                        logging.warning(f"Failed to extract page {page_num} with pdfplumber: {e}")
                        
        except Exception as e:
            logging.warning(f"pdfplumber failed for {filename}: {e}")
            
            # Fallback: PyPDF2
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        text = page.extract_text() or ""
                        section_type = self.detect_section_type(text)
                        
                        pages_data.append({
                            'page_number': page_num,
                            'text': text,
                            'section_type': section_type,
                            'method': 'PyPDF2'
                        })
                        
                    except Exception as e:
                        logging.warning(f"Failed to extract page {page_num} with PyPDF2: {e}")
                        
            except Exception as e:
                logging.error(f"Both PDF extraction methods failed for {filename}: {e}")
                return []
        
        return pages_data
    
    def detect_section_type(self, text: str) -> str:
        """Detect the type of document section based on content patterns."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['table of contents', 'contents', 'index']):
            return 'table_of_contents'
        elif any(word in text_lower for word in ['statement of work', 'sow', 'scope of work']):
            return 'statement_of_work'
        elif any(word in text_lower for word in ['technical data', 'specifications', 'requirements']):
            return 'technical_specs'
        elif any(word in text_lower for word in ['terms and conditions', 'contract terms', 'general conditions']):
            return 'terms_conditions'
        elif any(word in text_lower for word in ['wage determination', 'labor standards', 'prevailing wage']):
            return 'wage_determination'
        elif any(word in text_lower for word in ['sar', 'source approval', 'approved sources']):
            return 'source_approval'
        elif any(word in text_lower for word in ['amendment', 'modification', 'change']):
            return 'amendment'
        elif any(word in text_lower for word in ['attachment', 'exhibit', 'appendix']):
            return 'attachment'
        else:
            return 'general_content'
    
    def calculate_relevance_score(self, text: str) -> Tuple[float, List[str]]:
        """Calculate relevance score based on SOS-specific keywords."""
        text_lower = text.lower()
        score = 0.0
        found_keywords = []
        
        for category, keywords in self.sos_keywords.items():
            category_score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    # Weight critical keywords higher
                    weight = 3.0 if category == 'critical' else 1.0
                    category_score += weight
                    found_keywords.append(f"{category}:{keyword}")
            
            score += category_score
        
        # Normalize by text length (per 1000 characters)
        normalized_score = score / max(len(text) / 1000, 1)
        
        return normalized_score, found_keywords
    
    def intelligent_chunk_splitting(self, pages_data: List[Dict], filename: str) -> List[DocumentChunk]:
        """
        Intelligently split document into chunks with context preservation.
        """
        chunks = []
        chunk_id_counter = 0
        
        for page_data in pages_data:
            page_text = page_data['text']
            page_num = page_data['page_number']
            section_type = page_data['section_type']
            
            if not page_text.strip():
                continue
            
            # For critical sections, use smaller chunks to preserve precision
            if section_type in ['source_approval', 'statement_of_work', 'technical_specs']:
                text_chunks = self.token_splitter.split_text(page_text)
            else:
                text_chunks = self.recursive_splitter.split_text(page_text)
            
            for chunk_text in text_chunks:
                if len(chunk_text.strip()) < 50:  # Skip tiny chunks
                    continue
                
                # Calculate relevance and extract keywords
                relevance_score, keywords = self.calculate_relevance_score(chunk_text)
                
                # Count tokens
                token_count = len(self.tokenizer.encode(chunk_text))
                
                chunk = DocumentChunk(
                    chunk_id=f"{filename}_chunk_{chunk_id_counter:04d}",
                    content=chunk_text,
                    page_number=page_num,
                    section_type=section_type,
                    relevance_score=relevance_score,
                    keywords=keywords,
                    source_file=filename,
                    char_count=len(chunk_text),
                    token_count=token_count
                )
                
                chunks.append(chunk)
                chunk_id_counter += 1
        
        return chunks
    
    def process_pdf_to_rag(self, pdf_content: bytes, filename: str) -> List[DocumentChunk]:
        """
        Main method to convert PDF into RAG-ready chunks.
        """
        logging.info(f"Processing PDF: {filename} ({len(pdf_content)} bytes)")
        
        # Check cache first
        cache_key = self.get_cache_key(pdf_content, filename)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if os.path.exists(cache_file):
            try:
                # Check if cache is less than 24 hours old
                if time.time() - os.path.getmtime(cache_file) < 86400:
                    logging.info(f"Loading cached chunks for {filename}")
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)
                    
                    # Reconstruct DocumentChunk objects
                    chunks = []
                    for chunk_data in cached_data:
                        chunk = DocumentChunk(**chunk_data)
                        chunks.append(chunk)
                    
                    return chunks
            except Exception as e:
                logging.warning(f"Failed to load cache for {filename}: {e}")
        
        # Extract text with metadata
        start_time = time.time()
        pages_data = self.extract_text_with_metadata(pdf_content, filename)
        
        if not pages_data:
            logging.error(f"No text extracted from {filename}")
            return []
        
        # Create intelligent chunks
        chunks = self.intelligent_chunk_splitting(pages_data, filename)
        
        processing_time = time.time() - start_time
        total_chars = sum(chunk.char_count for chunk in chunks)
        total_tokens = sum(chunk.token_count for chunk in chunks)
        
        logging.info(f"PDF Processing Summary for {filename}:")
        logging.info(f"  - Pages processed: {len(pages_data)}")
        logging.info(f"  - Chunks created: {len(chunks)}")
        logging.info(f"  - Total characters: {total_chars:,}")
        logging.info(f"  - Total tokens: {total_tokens:,}")
        logging.info(f"  - Processing time: {processing_time:.2f}s")
        logging.info(f"  - High relevance chunks: {sum(1 for c in chunks if c.relevance_score > 2.0)}")
        
        # Cache the results
        try:
            cache_data = [chunk.__dict__ for chunk in chunks]
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            logging.info(f"Cached {len(chunks)} chunks for {filename}")
        except Exception as e:
            logging.warning(f"Failed to cache chunks for {filename}: {e}")
        
        return chunks
    
    def get_top_relevant_chunks(self, chunks: List[DocumentChunk], 
                               max_chunks: int = 20, 
                               min_relevance: float = 0.5) -> List[DocumentChunk]:
        """
        Get the most relevant chunks for SOS analysis.
        """
        # Filter by minimum relevance
        relevant_chunks = [c for c in chunks if c.relevance_score >= min_relevance]
        
        # Sort by relevance score (descending)
        relevant_chunks.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Take top chunks, but ensure we include critical sections
        top_chunks = []
        critical_sections = ['source_approval', 'statement_of_work', 'technical_specs']
        
        # First, add high-relevance chunks from critical sections
        for chunk in relevant_chunks:
            if chunk.section_type in critical_sections and len(top_chunks) < max_chunks:
                top_chunks.append(chunk)
        
        # Then add other high-relevance chunks
        for chunk in relevant_chunks:
            if chunk not in top_chunks and len(top_chunks) < max_chunks:
                top_chunks.append(chunk)
        
        logging.info(f"Selected {len(top_chunks)} most relevant chunks from {len(chunks)} total")
        
        return top_chunks
    
    def chunks_to_analysis_text(self, chunks: List[DocumentChunk], 
                               include_metadata: bool = True) -> str:
        """
        Convert processed chunks back to analysis-ready text.
        """
        if not chunks:
            return ""
        
        # Group chunks by section type for better organization
        sections = {}
        for chunk in chunks:
            section = chunk.section_type
            if section not in sections:
                sections[section] = []
            sections[section].append(chunk)
        
        # Build organized text
        analysis_text = f"=== DOCUMENT ANALYSIS: {chunks[0].source_file} ===\n\n"
        
        # Priority order for sections
        section_priority = [
            'source_approval', 'statement_of_work', 'technical_specs', 
            'terms_conditions', 'general_content', 'attachment'
        ]
        
        for section_type in section_priority:
            if section_type in sections:
                section_chunks = sections[section_type]
                # Sort by relevance within section
                section_chunks.sort(key=lambda x: x.relevance_score, reverse=True)
                
                analysis_text += f"\n--- {section_type.upper().replace('_', ' ')} ---\n"
                
                for chunk in section_chunks:
                    if include_metadata:
                        analysis_text += f"\n[Page {chunk.page_number} | Relevance: {chunk.relevance_score:.1f} | Keywords: {', '.join(chunk.keywords[:3])}]\n"
                    
                    analysis_text += f"{chunk.content}\n"
        
        # Add processing summary
        total_tokens = sum(chunk.token_count for chunk in chunks)
        avg_relevance = sum(chunk.relevance_score for chunk in chunks) / len(chunks)
        
        analysis_text += f"\n=== PROCESSING SUMMARY ===\n"
        analysis_text += f"Chunks processed: {len(chunks)}\n"
        analysis_text += f"Total tokens: {total_tokens:,}\n"
        analysis_text += f"Average relevance: {avg_relevance:.2f}\n"
        analysis_text += f"High relevance chunks: {sum(1 for c in chunks if c.relevance_score > 2.0)}\n"
        
        return analysis_text
