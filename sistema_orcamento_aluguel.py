"""
Sistema de Orçamento de Aluguel - Imobiliária R.M
Autor: [Seu Nome]
Descrição: Aplicação para gerar orçamentos de aluguel de imóveis
"""

import csv
from datetime import datetime
import os

class Imovel:
    """Classe base para todos os tipos de imóveis"""
    
    def __init__(self, tipo, quartos=1, vagas_garagem=0):
        self.tipo = tipo
        self.quartos = quartos
        self.vagas_garagem = vagas_garagem
        self.valor_base = self._definir_valor_base()
        self.valor_mensal = self.calcular_valor_mensal()
    
    def _definir_valor_base(self):
        """Define o valor base de acordo com o tipo de imóvel"""
        valores_base = {
            'Apartamento': 700.00,
            'Casa': 900.00,
            'Estudio': 1200.00
        }
        return valores_base.get(self.tipo, 0)
    
    def calcular_valor_mensal(self):
        """Calcula o valor mensal do aluguel com acréscimos"""
        valor = self.valor_base
        
        # Acréscimo para 2 quartos
        if self.quartos == 2:
            if self.tipo == 'Apartamento':
                valor += 200.00
            elif self.tipo == 'Casa':
                valor += 250.00
        
        # Acréscimo para vagas de garagem
        if self.vagas_garagem > 0:
            if self.tipo == 'Estudio':
                valor += 250.00  # Primeira vaga
                if self.vagas_garagem > 2:
                    valor += (self.vagas_garagem - 2) * 60.00
            else:
                valor += 300.00 * self.vagas_garagem
        
        return valor
    
    def aplicar_desconto(self, tem_criancas):
        """Aplica desconto de 5% para apartamentos sem crianças"""
        if self.tipo == 'Apartamento' and not tem_criancas:
            self.valor_mensal *= 0.95  # 5% de desconto
        return self.valor_mensal
    
    def __str__(self):
        return f"{self.tipo} - {self.quartos} quarto(s) - {self.vagas_garagem} vaga(s)"

class Contrato:
    """Classe para gerenciar o contrato de locação"""
    
    def __init__(self, imovel, tem_criancas=True):
        self.imovel = imovel
        self.tem_criancas = tem_criancas
        self.valor_contrato = 2000.00
        self.valor_mensal_final = imovel.aplicar_desconto(tem_criancas)
        self.parcelas_contrato = []
    
    def calcular_parcelas_contrato(self, num_parcelas):
        """Calcula as parcelas do contrato (máximo 5x)"""
        if num_parcelas > 5:
            num_parcelas = 5
        
        valor_parcela = self.valor_contrato / num_parcelas
        self.parcelas_contrato = [valor_parcela] * num_parcelas
        return self.parcelas_contrato
    
    def gerar_parcelas_mensais(self):
        """Gera as 12 parcelas mensais do orçamento"""
        parcelas_mensais = []
        for mes in range(1, 13):
            parcela = {
                'Mês': mes,
                'Valor': self.valor_mensal_final,
                'Data': datetime.now().strftime('%Y-%m-%d')
            }
            parcelas_mensais.append(parcela)
        return parcelas_mensais
    
    def salvar_csv(self, nome_arquivo='orcamento_parcelas.csv'):
        """Salva as 12 parcelas em um arquivo CSV"""
        parcelas = self.gerar_parcelas_mensais()
        
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
            campos = ['Mês', 'Valor', 'Data']
            escritor = csv.DictWriter(arquivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(parcelas)
        
        print(f"\nArquivo '{nome_arquivo}' gerado com sucesso!")
        return nome_arquivo

class Interface:
    """Classe para interface com o usuário"""
    
    @staticmethod
    def limpar_tela():
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def cabecalho():
        """Exibe o cabeçalho do sistema"""
        print("=" * 50)
        print("   SISTEMA DE ORÇAMENTO DE ALUGUEL - R.M IMOBILIÁRIA")
        print("=" * 50)
    
    @staticmethod
    def menu_principal():
        """Exibe o menu principal"""
        print("\n1 - Novo Orçamento")
        print("2 - Sair")
        return input("\nEscolha uma opção: ")
    
    @staticmethod
    def escolher_tipo_imovel():
        """Menu para escolha do tipo de imóvel"""
        print("\nTIPOS DE IMÓVEL:")
        print("1 - Apartamento (R$ 700,00 - 1 quarto)")
        print("2 - Casa (R$ 900,00 - 1 quarto)")
        print("3 - Estúdio (R$ 1200,00)")
        
        opcao = input("\nEscolha o tipo de imóvel (1-3): ")
        
        tipos = {
            '1': 'Apartamento',
            '2': 'Casa',
            '3': 'Estudio'
        }
        return tipos.get(opcao, 'Apartamento')
    
    @staticmethod
    def obter_quartos(tipo_imovel):
        """Obtém número de quartos (exceto para estúdio)"""
        if tipo_imovel == 'Estudio':
            return 1
        
        while True:
            try:
                quartos = int(input(f"Número de quartos (1 ou 2): "))
                if quartos in [1, 2]:
                    return quartos
                else:
                    print("Por favor, digite 1 ou 2")
            except ValueError:
                print("Digite um número válido!")
    
    @staticmethod
    def obter_vagas_garagem(tipo_imovel):
        """Obtém número de vagas de garagem"""
        while True:
            try:
                if tipo_imovel == 'Estudio':
                    print("\nVagas de estacionamento:")
                    print("- Primeira vaga: R$ 250,00")
                    print("- Vagas adicionais: R$ 60,00 cada")
                else:
                    print("\nVaga de garagem: R$ 300,00 cada")
                
                vagas = int(input("Número de vagas desejadas: "))
                if vagas >= 0:
                    return vagas
                else:
                    print("Digite um número positivo!")
            except ValueError:
                print("Digite um número válido!")
    
    @staticmethod
    def tem_criancas():
        """Pergunta se há crianças no imóvel"""
        resposta = input("\nHá crianças no imóvel? (s/n): ").lower()
        return resposta == 's'
    
    @staticmethod
    def exibir_resumo(imovel, contrato):
        """Exibe resumo do orçamento"""
        Interface.limpar_tela()
        Interface.cabecalho()
        
        print("\n" + "=" * 50)
        print("RESUMO DO ORÇAMENTO")
        print("=" * 50)
        
        print(f"\nTipo de Imóvel: {imovel.tipo}")
        print(f"Quantidade de Quartos: {imovel.quartos}")
        print(f"Vagas de Garagem: {imovel.vagas_garagem}")
        
        print(f"\nValor Base: R$ {imovel.valor_base:.2f}")
        
        # Mostra acréscimos
        if imovel.quartos == 2:
            acrescimo = 200.00 if imovel.tipo == 'Apartamento' else 250.00
            print(f"Acréscimo (2 quartos): + R$ {acrescimo:.2f}")
        
        if imovel.vagas_garagem > 0:
            if imovel.tipo == 'Estudio':
                valor_vagas = 250.00 + max(0, imovel.vagas_garagem - 2) * 60.00
                print(f"Acréscimo (vagas): + R$ {valor_vagas:.2f}")
            else:
                print(f"Acréscimo (vagas): + R$ {300.00 * imovel.vagas_garagem:.2f}")
        
        if imovel.tipo == 'Apartamento' and not contrato.tem_criancas:
            print(f"Desconto (sem crianças): - R$ {imovel.valor_mensal * 0.05:.2f}")
        
        print(f"\nVALOR MENSAL DO ALUGUEL: R$ {contrato.valor_mensal_final:.2f}")
        print(f"VALOR DO CONTRATO: R$ {contrato.valor_contrato:.2f}")
        
        # Opções de parcelamento
        print("\nOpções de parcelamento do contrato:")
        for i in range(1, 6):
            parcela = contrato.valor_contrato / i
            print(f"{i}x de R$ {parcela:.2f}")
        
        while True:
            try:
                parcelas = int(input("\nEm quantas vezes deseja parcelar o contrato (1-5)? "))
                if 1 <= parcelas <= 5:
                    break
                else:
                    print("Digite um número entre 1 e 5!")
            except ValueError:
                print("Digite um número válido!")
        
        parcelas_contrato = contrato.calcular_parcelas_contrato(parcelas)
        print(f"\nContrato parcelado em {parcelas}x de R$ {parcelas_contrato[0]:.2f}")
        
        # Pergunta se quer gerar CSV
        resposta = input("\nDeseja gerar arquivo CSV com as 12 parcelas mensais? (s/n): ").lower()
        if resposta == 's':
            contrato.salvar_csv()

def main():
    """Função principal do programa"""
    interface = Interface()
    
    while True:
        interface.limpar_tela()
        interface.cabecalho()
        
        opcao = interface.menu_principal()
        
        if opcao == '2':
            print("\nObrigado por usar o sistema!")
            break
        
        elif opcao == '1':
            # Coleta dados do imóvel
            tipo_imovel = interface.escolher_tipo_imovel()
            quartos = interface.obter_quartos(tipo_imovel)
            vagas = interface.obter_vagas_garagem(tipo_imovel)
            criancas = interface.tem_criancas()
            
            # Cria objetos
            imovel = Imovel(tipo_imovel, quartos, vagas)
            contrato = Contrato(imovel, not criancas)  # not criancas = sem crianças
            
            # Exibe resumo
            interface.exibir_resumo(imovel, contrato)
            
            input("\nPressione Enter para continuar...")
        
        else:
            print("\nOpção inválida!")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()