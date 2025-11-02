# File handling and text processing utilities
import os
import re
import hashlib
from typing import Dict, List
import zipfile
import tempfile
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

class FileManager:
    def __init__(self, base_path=None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.file_cache = {}
        self.operations_log = []
    
    def set_base_path(self, path: str):
        """Set the base directory for file operations"""
        self.base_path = Path(path)
        if not self.base_path.exists():
            self.base_path.mkdir(parents=True, exist_ok=True)
    
    def list_files(self, pattern="*", recursive=False) -> List[Path]:
        """List files matching pattern"""
        method = self.base_path.rglob if recursive else self.base_path.glob
        files = list(method(pattern))
        self.log_operation(f"list_files: {pattern}, recursive: {recursive}")
        return files
    
    def read_file(self, file_path: str, encoding='utf-8') -> str:
        """Read file content with enhanced error handling"""
        full_path = self.base_path / file_path
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path} in directory {self.base_path}")
        
        try:
            with open(full_path, 'r', encoding=encoding) as file:
                content = file.read()
            self.file_cache[str(full_path)] = content
            self.log_operation(f"read_file: {file_path}")
            return content
        except UnicodeDecodeError:
            raise ValueError(f"Cannot decode file {file_path} with encoding {encoding}")
    
    def write_file(self, file_path: str, content: str, encoding='utf-8'):
        """Write content to file"""
        full_path = self.base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding=encoding) as file:
            file.write(content)
        
        self.file_cache[str(full_path)] = content
        self.log_operation(f"write_file: {file_path}")
    
    def append_to_file(self, file_path: str, content: str, encoding='utf-8'):
        """Append content to file"""
        full_path = self.base_path / file_path
        with open(full_path, 'a', encoding=encoding) as file:
            file.write(content)
        
        if str(full_path) in self.file_cache:
            self.file_cache[str(full_path)] += content
        self.log_operation(f"append_to_file: {file_path}")
    
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists"""
        full_path = self.base_path / file_path
        return full_path.exists()
    
    def get_file_info(self, file_path: str) -> Dict:
        """Get file metadata"""
        full_path = self.base_path / file_path
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat = full_path.stat()
        return {
            'path': str(full_path),
            'size': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'is_file': full_path.is_file(),
            'is_dir': full_path.is_dir()
        }
    
    def calculate_hash(self, file_path: str, algorithm='md5') -> str:
        """Calculate file hash"""
        full_path = self.base_path / file_path
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        hash_func = getattr(hashlib, algorithm)()
        
        with open(full_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_func.update(chunk)
        
        file_hash = hash_func.hexdigest()
        self.log_operation(f"calculate_hash: {file_path}, algorithm: {algorithm}")
        return file_hash

    def search_in_files(self, pattern: str, file_pattern="*.txt", recursive=False) -> Dict[str, List[str]]:
        """Search for pattern in files"""
        files = self.list_files(file_pattern, recursive)
        results = {}
        regex = re.compile(pattern, re.IGNORECASE)
        
        for file_path in files:
            if file_path.is_file():
                try:
                    content = self.read_file(str(file_path.relative_to(self.base_path)))
                    matches = regex.findall(content)
                    if matches:
                        results[str(file_path)] = matches
                except (UnicodeDecodeError, PermissionError):
                    continue
        
        self.log_operation(f"search_in_files: {pattern}, files: {file_pattern}")
        return results
    
    def backup_files(self, file_paths: List[str], backup_name: str):
        """Create zip backup of files"""
        backup_path = self.base_path / f"{backup_name}.zip"
        
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                full_path = self.base_path / file_path
                if full_path.exists() and full_path.is_file():
                    zipf.write(full_path, file_path)
        
        self.log_operation(f"backup_files: {backup_name}, files: {len(file_paths)}")
        return backup_path

class TextProcessor:
    def __init__(self):
        self.text = ""
        self.processed_text = ""
        self.stats = {}
    
    def load_text(self, text: str):
        """Load text for processing"""
        self.text = text
        self.processed_text = text
        return self
    
    def load_from_file(self, file_path: str, file_manager: FileManager):
        """Load text from file using FileManager"""
        self.text = file_manager.read_file(file_path)
        self.processed_text = self.text
        return self
    
    def to_lowercase(self):
        """Convert text to lowercase"""
        self.processed_text = self.processed_text.lower()
        return self
    
    def to_uppercase(self):
        """Convert text to uppercase"""
        self.processed_text = self.processed_text.upper()
        return self
    
    def remove_punctuation(self):
        """Remove punctuation from text"""
        self.processed_text = re.sub(r'[^\w\s]', '', self.processed_text)
        return self
    
    def remove_extra_spaces(self):
        """Remove extra whitespace"""
        self.processed_text = re.sub(r'\s+', ' ', self.processed_text).strip()
        return self
    
    def remove_stopwords(self, custom_stopwords=None):
        """Remove common stopwords"""
        stopwords = custom_stopwords or {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'
        }
        words = self.processed_text.split()
        filtered_words = [word for word in words if word.lower() not in stopwords]
        self.processed_text = ' '.join(filtered_words)
        return self
    
    def calculate_text_stats(self) -> Dict:
        """Calculate text statistics"""
        words = self.processed_text.split()
        sentences = re.split(r'[.!?]+', self.processed_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        word_freq = Counter(words)
        char_count = len(self.processed_text)
        word_count = len(words)
        sentence_count = len(sentences)
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        self.stats = {
            'characters': char_count,
            'words': word_count,
            'sentences': sentence_count,
            'lines': self.processed_text.count('\n') + 1,
            'unique_words': len(word_freq),
            'avg_word_length': round(avg_word_length, 2),
            'avg_sentence_length': round(avg_sentence_length, 2),
            'most_common_words': word_freq.most_common(10)
        }
        
        return self.stats
    
    def find_and_replace(self, find_text: str, replace_text: str, case_sensitive=True):
        """Find and replace text"""
        flags = 0 if case_sensitive else re.IGNORECASE
        self.processed_text = re.sub(re.escape(find_text), replace_text, self.processed_text, flags=flags)
        return self
    
    def extract_emails(self) -> List[str]:
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, self.text)
    
    def extract_phone_numbers(self) -> List[str]:
        """Extract phone numbers from text"""
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        return re.findall(phone_pattern, self.text)
    
    def extract_urls(self) -> List[str]:
        """Extract URLs from text"""
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*\??[/\w\.-=&%]*'
        return re.findall(url_pattern, self.text)
    
    def get_processed_text(self) -> str:
        """Get the processed text"""
        return self.processed_text
    
    def reset_processing(self):
        """Reset processed text to original"""
        self.processed_text = self.text
        return self

    def log_operation(self, operation: str):
        """Log operation for tracking"""
        self.operations_log.append({
            'timestamp': datetime.now(),
            'operation': operation
        })

# Demonstration
if os.name == "__main__":
    # File manager demo
    print("File Manager Demo:")
    file_mgr = FileManager()
    
    # Create test files
    test_content = """Hello World! This is a test file.
It contains multiple lines of text for testing purposes.
Email: test@example.com, Phone: 123-456-7890
Visit our website: https://www.example.com"""
    
    file_mgr.write_file("test1.txt", test_content)
    file_mgr.write_file("test2.txt", "Another test file with different content.")
    
    # List files
    files = file_mgr.list_files("*.txt")
    print(f"Found files: {[f.name for f in files]}")
    
    # Search in files
    results = file_mgr.search_in_files(r'\b\w+@\w+\.\w+\b', "*.txt")
    print(f"Email addresses found: {results}")
    
    # Text processing demo
    print("\nText Processing Demo:")
    processor = TextProcessor()
    processor.load_text(test_content)
    
    stats = processor.calculate_text_stats()
    print(f"Text statistics: {stats}")
    
    # Process text
    processed = (processor
                .to_lowercase()
                .remove_punctuation()
                .remove_extra_spaces()
                .get_processed_text())
    
    print(f"Processed text: {processed}")
    
    # Extract information
    emails = processor.extract_emails()
    phones = processor.extract_phone_numbers()
    urls = processor.extract_urls()
    
    print(f"Extracted emails: {emails}")
    print(f"Extracted phones: {phones}")
    print(f"Extracted URLs: {urls}")