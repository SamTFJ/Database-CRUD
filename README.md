### Primeiro, crie a pasta virtual .venv

```
python3 -m venv .venv
```

### Em seguida, ative a .venv

```
source .venv/bin/activate 
```

### Depois, instale os requisitos do projeto

```
.venv/bin/python3 -m pip install -r requirements.txt
```

### Por fim, para rodar

```
.venv/bin/python3 -m dbconnection
```

### Dependências adicionais (se ainda não estiverem instaladas)

Este projeto requer `psycopg2` (ou `psycopg2-binary`) e `python-dotenv` para se comunicar com o PostgreSQL e carregar variáveis de ambiente a partir de um arquivo `.env`. Caso essas bibliotecas não estejam presentes no seu ambiente ou no `requirements.txt`, instale-as manualmente:

```bash
# Instalar psycopg2-binary (recomendado para desenvolvimento) e python-dotenv
.venv/bin/python3 -m pip install psycopg2-binary python-dotenv
```

> Nota: Em alguns sistemas pode ser preferível usar `psycopg2` (não binário) em produção. Se a instalação de `psycopg2` falhar, certifique-se de que as bibliotecas e headers do cliente PostgreSQL estejam instalados (ex.: `libpq-dev` no Debian/Ubuntu).

### Como executar a aplicação (recomendado)

Após instalar as dependências e ativar o ambiente virtual, rode o ponto de entrada principal da aplicação:

```bash
.venv/bin/python3 main.py
```

(Se ainda precisar rodar o módulo diretamente para testes, pode usar o comando mostrado anteriormente. O ponto de entrada recomendado para a aplicação é `main.py`.)
