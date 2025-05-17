import os
import xml.etree.ElementTree as ET
from datetime import datetime
from openair_writer import gerar_openair_a_partir_de_zonas

def extrair_zonas_aixm(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    ns = {
        "aixm": "http://www.aixm.aero/schema/5.1",
        "gml": "http://www.opengis.net/gml/3.2"
    }

    zonas = []

    for airspace in root.findall(".//aixm:Airspace", ns):
        nome = airspace.findtext(".//aixm:name", default="SEM_NOME", namespaces=ns)
        tipo = airspace.findtext(".//aixm:type", default="R", namespaces=ns)
        limite_inf = airspace.findtext(".//aixm:lowerLimit", default="SFC", namespaces=ns)
        limite_sup = airspace.findtext(".//aixm:upperLimit", default="UNL", namespaces=ns)

        geos = airspace.findall(".//gml:posList", ns)
        if not geos:
            continue

        for geo in geos:
            coords = geo.text.strip().split()
            if len(coords) >= 4:
                lat = f"{int(float(coords[0]))}:{int((float(coords[0]) % 1) * 60)}:00 S"
                lon = f"{int(float(coords[1]))}:{int((float(coords[1]) % 1) * 60)}:00 W"
                zonas.append({
                    "tipo": tipo,
                    "nome": nome,
                    "lat": lat,
                    "lon": lon,
                    "al": limite_inf,
                    "ah": limite_sup,
                    "raio": 5
                })
                break
    return zonas

def processar_xmls(diretorio='aixm_xml'):
    if not os.path.exists(diretorio):
        print("[ERRO] Diretório 'aixm_xml' não encontrado.")
        return
    zonas = []
    arquivos = [f for f in os.listdir(diretorio) if f.endswith('.xml')]
    for arq in arquivos:
        caminho = os.path.join(diretorio, arq)
        print(f"[INFO] Processando: {arq}")
        try:
            zonas += extrair_zonas_aixm(caminho)
        except Exception as e:
            print(f"[ERRO] Falha ao processar {arq}: {e}")
    print(f"[OK] {len(zonas)} zonas extraídas.")
    gerar_openair_a_partir_de_zonas(zonas, datetime.utcnow().date())