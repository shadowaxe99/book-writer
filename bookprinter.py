def markdown_hash(title):
    title = title.lower()
    
    result = []
    for char in title:
        if char.isalnum():
            result.append(char)
        elif char == ' ' or char == '-':
            result.append('-')
    
    return '#' + ''.join(result)


def create_book_frontpage(book_base_dir, book):
    title = book['title']
    toc = book['toc']
    summary = book['summary'] or f'Summary of "{title}" will be here'

    frontpage_file = f"{book_base_dir}/README.md"

    with open(frontpage_file, "w") as f:
        f.write(f"# {title}\n\n")
        f.write(f"{summary}\n\n")
        f.write(f"## Índice\n\n")

        for chapter in toc["chapters"]:
            chapter_number = chapter['number']
            chapter_title = chapter['title']
            chapter_file = chapter['file']

            f.write(f"- [{chapter_number}. {chapter_title}](./{chapter_file})\n")

            for section in chapter['sections']:
                section_number = section['number']
                section_title = section['title']
                section_desc = f'{chapter_number}.{section_number}. {section_title}'
                hash = markdown_hash(section_desc)
                f.write(f"  - [{section_desc}](./{chapter_file}{hash})\n")
            f.write("\n---\n\n")
        f.write("\n")

def create_chapter_file(book_base_dir, book, chapter):
    title = book['title']
    chapter_number = chapter['number']
    chapter_title = chapter['title']
    chapter_file_path = f"{book_base_dir}/{chapter['file']}"

    chapter_content = chapter.get('content') or f'Chapter "{chapter_title}" content will be here'

    try:
        with open(chapter_file_path, "w") as f:
            f.write(f"# {title}\n\n")
            f.write(f"## {chapter_number}. {chapter_title}\n\n")
            f.write(chapter_content)
            f.write("\n\n")

            for section in chapter['sections']:
                section_number = section['number']
                section_title = section['title']
                section_content = section.get('content') or f'Section "{section_title}" content will be here'

                f.write(f"### {chapter_number}.{section_number}. {section_title}\n\n")
                f.write(section_content)
                f.write("\n\n")
    except IOError as e:
        raise IOError(f"Failed to create chapter file: {chapter_file_path}") from e

def create_chapters(book_base_dir, book):
    for chapter in book['toc']["chapters"]:
        create_chapter_file(book_base_dir, book, chapter)

def print_book(book_base_dir, book):
    create_book_frontpage(book_base_dir, book)
    create_chapters(book_base_dir, book)