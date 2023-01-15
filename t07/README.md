# T08 - IMPLEMENTAÇÃO DE JUNÇÃO

Implementar, na linguagem de sua preferência, um dos algoritmos de junção descritos em anexo, manipulando dados armazenados em disco rígido. A implementação pode ser feita em grupos de até cinco alunos e apenas um aluno do grupo deve anexar na entrega os arquivos com o código fonte implementado e os arquivos de índice criados. Um relatório com a documentação dos algoritmos e das estruturas de dados deve ser entregue, de forma individual por todos os alunos do grupo, em pdf, nesta plataforma, citando todos os colegas do grupo, destacando o colega que fez a entrega dos códigos fontes implementados pelo grupo.

---

# IMPLEMENTAÇÃO DE UM ALGORITMO DE JUNÇÃO

SEJAM:

- TABELA 1: ALUNO

  - SEQ_ALUNO INT(4)
  - CODIGO_CURSO CHAR(3)
  - NOME_ALUNO CHAR(33)

- TABELA 2: CURSO
  - SEQ_CURSO SERIAL ou INT(4)
  - CODIGO_CURSO CHAR(3)
  - NOME_CURSO CHAR(17)

PEDE-SE:

ESCOLHER UM DOS ALGORITMOS ABAIXO PARA
IMPLEMENTAR A JUNÇAO_NATURAL(ALUNO, CURSO):

- JUNÇÃO BASEADA EM SORT MERGE

- JUNÇÃO BASEADA EM BLOCOS

- JUNÇÃO BASEADA EM HASH JOIN

OBS:

- Considere M e N como o número de páginas das Tabelas 1 e 2,
  respectivamente, e B o número de slots da bufferpool.

- M, N e B devem ser parâmetros para execução do código,
  considerando M > N > B.

---

Entregar:

- Programa fonte (3 pontos)
- Descrição dos algoritmos e estruturas de dados (3 pontos)

---
