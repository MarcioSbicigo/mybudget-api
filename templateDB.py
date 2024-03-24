import datetime
from pymongo import MongoClient
import pandas as pd
import os

# mongodb://localhost:27017/ ou mongodb://mongodb:27017/
# Linux: export MONGO_URI='mongodb://localhost:27017/myBudget'
# Windows: $Env:MONGO_URI = "mongodb://localhost:27017/myBudget"
class MyBudgetDatabase:
    
    def __init__(self, mongo_url=os.environ.get('MONGO_URI'), database_name='myBudget'):
        self.mongo_url = mongo_url
        self.database_name = database_name
        self.client = MongoClient(self.mongo_url)
        self.db = self.client[self.database_name]

    # Função que insere logs no MongoDb
    # Recebe uma string e o nome da collection como parâmetro
    def insert_log(self, event, collection):
        app_log = self.db[collection]
        datetime_log = datetime.datetime.now()
        log = {'Evento': event, 'timestamp': datetime_log}
        app_log.insert_one(log)

    # Função que carrega as categorias do MongoDB
    # Recebe o nome da collection como parâmetro
    def load_categories(self, collection):
        categories_data = list(self.db[collection].find({}, {'_id': 0, 'nome': 1}))
        categories_df = pd.DataFrame(categories_data)
        return categories_df
    
    # Função que insere novas categorias no MongoDB    
    # Recebe o nome da collection e a categoria como parâmetro
    def insert_category(self, collection, category):
        try:
            self.db[collection].insert_one({'nome': category})
                
            if collection == 'categorias_receita':
                self.insert_log(f'Categoria de receita "{category}" inserida.', 'log_operacoes')
            elif collection == 'categorias_despesa':
                self.insert_log(f'Categoria de despesa "{category}" inserida.', 'log_operacoes')
                
        except Exception as error:
            print(f'ERRO: {error}')
            self.insert_log(str(error), 'log_errors')
    
    # Função que remove categorias existentes no MongoDB
    # Recebe o nome da collection e a categoria como parâmetro
    def remove_category(self, collection, category):
        try:
            self.db[collection].delete_one({'nome': category})
            
            if collection == 'categorias_receita':
                self.insert_log(f'Categoria de receita "{category}" removida.', 'log_operacoes')
            elif collection == 'categorias_despesa':
                self.insert_log(f'Categoria de despesa "{category}" removida.', 'log_operacoes')

        except Exception as error:
            print(f'ERRO: {error}')
            self.insert_log(str(error), 'log_errors')
    
    # Função que carrega os dados de receitas/despesas do MongoDB
    # Recebe o nome da collection como parâmetro
    def load_data(self, collection):
        data = None
        if collection in self.db.list_collection_names():
            cursor = self.db[collection].find({}, {'_id': 0})
            data = pd.DataFrame(list(cursor))
            if 'Data' in data.columns:
                data['Data'] = pd.to_datetime(data['Data'])
                data['Data'] = data['Data'].dt.date
                
                data = data[data['Descrição'] != '*transacao-inicial*']
            
            self.insert_log(f'Dados de {collection} carregados.', 'log_aplicacao')
        return data
    
    # Função que insere dados de receitas/despesas no MongoDB
    # Recebe o nome da collection e as informações do registro como parâmetro
    def insert_data(self, collection, valor, recebido, fixo, date, categoria, descricao):
        dados = {
            'Valor': valor, 
            'Recebido': recebido, 
            'Fixo': fixo, 
            'Data': date,
            'Categoria': categoria, 
            'Descrição': descricao
        }
        
        try:
            self.db[collection].insert_one(dados)
            
            if collection=='receitas':
                self.insert_log(f'Nova receita inserida.', 'log_operacoes')
            elif collection=='despesas':
                self.insert_log(f'Nova despesa inserida.', 'log_operacoes')
                
        except Exception as error:
            print(f'ERRO: {error}')
            self.insert_log(str(error), 'log_errors')

    # Função que cria as collections de categorias de receitas/despesas
    # Recebe o nome da collection como parâmetro
    def init_categories(self, collection, categories):
        list_categories = categories
        
        # Criando a collection de categorias de receita ou despesa
        try:
            if self.db[collection].count_documents({}) == 0:
                
                for categoria in list_categories:
                    # Verificando se a categoria já existe na coleção
                    if self.db[collection].count_documents({'nome': categoria}) == 0:
                        cat = {
                            'nome': categoria
                            }
                        self.db[collection].insert_one(cat)
                        
                        self.insert_log(f'Collection {collection} criada.', 'log_aplicacao')
                        
                print(f'Collection {collection} criada.\n')               
        except Exception as error:
            self.insert_log(f'Erro ao criar a collection {collection}: {error}', 'log_errors')
            print(f'Erro ao criar a collection {collection}: {error}')
    
    # Função que cria as collections de receitas/despesas
    # Recebe o nome da collection como parâmetro
    def init_receitas_despesas(self, collection):
        
        try:
            # Criando DataFrames vazios
            data_structure = {'Valor': [0], 'Recebido': [1], 'Fixo': [0], 'Data': [datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')], 'Categoria': [''], 'Descrição': ['*transacao-inicial*']}
                    
            df_receitas_despesas = pd.DataFrame(data_structure)
                    
            # Salvando o DataFrame de despesas no MongoDB
            self.db[collection].insert_many(df_receitas_despesas.to_dict('records'))
                    
            self.insert_log(f'Collection {collection} criada.', 'log_aplicacao')
            print(f'Collection {collection} criada.\n')
                
        except Exception as error:
            self.insert_log(f'Erro ao criar collection de {collection}: {error}', 'log_errors')
            print(f'Erro ao criar collection de {collection}: {error}')
    
    # def active_session(self, session_id, username):      
    #     try:
    #         if 'AllUsers' in self.db.list_collection_names():
    #             user = self.db['AllUsers'].find_one({'username': username})
                
    #             if user and 'session_id' in user:
    #                 print(f"Session ID parametro: {session_id}\n")
    #                 print(f"\nSession ID função: {user.get("session_id")}\n")
                    
    #                 return True if session_id == user.get("session_id") else False
    def active_session(self, user_info):      
        try:
            if 'AllUsers' in self.db.list_collection_names():
                if 'username' in user_info:
                    user = self.db['AllUsers'].find_one({'username': user_info['username']})
                    
                    if user and ('session_id' in user):
                        print(f"Session ID parametro: {user_info.get('session_id')}\n")
                        print(f"Session ID retornado do mongo para a função: {user.get('session_id')}\n")
                        
                        return True if user_info.get('session_id') == user.get('session_id') else False
                else:
                    print("O usuário não foi encontrado no banco de dados")
                    return False               
        except Exception as error:
            self.insert_log(f'Erro ao verificar o session_id de {user_info.get('username')}: {error}', 'log_errors')
            print(f'Erro ao verificar o session_id de {user_info.get('username')}: {error}')
            
                 
my_budget_db = MyBudgetDatabase()

# Criando collections no MongoDB
if my_budget_db.db['receitas'].count_documents({}) == 0:
    my_budget_db.init_receitas_despesas('receitas')
    
if my_budget_db.db['despesas'].count_documents({}) == 0:
    my_budget_db.init_receitas_despesas('despesas')

if my_budget_db.db['categorias_receita'].count_documents({}) == 0:
    lista_categorias_receitas = ["Salário", "Rendimentos", "Vendas", "Cashback"]
    my_budget_db.init_categories('categorias_receita', lista_categorias_receitas)
    
if my_budget_db.db['categorias_despesa'].count_documents({}) == 0:
    lista_categorias_despesas = ["Alimentação", "Aluguel", "Água", "Luz", "Combustível", "Saúde", "Lazer"]
    my_budget_db.init_categories('categorias_despesa', lista_categorias_despesas)