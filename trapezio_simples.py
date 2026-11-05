"""
Equipe 1: Ana Alice Dias, Caio Vasconcelos e Yasmin dos Santos
Tema 1 - Deslocamento de um veículo | Método: Regra do Trapézio Simples

Como executar (Python 3.8+):
    python trapezio_simples.py
    Opcional, para a verificação com SciPy: pip install scipy
"""

import sys
from fractions import Fraction

# Evita erro ao imprimir acentos e símbolos em terminais antigos do Windows
try:
    sys.stdout.reconfigure(errors="replace")
except (AttributeError, ValueError):
    pass


# Dados do problema: intervalo [A, B] em segundos e número de subintervalos
A = 0.0
B = 10.0
N = 1


# Velocidade do veículo (m/s)
def v(t):
    return 2 + 0.4 * t + 0.05 * t ** 2


# Segunda derivada: v'(t) = 0,4 + 0,1t  ->  v''(t) = 0,1 (constante, m/s³)
def v_segunda_derivada(t):
    return 0.1


# Primitiva de v(t), em frações exatas para o valor de referência
def primitiva_v(t):
    t = Fraction(t)
    return 2 * t + Fraction(1, 5) * t ** 2 + Fraction(1, 60) * t ** 3


# Regra do Trapézio Simples: I ≈ (h/2)·[f(a) + f(b)], com h = b - a
def trapezio_simples(f, a, b):
    h = b - a
    return (h / 2) * (f(a) + f(b))


# Formata número com vírgula decimal
def br(x, casas=4):
    return f"{x:.{casas}f}".replace(".", ",")


def main():
    linha = "=" * 70

    # 1. Aproximação numérica
    h = (B - A) / N
    v_a, v_b = v(A), v(B)
    d_num = trapezio_simples(v, A, B)

    # 2. Valor de referência pela integração analítica: S(b) - S(a)
    d_ref_exato = primitiva_v(B) - primitiva_v(A)
    d_ref = float(d_ref_exato)

    # 3. Erro absoluto e erro relativo percentual
    ea = abs(d_ref - d_num)
    er = ea / abs(d_ref) * 100

    # 4. Erro de truncamento teórico: E = -(h³/12)·v''(ξ)
    #    Como v''(t) = 0,1 é constante, qualquer ξ em [a, b] dá o mesmo
    #    valor, e a fórmula fornece o erro exato do método nesta função.
    e_teorico = -(h ** 3 / 12) * v_segunda_derivada(A)

    # 5. Exibição dos resultados
    print(linha)
    print("  INTEGRAÇÃO NUMÉRICA - REGRA DO TRAPÉZIO SIMPLES")
    print("  Tema 1: Deslocamento de um veículo")
    print(linha)

    print("\n[1] Dados do problema")
    print("    Função .............: v(t) = 2 + 0,4t + 0,05t²   [m/s]")
    print(f"    Intervalo ..........: [a, b] = [{br(A, 0)}, {br(B, 0)}]   [s]")
    print(f"    Nº de subintervalos : n = {N}")
    print(f"    Passo ..............: h = (b - a)/n = {br(h, 0)} s")

    print("\n[2] Pontos utilizados")
    print("      i      t_i (s)      v(t_i) (m/s)")
    print(f"      0      {br(A, 1):>7}      {br(v_a):>12}")
    print(f"      1      {br(B, 1):>7}      {br(v_b):>12}")

    print("\n[3] Substituição na fórmula   D ≈ (h/2)·[v(t0) + v(t1)]")
    print(f"    D ≈ ({br(h, 0)}/2)·[{br(v_a)} + {br(v_b)}]")
    print(f"      = {br(h / 2, 0)}·{br(v_a + v_b)}")
    print(f"      = {br(d_num)} m")

    print("\n[4] Valor de referência (integração analítica)")
    print("    S(t) = 2t + 0,2t² + (0,05/3)t³   (primitiva de v)")
    print(f"    Iref = S(10) - S(0) = {d_ref_exato} ≈ {br(d_ref, 6)} m")

    print("\n[5] Comparação e erros")
    print(f"    Aproximação numérica   Inum = {br(d_num, 6)} m")
    print(f"    Valor de referência    Iref = {br(d_ref, 6)} m")
    print(f"    Erro absoluto          Ea   = {br(ea, 6)} m")
    print(f"    Erro relativo          Er   = {br(er, 4)} %")
    if d_num > d_ref:
        print("    O Trapézio Simples superestimou o deslocamento.")
    elif d_num < d_ref:
        print("    O Trapézio Simples subestimou o deslocamento.")

    # 6. A fórmula teórica do erro reproduz exatamente o erro observado
    print("\n[6] Conferência pelo erro de truncamento teórico")
    print("    E = -(h³/12)·v''(ξ),  com v''(t) = 0,1 m/s³ (constante)")
    print(f"    E = -({br(h, 0)}³/12)·0,1 = {br(e_teorico, 6)} m")
    print(f"    Inum + E = {br(d_num + e_teorico, 6)} m   (coincide com Iref)")

    # 7. Funções prontas usadas SÓ para conferência, cada uma de um item:
    #    trapezoid confere a implementação do método; quad, a referência.
    print("\n[7] Verificação complementar (não substitui o método)")
    try:
        from scipy.integrate import trapezoid, quad
        print(f"    trapezoid (confere o método)    = "
              f"{br(trapezoid([v_a, v_b], [A, B]), 6)} m")
        print(f"    quad (confere a referência)     = "
              f"{br(quad(v, A, B)[0], 6)} m")
    except ImportError:
        print("    SciPy não instalado (pip install scipy); "
              "verificação ignorada.")

    print("\n" + linha)
    print(f"  Resultado: deslocamento aproximado de {br(d_num, 2)} m em 10 s,")
    print(f"  contra {br(d_ref, 2)} m do valor exato "
          f"(erro relativo de {br(er, 2)} %).")
    print(linha)


if __name__ == "__main__":
    main()
