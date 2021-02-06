# Copyright 2021 Miles Barr
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

def collapse(typ):
    while typ[0] == "forward":
        typ = typ[1]
    return typ


def dup(typ, copied):
    if type(typ) != list:
        return typ
    if id(typ) in copied:
        return copied[id(typ)]
    copied[id(typ)] = [dup(x, copied) for x in typ]
    return copied[id(typ)]


def unify(type_a, type_b):
    type_a = collapse(type_a)
    type_b = collapse(type_b)
    if type_a[0] == "any":
        type_a[:] = ["forward", type_b]
    elif type_b[0] == "any":
        type_b[:] = ["forward", type_a]
    elif type_a[0] == "lambda" and type_b[0] == "lambda":
        unify(type_a[1], type_b[1])
        unify(type_a[2], type_b[2])
        type_b[:] = ["forward", type_a]
    elif not (type_a[0] == type_b[0] and type_a[0] in ["int", "bool"]):
        assert False, "type mismatch between `{}` and `{}`".format(type_a[0], type_b[0])


def infer(expr, env):
    if expr[0] == "identifier":
        return collapse(env[expr[1]])
    elif expr[0] == "let":
        env = env.copy()
        env[expr[1]] = ["any"]
        unify(env[expr[1]], infer(expr[2], env))
        return infer(expr[3], env)
    elif expr[0] == "lambda":
        env = env.copy()
        env[expr[1]] = ["any"]
        return ["lambda", env[expr[1]], infer(expr[2], env)]
    elif expr[0] == "apply":
        ret = ["any"]
        unify(dup(infer(expr[1], env), {}), ["lambda", infer(expr[2], env), ret])
        return collapse(ret)
    elif expr[0] in ["int", "bool"]:
        return [expr[0]]
    else:
        assert False


# fmt: off

# Identity Function

print(infer(
    ["let", "identity", ["lambda", "x", ["identifier", "x"]],
        ["apply", ["identifier", "identity"], ["bool", True]]], {}))

# Factorial Function

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
