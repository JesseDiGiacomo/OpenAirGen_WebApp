from aixm_downloader import baixar_arquivo_aixm
from aixm_parser import processar_xmls

if __name__ == "__main__":
    baixar_arquivo_aixm()
    processar_xmls()