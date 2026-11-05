# -*- coding: utf-8 -*-
"""
==============================================================================
 CENTRO UNIVERSITÁRIO DO ESTADO DO PARÁ – CESUPA
 Engenharia da Computação – Cálculo Numérico – Turma EC6MA
 Professora: Suzane Alfaia Dias
 Equipe 1: Ana Alice Dias, Caio Vasconcelos e Yasmin dos Santos

 Atividade: Integração Numérica
 Tema 1 – Deslocamento de um veículo
 Método atribuído: Regra do Trapézio Simples
==============================================================================

PROBLEMA
    A velocidade de um veículo é dada por
        v(t) = 2 + 0,4t + 0,05t²        (v em m/s e t em s)
    e o deslocamento entre t = 0 s e t = 10 s é
        D = integral de v(t) dt, de 0 a 10   (D em metros)

MÉTODO
    Regra do Trapézio Simples (um único subintervalo, n = 1):
        integral de f(x) dx em [a, b]  ≈  (h/2) · [f(a) + f(b)],  h = b - a

O QUE O PROGRAMA FAZ
    1. Define a função v(t), o intervalo [a, b] e o número de subintervalos.
    2. Calcula a aproximação pela fórmula do Trapézio Simples, implementada
       explicitamente (sem funções prontas de integração).
    3. Calcula o valor de referência por integração analítica (primitiva).
    4. Exibe a tabela de pontos, a substituição na fórmula, o erro absoluto
       e o erro relativo percentual.
    5. Confere o erro obtido com a fórmula teórica do erro de truncamento.
    6. (Opcional) Faz uma verificação complementar com scipy.integrate.quad.
    7. (Opcional) Gera o gráfico da aproximação com a opção --grafico.

COMO EXECUTAR
    Requisito: Python 3.8 ou superior (https://www.python.org/downloads/).
    O cálculo principal usa apenas a biblioteca padrão do Python.

    1. Abra um terminal (Prompt de Comando, PowerShell ou o terminal do
       VS Code) na pasta onde está este arquivo.
    2. Execute:
           python trapezio_simples.py        (Windows)
           python3 trapezio_simples.py       (Linux ou macOS)
    3. Opcional - gerar o gráfico (salvo como grafico_trapezio_simples.png):
           pip install matplotlib
           python trapezio_simples.py --grafico
    4. Opcional - verificação complementar com o SciPy:
           pip install scipy
       Se o SciPy estiver instalado, a verificação aparece automaticamente.
==============================================================================
"""

import sys
from fractions import Fraction

# Evita que o programa pare por causa de algum caractere especial em
# terminais com codificação limitada (por exemplo, consoles antigos do
# Windows). Caracteres que não puderem ser exibidos viram "?".
try:
    sys.stdout.reconfigure(errors="replace")
except (AttributeError, ValueError):
    pass


# ----------------------------------------------------------------------------
# 1. DADOS DO PROBLEMA: função, intervalo e número de subintervalos
# ----------------------------------------------------------------------------
A = 0.0    # limite inferior de integração: t = 0 s
B = 10.0   # limite superior de integração: t = 10 s
N = 1      # número de subintervalos (o Trapézio Simples usa apenas 1)


def v(t):
    """Velocidade do veículo, em m/s, no instante t (em segundos)."""
    return 2 + 0.4 * t + 0.05 * t ** 2


def v_segunda_derivada(t):
    """Segunda derivada de v(t), em m/s³.

    v'(t)  = 0,4 + 0,1t   (aceleração, em m/s²)
    v''(t) = 0,1          (constante)

    Usada apenas para conferir o erro com a fórmula teórica."""
    return 0.1


def primitiva_v(t):
    """Primitiva (antiderivada) de v(t), obtida por integração analítica:

        S(t) = 2t + 0,2t² + (0,05/3)t³

    Os coeficientes são frações exatas (0,2 = 1/5 e 0,05/3 = 1/60) para que
    o valor de referência não tenha erro de arredondamento."""
    t = Fraction(t)
    return 2 * t + Fraction(1, 5) * t ** 2 + Fraction(1, 60) * t ** 3


# ----------------------------------------------------------------------------
# 2. MÉTODO NUMÉRICO: Regra do Trapézio Simples (implementação explícita)
# ----------------------------------------------------------------------------
def trapezio_simples(f, a, b):
    """Aproxima a integral de f no intervalo [a, b] pela Regra do Trapézio
    Simples.

    A curva f(x) é substituída pela reta que passa por (a, f(a)) e (b, f(b)).
    A área sob essa reta é a área de um trapézio de altura h = b - a e bases
    f(a) e f(b):

                    I  ≈  (h / 2) · [f(a) + f(b)]
    """
    h = b - a                       # passo: h = (b - a)/n, com n = 1
    f_a = f(a)                      # valor da função no extremo esquerdo
    f_b = f(b)                      # valor da função no extremo direito
    return (h / 2) * (f_a + f_b)    # fórmula do Trapézio Simples


# ----------------------------------------------------------------------------
# 3. ERROS
# ----------------------------------------------------------------------------
def erro_absoluto(i_ref, i_num):
    """Erro absoluto: Ea = |Iref - Inum|."""
    return abs(i_ref - i_num)


def erro_relativo_percentual(i_ref, i_num):
    """Erro relativo percentual: Er(%) = |Iref - Inum| / |Iref| · 100."""
    return abs(i_ref - i_num) / abs(i_ref) * 100


# ----------------------------------------------------------------------------
# 4. FUNÇÕES AUXILIARES DE EXIBIÇÃO
# ----------------------------------------------------------------------------
def br(x, casas=4):
    """Formata um número com vírgula decimal (padrão brasileiro)."""
    return f"{x:.{casas}f}".replace(".", ",")


def gerar_grafico(d_num, d_ref, nome_arquivo="grafico_trapezio_simples.png"):
    """Gera a figura com a área exata sob v(t) e o trapézio usado pelo
    método. Requer o pacote matplotlib (pip install matplotlib)."""
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        from matplotlib import font_manager
    except ImportError:
        print("\n  matplotlib não instalado. Para gerar o gráfico, execute:")
        print("      pip install matplotlib")
        return

    # Fonte do gráfico igual à do relatório (Arial ou a equivalente que
    # estiver instalada no computador)
    instaladas = {fonte.name for fonte in font_manager.fontManager.ttflist}
    for nome in ("Arial", "Liberation Sans", "DejaVu Sans"):
        if nome in instaladas:
            plt.rcParams["font.family"] = nome
            break
    plt.rcParams["hatch.linewidth"] = 0.6

    # Cores (curva real em azul, trapézio em laranja) e tons de texto
    azul, laranja = "#2a78d6", "#eb6834"
    tinta, tinta_sec, grade, eixo = "#0b0b0b", "#52514e", "#e1e0d9", "#c3c2b7"

    # Pontos para desenhar a curva v(t) e a reta do trapézio
    ts = [A + (B - A) * k / 400 for k in range(401)]
    curva = [v(t) for t in ts]
    reta = [v(A) + (v(B) - v(A)) * (t - A) / (B - A) for t in ts]

    fig, ax = plt.subplots(figsize=(6.3, 3.9), dpi=100)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Área exata sob a curva (o deslocamento real)
    ax.fill_between(ts, 0, curva, color=azul, alpha=0.12, linewidth=0,
                    label=f"Área sob v(t) = {br(d_ref, 2)} m (valor exato)")
    # Região entre a reta e a curva: é o erro do Trapézio Simples
    erro_area = br(d_num - d_ref, 2)
    ax.fill_between(ts, curva, reta, facecolor=(0.922, 0.408, 0.204, 0.16),
                    edgecolor=laranja, hatch="////", linewidth=0,
                    label=f"Área a mais do trapézio = {erro_area} m (erro)")
    # Curva real e lados do trapézio
    ax.plot(ts, curva, color=azul, linewidth=2, solid_capstyle="round",
            label="v(t) = 2 + 0,4t + 0,05t²")
    ax.plot([A, A, B, B], [0, v(A), v(B), 0], color=laranja, linewidth=2,
            solid_joinstyle="round",
            label=f"Trapézio Simples: área = {br(d_num, 2)} m")
    # Pontos usados pelo método, com anel branco para destacar sobre as linhas
    ax.scatter([A, B], [v(A), v(B)], s=60, color=laranja, edgecolors="white",
               linewidths=2, zorder=5)
    ax.annotate(f"v(0) = {br(v(A), 0)} m/s", (A, v(A)), xytext=(10, -10),
                textcoords="offset points", va="top", color=tinta,
                fontsize=9)
    ax.annotate(f"v(10) = {br(v(B), 0)} m/s", (B, v(B)), xytext=(-10, 8),
                textcoords="offset points", ha="right", color=tinta,
                fontsize=9)

    # Eixos, grade e legenda discretos
    ax.set_xlim(A - 0.15, B + 0.15)
    ax.set_ylim(0, 12.5)
    ax.set_xticks(range(0, 11, 2))
    ax.set_xlabel("Tempo t (s)", color=tinta_sec, fontsize=10)
    ax.set_ylabel("Velocidade v(t) (m/s)", color=tinta_sec, fontsize=10)
    ax.tick_params(colors=tinta_sec, labelsize=9, length=0)
    ax.grid(axis="y", color=grade, linewidth=0.8)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(eixo)
    ax.legend(loc="upper left", fontsize=8.5, frameon=False,
              labelcolor=tinta)

    fig.tight_layout()
    fig.savefig(nome_arquivo, dpi=300, facecolor="white")
    print(f"\n  Gráfico salvo em: {nome_arquivo}")

    # Abre a janela do gráfico quando houver interface gráfica disponível
    if matplotlib.get_backend().lower() != "agg":
        plt.show()
    plt.close(fig)


# ----------------------------------------------------------------------------
# 5. PROGRAMA PRINCIPAL
# ----------------------------------------------------------------------------
def main():
    linha = "=" * 70

    # Etapa 1 - aproximação numérica pela Regra do Trapézio Simples
    h = (B - A) / N                      # passo (n = 1, então h = b - a)
    v_a, v_b = v(A), v(B)                # valores da função nos dois pontos
    d_num = trapezio_simples(v, A, B)    # Inum

    # Etapa 2 - valor de referência por integração analítica
    # (Teorema Fundamental do Cálculo: D = S(b) - S(a))
    d_ref_exato = primitiva_v(B) - primitiva_v(A)
    d_ref = float(d_ref_exato)           # Iref

    # Etapa 3 - erros pedidos na atividade
    ea = erro_absoluto(d_ref, d_num)
    er = erro_relativo_percentual(d_ref, d_num)

    # Etapa 4 - erro de truncamento teórico: E = -(h³/12)·v''(ξ)
    # Como v''(t) = 0,1 é constante, qualquer ξ em [a, b] dá o mesmo valor,
    # e a fórmula fornece o erro exato do método para esta função.
    e_teorico = -(h ** 3 / 12) * v_segunda_derivada(A)

    # ------------------------------------------------------------------ saída
    print(linha)
    print("  INTEGRAÇÃO NUMÉRICA - REGRA DO TRAPÉZIO SIMPLES")
    print("  Tema 1: Deslocamento de um veículo (Equipe 1)")
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

    print("\n[6] Conferência pelo erro de truncamento teórico")
    print("    E = -(h³/12)·v''(ξ),  com v''(t) = 0,1 m/s³ (constante)")
    print(f"    E = -({br(h, 0)}³/12)·0,1 = {br(e_teorico, 6)} m")
    print(f"    Inum + E = {br(d_num + e_teorico, 6)} m   (coincide com Iref)")

    # Verificação complementar: função pronta usada SÓ para conferência
    print("\n[7] Verificação complementar (não substitui o método)")
    try:
        from scipy.integrate import quad
        valor_quad, _ = quad(v, A, B)
        print(f"    scipy.integrate.quad = {br(valor_quad, 6)} m")
    except ImportError:
        print("    SciPy não instalado; verificação ignorada.")
        print("    (para instalar: pip install scipy)")

    print("\n" + linha)
    print(f"  Resultado: deslocamento aproximado de {br(d_num, 2)} m em 10 s,")
    print(f"  contra {br(d_ref, 2)} m do valor exato "
          f"(erro relativo de {br(er, 2)} %).")
    print(linha)

    # Gráfico opcional (python trapezio_simples.py --grafico)
    if "--grafico" in sys.argv:
        gerar_grafico(d_num, d_ref)


if __name__ == "__main__":
    main()
