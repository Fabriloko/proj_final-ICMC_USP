import pandas as pd
import requests as rq
from io import StringIO

import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression as LR

class Modelo():
    def __init__(self, type):
        """
        Importante definir o tipo de modelo utilizado.
        Atualmente a seguinte lista é permitida para execução:
        ['SVC', 'LR']
        SVC - Suport Vector Clasification 
        LR = Linear Regression
        """
        self.model
        self.type = type #Tipo de Modelo
        pass

    def CarregarDataset(self, path):
        """
        Carrega o conjunto de dados a partir de um arquivo CSV.

        Parâmetros:
        - path (str): Caminho para o arquivo CSV contendo o dataset.
        
        O dataset é carregado com as seguintes colunas: SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm e Species.
        """
        raw_url = f"https://raw.githubusercontent.com/Fabriloko/proj_final-ICMC_USP/refs/heads/main/proj_final-ICMC_USP/{path}"
        self.columns = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species']

        response = rq.get(raw_url)

        if response.status_code == 200:
            data = StringIO(response.text)
            self.df = pd.read_csv(data, names= self.columns)
        else:
            print(f"Error: Unable to fetch file (HTTP {response.status_code})")
            None

    def TratamentoDeDados(self):
        """
        Realiza o pré-processamento dos dados carregados.

        Sugestões para o tratamento dos dados:
            * Utilize `self.df.head()` para visualizar as primeiras linhas e entender a estrutura.
            * Verifique a presença de valores ausentes e faça o tratamento adequado.
            * Considere remover colunas ou linhas que não são úteis para o treinamento do modelo.
        
        Dicas adicionais:
            * Explore gráficos e visualizações para obter insights sobre a distribuição dos dados.
            * Certifique-se de que os dados estão limpos e prontos para serem usados no treinamento do modelo.
        """
        print('Verificação de valores faltantes:\n')
        for col in self.columns:
            print(f'Número de missing na coluna {col}: {self.df[col].isnull().sum()}')
        
        print(f'\nDetalhamento dos dados:\n{self.df.describe()}\n')

        count = self.df.value_counts(['Species'])
        print(f'Contagem dos Dados:\n{count}\n')

        for specie in self.df['Species'].unique():
            heatmap = self.df[self.df['Species'] == specie].copy()
            heatmap = heatmap.drop(['Species'], axis= 1)
            heatmap = heatmap.corr()

            fig, axs = plt.subplots(figsize= (8, 6), layout= "tight")
            fig.suptitle(f'Heatmap {specie}')
            fig.subplots_adjust(left= 0.2, wspace= 0.6)

            im = axs.imshow(heatmap, vmin= -1, vmax= 1, cmap= 'coolwarm')

            axs.set_xticks(np.arange(len(heatmap.columns)), labels= heatmap.columns)
            axs.set_yticks(np.arange(len(heatmap.columns)), labels= heatmap.columns)

            plt.setp(axs.get_xticklabels(), rotation= 45, ha= "right", rotation_mode= "anchor")

            heatmap = heatmap.rename(columns={"SepalLengthCm": 0, "SepalWidthCm": 1, "PetalLengthCm": 2, "PetalWidthCm": 3})

            for i in heatmap:
                for j in heatmap:
                    text = axs.text(j, i, round(heatmap[i][j], 2), ha= "center", va= "center", color= "black")

            plt.show()

        pass

    def Treinamento(self):
        """
        Treina o modelo de machine learning.

        Detalhes:
            * Utilize a função `train_test_split` para dividir os dados em treinamento e teste.
            * Escolha o modelo de machine learning que queira usar. Lembrando que não precisa ser SMV e Regressão linear.
            * Experimente técnicas de validação cruzada (cross-validation) para melhorar a acurácia final.
        
        Nota: Esta função deve ser ajustada conforme o modelo escolhido.
        """ 
        X = self.df.copy()
        X.drop('Species', axis= 1)

        y = self.df['Species'].copy()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, shuffle= True, stratify= y)

        if self.type == 'LR':
            self.model = LR.fit(X_train, y_train)
        elif self.type == 'SVC':
            self.model = SVC.fit(X_train, y_train)
        else:
            print('!!! Nenhum tipo de modelo valido foi escolhido !!! \n Tente novamente :)')

        pass

    def Teste(self):
        """
        Avalia o desempenho do modelo treinado nos dados de teste.

        Esta função deve ser implementada para testar o modelo e calcular métricas de avaliação relevantes, 
        como acurácia, precisão, ou outras métricas apropriadas ao tipo de problema.
        """
        pass

    def Train(self):
        """
        Função principal para o fluxo de treinamento do modelo.

        Este método encapsula as etapas de carregamento de dados, pré-processamento e treinamento do modelo.
        Sua tarefa é garantir que os métodos `CarregarDataset`, `TratamentoDeDados` e `Treinamento` estejam implementados corretamente.
        
        Notas:
            * O dataset padrão é "iris.data", mas o caminho pode ser ajustado.
            * Caso esteja executando fora do Colab e enfrente problemas com o path, use a biblioteca `os` para gerenciar caminhos de arquivos.
        """
        self.CarregarDataset("iris.data")  # Carrega o dataset especificado.

        # Tratamento de dados opcional, pode ser comentado se não for necessário
        self.TratamentoDeDados()

        self.Treinamento()  # Executa o treinamento do modelo

# Lembre-se de instanciar as classes após definir suas funcionalidades
# Recomenda-se criar ao menos dois modelos (e.g., Regressão Linear e SVM) para comparar o desempenho.
# A biblioteca já importa LinearRegression e SVC, mas outras escolhas de modelo são permitidas.

model = Modelo('LR')

model.CarregarDataset("iris.data")

# model.TratamentoDeDados()

model.Treinamento()