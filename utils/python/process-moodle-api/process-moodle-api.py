import json
import sys
from pathlib import Path

import requests

if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) != 3:
        raise Exception("There must be 2 arguments: 1 - the moodle result file, 2 - the download destination path")
    materials = sys.argv[1]
    path = Path(sys.argv[2])
    with open(materials, "r") as jFile:
        response = json.load(jFile)
    for item in response:
        # daca exista nume al sectiunii de pe pagina cursului si e diferit de tama/teme/proiect/proiecte si e vizibil pt utiliz
        if item['name'].strip() and "tem" not in item['name'].lower() and "proiect" not in item['name'].lower() and item['uservisible']:
            print("\nStart section: ", item['name'] + '\n')
            p = path / item['name'] # adauga numele sectiunii la calea destinatiei
            p.mkdir(parents=True, exist_ok=True) # creeaza folder la calea data
            for module in item['modules']: # modules = numele cheii din dict unde se gasesc materialele
                if 'contents' in module:
                    for content in module['contents']:
                        if 'fileurl' in content: # fileurl = cheie din dictionarul contents care contine linkul catre materiale
                            try:
                                print("---------------------------------------------------------------------------------------------------")
                                print("Start downloading: ", content['filename'])
                                request = requests.get(content['fileurl'], stream=True, allow_redirects=True)
                                filepath = p / content['filename'] # calea catre fisierul extras
                                with open(filepath, "wb") as Pypdf:
                                    for chunk in request.iter_content(chunk_size=1024):
                                        if chunk:
                                            Pypdf.write(chunk)
                            except requests.exceptions.RequestException as e:
                                raise e
                            print("Finished downloading: ", content['filename'])
            print(f"\nFinished section: {item['name']} \n")
