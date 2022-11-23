from typing_extensions import Self
from datetime import date
from model.clientes import Clientes
from model.automoveis import Automoveis

class Locacoes:
    def __init__(self,codigo_locacao:int=None, cliente:Clientes=None, automoveis:Automoveis=None, data_locacao:str=None,data_devolucao:str=None):
        self.set_codigo_locacao(codigo_locacao)
        self.set_data_devolucao(data_devolucao)
        self.set_cliente(cliente)
        self.set_automoveis(automoveis)
        self.set_data_locacao(data_locacao)

    def set_codigo_locacao(self,codigo_locacao:int):
        self.codigo_locacao = codigo_locacao
        

    def set_data_devolucao(self,data_devolucao:str):
        self.data_devolucao=data_devolucao
    
    def set_cliente(self, cliente:Clientes):
        self.cliente = cliente

    def set_automoveis(self, automoveis:Automoveis):
        self.cliente = automoveis

    
    def set_Placa(self,Placa:str):
        self.Placa = Placa
    
    def set_nome_modelo(self,nome_modelo:str):
        self.nome_modelo = nome_modelo
    
    def set_nome_marca(self,nome_marca:str):
        self.nome_modelo = nome_marca
    
    def set_data_locacao(self,data_locacao:str):
        self.data_locacao = data_locacao

    def get_codigo_locacao(self) -> int:
        return self.codigo_locacao


    def get_data_devolucao(self) -> date:
        return self.data_devolucao

    def get_cliente(self) -> Clientes:
        return self.cliente
    
    def get_automoveis(self) -> Automoveis:
        return self.automoveis
    
    def get_nome_modelo(self) -> str:
        return self.nome_modelo
    
    def get_nome_marca(self) -> str:
        return self.nome_marca
    
    def get_data_locacao(self) -> date:
        return self.data_locacao

    def to_string(self) -> str:
        return f"Data de devolução: {self.get_data_devolucao()} | CPF: {self.get_cliente().get_cpf()} | Placa: {self.get_automoveis().get_Placa()} | Nome do modelo: {self.get_nome_modelo()} | Nome da marca {self.get_nome_marca()} | Devolução: {self.get_data_devolucao()}" 