# Hindley–Milner in Python

A Hindley–Milner type system allows a programming language's types to be inferred with few or no explicit type annotations. A unique property of Hindley–Milner type systems is that type constraints are propagated both forward and backward throughout a program. More concretely, that means a variable both inherits type constraints from assigned expressions and imposes type constraints on assigned expressions based on how the variables is used. The body of a function (or lambda) imposes type constraints on the parameters and return value of the function. When calling a function, the function's constraints are duplicated onto the arguments and the expression where the function is used. As a result, a Hindley–Milner type system forms a system of type constraints across an entire program.

Although a Hindley–Milner type system can sound daunting, its implementation can be quite simple. This repository contains a minimal example of a Hindley–Milner type system implemented in Python. The example is intended as a learning tool to more easily understand the implementation of a Hindley–Milner type system. One could extrapolate the same concepts from the example to implement a Hindley–Milner type system for a full-fledged programming language.

## Examples

### Identity Function

Python representation:
```py
identity = lambda x: x
print(type(identity(True)))
```

Hindley–Milner type inference:
```py
print(infer(
    ["let", "identity", ["lambda", "x", ["identifier", "x"]],
        ["apply", ["identifier", "identity"], ["bool", True]]], {}))
```

### Factorial Function

Python representation:
```py
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

print(type(factorial(1)))
```

Hindley–Milner type inference:
```py
if_type = ["any"]
print(infer(
    ["let", "factorial", ["lambda", "n",
        ["apply", ["apply", ["apply", ["identifier", "if"],
            ["apply", ["identifier", "zero?"], ["identifier", "n"]]],
            ["int", 1]],
            ["apply", ["apply", ["identifier", "*"],
                ["identifier", "n"]],
                ["apply", ["identifier", "factorial"],
                    ["apply", ["apply", ["identifier", "-"],
                        ["identifier", "n"]], ["int", 1]]]]]],
        ["apply", ["identifier", "factorial"], ["int", 123]]], {
    "if": ["lambda", ["bool"],
        ["lambda", if_type, ["lambda", if_type, if_type]]],
    "zero?": ["lambda", ["int"], ["bool"]],
    "*": ["lambda", ["int"], ["lambda", ["int"], ["int"]]],
    "-": ["lambda", ["int"], ["lambda", ["int"], ["int"]]]
}))
```
