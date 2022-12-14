from bson import ObjectId
import pandas as pd
from model.locacoes import Locacoes
from conexion.mongo_queries import MongoQueries
from reports.relatorios import Relatorio
from model.clientes import Clientes
from model.automoveis import Automoveis
from controller.controller_cliente import Controller_Cliente
from controller.controller_automoveis import Controller_Automoveis
from datetime import datetime,date,timedelta
class Controller_Locacoes:
    def __init__(self):
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        self.ctrl_cliente = Controller_Cliente()
        self.ctrl_automoveis = Controller_Automoveis()
        
    def inserir_locacoes(self) -> Locacoes:
        # Cria uma nova conexão com o banco
        self.mongo.connect()

        codigo = str(input("Codigo de locacao"))
        if self.verifica_existencia_locacao(codigo):
            self.relatorio.get_relatorio_clientes()
            n_cpf = str(input("Digite o número do CPF do Cliente: "))
            cliente = self.valida_cliente(n_cpf)
            if cliente == None:
                return None

            self.relatorio.get_relatorio_automoveis()
            n_placa = str(input("Digite a placa do Automovel: "))
            automovel = self.valida_automovel(n_placa)
            if automovel == None:
                return None
        
        

        
            ddata_locacao = datetime.today().strftime("%m-%d-%Y")
            dias = int(input("Digite os dias de locacao: "))
            d_devolucao =  datetime.today() + timedelta(days=dias)
            ddata_devolucao = d_devolucao.strftime("%m-%d-%Y")
        #proxima_locacao = self.mongo.db["locacoes"].aggregate([
        #                                           {
         #                                               '$group': {
          #                                                  '_id': '$locacoes', 
           #                                                 'proxima_locacao': {
            #                                                    '$max': '$codigo_locacao'
             #                                               }
              #                                          }
               #                                     }, {
                #                                        '$project': {
                 #                                           'proxima_locacao': {
                  #                                              '$sum': [
                   #                                                 '$proxima_locacao', 1
                    #                                            ]
                     #                                       }, 
                      #                                      '_id': 0
                       #                                 }
                        ##                            }
                          #                      ])

        #proxima_locacao = int(list(proxima_locacao)[0]['proxima_locacao'])
            data = dict(codigo_locacao = codigo,cpf = cliente.get_cpf(),placa = automovel.get_Placa(),data_locacao = ddata_locacao,data_devolucao = ddata_devolucao )
        
        # Insere e Recupera o código do novo produto
            id_locacao = self.mongo.db["locacoes"].insert_one(data)
        # Recupera os dados do novo produto criado transformando em um DataFrame
            df_locacoes = self.recupera_locacao(id_locacao.inserted_id)
        # Cria um novo objeto Produto
            nova_locacao = Locacoes(df_locacoes.codigo_locacao.values[0], cliente, automovel,df_locacoes.data_locacao.values[0],df_locacoes.data_devolucao.values[0])
        # Exibe os atributos do novo produto
            print(nova_locacao.to_string())
            self.mongo.close()
        # Retorna o objeto novo_produto para utilização posterior, caso necessário
            return nova_locacao
        else: 
            self.mongo.close()
            print(f"O codigo {codigo} já existe.")
            return None

    def atualizar_locacao(self) -> Automoveis:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do produto a ser alterado
        codigo_locacao = str(input("Código da Locaçao que irá alterar: "))


        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_locacao(codigo_locacao):
            
            self.relatorio.get_relatorio_clientes()
            ncpf = str(input("Digite o número do CPF do Cliente: "))
            cliente = self.valida_cliente(ncpf)
            if cliente == None:
                return None
            self.relatorio.get_relatorio_automoveis()
            nplaca = str(input("Digite a placa do Automovel: "))
            automovel = self.valida_automovel(nplaca)
            if automovel == None:
                return None
            
            
            # Solicita a nova descrição do produto
            locacao= datetime.today().strftime("%m-%d-%Y")
            dias = int(input("Digite os dias de locacao: "))
            d_devolucao =  datetime.today() + timedelta(days=dias)
            dd_devolucao = d_devolucao.strftime("%m-%d-%Y")

            
            data = dict(codigo_locacao = codigo_locacao,cpf = cliente.get_cpf(),placa = automovel.get_Placa(),data_locacao = locacao,data_devolucao = dd_devolucao )

            # Atualiza a descrição do produto existente
            self.mongo.db["locacoes"].update_one(data)
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_locacoes = self.recupera_locacao_codigo(codigo_locacao)
            # Cria um novo objeto Produto
            locacoes_atualizado = Locacoes(df_locacoes.codigo_locacao.values[0], cliente, automovel,df_locacoes.data_locacao.values[0],df_locacoes.data_devolucao.values[0])
            # Exibe os atributos do novo produto
            print(locacoes_atualizado.to_string())
            self.mongo.close()
            # Retorna o objeto produto_atualizado para utilização posterior, caso necessário
            return locacoes_atualizado
        else:
            self.mongo.close()
            print(f"O código {codigo_locacao} não existe na base.")
            return None

    def excluir_locacao(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do produto a ser alterado
        codigo_locacao = str(input("Código da Locacao que irá excluir: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_locacao(codigo_locacao):            
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_locacoes = self.recupera_locacao_codigo(codigo_locacao)
            cliente  = self.valida_cliente(df_locacoes.cpf.values[0])
            automovel = self.valida_automovel(df_locacoes.placa.values[0])
            # Revome o produto da tabela
            self.mongo.db["locacoes"].delete_one({"codigo_locacao":f"{codigo_locacao}"})
            # Cria um novo objeto Produto para informar que foi removido
            locacao_excluido = Locacoes(df_locacoes.codigo_locacao.values[0], cliente, automovel,df_locacoes.data_locacao.values[0],df_locacoes.data_devolucao.values[0])
            # Exibe os atributos do produto excluído
            print("Locacao Removida com Sucesso!")
            print(locacao_excluido.to_string())
            self.mongo.close()
        else:
            self.mongo.close()
            print(f"O código {codigo_locacao} não existe.")

    def verifica_existencia_locacao(self, codigo:str=None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_locacao = pd.DataFrame(self.mongo.db["locacoes"].find({"codigo_locacao":codigo}, {"codigo_locacao": 1,"cpf":1 ,"placa": 1,"data_locacao":1,"data_devolucao":1,"_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_locacao.empty

    def recupera_locacao(self, _id:ObjectId=None) -> pd.DataFrame:
        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_produto = pd.DataFrame(list(self.mongo.db["locacoes"].find({"_id":_id}, {"codigo_locacao": 1,"cpf":1 ,"placa": 1,"data_locacao":1,"data_devolucao":1,"_id": 0})))
        return df_produto

    def recupera_locacao_codigo(self, codigo:str=None, external: bool = False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_produto = pd.DataFrame(list(self.mongo.db["locacoes"].find({"codigo_locacao":codigo}, {"codigo_locacao": 1,"cpf":1 ,"placa": 1,"data_locacao":1,"data_devolucao":1,"_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_produto


    def valida_cliente(self, cpf:str=None) -> Clientes:
        if self.ctrl_cliente.verifica_existencia_cliente(cpf=cpf, external=True):
            print(f"O CPF {cpf} informado não existe na base.")
            return None
        else:
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_cliente = self.ctrl_cliente.recupera_cliente(cpf=cpf, external=True)
            # Cria um novo objeto cliente
            cliente = Clientes(df_cliente.cpf.values[0], df_cliente.nome.values[0],df_cliente.endereco.values[0],df_cliente.telefone.values[0])
            return cliente

    def valida_automovel(self, placa:str=None) -> Automoveis:
        if self.ctrl_automoveis.verifica_existencia_automoveis(placa=placa, external=True):
            print(f"A Placa {placa} informada não existe na base.")
            return None
        else:
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_automoveis = self.ctrl_automoveis.recupera_automoveis(placa, external=True)
            # Cria um novo objeto cliente
            automoveis = Automoveis(df_automoveis.placa.values[0],df_automoveis.modelo.values[0],df_automoveis.marca.values[0],df_automoveis.renavam.values[0],df_automoveis.cor.values[0] ,df_automoveis.n_portas.values[0], df_automoveis.tipo_combustivel.values[0])
            return automoveis