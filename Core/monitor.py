from dotenv import load_dotenv
import os

load_dotenv()


class Monitor:

    def __init__(self, browser):

        self.browser = browser
        self.page = browser.page

    def abrir_fila(self):

        TICKET_URL = os.getenv("TICKET_URL")

        print("[MONITOR] Abrindo fila")

        self.page.goto("TICKET_URL")

        self.page.wait_for_load_state("networkidle")

    def buscar_chamados(self):

        print("[MONITOR] Buscando chamados")

        self.page.wait_for_selector("table tbody tr")

        linhas = self.page.locator(
            "table tbody tr"
        ).all()

        chamados = []

        for linha in linhas:

            try:

                id_chamado = linha.locator(
                    "span.text-nowrap"
                ).first.inner_text()

                print(f"Chamado encontrado: {id_chamado}")

                chamados.append({
                    "id": id_chamado
                })

            except Exception as erro:

                print(f"[ERRO] {erro}")

        return chamados
    
    def abrir_chamado(self, id_chamado):

        print(f"[ABRINDO] Chamado {id_chamado}")

        self.page.goto(
            f"ID_TICKET={id_chamado}"
        )

        self.page.wait_for_load_state("networkidle")

    def ler_categoria(self):

        categoria = self.page.locator(
            'select[name="itilcategories_id"] option[selected]'
        ).inner_text()

        print(f"[CATEGORIA] {categoria}")

        return categoria
    
    def ler_conversa_chamado(self):

        print("[MONITOR] Lendo conversa do chamado")

        timeline = self.page.locator("div.itil-timeline")

        texto = timeline.inner_text()

        return texto.lower()