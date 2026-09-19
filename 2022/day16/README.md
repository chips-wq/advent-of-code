# Memoization

What should my function look like to be memoized ?

```python

def f(x: int, y: int) -> int:
    pass

```

* `f` does some expensive computation
* `f` is a pure function
    * for any x, y int, `f(x, y)` is always the same
    * (i.e) it's a function in the mathematical sense


```python

D = {}
def g(x: int, y: int) -> int:
    if (x, y) in D: return D[(x, y)]
    ret = f(x, y)
    D[(x, y)] = ret
    return ret

```
