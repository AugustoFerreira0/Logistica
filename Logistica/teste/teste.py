import sqlite3

class SistemaLogistica:
    def __init__(self, nome_banco="logistica.db"):
        self.nome_banco = nome_banco
        self.inicializar_banco()

    def inicializar_banco(self):
        # Remover a tabela se ela existir
        with sqlite3.connect(self.nome_banco) as conexao:
            cursor = conexao.cursor()
            conexao.commit()

            # Criar a tabela de produtos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT UNIQUE,
                    quantidade INTEGER,
                    remetente TEXT,
                    destinatario TEXT,
                    endereco TEXT,
                    cep INTEGER
                )
            ''')
            conexao.commit()

    def adicionar_produto(self, nome, quantidade, remetente, destinatario, endereco, cep):
        # Adiciona um produto ao estoque com informações adicionais
        with sqlite3.connect(self.nome_banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO produtos (nome, quantidade, remetente, destinatario, endereco, cep)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, quantidade, remetente, destinatario, endereco, cep))
            conexao.commit()

    def verificar_estoque(self, nome_produto):
        # Verifica a quantidade de um produto no estoque
        with sqlite3.connect(self.nome_banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                SELECT quantidade FROM produtos WHERE nome = ?
            ''', (nome_produto,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else 0

    def remover_produto_por_id(self, produto_id):
        # Verifica se o produto com o ID fornecido existe antes de removê-lo
        if self.verificar_produto_por_id(produto_id):
            with sqlite3.connect(self.nome_banco) as conexao:
                cursor = conexao.cursor()
                cursor.execute('''
                    DELETE FROM produtos WHERE id = ?
                ''', (produto_id,))
                conexao.commit()
                print(f"Produto com ID {produto_id} removido do estoque.")
        else:
            print(f"Produto com ID {produto_id} não encontrado no estoque.")

    def verificar_produto_por_id(self, produto_id):
        # Verifica se o produto com o ID fornecido existe no estoque
        with sqlite3.connect(self.nome_banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                SELECT id FROM produtos WHERE id = ?
            ''', (produto_id,))
            resultado = cursor.fetchone()
            return resultado is not None

    def listar_produtos(self):
        # Lista todos os produtos no estoque
        with sqlite3.connect(self.nome_banco) as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                SELECT * FROM produtos
            ''')
            produtos = cursor.fetchall()
            if produtos:
                print("Produtos no estoque:")
                for produto in produtos:
                    print(f"ID: {produto[0]}, Nome: {produto[1]}, Quantidade: {produto[2]}, Remetente: {produto[3]}, Destinatário: {produto[4]}, Endereço: {produto[5]}, CEP: {produto[6]}")
            else:
                print("Nenhum produto encontrado no estoque.")

    def adicionar_produto_interativo(self):
        # Permite que o usuário insira um novo produto com informações adicionais
        nome = input("Digite o nome do produto: ")
        quantidade = self.obter_quantidade_valida()
        remetente = input("Digite o nome do remetente: ")
        destinatario = input("Digite o nome do destinatário: ")
        endereco = input("Digite o endereço: ")
        cep = self.obter_cep_valido()

        self.adicionar_produto(nome, quantidade, remetente, destinatario, endereco, cep)
        print(f"{quantidade} unidades de {nome} adicionadas ao estoque.")

    def obter_cep_valido(self):
        # Valida e obtém um CEP contendo apenas números
        while True:
            cep = input("Digite o CEP (apenas números): ")
            if cep.isdigit():
                return cep
            else:
                print("Por favor, insira um CEP válido contendo apenas números.")

    def remover_produto_por_id_interativo(self):
        # Permite que o usuário remova um produto pelo ID
        produto_id = int(input("Digite o ID do produto que deseja remover: "))
        self.remover_produto_por_id(produto_id)

    def listar_produtos_interativo(self):
        # Lista todos os produtos no estoque
        self.listar_produtos()

    def obter_quantidade_valida(self):
        # Valida e obtém uma quantidade válida do usuário
        while True:
            try:
                quantidade = int(input("Digite a quantidade: "))
                if quantidade >= 0:
                    return quantidade
                else:
                    print("Por favor, insira uma quantidade não negativa.")
            except ValueError:
                print("Por favor, insira um número válido.")

    def fechar_conexao(self):
        # Não é necessário, pois o uso de "with" já fecha automaticamente a conexão
        pass

# Exemplo de uso
sistema = SistemaLogistica()

while True:
    print("\nEscolha uma opção:")
    print("1. Adicionar produto")
    print("2. Listar produtos")
    print("3. Remover produto por ID")
    print("4. Sair")

    escolha = input("Digite o número da opção desejada: ")

    if escolha == '1':
        sistema.adicionar_produto_interativo()
    elif escolha == '2':
        sistema.listar_produtos_interativo()
    elif escolha == '3':
        sistema.remover_produto_por_id_interativo()
    elif escolha == '4':
        print("Saindo do programa. Até logo!")
        break
    else:
        print("Opção inválida. Tente novamente.")
