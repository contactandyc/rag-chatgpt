
def segment_text(inp, max_length=2000, lines_back=3):
    lines = inp.splitlines()
    idx = 0
    segments = []
    input_len = 0
    input_text = []

    while idx < len(lines):
        start_idx = idx
        input_text = [lines[idx]]
        input_len = len(lines[idx])
        idx = idx + 1
        while idx < len(lines):
            l = lines[idx]
            if input_len + len(l) > max_length:
                segments.append('\n'.join(input_text))
                if idx - lines_back > start_idx:
                    idx = idx - lines_back
                break
            else:
                input_text.append(l)
                input_len = input_len + len(l)
                idx = idx + 1
    if input_len > 0:
        segments.append('\n'.join(input_text))

    return segments