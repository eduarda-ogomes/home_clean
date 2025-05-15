import schedule
import time
from gerenciador import Gerenciador

def redistribuir_semanal():
    g = Gerenciador()
    g.carregar_de_json("dados.json")
    g.redistribuir_tarefas()
    g.salvar_em_json("dados.json")
    print("Tarefas redistribuídas automaticamente.")

schedule.every().monday.at("08:00").do(redistribuir_semanal)

while True:
    schedule.run_pending()
    time.sleep(1)
