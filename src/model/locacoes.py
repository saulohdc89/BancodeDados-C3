from typing_extensions import Self
from datetime import date
from model.clientes import Clientes
from model.automoveis import Automoveis

class Locacoes:
    def __init__(self,codigo_locacao:str=None, cliente:Clientes=None, automoveis:Automoveis=None, data_locacao:str=None,data_devolucao:str=None):
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
        self.automoveis = automoveis

    
    def set_Placa(self,Placa:str):
        self.Placa = Placa
    
   
    
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
    
   
    
    def get_data_locacao(self) -> date:
        return self.data_locacao

    def to_string(self) -> str:
        return f"Data de devolução: {self.get_data_devolucao()} | CPF: {self.get_cliente().get_cpf()} | Placa: {self.get_automoveis().get_Placa()} | Locacao: {self.get_data_locacao()} | Devolução: {self.get_data_devolucao()}" 