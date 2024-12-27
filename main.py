import sys
import mysql.connector
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon

class BuscaPrecoApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Configurações de estilo
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 5px;
                font-size: 14px;
            }
        """)

        # Ícone do app
        self.setWindowIcon(QIcon('icones/price-tag.ico'))
        
        # Configurações da janela
        self.setWindowTitle('Busca de Preço')
        self.setGeometry(100, 100, 600, 400)
        
        # Inicializar interface e banco de dados
        self.iniciar_interface()
        self.conectar_banco_dados()

    def iniciar_interface(self):
        # Layout principal
        layout_principal = QVBoxLayout()
        
        # Título
        titulo = QLabel('Sistema de Busca de Preços')
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont('Arial', 18, QFont.Bold))
        layout_principal.addWidget(titulo)
        
        # Campo de entrada
        input_layout = QHBoxLayout()
        self.input_cod_barras = QLineEdit()
        self.input_cod_barras.setPlaceholderText('📱 Digite ou bipe o código de barras')
        self.input_cod_barras.returnPressed.connect(self.buscar_produto)
        input_layout.addWidget(self.input_cod_barras)
        
        layout_principal.addLayout(input_layout)
        
        # Frame para resultados
        self.frame_resultado = QFrame()
        self.frame_resultado.setVisible(False)
        layout_resultado = QVBoxLayout()
        
        # Labels para nome do produto e preço
        self.label_produto = QLabel()
        self.label_produto.setAlignment(Qt.AlignCenter)
        self.label_produto.setFont(QFont('Arial', 24, QFont.Bold))
        
        self.label_preco = QLabel()
        self.label_preco.setAlignment(Qt.AlignCenter)
        self.label_preco.setFont(QFont('Arial', 20))
        
        layout_resultado.addWidget(self.label_produto)
        layout_resultado.addWidget(self.label_preco)
        
        self.frame_resultado.setLayout(layout_resultado)
        layout_principal.addWidget(self.frame_resultado)
        
        self.setLayout(layout_principal)

    def conectar_banco_dados(self):
        try:
            self.conexao = mysql.connector.connect(
                host='localhost',
                user='user_busca_preco',
                database='busca_preco'
            )
        except mysql.connector.Error as erro:
            QMessageBox.critical(self, 'Erro de Conexão', 
                                 f'Não foi possível conectar ao banco de dados:\n{erro}')
            sys.exit(1)

    def buscar_produto(self):
        cod_barras = self.input_cod_barras.text()
        
        try:
            cursor = self.conexao.cursor(dictionary=True)
            consulta = "SELECT nome_produto, preco FROM produtos_agregados WHERE cod_barras = %s"
            cursor.execute(consulta, (cod_barras,))
            
            resultado = cursor.fetchone()
            
            if resultado:
                # Atualizar labels
                self.label_produto.setText(resultado['nome_produto'])
                self.label_preco.setText(f'R$ {resultado["preco"]:.2f}')
                
                # Mostrar frame de resultado
                self.frame_resultado.setVisible(True)
                
                # Limpar após 5 segundos
                QTimer.singleShot(5000, self.limpar_resultado)
            else:
                # Mostrar imagem de produto não encontrado na label
                self.label_produto.setText('Produto não encontrado. Verifique no Balcão')
                self.label_preco.setText('')
                self.frame_resultado.setVisible(True)
                

                # Fechar mensagem automaticamente após 5 segundos
                QTimer.singleShot(5000, self.limpar_resultado)
            
            self.input_cod_barras.clear()
            
        except mysql.connector.Error as erro:
            QMessageBox.critical(self, 'Erro de Busca', 
                                 f'Ocorreu um erro durante a busca:\n{erro}')
        finally:
            cursor.close()

    def limpar_resultado(self):
        # Limpar labels e esconder frame
        self.label_produto.clear()
        self.label_preco.clear()
        self.frame_resultado.setVisible(False)

def main():
    app = QApplication(sys.argv)
    janela = BuscaPrecoApp()
    janela.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
