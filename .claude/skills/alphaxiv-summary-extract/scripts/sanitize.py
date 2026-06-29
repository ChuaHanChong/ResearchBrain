"""Repair math/symbol corruption from KaTeX text extraction.

Selenium's `textContent` on a KaTeX element grabs three layers at once (rendered glyphs, the
`\\LaTeX` source, and a duplicate) plus stray control chars, so "π₀.₅" arrives as
"π0.5\\pi_{0.5}π0.5​" and "±" as a backspace. This collapses them back to clean text; inline
$…$, `code`, and ``` blocks are masked first so genuine LaTeX (e.g. a $\\pi_0$ title) is untouched.
"""

import re

# zero-width spaces + C0 control chars (keep \t and \n)
_ZW = re.compile(r'[​‌‍⁠﻿\x00-\x08\x0b\x0c\x0e-\x1f]')

# literal \uXXXX escapes that leaked as text -> the real character
_UESC = {
    '\\u03c0': 'π', '\\u00b1': '±', '\\u03bc': 'μ', '\\u03b1': 'α', '\\u03b2': 'β',
    '\\u03b3': 'γ', '\\u03b4': 'δ', '\\u03b5': 'ε', '\\u03b8': 'θ', '\\u03bb': 'λ',
    '\\u03c1': 'ρ', '\\u03c3': 'σ', '\\u03c4': 'τ', '\\u03c6': 'φ', '\\u03c8': 'ψ',
    '\\u03c9': 'ω', '\\u03b7': 'η', '\\u00d7': '×', '\\u00b7': '·', '\\u03be': 'ξ',
    '\\u2248': '≈', '\\u2013': '–', '\\u2014': '—', '\\u2016': '‖', '\\u00b2': '²',
    '\\u00b3': '³', '\\u2212': '−', '\\u00b0': '°', '\\u2264': '≤', '\\u2265': '≥',
    '\\u2192': '→', '\\u2208': '∈', '\\u221a': '√', '\\u221e': '∞', '\\u2211': '∑',
    '\\u2207': '∇', '\\u2202': '∂', '\\u2243': '≃', '\\u2260': '≠', '\\u2261': '≡',
    '\\u03c7': 'χ', '\\u025b': 'ɛ', '\\u2113': 'ℓ', '\\u03d5': 'ϕ',
    '\\u0393': 'Γ', '\\u0394': 'Δ', '\\u0398': 'Θ', '\\u039b': 'Λ', '\\u039e': 'Ξ',
    '\\u03a0': 'Π', '\\u03a3': 'Σ', '\\u03a6': 'Φ', '\\u03a8': 'Ψ', '\\u03a9': 'Ω',
}

# leaked LaTeX greek-letter commands -> the letter (applied AFTER the triple-render collapse)
_GREEK = {
    'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε', 'varepsilon': 'ε',
    'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'vartheta': 'ϑ', 'iota': 'ι', 'kappa': 'κ',
    'lambda': 'λ', 'mu': 'μ', 'nu': 'ν', 'xi': 'ξ', 'pi': 'π', 'varpi': 'ϖ', 'rho': 'ρ',
    'sigma': 'σ', 'varsigma': 'ς', 'tau': 'τ', 'upsilon': 'υ', 'phi': 'ϕ', 'varphi': 'φ',
    'chi': 'χ', 'psi': 'ψ', 'omega': 'ω', 'Gamma': 'Γ', 'Delta': 'Δ', 'Theta': 'Θ',
    'Lambda': 'Λ', 'Xi': 'Ξ', 'Pi': 'Π', 'Sigma': 'Σ', 'Phi': 'Φ', 'Psi': 'Ψ', 'Omega': 'Ω',
}
_GREEK_RX = re.compile(r'\\(' + '|'.join(_GREEK) + r')\b')


def sanitize(text: str) -> str:
    """Return `text` with KaTeX triple-render, leaked LaTeX, control chars, and mangled ±
    repaired. Inline $…$, `code`, and ``` fenced blocks are protected verbatim."""
    if not text:
        return text

    holds: list = []

    def _mask(m):
        holds.append(m.group(0))
        return f"{len(holds) - 1}"  # … sentinel: collides with no rule or text

    text = re.sub(r'```.*?```', _mask, text, flags=re.S)
    text = re.sub(r'`[^`\n]+`', _mask, text)
    text = re.sub(r'\$[^$\n]{1,90}\$', _mask, text)

    text = _ZW.sub('', text)
    for k, v in _UESC.items():
        text = text.replace(k, v)
    text = re.sub(r'(?:\\?textpm|\textpm|extpm|\\pm)', '±', text)
    # pi-family triple render:  π0.5 \pi_{0.5} π0.5  ->  π0.5   (subscript may itself be a \command)
    text = re.sub(r'(π[\w.]*?)\\pi(?:[_^](?:\{[^}]*\}|\\?[a-zA-Z0-9]+))*(π[\w.]*?)(?=[^\w.]|$)',
                  lambda m: m.group(1) if m.group(1) == m.group(2) else m.group(0), text)
    text = re.sub(r'(π[\d.]+)_\{\*{0,2}[\d.]+\*{0,2}\}\*{0,2}[\d.]+\*{0,2}', r'\1', text)
    # generic  R \cmd{...} R  ->  R  (R must start alnum/greek, no delimiters — protects $…$ / `code`)
    text = re.sub(r'([A-Za-z0-9α-ωΑ-Ωϕ][^\s\\*`$()\[\]]{0,14})\\[a-zA-Z]+(?:[_^]?\{[^}]*\}|[_^]\\?\w+)*\1', r'\1', text)
    # generic  R <letters>_\cmd R  ->  R   (e.g. FθF_\thetaFθ); subscript MUST be a \command
    text = re.sub(r'([^\s*\\`]{1,8})[A-Za-z]*[_^]\\[a-zA-Z]+(?:[_^](?:\{[^}]*\}|\\?\w+))*\1', r'\1', text)
    # mangled '±' shown as ' 1 ' between numbers (>= one decimal side)
    text = re.sub(r'(\d\.\d+\*{0,2}) 1 (\*{0,2}\d)', r'\1 ± \2', text)
    text = re.sub(r'(\d\*{0,2}) 1 (\*{0,2}\d\.\d)', r'\1 ± \2', text)
    # simplify remaining raw LaTeX wrappers + leaked greek commands
    text = re.sub(r'\\(?:tilde|hat|bar|vec|mathbf|mathcal|mathrm|operatorname|text|boldsymbol)\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'(\1)/(\2)', text)
    text = _GREEK_RX.sub(lambda m: _GREEK[m.group(1)], text)
    text = re.sub(r'\\sqrt\{([^}]*)\}', r'√(\1)', text)
    text = re.sub(r'\\times\b', '×', text)
    text = re.sub(r'\\cdot\b', '·', text)
    text = re.sub(r'\\infty\b', '∞', text)
    text = re.sub(r'\\(?:leq|le)\b', '≤', text)
    text = re.sub(r'\\(?:geq|ge)\b', '≥', text)
    text = re.sub(r'\\approx\b', '≈', text)

    for i, h in enumerate(holds):
        text = text.replace(f"{i}", h)
    return text
