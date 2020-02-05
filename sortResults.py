import operator
def sortIncreasing(results):
    results.sort(key = operator.itemgetter(1))
    return results
def sortDecreasing(results):
    results.sort(key = operator.itemgetter(1), reverse = True)
    return results