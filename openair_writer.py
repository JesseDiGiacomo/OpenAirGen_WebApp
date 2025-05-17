import os
from datetime import datetime

def gerar_openair_a_partir_de_zonas(zonas, data):
    conteudo = ""
    for z in zonas:
        conteudo += "AC {0}\nAN {1}\nAL {2}\nAH {3}\nDP {4} {5}\nDC {6}\n\n".format(
            z.get('tipo', 'R'),
            z.get('nome', 'SEM_NOME'),
            z.get('al', 'SFC'),
            z.get('ah', 'UNL'),
            z['lat'],
            z['lon'],
            z.get('raio', 5)
        )
    ano, mes, dia = data.year, str(data.month).zfill(2), str(data.day).zfill(2)
    pasta = f"./data/{ano}/{mes}"
    os.makedirs(pasta, exist_ok=True)
    caminho = f"{pasta}/espaco_aereo_{ano}-{mes}-{dia}.txt"
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"[OK] Arquivo gerado: {caminho}")
    return caminho