import sqlite3

class Aluno:
    def __init__(self, aluno_id, nome):
        self.aluno_id = aluno_id
        self.nome = nome

    def registrar_frequencia(self):
        cursor.execute('INSERT INTO Frequencias (aluno_id) VALUES (?)', (self.aluno_id,))
        conn.commit()

    def registrar_nota(self, nota):
        cursor.execute('INSERT INTO Notas (aluno_id, nota) VALUES (?, ?)', (self.aluno_id, nota))
        conn.commit()

    def calcular_media(self):
        cursor.execute('SELECT nota FROM Notas WHERE aluno_id = ?', (self.aluno_id,))
        notas = cursor.fetchall()
        if notas:
            return sum(nota[0] for nota in notas) / len(notas)
        else:
            return 0

    def excluir_aluno(self):
        cursor.execute('DELETE FROM Alunos WHERE id = ?', (self.aluno_id,))
        cursor.execute('DELETE FROM Frequencias WHERE aluno_id = ?', (self.aluno_id,))
        cursor.execute('DELETE FROM Notas WHERE aluno_id = ?', (self.aluno_id,))
        conn.commit()
        print(f"Aluno {self.nome} excluído com sucesso!")

def criar_tabelas():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Frequencias (
            aluno_id INTEGER,
            FOREIGN KEY (aluno_id) REFERENCES Alunos(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Notas (
            aluno_id INTEGER,
            nota REAL,
            FOREIGN KEY (aluno_id) REFERENCES Alunos(id)
        )
    ''')

    conn.commit()

def adicionar_aluno(nome):
    cursor.execute('INSERT INTO Alunos (nome) VALUES (?)', (nome,))
    conn.commit()
    print(f"Aluno {nome} adicionado com sucesso!")

def encontrar_aluno(nome):
    cursor.execute('SELECT id, nome FROM Alunos WHERE nome = ?', (nome,))
    aluno = cursor.fetchone()
    if aluno:
        return Aluno(aluno[0], aluno[1])
    else:
        return None

def excluir_aluno():
    nome = input("Digite o nome do aluno que deseja excluir: ")
    aluno = encontrar_aluno(nome)
    if aluno:
        aluno.excluir_aluno()
    else:
        print("Aluno não encontrado.")

def menu():
    while True:
        print("\nSistema de Controle Escolar")
        print("1 - Adicionar Aluno")
        print("2 - Registrar Frequência")
        print("3 - Registrar Nota")
        print("4 - Calcular Média")
        print("5 - Excluir Aluno")
        print("6 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Digite o nome do aluno: ")
            adicionar_aluno(nome)
        elif opcao == "2":
            nome = input("Digite o nome do aluno: ")
            aluno = encontrar_aluno(nome)
            if aluno:
                aluno.registrar_frequencia()
                print(f"Frequência registrada para o aluno {nome}.")
            else:
                print("Aluno não encontrado.")
        elif opcao == "3":
            nome = input("Digite o nome do aluno: ")
            aluno = encontrar_aluno(nome)
            if aluno:
                nota = float(input("Digite a nota do aluno: "))
                aluno.registrar_nota(nota)
                print(f"Nota registrada para o aluno {nome}.")
            else:
                print("Aluno não encontrado.")
        elif opcao == "4":
            nome = input("Digite o nome do aluno: ")
            aluno = encontrar_aluno(nome)
            if aluno:
                media = aluno.calcular_media()
                print(f"A média de {nome} é: {media:.2f}")
            else:
                print("Aluno não encontrado.")
        elif opcao == "5":
            excluir_aluno()
        elif opcao == "6":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('escola.db')
cursor = conn.cursor()

criar_tabelas()
menu()

# Fechar a conexão com o banco de dados ao sair do programa
conn.close()
