def get_content_only(line):
    if line[0].isdigit() or line.startswith("-") or line.startswith("*") \
            or line.startswith(" ") or line.startswith("#"):
        return line.split(" ", 1)[1]
    return line
