"""Extract structured features from a saved HTML snapshot — used as cheap pre-classification signal."""


def extract_features(html_path: str) -> dict:
    """Return {'title': str, 'visible_text': str, 'has_payment_form': bool,
             'currencies': [...], 'languages': [...], 'logo_urls': [...]}.

    TODO: parse with BeautifulSoup; detect <form> elements with payment-like fields
    (card number, CVV); detect currency symbols in the visible text.
    """
    raise NotImplementedError
