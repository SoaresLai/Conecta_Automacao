class ChamadosFlow:

    def __init__(self, browser):

        self.browser = browser
        self.page = browser.page

class ChamadosFlow:

    def __init__(self, browser):

        self.browser = browser
        self.page = browser.page

    def abrir_meus_chamados(self):

        print("[MENU] Abrindo Assistência")

        menu = self.page.locator(
            'li[title="Assistência"]'
        )

        menu.click()

        self.page.wait_for_timeout(1000)

        print("[MENU] Abrindo Chamados")

        self.page.locator(
            'a[href="/front/ticket.php"]'
        ).click()

        self.page.wait_for_load_state("networkidle")

        print("[FILTRO] Abrindo filtro")


        self.page.wait_for_load_state("networkidle")

        print("[OK] Fila carregada")