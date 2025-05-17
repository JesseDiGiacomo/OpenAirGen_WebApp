import requests
from bs4 import BeautifulSoup
import zipfile
import io
import os

def baixar_arquivo_aixm():
    pagina = "https://aisweb.decea.mil.br/?i=publicacoes&p=aixm"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(pagina, headers=headers)
    if res.status_code != 200:
        print("[ERRO] Não foi possível acessar a página de publicações AIXM.")
        return

    soup = BeautifulSoup(res.text, "html.parser")
    blocos = soup.find_all("div", class_="plan")

    mais_recente = None
    url_mais_recente = None

    for bloco in blocos:
        h3 = bloco.find("h3")
        if not h3:
            continue
        emenda = h3.find("strong")
        if not emenda:
            continue
        data_txt = emenda.text.strip().replace("AMDT", "").strip()
        try:
            from datetime import datetime
            data_amdt = datetime.strptime(data_txt, "%d/%m/%y")
        except:
            continue

        link = bloco.find("a", href=True, string=lambda text: "completo" in text.lower())
        if not link:
            continue
        href = link["href"]
        full_url = "https://aisweb.decea.mil.br/" + href.lstrip("/")

        if not mais_recente or data_amdt > mais_recente:
            mais_recente = data_amdt
            url_mais_recente = full_url

    if not url_mais_recente:
        print("[ERRO] Nenhum arquivo AIXM completo encontrado.")
        return

    print(f"[INFO] Baixando arquivo AIXM mais recente: {url_mais_recente}")
    r = requests.get(url_mais_recente, headers=headers)
    if r.status_code == 200:
        os.makedirs("aixm_xml", exist_ok=True)
        with zipfile.ZipFile(io.BytesIO(r.content)) as z:
            z.extractall("aixm_xml")
        print("[OK] Arquivo AIXM extraído para pasta 'aixm_xml'.")
    else:
        print(f"[ERRO] Falha no download: status {r.status_code}")