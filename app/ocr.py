import pytesseract
from PIL import Image


LANGUAGE_MAP = {
    "Latin": ["eng"],
    "Kannada": ["kan"],
    "Devanagari": ["hin", "mar"],
    "Gujarati": ["guj"],
    "Bengali": ["ben"],
    "Malayalam": ["mal"],
    "Tamil": ["tam"],
    "Telugu": ["tel"],
    "Gurmukhi": ["pan"],
    "Arabic": ["urd"],
}


def get_available_languages():
    languages = pytesseract.get_languages(
        config=""
    )

    return [
        language
        for language in languages
        if language not in {"osd", "equ"}
    ]


def detect_script(image):
    try:
        result = pytesseract.image_to_osd(
            image,
            config="--psm 0"
        )

        script = None
        confidence = 0.0

        for line in result.splitlines():

            if line.startswith("Script:"):
                script = line.split(
                    ":", 1
                )[1].strip()

            elif line.startswith(
                "Script confidence:"
            ):
                confidence = float(
                    line.split(
                        ":", 1
                    )[1].strip()
                )

        return script, confidence

    except Exception:
        return None, 0.0


def select_ocr_languages(image):
    available_languages = (
        get_available_languages()
    )

    script, confidence = detect_script(
        image
    )

    candidates = []

    if script in LANGUAGE_MAP:

        for language in LANGUAGE_MAP[script]:

            if language in available_languages:
                candidates.append(language)

    # English is useful as a second language
    # when the detected script is uncertain.
    if confidence < 20:

        if "eng" in available_languages:
            candidates.insert(0, "eng")

    # Always make sure at least one language
    # is available.
    if not candidates:

        if "eng" in available_languages:
            candidates.append("eng")
        elif available_languages:
            candidates.append(
                available_languages[0]
            )

    # Remove duplicates while preserving order.
    candidates = list(
        dict.fromkeys(candidates)
    )

    return "+".join(candidates)


def extract_text_from_image(
    image,
    languages=None
):
    if languages is None:

        languages = select_ocr_languages(
            image
        )

    text = pytesseract.image_to_string(
        image,
        lang=languages
    )

    return text.strip()


def extract_text_from_image_bytes(
    image_bytes,
    languages=None
):
    from io import BytesIO

    image = Image.open(
        BytesIO(image_bytes)
    )

    return extract_text_from_image(
        image,
        languages
    )