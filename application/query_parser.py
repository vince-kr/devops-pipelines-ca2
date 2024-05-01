import config
from spacy.tokens.doc import Doc


def _retrieve_from_query(query: Doc, retrieve_from: set[str]) -> set[str]:
    query_lemmas = set(token.lemma_ for token in query)
    intersection = retrieve_from & query_lemmas
    return intersection if len(intersection) > 0 else None

def retrieve_crop(query: Doc) -> set[str]:
    return _retrieve_from_query(query, config.CROPS)

def retrieve_action(query: Doc) -> set[str]:
    return _retrieve_from_query(query, config.ACTIONS)
