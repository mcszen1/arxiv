from datetime import datetime
import os
import json
import pandas as pd
import arxivscraper
import streamlit as st

def scrape_ai(start_date, end_date):
    folder = "ARXIV"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Formatação das datas
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError as e:
        print("Erro na formatação das datas:", e)
        return

    scraper = arxivscraper.Scraper(category='cs', date_from=start_date, date_until=end_date, filters={'categories':['cs.AI']})
    output = scraper.scrape()

    if not isinstance(output, list) or not output:
        print("Nenhum dado retornado pelo scraper.")
        return


def main():
    st.title("ArXiv Scraper de IA")
    
    # Criação de input para as datas
    start_date = st.date_input("Data de início", datetime.today()).strftime("%Y-%m-%d")
    end_date = st.date_input("Data de término", datetime.today()).strftime("%Y-%m-%d")

    # Botão para iniciar o scraping
    if st.button("Iniciar Scraping"):
        if start_date <= end_date:
            # Chama a função scrape_ai e captura o DataFrame retornado
            df = scrape_ai(start_date, end_date)

            # Verifica se o DataFrame foi retornado e possui dados
            if df is not None and not df.empty:
                st.success("Scraping concluído com sucesso!")

                # Mostra o DataFrame na interface
                st.dataframe(df)

                # Permite o download do DataFrame como CSV
                csv = df.to_csv(index=False)
                st.download_button(label="Baixar Dados em CSV",
                                   data=csv,
                                   file_name='arxiv_data.csv',
                                   mime='text/csv')

            else:
                st.error("Nenhum dado encontrado para as datas selecionadas.")
        else:
            st.error("A data de início deve ser anterior à data de término.")

if __name__ == "__main__":
    main()
