def get_content_only(line):
    if line[0].isdigit() or line.startswith("- ") or line.startswith("* ") \
            or line.startswith(" ") or line.startswith("#"):
        return line.split(" ", 1)[1]
    elif line.startswith("**") and line.endswith("**"):
        return line[2:-2]
    elif line.startswith("*") and line.endswith("*"):
        return line[1:-1]
    return line
