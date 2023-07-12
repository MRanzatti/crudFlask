# O código abaixo é um exemplo básico de uma aplicação web em Flask que utiliza um banco de dados MySQL para armazenar
# informações. A comunicação entre o código e o banco de dados é feita através da biblioteca SQLAlchemy, que é integrada
# ao Flask e facilita a realização das operações de CRUD (Create, Read, Update, Delete).


# Quando vamos criar uma aplicação web em Flask identficamos que são necessarias algumas funções, como a
# render_template (função utilizada para renderizar templates em HTML)
# request (função utilizada para lidar com requisições HTTP ( POST e GET))
# url_for (função utilizada para construir URLs para rotas definidas em uma aplicação Flask)
# redirect (função utilizada para redirecionar o cliente para uma nova URL)

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# rota definida para uma comunicação da minha aplicação com meu banco de dados MYSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/db_webrota'
db = SQLAlchemy(app)


# criando a minha tabela no meu banco de dados local
class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    cep = db.Column(db.Integer)
    endereco = db.Column(db.String(100))
    numero = db.Column(db.Integer)
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(100))

    def __init__(self, nome, email, cep, endereco, numero, bairro, cidade, estado):
        self.nome = nome
        self.email = email
        self.cep = cep
        self.endereco = endereco
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado


# inicio do rotas
# 1° usei um decorador para indicar uma rota, para qual essa função será responsavel.
# 2° defini uma função para que quando a raiz for acessada, ela será executada.
# 3° usei a função importada no inicio do codigo para renderizar um templeate HTML.
# Nesse HTML temos a pagina principal mostrando dois caminhos, o de cadastrar o usuario e o de listar os usuarios
@app.route('/')
def index():
    return render_template("index.html")


# cadastrar usuarios
# 1° utilizada um decorador para indicar uma rota, para qual essa função será responsavel.
# 2° definida uma função para que quando a raiz for acessada, ela será executada.
# 3° utilizada a função importada no inicio do codigo para renderizar um templeate HTML.
# nessa etapa eu tenho dois espaços para inserir os dados
@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html")


# 1° rota definida para receber requisições do tipo POST.
# 2° a função cadastro tem como objetivo processar os dados informados nos campos do HTML
# 3° verifica se é um requisição do tipo POST, se for ele executara quando o dados for submetidos
# 4° verifica se os campos de nome e e-mail foram preenchidos, se sim, ele cria os valores dentro do banco
# 5° confirma a transação no banco.
@app.route("/cadastro", methods=['POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        cep = request.form.get("cep")
        endereco = request.form.get("endereco")
        numero = request.form.get("numero")
        bairro = request.form.get("bairro")
        cidade = request.form.get("cidade")
        estado = request.form.get("estado")

        if nome and email and cep and endereco and numero and bairro and cidade and estado:
            u = Usuarios(nome, email, cep, endereco, numero, bairro, cidade, estado)
            db.session.add(u)
            db.session.commit()

    return redirect(url_for("index"))


# Listagem dos usuarios
# 1° usei um decorador para indicar uma rota, para qual essa função será responsavel.
# 2° defini uma função para que quando a raiz for acessada, ela será executada.
# 3° usei a função importada no inicio do codigo para renderizar um templeate HTML.
# 4° a função irá fazer a listagem dos usuarios cadastrados no banco de dados.
@app.route("/lista")
def lista():
    usuarios = Usuarios.query.all()
    return render_template("lista.html", usuarios=usuarios)


# exclusão do usuario
# 1° usei um decorador para indicar uma rota, para qual essa função será responsavel.
# 2° defini uma função para que quando a raiz for acessada, ela será executada.
# 3° usei a função importada no inicio do codigo para renderizar um templeate HTML.
# 4° a função irá fazer a exlusão do usuario atraves do ID
@app.route("/excluir/<id>")
def excluir(id):
    usuario = Usuarios.query.filter_by(id=id).first()
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for("lista"))


# atualização do usuario
# 1° usei um decorador para indicar uma rota, para qual essa função será responsavel.
# 2° defini uma função para que quando a raiz for acessada, ela será executada.
# 3° usei a função importada no inicio do codigo para renderizar um templeate HTML.
# 4° a função irá fazer a atualização do usuario atraves do ID
@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    usuario = Usuarios.query.filter_by(id=id).first()
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        cep = request.form.get("cep")
        endereco = request.form.get("endereco")
        numero = request.form.get("numero")
        bairro = request.form.get("bairro")
        cidade = request.form.get("cidade")
        estado = request.form.get("estado")

        if nome and email and cep and endereco and numero:
            usuario.nome = nome
            usuario.email = email
            usuario.cep = cep
            usuario.endereco = endereco
            usuario.numero = numero
            usuario.bairro = bairro
            usuario.cidade = cidade
            usuario.estado = estado

            db.session.commit()

            return redirect(url_for("lista"))

    return render_template("atualizar.html", usuario=usuario)


# Defini uma rota
# Renderiza uma pagina HTML e exibe o mapa do google maps atraves da API do google maps
# A função initMap é a responsavel por inicializar o mapa.
@app.route('/mapa')
def mapa():
    pagina_inicio = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Google Maps - Positions</title>
        <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDaSayk4TVLTabK2Rf2TQZNtgRImGwW_lg"></script>
        <style>
            #map {
                height: 1000px;
                width: 100%;
            }
        </style>
    </head>
    <body>
    <div id="map"></div>
    <script>
        var map;

        function initMap() {
            map = new google.maps.Map(document.getElementById('map'), {
                center: {lat: -18.92295000, lng: -48.27078200}, // coordenada da posição 1, para centralizar
                zoom: 16
            });
        }

        initMap();'''

    # faz a leitura do Json disponibilizado e atribui a um obejto (meu_json)
    # carrega os dados dos json
    with open("positions.json", "r") as meu_json:
        dados = json.load(meu_json)

    # inicio um loop para pagar todos os dados do json e jogar em uma nova variavel
    # pego a quantidade de linhas no arquivo json
    # inicio um loop percorrendo os elementos da lista data
    # utiliza um contador para contar o numero de elementos, será utilizada posteriormente.
    for i in dados:
        data = dados['data']
        ultima_linha = 0
        for j in data:
            ultima_linha = ultima_linha + 1

        # criei 3 variaveis
        # pontos e lineCoordinates são iniciadas vazias
        # inicio outro loop para buscar os elementos de latitude e longitude em data
        pontos = ''
        lineCoordinates = ''
        linha = 1
        for j in data:
            latitude = j['latitude']
            longitude = j['longitude']

            # chamei a variavel pontos para que seja responsavel por adicionar marcadores no google maps
            pontos = pontos + '\nvar marker_' + str(
                linha) + ' = new google.maps.Marker({position: {lat: ' + latitude + ', lng: ' + longitude + '},map: map,title: \'Position ' + str(
                linha) + '\' });'

            # chamei a variavel lineCoordinates para que seja responavel pela sequencia das coordenadas
            lineCoordinates = lineCoordinates + '\nmarker_' + str(linha) + '.getPosition()'

            # aqui eu verifico se a linha é menor que a ultima linha, se for, ela vai fazer a sequencia das coordenadas analisando as coordenadas separando-as por uma virgula
            if linha <= ultima_linha - 1:
                lineCoordinates = lineCoordinates + ','

            # variavel de incremento para meus vetores
            linha = linha + 1

    # usando a variavel para armazenar as coordenadas dos marcadores
    lineCoordinates = '\n\nvar lineCoordinates = [' + lineCoordinates + '];'

    # concatena as variaveis pontos e lineCoordinates, essa concatenação será responsavel por exibir os marcadores no google maps
    coordenada = pontos + lineCoordinates

    pagina_final = '''
        \n\nvar polyline = new google.maps.Polyline({
                path: lineCoordinates,
                geodesic: true,
                strokeColor: '#0000ff', // Cor da linha (vermelho)
                strokeOpacity: 1.0,
                strokeWeight: 5
            });

            polyline.setMap(map);

        </script>
        </body>
        </html>'''

    # crio um arquivo HTML que irá exibir o mapa
    arquivo = pagina_inicio + coordenada + pagina_final

    # abro o arquivo
    arquivo_final = open("templates/mapa.html", "w", encoding="utf-8")
    arquivo_final.write(arquivo)

    return redirect(url_for("abrir_mapa"))


@app.route('/abrir_mapa')
def abrir_mapa():
    return render_template('mapa.html')


# acrescentei a função db.create_all para criar todas as tabelas definidas
with app.app_context():
    db.create_all()

# faz a aplicação Flask iniciar um servidor
if __name__ == '__main__':
    app.run(debug=True)
