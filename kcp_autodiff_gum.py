#!/usr/bin/env python3
"""
KCP SCIENTIFIC CORE — AUTOMATIC DIFFERENTIATION (DUAL NUMBERS) + GUM UNCERTAINTY
Stdlib-Only | Propaga incerteza exata de 1.ª ordem em qualquer expressão científica.
Adicionado pela janela lead (23-11): selftest com valores cruzados por diferenças finitas.
"""
from __future__ import annotations
from dataclasses import dataclass
import ast
import math

@dataclass(frozen=True, slots=True)
class Dual:
    """Número Dual (val + der * ε, com ε² = 0) para derivação exata."""
    val: float
    der: float = 0.0

    def __add__(self, o: Dual | float) -> Dual:
        o = o if isinstance(o, Dual) else Dual(float(o), 0.0)
        return Dual(self.val + o.val, self.der + o.der)

    def __radd__(self, o: float) -> Dual:
        return Dual(float(o) + self.val, self.der)

    def __sub__(self, o: Dual | float) -> Dual:
        o = o if isinstance(o, Dual) else Dual(float(o), 0.0)
        return Dual(self.val - o.val, self.der - o.der)

    def __rsub__(self, o: float) -> Dual:
        return Dual(float(o) - self.val, -self.der)

    def __mul__(self, o: Dual | float) -> Dual:
        o = o if isinstance(o, Dual) else Dual(float(o), 0.0)
        return Dual(self.val * o.val, self.der * o.val + self.val * o.der)

    def __rmul__(self, o: float) -> Dual:
        return Dual(float(o) * self.val, float(o) * self.der)

    def __truediv__(self, o: Dual | float) -> Dual:
        o = o if isinstance(o, Dual) else Dual(float(o), 0.0)
        if o.val == 0.0:
            raise ZeroDivisionError("Divisão por zero na avaliação científica.")
        return Dual(self.val / o.val, (self.der * o.val - self.val * o.der) / (o.val ** 2))

    def __rtruediv__(self, o: float) -> Dual:
        if self.val == 0.0:
            raise ZeroDivisionError("Divisão por zero na avaliação científica.")
        return Dual(float(o) / self.val, (-float(o) * self.der) / (self.val ** 2))

    def __pow__(self, o: Dual | float) -> Dual:
        o = o if isinstance(o, Dual) else Dual(float(o), 0.0)
        val = self.val ** o.val
        if o.der == 0.0:
            der = o.val * (self.val ** (o.val - 1.0)) * self.der
        else:
            der = val * (o.der * math.log(self.val) + (o.val * self.der / self.val))
        return Dual(val, der)

    def __neg__(self) -> Dual:
        return Dual(-self.val, -self.der)

def d_sqrt(x: Dual) -> Dual:
    s = math.sqrt(x.val)
    return Dual(s, x.der / (2.0 * s))

def d_exp(x: Dual) -> Dual:
    e = math.exp(x.val)
    return Dual(e, e * x.der)

def d_log(x: Dual) -> Dual:
    return Dual(math.log(x.val), x.der / x.val)

def d_log10(x: Dual) -> Dual:
    return Dual(math.log10(x.val), x.der / (x.val * math.log(10.0)))

def d_sin(x: Dual) -> Dual:
    return Dual(math.sin(x.val), math.cos(x.val) * x.der)

def d_cos(x: Dual) -> Dual:
    return Dual(math.cos(x.val), -math.sin(x.val) * x.der)

SAFE_FUNCS = {
    "sqrt": d_sqrt,
    "exp": d_exp,
    "log": d_log,
    "log10": d_log10,
    "sin": d_sin,
    "cos": d_cos,
}

def _eval_ast(node: ast.AST, vars_dual: dict[str, Dual]) -> Dual:
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body, vars_dual)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return Dual(float(node.value), 0.0)
    if isinstance(node, ast.Name):
        if node.id == "pi":
            return Dual(math.pi, 0.0)
        if node.id == "e":
            return Dual(math.e, 0.0)
        return vars_dual[node.id]
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_ast(node.operand, vars_dual)
    if isinstance(node, ast.BinOp):
        l, r = _eval_ast(node.left, vars_dual), _eval_ast(node.right, vars_dual)
        if isinstance(node.op, ast.Add): return l + r
        if isinstance(node.op, ast.Sub): return l - r
        if isinstance(node.op, ast.Mult): return l * r
        if isinstance(node.op, ast.Div): return l / r
        if isinstance(node.op, ast.Pow): return l ** r
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in SAFE_FUNCS:
        if len(node.args) != 1:
            raise ValueError("Funções científicas aceitam apenas 1 argumento.")
        return SAFE_FUNCS[node.func.id](_eval_ast(node.args[0], vars_dual))
    raise ValueError(f"Operação não autorizada no AST: {type(node).__name__}")

def evaluate_scientific_gum(formula: str, env: dict[str, tuple[float, float]]) -> tuple[float, float]:
    """
    Avalia qualquer fórmula científica e calcula a incerteza combinada padrão GUM:
    u_c = sqrt( sum( (df/dx_i * u_i)^2 ) )
    """
    tree = ast.parse(formula, mode="eval")
    base_vars = {k: Dual(v, 0.0) for k, (v, _) in env.items()}
    nominal = _eval_ast(tree, base_vars).val

    variance_sum = 0.0
    for target_var, (val, unc) in env.items():
        if unc == 0.0:
            continue
        seeded = {k: Dual(v, 1.0 if k == target_var else 0.0) for k, (v, _) in env.items()}
        partial_der = _eval_ast(tree, seeded).der
        variance_sum += (partial_der * unc) ** 2

    return round(nominal, 6), round(math.sqrt(variance_sum), 6)

def selftest():
    # cross-check independente por diferenças finitas centrais
    def fd(formula, env, h=1e-6):
        def f(xs):
            return _eval_ast(ast.parse(formula, mode="eval"), {k: Dual(v, 0.0) for k, v in xs.items()}).val
        nom = f({k: v[0] for k, v in env.items()})
        var = 0.0
        for k, (v0, u) in env.items():
            if u == 0:
                continue
            plus = dict(env); minus = dict(env)
            plus[k] = (v0 + h, 0.0); minus[k] = (v0 - h, 0.0)
            der = (f({kk: vv[0] for kk, vv in plus.items()}) - f({kk: vv[0] for kk, vv in minus.items()})) / (2 * h)
            var += (der * u) ** 2
        return nom, math.sqrt(var)
    casos = [
        ("eps * 5.670374e-8 * area * (temp_k ** 4)", {"eps": (0.95, 0.02), "area": (2.0, 0.01), "temp_k": (300.0, 0.5)}),
        ("6.1 + log10(hco3 / (0.03 * pco2))", {"hco3": (24.0, 0.5), "pco2": (40.0, 1.0)}),
        ("exp(-lambda_ * t)", {"lambda_": (0.1, 0.005), "t": (10.0, 0.2)}),
        ("sqrt(g * l)", {"g": (9.81, 0.01), "l": (1.0, 0.002)}),
    ]
    ok = 0
    for formula, env in casos:
        ad = evaluate_scientific_gum(formula, env)
        fdv = fd(formula, env)
        diff = abs(ad[0] - fdv[0]) + abs(ad[1] - fdv[1])
        print(("PASS" if diff < 1e-4 else "FAIL"), formula[:36] + "...", "autodiff", ad, "vs fin-diff", (round(fdv[0], 6), round(fdv[1], 6)))
        if diff < 1e-4:
            ok += 1
    print("kcp_autodiff_gum SELFTEST:", str(ok) + "/" + str(len(casos)))
    return ok == len(casos)

if __name__ == "__main__":
    # Demonstração científica real
    p_val, p_unc = evaluate_scientific_gum(
        "eps * 5.670374e-8 * area * (temp_k ** 4)",
        {"eps": (0.95, 0.02), "area": (2.0, 0.01), "temp_k": (300.0, 0.5)},
    )
    print(f"Radiação Térmica (Stefan-Boltzmann): {p_val} ± {p_unc} W")
    ph_val, ph_unc = evaluate_scientific_gum(
        "6.1 + log10(hco3 / (0.03 * pco2))",
        {"hco3": (24.0, 0.5), "pco2": (40.0, 1.0)},
    )
    print(f"Equilíbrio Ácido-Base (pH Sanguíneo): {ph_val} ± {ph_unc}")
    print("selftest:", "VERDE" if selftest() else "VERMELHO")
