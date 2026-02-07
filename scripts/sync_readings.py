#!/usr/bin/env python3
"""
Sync Reader books to Hugo readings page
Run daily via cron: 0 0 * * * /usr/bin/python3 /Users/tech/Desktop/Portfolio/quickstart/scripts/sync_readings.py
"""

import json
import subprocess
import re
from datetime import datetime

READINGS_FILE = "/Users/tech/Desktop/Portfolio/quickstart/content/readings.md"

def fetch_reader_books():
    """Fetch books from Reader using the MCP CLI"""
    try:
        # Fetch EPUBs
        result = subprocess.run(
            ["opencode", "--mcp-call", "Reader", "reader_list_documents", 
             "--category", "epub", "--limit", "100"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Parse the JSON response from the output
        output = result.stdout
        # Find JSON in the output (it might have other text)
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return data.get("results", [])
        return []
    except Exception as e:
        print(f"Error fetching books: {e}")
        return []

def categorize_books(books):
    """Categorize books by reading progress"""
    currently_reading = []
    future_reads = []
    already_read = []
    
    for book in books:
        progress = book.get("reading_progress", 0)
        title = book.get("title", "Unknown")
        author = book.get("author", "Unknown")
        
        book_data = {
            "title": title,
            "author": author,
            "progress": round(progress * 100, 1)
        }
        
        if progress == 0:
            future_reads.append(book_data)
        elif progress >= 0.99:
            already_read.append(book_data)
        else:
            currently_reading.append(book_data)
    
    return currently_reading, future_reads, already_read

def generate_readings_content(currently_reading, future_reads, already_read):
    """Generate the markdown content for readings page"""
    
    content = """+++ 
draft = false
date = """ + datetime.now().strftime("%Y-%m-%dT%H:%M:%S+05:30") + """
title = "Readings"
description = "My reading journey - what I am reading, what I want to read, and what I have read"
slug = "readings"
authors = []
tags = []
categories = []
+++

## Currently Reading

| Title | Author | Progress | Notes |
|-------|--------|----------|-------|
"""
    
    for book in currently_reading:
        content += f"| {book['title']} | {book['author']} | {book['progress']}% | |\n"
    
    if not currently_reading:
        content += "| *No books currently in progress* | | | |\n"
    
    content += """
---

## Future Reads

| Title | Author | Priority | Notes |
|-------|--------|----------|-------|
"""
    
    for book in future_reads:
        content += f"| {book['title']} | {book['author']} | | |\n"
    
    if not future_reads:
        content += "| *No books in queue* | | | |\n"
    
    content += """
---

## Already Read

| Title | Author | Year Read | Rating | Notes |
|-------|--------|-----------|--------|-------|
"""
    
    for book in already_read:
        content += f"| {book['title']} | {book['author']} | | | |\n"
    
    if not already_read:
        content += "| *No completed books yet* | | | | |\n"
    
    return content

def main():
    print("Fetching books from Reader...")
    books = fetch_reader_books()
    
    if not books:
        print("No books found or error occurred")
        return
    
    print(f"Found {len(books)} books")
    
    currently_reading, future_reads, already_read = categorize_books(books)
    
    print(f"Currently reading: {len(currently_reading)}")
    print(f"Future reads: {len(future_reads)}")
    print(f"Already read: {len(already_read)}")
    
    content = generate_readings_content(currently_reading, future_reads, already_read)
    
    with open(READINGS_FILE, 'w') as f:
        f.write(content)
    
    print(f"Updated {READINGS_FILE}")
    print("Sync complete!")

if __name__ == "__main__":
    main()
