# Bibliotecas
from shiny import ui, render, App
import pandas as pd
import plotnine as p9

# Dados
dados = pd.read_csv("dashboard/dados/dados.csv", converters = {"data": pd.to_datetime})

# Interface do Usuário
app_ui = ui.page_sidebar(

    # |-- Inputs
    ui.sidebar(
        ui.markdown(
            "**Entra em campo a seleção de dados macroeconômicos! ⚽**"
            ),
        ui.markdown(
            "Defina os times de países e indicadores, explore o jogo de visualizações e marque gol na análise de dados!"
            ),
        ui.input_selectize(
            id = "botao_variavel",
            label = "Selecionar variável:",
            choices = dados.variavel.unique().tolist(),
            selected = "PIB (%, cresc. anual)"
            ),
        ui.input_radio_buttons(
            id = "botao_grafico",
            label = "Selecionar tipo de gráfico:",
            choices = ["Coluna", "Linha", "Área"],
            selected = "Linha"
            )
        ),

    # |-- Outputs
    ui.layout_columns(
        ui.card(
            ui.input_selectize(
                id = "botao_pais1",
                label = "Selecione o 1º país:",
                choices = dados.pais.unique().tolist(),
                selected = "Argentina"
                ),
            ui.output_plot("grafico_pais1")
            ),
        ui.card(
            ui.input_selectize(
                id = "botao_pais2",
                label = "Selecione o 2º país:",
                choices = dados.pais.unique().tolist(),
                selected = "Brazil"
                ),
            ui.output_plot("grafico_pais2")
            ),
    ),

    title = ui.h2(ui.strong("⚽Macro Copa"))
)


# Lógica de Servidor
def server(input, output, session):
    
    @render.plot
    def grafico_pais1():
        selecao_pais1 = input.botao_pais1()
        selecao_var = input.botao_variavel()
        tabela_pais1 = dados.query("pais == @selecao_pais1 and variavel == @selecao_var")
        grafico_pais1 = (
            p9.ggplot(tabela_pais1) +
            p9.aes(x = "data", y = "valor")
        )
        if input.botao_grafico() == "Coluna":
            return grafico_pais1 + p9.geom_col()
        elif input.botao_grafico() == "Linha":
            return grafico_pais1 + p9.geom_line()
        else:
            return grafico_pais1 + p9.geom_area()
    
    @render.plot
    def grafico_pais2():
        selecao_pais2 = input.botao_pais2()
        selecao_var = input.botao_variavel()
        tabela_pais2 = dados.query("pais == @selecao_pais2 and variavel == @selecao_var")
        grafico_pais2 = (
            p9.ggplot(tabela_pais2) +
            p9.aes(x = "data", y = "valor")
        )
        if input.botao_grafico() == "Coluna":
            return grafico_pais2 + p9.geom_col()
        elif input.botao_grafico() == "Linha":
            return grafico_pais2 + p9.geom_line()
        else:
            return grafico_pais2 + p9.geom_area()

# Dashboard
app = App(app_ui, server)