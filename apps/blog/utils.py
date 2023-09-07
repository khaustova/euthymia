def get_word(n: int) -> int:
    """
    Возвращает группу склонения существительного после числительного.
    """
    n %= 100
    if n >= 5 and n <= 20:
        return 0
    n %= 10
    if n == 1:
        return 1
    elif n >= 2 and n <= 4:
        return 2
    return 0
