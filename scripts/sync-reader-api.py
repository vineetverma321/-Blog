#!/usr/bin/env python3
"""
Sync Reader books via API
Requires READER_API_TOKEN environment variable
"""

import os
import json
import requests
from datetime import datetime

READER_API_BASE = "https://readwise.io/api/v3"
READINGS_FILE = "content/readings.md"


def get_reader_books():
    """Fetch books from Reader API"""
    token = os.environ.get("READER_API_TOKEN")
    if not token:
        raise RuntimeError("READER_API_TOKEN not set")

    headers = {"Authorization": f"Token {token}"}

    books = []
    next_cursor = None

    while True:
        params = {"category": "epub", "limit": 100}
        if next_cursor:
            params["pageCursor"] = next_cursor

        response = requests.get(
            f"{READER_API_BASE}/list/", headers=headers, params=params
        )

        if response.status_code != 200:
            raise RuntimeError(f"Error fetching epub books: {response.status_code}")

        data = response.json()
        books.extend(data.get("results", []))

        next_cursor = data.get("nextPageCursor")
        if not next_cursor:
            break

    # Also fetch PDFs
    next_cursor = None
    while True:
        params = {"category": "pdf", "limit": 100}
        if next_cursor:
            params["pageCursor"] = next_cursor

        response = requests.get(
            f"{READER_API_BASE}/list/", headers=headers, params=params
        )

        if response.status_code != 200:
            raise RuntimeError(f"Error fetching pdf books: {response.status_code}")

        data = response.json()
        books.extend(data.get("results", []))

        next_cursor = data.get("nextPageCursor")
        if not next_cursor:
            break

    return books


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
            "progress": round(progress * 100, 1),
        }

        if progress == 0:
            future_reads.append(book_data)
        elif progress >= 0.99:
            already_read.append(book_data)
        else:
            currently_reading.append(book_data)

    return currently_reading, future_reads, already_read


def generate_readings_content(currently_reading, future_reads, already_read):
    """Generate markdown content"""

    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+05:30")
    today = datetime.now().strftime("%Y-%m-%d")

    content = f"""+++ 
draft = false
date = {now}
title = "Readings"
description = "My reading journey - what I am reading, what I want to read, and what I have read (Last synced: {today})"
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
    print("Fetching books from Reader API...")
    books = get_reader_books()

    print(f"Found {len(books)} books")

    currently_reading, future_reads, already_read = categorize_books(books)

    print(f"Currently reading: {len(currently_reading)}")
    print(f"Future reads: {len(future_reads)}")
    print(f"Already read: {len(already_read)}")

    content = generate_readings_content(currently_reading, future_reads, already_read)

    with open(READINGS_FILE, "w") as f:
        f.write(content)

    print(f"Updated {READINGS_FILE}")
    print("Sync complete!")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Sync failed: {error}")
        raise SystemExit(1)
