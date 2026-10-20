def newest_first(rows):
    """Rows with equal dates keep their original relative order."""
    return sorted(rows, key=lambda r: r["date"], reverse=True)
