from text_checks import is_text_variant, normalize_text


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
    AUTISM_VARIANTS = ["autism", "autyzm", "autistic", "lubiepociagi"]

    assert is_text_variant("No related words here", AUTISM_VARIANTS, verbose=True) is False
    assert is_text_variant("aut", AUTISM_VARIANTS, verbose=True) is False
    assert is_text_variant("autonomous", AUTISM_VARIANTS, verbose=True) is False
    assert is_text_variant("automatic", AUTISM_VARIANTS, verbose=True) is False
    assert is_text_variant("autograph", AUTISM_VARIANTS, verbose=True) is False
    assert is_text_variant("autumn", AUTISM_VARIANTS, verbose=True) is False
    assert is_text_variant("autis", AUTISM_VARIANTS, verbose=True) is False
    assert is_text_variant("have autism", AUTISM_VARIANTS, verbose=True) is True
    assert is_text_variant("This is an autyzm case", AUTISM_VARIANTS, verbose=True) is True
    assert is_text_variant("aut|sm", AUTISM_VARIANTS, verbose=True) is True
    assert is_text_variant("aµtism", AUTISM_VARIANTS, verbose=True) is True
    assert is_text_variant("aut¡sm", AUTISM_VARIANTS, verbose=True) is True
    assert is_text_variant("au-tis", AUTISM_VARIANTS, verbose=True) is False
    assert is_text_variant("aut-ism", AUTISM_VARIANTS, verbose=True) is True
    assert is_text_variant("autis-m", AUTISM_VARIANTS, verbose=True) is True
    assert is_text_variant("а  u  t  i s  m", AUTISM_VARIANTS, verbose=True) is True
    assert is_text_variant("а_u-t  i=s+m", AUTISM_VARIANTS, verbose=True) is True
    assert is_text_variant("miautyzm", AUTISM_VARIANTS, verbose=True) is True
    # assert True is False # Ensure debug prints

def test_meow_detection():
    MEOW_VARIANTS = ["meow", "miau", "nya"]

    assert is_text_variant("No cats here", MEOW_VARIANTS, verbose=True) is False
    assert is_text_variant("meadow", MEOW_VARIANTS, verbose=True) is False
    assert is_text_variant("meanwhile", MEOW_VARIANTS, verbose=True) is False
    assert is_text_variant("potezny ai slop", MEOW_VARIANTS, verbose=True) is False
    assert is_text_variant("anyway", MEOW_VARIANTS, verbose=True) is False
    assert is_text_variant("Semi autism", MEOW_VARIANTS, verbose=True) is False  
    assert is_text_variant("Same owoce", MEOW_VARIANTS, verbose=True) is False  
    assert is_text_variant("miami", MEOW_VARIANTS, verbose=True) is False
    assert is_text_variant("dynamic", MEOW_VARIANTS, verbose=True) is False 
    assert is_text_variant("meo", MEOW_VARIANTS, verbose=True) is False
    assert is_text_variant("mia", MEOW_VARIANTS, verbose=True) is False
    assert is_text_variant("ny", MEOW_VARIANTS, verbose=True) is False
    assert is_text_variant("the cat goes meow", MEOW_VARIANTS, verbose=True) is True
    assert is_text_variant("miau!", MEOW_VARIANTS, verbose=True) is True
    assert is_text_variant("nyaa~~", MEOW_VARIANTS, verbose=True) is True
    assert is_text_variant("m¡au", MEOW_VARIANTS, verbose=True) is True
    assert is_text_variant("m-e-o-w", MEOW_VARIANTS, verbose=True) is True
    assert is_text_variant("m i a u", MEOW_VARIANTS, verbose=True) is True
    assert is_text_variant("n_y_a", MEOW_VARIANTS, verbose=True) is True
    assert is_text_variant("m.e.o.w", MEOW_VARIANTS, verbose=True) is True
    assert is_text_variant("m  3  o = w", MEOW_VARIANTS, verbose=True) is False
    assert is_text_variant("m3ow", MEOW_VARIANTS, verbose=True) is False
    assert is_text_variant("ny4", MEOW_VARIANTS, verbose=True) is False
    assert is_text_variant("miautyzm", MEOW_VARIANTS, verbose=True) is True
    # assert True is False # Ensure debug prints