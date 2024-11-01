import os
import time
from datetime import datetime
import requests
from openpyxl import Workbook
from tqdm import tqdm

class CustCalculator:
    def __init__(self):
        self.credit = 200
        self.geo_cust = 0.005
        self.places_cust = 0.032

    def calcular_gastos(self, places_requests, geocoding_requests):
        total_geocoding_cost = geocoding_requests * self.geo_cust
        total_places_cost = places_requests * self.places_cust
        total_cost = total_geocoding_cost + total_places_cost
        remaining_credits = self.credit - total_cost
        return total_cost, remaining_credits

    def calculator(self):
        places_requests = int(input("Quantas requisições da API Place foi Realizada: "))
        geocoding_requests = int(input("Quantas requisições da API Geocoding foi Realizada: "))
        total_cost, remaining_credits = self.calcular_gastos(places_requests, geocoding_requests)
        print(f"Gasto Total: R$ {total_cost:.2f}")
        print(f"Créditos Restantes: R$ {remaining_credits:.2f}")

def limpar_terminal():
    """Limpa o terminal para uma nova exibição."""
    os.system('cls' if os.name == 'nt' else 'clear')

class APIKeyManager:
    """Gerencia a API_KEY: permite salvar, editar e excluir."""
    def __init__(self):
        self.api_key = self.load_api_key()
    def load_api_key(self):
        """Carrega a API_KEY se existir"""
        if os.path.exists("api_key.txt"):
            with open("api_key.txt", "r") as file:
                return file.read().strip()
        return None

    def save_api_key(self, key):
        """Salva a API_KEY"""
        with open("api_key.txt", "w") as file:
            file.write(key)
        self.api_key = key

    def edit_api_key(self):
        """Edita a API_KEY"""
        new_key = input("Digite a nova API_KEY: ")
        self.save_api_key(new_key)

    def delete_api_key(self):
        """Deleta a API_KEY"""
        if os.path.exists("api_key.txt"):
            os.remove("api_key.txt")
            self.api_key = None

class EmpresaBusca:
    """Realiza a busca de empresas com a API do Google Places."""
    def __init__(self, api_key):
        self.api_key = api_key

    def coodernadas(self, local):
        """Obtém as coordenadas da cidade."""
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": local, "key": self.api_key}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            resultados = response.json().get("results")
            if resultados:
                location = resultados[0].get("geometry").get("location")
                return location.get("lat"), location.get("lng")
        return None, None

    def buscar_empresas(self, lat, lng, keyword, radius=50000, limite_empresas=200):
        """Busca empresas por coordenadas."""
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": f"{lat},{lng}",
            "radius": radius,
            "keyword": keyword,
            "key": self.api_key
        }
        detalhes_empresas = []
        with tqdm(total=limite_empresas, desc="Buscando empresas") as pbar:
            while True:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    empresas = response.json().get("results", [])
                    for empresa in empresas:
                        detalhes_empresas.append(self.obter_detalhes_empresa(empresa["place_id"]))
                        pbar.update(1)
                        if len(detalhes_empresas) >= limite_empresas:
                            break
                    if len(detalhes_empresas) >= limite_empresas:
                        break
                    next_page_token = response.json().get("next_page_token")
                    if next_page_token:
                        params["pagetoken"] = next_page_token
                        time.sleep(3)
                    else:
                        break
                else:
                    return None
        return detalhes_empresas

    def obter_detalhes_empresa(self, place_id):
        """Obtém detalhes da empresa pelo place_id."""
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            "place_id": place_id,
            "fields": """name,
                        formatted_address,
                        opening_hours,
                        formatted_phone_number
                        ,website,place_id""",
            "key": self.api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            detalhes = response.json().get("result", {})
            horario_funcionamento = detalhes.get("opening_hours", {}).get("weekday_text", [])
            horario_funcionamento_str = "\n".join(horario_funcionamento)
            telefone = detalhes.get("formatted_phone_number", "Não disponível")
            site = detalhes.get("website", "Não disponível")
            url_google_maps = f"https://www.google.com/maps/search/?api=1&query={requests.utils.quote(detalhes.get('name'))}+{requests.utils.quote(detalhes.get('formatted_address'))}"
            return {
                "nome": detalhes.get("name"),
                "endereco": detalhes.get("formatted_address"),
                "horario_funcionamento": horario_funcionamento_str,
                "telefone": telefone,
                "site": site,
                "status": "Aberto"
                if detalhes.get("opening_hours", {}).get("open_now")
                else "Fechado",
                "url_google_maps": url_google_maps,
            }
        return {}

class EmpresaCLI:
    """Interface CLI principal com menu de opções"""
    def __init__(self):
        self.api_manager = APIKeyManager()
        self.calculadora = CustCalculator()

    def menu(self):
        while True:
            limpar_terminal()
            print("Bem Vindo ao Busca de Empresas")
            print("1 - Buscar Empresas.")
            print("2 - Calcular Créditos Restantes")
            print("3 - Configurações")
            print("4 - Sair")
            opcao = input("Escolha uma opção: ")
            if opcao == "1":
                self.buscar_empresas()
            elif opcao == "2":
                limpar_terminal()
                self.calculadora.calculator()
                input("Pressione Enter para voltar ao menu...")
            elif opcao == "3":
                self.configuracoes()
            elif opcao == "4":
                break
            else:
                print("Opção inválida. Tente novamente.")

    def buscar_empresas(self):
        limpar_terminal()
        if not self.api_manager.api_key:
            print("Nenhuma API_KEY Encontrada.")
            input("Pressione Enter para voltar ao menu...")
            return
        cidade = input("Digite um nome de cidade: ")
        radius = int(input("Digite o raio de busca (em metros : limite - 50.000m): "))
        keyword = input("Digite o termo de pesquisa: ")
        empresa_busca = EmpresaBusca(self.api_manager.api_key)
        lat, lng = empresa_busca.coodernadas(cidade)
        if lat and lng:
            empresas = empresa_busca.buscar_empresas(lat,
                                                     lng,
                                                     keyword,
                                                     radius=radius,
                                                     limite_empresas=200)
            if empresas:
                nome_arquivo = f"empresas_maps_{cidade}_{datetime.now().date()}.xlsx"
                self.salvar_planilha(empresas, nome_arquivo)
                print(f"Dados salvos em {nome_arquivo}")
                input("Pressione Enter para voltar ao menu...")

    def salvar_planilha(self, dados, nome_arquivo="empresas.xlsx"):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Empresas"
        headers = ["Nome",
                   "Endereço Completo",
                   "Horário de Funcionamento",
                   "Telefone", "Site", "Status",
                   "URL Google Maps"]
        sheet.append(headers)
        for empresa in dados:
            sheet.append([
                empresa["nome"],
                empresa["endereco"],
                empresa["horario_funcionamento"],
                empresa["telefone"],
                empresa["site"],
                empresa["status"],
                empresa["url_google_maps"]
            ])
        workbook.save(nome_arquivo)

    def configuracoes(self):
        limpar_terminal()
        print("Configurações")
        print("1 - Salvar nova API_KEY")
        print("2 - Exibir API_KEY")
        print("3 - Editar API_KEY existente")
        print("4 - Deletar API_KEY")
        print("5 - Voltar ao menu")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            nova_chave = input("Digite a nova API_KEY: ")
            self.api_manager.save_api_key(nova_chave)
            print("API_KEY salva com sucesso.")
            input("Pressione Enter para voltar ao menu...")
        elif opcao == "2":
            print(f"API_KEY: {self.api_manager.api_key}")
            input("Pressione Enter para voltar ao menu...")
        elif opcao == "3":
            self.api_manager.edit_api_key()
            print("API_KEY editada com sucesso.")
            input("Pressione Enter para voltar ao menu...")
        elif opcao == "4":
            self.api_manager.delete_api_key()
            print("API_KEY deletada com sucesso.")
            input("Pressione Enter para voltar ao menu...")
        elif opcao == "5":
            return
        else:
            print("Opção inválida. Tente novamente.")
            input("Pressione Enter para voltar ao menu...")

if __name__ == "__main__":
    cli = EmpresaCLI()
    cli.menu()
