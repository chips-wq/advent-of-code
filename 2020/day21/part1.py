from collections import defaultdict, deque
import sys

infile = "example1.in" if len(sys.argv) <= 1 else sys.argv[1]

"""
D[allergen] = possible ingredients (domain of this allergen)

mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)

intersect lines 1 and 2 for dairy, you get `mxmvkd`.
D[dairy] = {mxmvkd}

!!!
Each allergen is found in exactly one ingredient.
Each ingredient contains zero or one allergen.
!!!

X_dairy != X_soy

i.e restriction of the sort (dairy, soy)

R = <{X_dairy, X_soy}, r>
r(v, v) = false
  ^  ^
 SAME INGREDIENT

for every possible thing in D[dairy], there must be something different in D[soy]
"""

with open(infile, "r") as f:
    lines = f.read().splitlines()
    D = {}
    D1 = defaultdict(int)

    for line in lines:
        ingredients = line.split("(")[0].strip()
        assert len(ingredients.split(" ")) == len(set(ingredients.split(" ")))
        ingredients = set(ingredients.split(" "))

        for ing in ingredients: D1[ing] += 1
        
        # allergens are the values of ingredients
        allergens = set(line.split("(contains")[1].strip().split(")")[0].split(", "))

        for allergen in allergens:
            if allergen not in D:
                D[allergen] = ingredients
            else:
                D[allergen] = (D[allergen] & ingredients)
    
    Q = deque([])
    uq_allergens = set(D.keys())
    for al1 in uq_allergens:
        for al2 in uq_allergens:
            if al1 == al2: continue
            Q.append((al1, al2))

    big_set = set()
    for small_set in D.values():
        big_set = (big_set | small_set)

    ans = 0
    for ing, vv in D1.items():
        if ing not in big_set: ans += vv
    print(f"{ans=}")
