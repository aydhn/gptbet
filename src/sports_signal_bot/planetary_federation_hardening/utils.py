def no_safe_visibility_preserved(record):
    return getattr(record, 'no_safe_visible', True)

def sovereignty_note_preserved(record):
    return getattr(record, 'sovereignty_note_visible', True)
