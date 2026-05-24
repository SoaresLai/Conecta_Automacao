from playwright.sync_api import sync_playwright
from Playwrite.Browser import FireFox
from Core.monitor import Monitor
from Core.Flow.chamados_flow import ChamadosFlow
from Core.Database.data import Database
from dotenv import load_dotenv
import os

load_dotenv()


def main():

    BASE_URL = os.getenv("BASE_URL")

    browser = FireFox()

    browser.startBrowser()

    browser.go_to("BASE_URL")

    browser.wait(3000)

    db = Database()

    fluxo = ChamadosFlow(browser)

    fluxo.abrir_meus_chamados()

    monitor = Monitor(browser)

    monitor.abrir_fila()

    chamados = monitor.buscar_chamados()

    # SALVAR CHAMADOS NO BANCO
    for chamado in chamados:

        id_chamado = chamado["id"]

        id_chamado = id_chamado.replace(" ", "")

        print(f"[SALVANDO] {id_chamado}")

        db.salvar_chamado(
            id_chamado=id_chamado
        )

    # PROCESSAR CHAMADOS
    for chamado in chamados:

        id_chamado = chamado["id"]

        id_chamado = id_chamado.replace(" ", "")

        monitor.abrir_chamado(
            id_chamado
        )

        categoria = monitor.ler_categoria()

        # SALVA CATEGORIA
        db.atualizar_categoria(
            id_chamado,
            categoria
        )

        # FILTRO DE CATEGORIA
        if "Acessos a Pastas" not in categoria:

            print("[SKIP] Não é categoria de pasta")

            continue

        # LER CONVERSA
        texto_chamado = monitor.ler_conversa_chamado()

        print(texto_chamado)

        # VALIDAR PERGUNTAS
        perguntas_encontradas = 0

        if "caminho completo da pasta" in texto_chamado:
            perguntas_encontradas += 1

        if "esse acesso seria por tempo indeterminado" in texto_chamado:
            perguntas_encontradas += 1

        if "poderia me dar mais detalhes" in texto_chamado:
            perguntas_encontradas += 1

        if "existe um pop dessas atividades" in texto_chamado:
            perguntas_encontradas += 1

        if "edição ou apenas visualização" in texto_chamado:
            perguntas_encontradas += 1

        if "dados sensíveis" in texto_chamado:
            perguntas_encontradas += 1

        perguntas_feitas = perguntas_encontradas >= 4

        # VALIDAR APROVAÇÃO
        tem_aprovacao = (
            "pedido de validação" in texto_chamado
        )

        # DEBUG
        print(f"Perguntas encontradas: {perguntas_encontradas}")

        print(f"Perguntas feitas? {perguntas_feitas}")

        print(f"Tem aprovação? {tem_aprovacao}")

        # SALVAR NO BANCO
        db.atualizar_validacoes(
            id_chamado=id_chamado,
            perguntas=perguntas_feitas,
            aprovacao=tem_aprovacao
        )

        # AÇÕES
        if not perguntas_feitas:

            print("[AÇÃO] Fazer perguntas padrão")

        elif perguntas_feitas and not tem_aprovacao:

            print("[AÇÃO] Solicitar aprovação")

        else:

            print("[OK] Chamado já tratado")

    print(chamados)


main()