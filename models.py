# models.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

# O '@dataclass' é um decorador que gera automaticamente métodos especiais
# como __init__(), __repr__(), etc. Isso torna a classe mais concisa e legível.
@dataclass
class Produto:
    """
    Representa o modelo de dados de um produto.
    Esta classe serve como um "molde" para todos os produtos que serão
    manipulados pelo sistema, garantindo que eles tenham uma estrutura consistente.
    """
    # Atributos do produto com tipos definidos para maior clareza e segurança.
    # 'Optional' indica que o valor pode ser o tipo definido ou 'None'.
    id: Optional[int] = None
    name: str = ""
    value: float = 0.0
    quantity: int = 0
    category: Optional[str] = None
    created_at: Optional[datetime] = None

    def validate(self):
        """
        Este método centraliza todas as regras de negócio para um produto.
        Ele verifica se os dados do objeto 'Produto' são válidos antes de
        serem enviados para o banco de dados. Se uma regra for violada,
        uma exceção 'ValueError' é lançada, impedindo a operação.
        """
        # --- Validação do Nome ---
        # Regra: O nome deve ser uma string e não pode ser vazio ou conter apenas espaços.
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("\nNome inválido: deve ser uma string não vazia.")
            
        # --- Validação do Valor ---
        # Regra: O valor deve ser um número e não pode ser negativo.
        try:
            # Tenta converter o valor para float, caso tenha vindo como string.
            val = float(self.value)
        except Exception:
            raise ValueError("\nValor inválido: deve ser numérico.")
        if val < 0:
            raise ValueError("\nValor inválido: deve ser maior ou igual a 0.")
            
        # --- Validação da Quantidade ---
        # Regra: A quantidade deve ser um número inteiro e não pode ser negativa.
        if not isinstance(self.quantity, int):
            try:
                # Tenta converter a quantidade para inteiro, caso tenha vindo de outra forma.
                q = int(self.quantity)
            except Exception:
                raise ValueError("\nQuantidade inválida: deve ser um número inteiro.")
            # Atualiza o valor no próprio objeto para garantir consistência.
            self.quantity = q
        if self.quantity < 0:
            raise ValueError("\nQuantidade inválida: deve ser maior ou igual a 0.")
            
        # --- Validação da Categoria ---
        # Regra: A categoria é opcional (pode ser None), mas se for fornecida,
        # deve ser uma string com no máximo 80 caracteres.
        if self.category is not None and (not isinstance(self.category, str) or len(self.category) > 80):
            raise ValueError("\nCategoria inválida: deve ser uma string com até 80 caracteres.")