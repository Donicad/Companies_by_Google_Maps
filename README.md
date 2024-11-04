# Companies by Google Maps
Programa utilizando a API Place e Geo do Google Maps para realizar extração de informações de empresas.

# Requisitos

- Ter Python instalado em seu computador

    Faça o download da versão mais atual do Python para seu sistema operacional no site oficial da linguagem [python.org](https://www.python.org/downloads/).

- Ter o Git instalado em seu computador 

    Faça o download da versão mais atual do GIT para seu sistema operacional no site oficial do [Git](https://git-scm.com/downloads).

- Ter uma conta na Google e ativar as APIs Place e Geolocation.

  - Para ativar as APIs é necessário criar um projeto no [Google Cloud](https://console.cloud.google.com/welcome?), no menu lateral terá uma opção chamada "APIs e Serviços" depois basta pesquisas as APIs necessarias e depois ativa-las.
  - Assim que criar um projeto com as APIs será entregue uma API_KEY. Necessária para funcionamento do programa.  

# Instalação do programa.

- Primeiro é necessário realizar um clone do repositório ou baixar diretamente do GitHub como pacote ZIP.

- Para realizar o clone do repositório abra uma pasta em seu computador no qual deseja salvar os arquivos e acesse ela pelo CMD ou IDE de sua preferência utilizando o comando "CD" em seguida o caminho para sua pasta.

- Exemplo:
```
    cd caminho/para/a/pasta
```

- Após entrar na pasta rode o comando 

    "git clone https://github.com/Donicad/Companies_by_Google_Maps"
- E espere finalizar a clonagem do repositório.

- Caso tenha baixado o repositório em ZIP pelo próprio GitHub, basta extrair o conteúdo na pasta onde deseja salvar os arquivos.

---

Após ter os arquivos salvos em sua máquina, acesse a pasta principal do repositório utilizando: "cd Companies_by_Google_Maps"

Feito isso basta instalar as Libs necessárias para o funcionamento do código.
Para isso utilize o seguinte comando, uma vez dentro da pasta onde se encontra o código fonte.

```
    # Caso seu sistema operacional seja Linux, deverá utilizar "pip3" 

    pip install -r requirements.txt
```
Agora espere todas as dependências serem instaladas.

---

Após a instalação das dependências execute o código com o seguinte comando:

```
    # Caso seu sistema operacional seja Linux, deverá utilizar "python3"
    python contacts_maps.py
```

Com isso o programa será iniciado.

---

# Funcionamento do Programa.

- Quando for iniciado o script, um menu será exibido com opções de 1 a 4.

### Explicações das opções.
    
**OPÇÃO 01** - "Buscar Empresas”: essa é a principal opção, onde ao escolher ela primeiramente será verificada se existe uma API_KEY salva nas configurações, se caso houver, o programa vai pedir o nome de uma cidade, em seguida o raio de busca seguindo o centro da cidade que foi passada. Esse raio tem o limite de 50.000 metros.

**OPÇÃO 02** - "Calcular Créditos Restantes”: aqui é possível realizar um cálculo para saber com quantos créditos gratuitos para uso a conta ainda possui, pois a google disponibiliza R$ 200,00 de créditos para usar nas requisições.
    - Para cada requisição feita usando o Place, é cobrado 0.032 centavos e para a Geo apenas 0.005 centavos.

- No painel de [Metricas](https://console.cloud.google.com/google/maps-apis/metrics?). É possível verificar quantas solicitações para as APIs foram feitas.

Com essas informações ao iniciar a calculadora será pedido o número de solicitações da API place e depois da Geo. Por fim será calculado o valor gasto até o momento e o valor restante dos R$ 200,00.

**OPÇÃO 03** - "Configurações”: Essa opção é para salvar a API KEY obtida no google cloud. Dentro dessa opção temos: 
- 1 - Salvar API_KEY
- 2 - Exibir API_KEY
- 3 - Editar API_KEY
- 4 - Deletar API_KEY

Com sua KEY disponibilizada ao criar o projeto na google cloud será possível salvá-la em um arquivo .txt que será lida ao iniciar a OPÇÃO 01.

---

Esse programa tem o intuito apenas de facilitar a procura de empresas no Google Maps, use apenas os créditos gratuitos, caso o valor gratuito se esgote e você continuar ao usar a API um valor será cobrado da sua conta Google. Tenha cuidado.
