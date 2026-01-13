from typing import Callable, Any


def order_items(
    original: list[Any], 
    reference: list[Any],
    getter: Callable = lambda x: x
) -> list[Any]:
    """Возвращает список, упорядоченный в соответствии с расположением элементов 
    в списке-образце.
    """
    ordered_indexes = []
    for item in original:
        try:
            ind = reference.index(getter(item))
        except:
            ind = len(original)
        ordered_indexes.append(ind)
        
    result = [y for x, y in sorted(zip(ordered_indexes, original), key=lambda x: x[0])]

    return result
