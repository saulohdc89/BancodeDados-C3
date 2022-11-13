import pandas as pd
from model.automoveis import Automoveis
from conexion.mongo_queries import MongoQueries
from reports.relatorios import Relatorio




class Controller_Item_Pedido:
    def __init__(self):
      
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()
        
        def inserir_automovel(self) -> Automoveis:
        
            self.mongo.connect()
        
        nova_Placa = input("Placa (Novo): ")

        if self.verifica_existencia_automoveis(nova_Placa):
            renavam =  input("RENAVAM: ")
            nova_cor = input("Cor:")
            N_portas = input("Numero de portas:")
            tipo_combustivel = input("Tipo de combustivel")
            nova_marca = input("Marca:")
            novo_modelo = input("Modelo:")
            self.mongo.db["automoveis"].insert_one({"placa": nova_Placa, "renavam": renavam,"n_portas":N_portas,"tipo_combustivel":tipo_combustivel,"marca":nova_marca, "modelo" : novo_modelo})
            df_automoveis = self.recupera_automoveis(nova_Placa)
            novo_automoveis = Automoveis(df_automoveis.placa.values[0],df_automoveis.renavam.values[0], df_automoveis.n_portas.values[0], df_automoveis.tipo_combustivel.values[0] ,df_automoveis.nova_marca.values[0],df_automoveis.novo_modelo.values[0])
            print(novo_automoveis.to_string())
            self.mongo.close()
            return novo_automoveis
        else:
            self.mongo.close()
            print(f"A Placa {nova_Placa} já está cadastrada.")
            return None
                


            data = dict(Placa = nova_Placa,r_nome_modelo = novo_modelo,nome_marca = nova_marca,RENAVAM = renavam,cor =nova_cor,n_portas=N_portas, combustivel = tipo_combustivel )



        # Recupera os dados do novo produto criado transformando em um DataFrame
        # Cria um novo objeto Produto
        # Exibe os atributos do novo produto
        print(novo_automoveis.to_string())
        # Retorna o objeto novo_produto para utilização posterior, caso necessário
        return novo_automoveis

    def atualizar_automoveis(self) -> Automoveis:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do item de pedido a ser alterado
        placa = input("Placa : ")

        # Verifica se o item de pedido existe na base de dados
        if not self.verifica_existencia_automoveis(placa):
            renavam =  input("RENAVAM: ")
            nova_cor = input("Cor:")
            N_portas = input("Numero de portas:")
            tipo_combustivel = input("Tipo de combustivel")
            nova_marca = input("Marca:")
            novo_modelo = input("Modelo:")
            self.mongo.db["automoveis"].update_one({"placa": f"{placa}"}, {"$set": {"renavam": renavam,"n_portas":N_portas,"tipo_combustivel":tipo_combustivel,"marca":nova_marca, "modelo" : novo_modelo}})
            df_automoveis = self.recupera_automoveis(placa)
            automoveis_atualizado = Automoveis(df_automoveis.placa.values[0],df_automoveis.renavam.values[0], df_automoveis.n_portas.values[0], df_automoveis.tipo_combustivel.values[0] ,df_automoveis.nova_marca.values[0],df_automoveis.novo_modelo.values[0])
            print(automoveis_atualizado.to_string())
            
            self.mongo.close()
            return automoveis_atualizado
        else:
            self.mongo.close()
            print(f"A Placa {placa} não existe.")
            return None
    

    def excluir_automoveis(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        # Solicita ao usuário o código do item de pedido a ser alterado
        placa = input("Placa : ")       

        # Verifica se o item de pedido existe na base de dados
        if not self.verifica_existencia_automoveis(placa):            
            # Recupera os dados do novo item de pedido criado transformando em um DataFrame
            df_automoveis = self.recupera_automoveis(placa)
            self.mongo.db["automoveis"].delete_one({"Placa":f"{placa}"})
            automovel_excluido  = Automoveis(df_automoveis.placa.values[0],df_automoveis.renavam.values[0], df_automoveis.n_portas.values[0], df_automoveis.tipo_combustivel.values[0] ,df_automoveis.nova_marca.values[0],df_automoveis.novo_modelo.values[0])
            self.mongo.close()
            print("Automovel Removido com Sucesso!")
            print(automovel_excluido.to_string())
        else:
            self.mongo.close()
            print(f"A Placa {placa} não existe.")

    def verifica_existencia_automoveis(self, Placa:str=None, external:bool=False) -> bool:
       if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()
        
            df_automoveis= pd.DataFrame(self.mongo.db["automoveis"].find({"placa":f"{Placa}"}, {"placa": 1, "renavam": 1,"cor":1,"n_portas":1,"nome_modelo":1,"nome_marca":1,"tipo_combustivel":1, "_id": 0}))

            if external:
            # Fecha a conexão com o Mongo
                self.mongo.close()

            return df_automoveis.empty

    def recupera_automoveis(self, Placa:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_automoveis = pd.DataFrame(list(self.mongo.db["automoveis"].find({"placa":f"{Placa}"}, {"placa": 1, "renavam": 1,"cor":1,"n_portas":1,"nome_modelo":1,"nome_marca":1,"tipo_combustivel":1, "_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_automoveis

    