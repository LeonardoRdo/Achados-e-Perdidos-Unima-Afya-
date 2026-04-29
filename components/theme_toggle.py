"""
components/theme_toggle.py — Botão de alternância de tema claro/escuro

Componente visual no estilo "switch" iOS/Material, com sol e lua.
Ao clicar, alterna entre tema claro e escuro do sistema.
"""

import customtkinter as ctk
from config import COLORS, alternar_tema, get_tema


class ThemeToggle(ctk.CTkFrame):
    """
    Botão toggle visual pra alternar entre tema claro e escuro.

    Visual:
    - No claro: fundo branco, círculo à esquerda com ícone de sol ☀
    - No escuro: fundo escuro, círculo à direita com ícone de lua 🌙

    Args:
        parent: widget pai
        on_toggle: callback chamado APÓS o tema alternar (recebe novo tema string)
    """

    LARGURA = 56
    ALTURA = 28
    PADDING = 3

    def __init__(self, parent, on_toggle=None):
        super().__init__(
            parent,
            width=self.LARGURA,
            height=self.ALTURA,
            corner_radius=14,
            fg_color=self._cor_fundo(),
            border_width=1,
            border_color=COLORS["ink_200"],
        )
        self.on_toggle = on_toggle
        self.pack_propagate(False)
        self.grid_propagate(False)

        # Círculo deslizante com ícone
        # Usamos um Label posicionado com .place() pra controlar a posição livremente
        self.bolinha = ctk.CTkLabel(
            self,
            text=self._icone(),
            font=("Segoe UI", 12),
            width=self.ALTURA - (self.PADDING * 2),
            height=self.ALTURA - (self.PADDING * 2),
            corner_radius=(self.ALTURA - (self.PADDING * 2)) // 2,
            fg_color=self._cor_bolinha(),
            text_color=self._cor_icone(),
        )
        self._posicionar_bolinha()

        # Bind do clique em todos os elementos pra qualquer área disparar
        self.configure(cursor="hand2")
        self.bolinha.configure(cursor="hand2")
        self.bind("<Button-1>", self._on_click)
        self.bolinha.bind("<Button-1>", self._on_click)

    def _on_click(self, event=None):
        """Alterna o tema e dispara o callback."""
        novo_tema = alternar_tema()

        # Atualiza visual deste próprio toggle imediatamente
        self.configure(fg_color=self._cor_fundo())
        self.bolinha.configure(
            text=self._icone(),
            fg_color=self._cor_bolinha(),
            text_color=self._cor_icone(),
        )
        self._posicionar_bolinha()

        # Dispara callback (que vai re-renderizar a tela inteira)
        if self.on_toggle:
            self.on_toggle(novo_tema)

    def _posicionar_bolinha(self):
        """Posiciona a bolinha à esquerda (light) ou direita (dark)."""
        tamanho_bolinha = self.ALTURA - (self.PADDING * 2)

        if get_tema() == "light":
            # Bolinha à esquerda
            x = self.PADDING
        else:
            # Bolinha à direita
            x = self.LARGURA - tamanho_bolinha - self.PADDING

        self.bolinha.place(x=x, y=self.PADDING)

    @staticmethod
    def _cor_fundo():
        """Cor de fundo do toggle (trilha)."""
        if get_tema() == "light":
            return "#E4E4E7"  # cinza claro neutro
        else:
            return "#3F3F46"  # cinza escuro

    @staticmethod
    def _cor_bolinha():
        """Cor da bolinha (círculo deslizante)."""
        if get_tema() == "light":
            return "#FFFFFF"  # branco no claro
        else:
            return "#18181B"  # preto no escuro

    @staticmethod
    def _icone():
        """Ícone exibido na bolinha."""
        if get_tema() == "light":
            return "☀"  # sol
        else:
            return "🌙"  # lua

    @staticmethod
    def _cor_icone():
        """Cor do ícone."""
        if get_tema() == "light":
            return "#F59E0B"  # amarelo do sol
        else:
            return "#FCD34D"  # amarelo da lua
