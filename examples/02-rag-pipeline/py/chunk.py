"""文档切片：按段落切，每段不超过 max_chars。"""


def chunk_by_paragraph(text: str, max_chars: int = 500) -> list[str]:
    """按段落切片。"""
    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current = ""
    for p in paragraphs:
        if len(current) + len(p) > max_chars and current:
            chunks.append(current.strip())
            current = p
        else:
            current += "\n\n" + p
    if current:
        chunks.append(current.strip())
    return chunks
