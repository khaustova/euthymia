from typing import List, Callable


def order_items(original: List, reference: List, getter: Callable = lambda x: x) -> List:
    """
    Возвращает список, упорядоченный в соответствии с расположением элементов 
    в списке-образце.
    """
    ordered_indexes = []
    for item in original:
        try:
            ind = reference.index(getter(item))
        except:
            ind = len(original)
        ordered_indexes.append(ind)

    return [y for x, y in sorted(zip(ordered_indexes, original), key=lambda x: x[0])]