from bot import is_autism_variant, normalize_text


def test_cyrillic_mapping():
    assert normalize_text("автор") == "abtop"
    assert normalize_text("АВТОР") == "ABTOP"


def test_greek_letters():
    assert normalize_text("αορν") == "aopv"


def test_autism_variants():
    assert normalize_text("аutism") == "autism"
    assert normalize_text("autyzм") == "autyzm"


def test_unicode_normalization():
    assert normalize_text("café") == "cafe"
    assert normalize_text("naïve") == "naive"


def test_empty_and_ascii():
    assert normalize_text("") == ""
    assert normalize_text("hello123") == "hello123"


def test_mixed_content():
    assert normalize_text("hello мир") == "hello mnp"
    assert normalize_text("test-123.txt") == "test-123.txt"


def test_autism_detection():
    ipsum = """Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque
    faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium
    tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar
    vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl
    malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent
    taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.
    """
    assert is_autism_variant(ipsum) is False
    assert is_autism_variant("No related words here") is False
    assert is_autism_variant(ipsum[0:100] + "auto" + ipsum[100:]) is False
    assert is_autism_variant(ipsum[0:100] + "auti" + ipsum[100:]) is False
    assert is_autism_variant("aut") is False
    assert is_autism_variant("autonomous") is False
    assert is_autism_variant("automatic") is False
    assert is_autism_variant("autograph") is False
    assert is_autism_variant("autumn") is False
    assert is_autism_variant("autis")
    assert is_autism_variant("have autism")
    assert is_autism_variant(ipsum[0:100] + "autism" + ipsum[100:])
    assert is_autism_variant("This is an autyzm case")
    assert is_autism_variant("aut|sm")
    assert is_autism_variant("aµtism")
    assert is_autism_variant("aut¡sm")
    assert is_autism_variant(ipsum[0:100] + "aut¡sm" + ipsum[100:])
    assert is_autism_variant("au-tis")
    assert is_autism_variant("aut-ism")
    assert is_autism_variant("autis-m")
    assert is_autism_variant("а  u  t  i s  m")
    assert is_autism_variant("а_u-t  i=s+m")
