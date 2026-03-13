
def find_duplicates(papers):
    seen = set()
    duplicates = set()
    for paper in papers:
        if paper in seen:
            duplicates.add(paper)
        else:
            seen.add(paper)
    return duplicates
