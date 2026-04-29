"""
screens/login.py — Tela de login

Simula login via Google OAuth: o usuário escolhe entre os perfis
pré-cadastrados (alunos e funcionários). Em produção seria substituído
pela integração real com Google OAuth 2.0.
"""

import customtkinter as ctk
from config import COLORS
import database as db


class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, on_login):
        super().__init__(parent, fg_color=COLORS["magenta"], corner_radius=0)
        self.on_login = on_login

        self._build()

    def _build(self):
        # Container central
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Card branco
        card = ctk.CTkFrame(
            container,
            fg_color=COLORS["white"],
            corner_radius=24,
            border_width=0
        )
        card.pack(padx=20, pady=20)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=44, pady=40)

        # Logo da Afya (caixa preta com texto)
        logo_box = ctk.CTkFrame(
            inner,
            fg_color=COLORS["ink_900"],
            corner_radius=12,
            height=70
        )
        logo_box.pack(pady=(0, 24))
        logo_box.pack_propagate(False)

        ctk.CTkLabel(
            logo_box,
            text="Afya",
            font=("Segoe UI", 32, "bold"),
            text_color=COLORS["magenta"],
        ).pack(side="left", padx=(28, 12), pady=12)

        ctk.CTkLabel(
            logo_box,
            text="CENTRO\nUNIVERSITÁRIO\nUNIMA · AL",
            font=("Segoe UI", 9, "bold"),
            text_color=COLORS["magenta"],
            justify="left"
        ).pack(side="left", padx=(0, 28), pady=12)

        # Título
        ctk.CTkLabel(
            inner,
            text="Bem-vindo",
            font=("Segoe UI", 26, "bold"),
            text_color=COLORS["ink_900"],
        ).pack()

        ctk.CTkLabel(
            inner,
            text="Acesse a central de itens perdidos\nda Afya com sua conta institucional.",
            font=("Segoe UI", 13),
            text_color=COLORS["ink_500"],
            justify="center"
        ).pack(pady=(8, 24))

        # Lista de usuários (simula OAuth com perfis)
        usuarios = db.listar_usuarios()

        # Separador "Selecione um perfil"
        ctk.CTkLabel(
            inner,
            text="SELECIONE UM PERFIL",
            font=("Segoe UI", 10, "bold"),
            text_color=COLORS["ink_400"]
        ).pack(pady=(0, 12))

        for u in usuarios:
            self._criar_botao_usuario(inner, u)

        # Footer
        ctk.CTkLabel(
            inner,
            text="Acesso restrito a contas @afya.edu.br\nProtótipo de validação · v1.0",
            font=("Segoe UI", 10),
            text_color=COLORS["ink_400"],
            justify="center"
        ).pack(pady=(20, 0))

    def _criar_botao_usuario(self, parent, usuario):
        """Cria um botão estilizado para cada usuário."""
        btn_frame = ctk.CTkFrame(
            parent,
            fg_color=COLORS["ink_25"],
            border_color=COLORS["ink_100"],
            border_width=1,
            corner_radius=10,
            height=58,
            cursor="hand2"
        )
        btn_frame.pack(fill="x", pady=4)
        btn_frame.pack_propagate(False)

        inner = ctk.CTkFrame(btn_frame, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=14, pady=10)

        # Avatar (emoji)
        avatar = ctk.CTkLabel(
            inner,
            text=usuario.get("foto_url", "👤"),
            font=("Segoe UI", 24),
            width=40, height=40,
            corner_radius=20,
            fg_color=COLORS["magenta_50"]
        )
        avatar.pack(side="left")

        # Info
        info = ctk.CTkFrame(inner, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=(12, 0))

        ctk.CTkLabel(
            info,
            text=usuario["nome"],
            font=("Segoe UI", 13, "bold"),
            text_color=COLORS["ink_900"],
            anchor="w"
        ).pack(anchor="w", fill="x")

        tipo_texto = "Aluno" if usuario["tipo"] == "aluno" else "Funcionário · Setor de Achados"
        ctk.CTkLabel(
            info,
            text=f"{usuario['email']}  ·  {tipo_texto}",
            font=("Segoe UI", 10),
            text_color=COLORS["ink_400"],
            anchor="w"
        ).pack(anchor="w", fill="x")

        # Seta indicando ação
        ctk.CTkLabel(
            inner,
            text="→",
            font=("Segoe UI", 18, "bold"),
            text_color=COLORS["ink_300"]
        ).pack(side="right", padx=(0, 4))

        # Bind do clique em todos os elementos filhos
        def selecionar(e=None, u=usuario):
            self.on_login(u)

        for w in [btn_frame, inner, info, avatar]:
            w.bind("<Button-1>", selecionar)

        # Hover effect
        def on_enter(e):
            btn_frame.configure(border_color=COLORS["magenta"], fg_color=COLORS["magenta_50"])

        def on_leave(e):
            btn_frame.configure(border_color=COLORS["ink_100"], fg_color=COLORS["ink_25"])

        for w in [btn_frame, inner, info, avatar]:
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)
