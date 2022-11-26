from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    


    def get_relatorio_clientes(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["clientes"].find({}, 
                                                 {"cpf": 1, 
                                                  "nome": 1,
                                                  "endereco": 1,
                                                  "telefone": 1,
                                                  "_id": 0
                                                 }).sort("nome", ASCENDING)
        df_cliente = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_cliente)
        input("Pressione Enter para Sair do Relatório de Clientes")

    def get_relatorio_automoveis(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["automoveis"].find({}, 
                                                     {"placa": 1, 
                                                      "modelo": 1, 
                                                      "marca": 1,
                                                      "renavam": 1, 
                                                      "cor:":1,
                                                      "n_portas":1,
                                                      "tipo_combustivel":1,
                                                      "_id": 0
                                                     }).sort("placa", ASCENDING)
        df_automoveis = pd.DataFrame(list(query_result))
        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_automoveis)        
        input("Pressione Enter para Sair do Relatório de Automoveis")

    def get_relatorio_locacoes(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Recupera os dados transformando em um DataFrame
        query_result = mongo.db["locacoes"].aggregate([{
                                                        "$lookup": {
                                                            "from": "clientes", 
                                                            "localField": "cpf", 
                                                            "foreignField": "cpf", 
                                                            "as": "cliente"
                                                        }
                                                    }, 
                                                    {
                                                        "$unwind": {
                                                            "path": "$cliente"}
                                                       
                                                    },
                                                    {
                                                        "$lookup": {
                                                            "from": "automoveis", 
                                                            "localField": "placa", 
                                                            "foreignField": "placa", 
                                                            "as": "automovel"
                                                        }
                                                    }, {
                                                        "$unwind": {
                                                            "path": "$automovel"
                                                        }
                                                    }, 
                                                        
                                                    
                                                     {
                                                        "$project": {
                                                            "codigo_locacao": 1, 
                                                            "cliente": "$cliente.nome",
                                                            "placa": "$automovel.placa",
                                                            "cpf":"$cliente.cpf",
                                                            "data_locacao": 1,
                                                            "data_devolucao": 1, 
                                                            "_id": 0
                                                         }
                                                   }])
        df_locacao = pd.DataFrame(list(query_result))
        # Fecha a conexão com o Mongo
        mongo.close()
        print(df_locacao)
        input("Pressione Enter para Sair do Relatório de Locacao")
    
    