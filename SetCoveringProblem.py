def set_cover(universe, subsets):
    """Find a family of subsets that covers the universal set"""
    elements = set(e for s in subsets for e in s)
    # Check the subsets cover the universe
    if elements != universe:
        return None
    covered = set()
    cover = []
    # Greedily add the subsets with the most uncovered points
    while covered != elements:
        subset = max(subsets, key=lambda s: len(s - covered))
        cover.append(subset)
        covered |= subset

    return cover


def main():
    universe = set(range(1, 6))
    subsets = [set([1, 2, 3]),
               set([2, 4]),
               set([3, 4]),
               set([4, 5])]
    cover = set_cover(universe, subsets)
    print(cover)


if __name__ == '__main__':
    main()