from playwright.sync_api import sync_playwright, Page

class FireFox:
    def __init__(self, headless=False):
        self.headless = headless
        self.playWright = None
        self.browser = None
        self.context = None
        self.page: Page = None

    def startBrowser(self):
        print("Iniciando serviço do browser...")
        self.playWright = sync_playwright().start()
        self.page = self.context.new_page()
        print("Serviço do browser inicializado.")
        return self.page
    
    def click(self, selector):
        self.page.click(selector)

    def fill(self, selector, value):
        self.page.fill(selector, value)

    def wait(self, tempo):
        self.page.wait_for_timeout(tempo)
    
    def go_to(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def wait(self, time_ms=1500):
        self.page.wait_for_timeout(time_ms)

    def click(self, selector):
        self.page.wait_for_selector(selector)
        self.page.locator(selector).first.click()

    def fill(self, selector, value):
        self.page.wait_for_selector(selector)
        self.page.fill(selector, value)

    def wait(self, time_ms=1500):
        self.page.wait_for_timeout(time_ms)
    
    def browser_close(self):
        print("Fechando o navegador")
        for operator in [self.page, self.context, self.browser]:
            if operator:
                operator.close()
            if self.playWright:
                self.playWright.stop()