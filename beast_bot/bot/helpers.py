def get_source_fields(source: str) -> set[str]:
    fields = set()
    buffer = ''
    write = False

    for character in source:
        if character == '}':
            write = False
            fields.add(buffer)
            buffer = ''
        elif write is True:
            buffer += character
        elif character == '{':
            write = True

    return fields
