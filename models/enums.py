import enum


class CategoriaHabilidade(str, enum.Enum):
    LINGUAGENS_PROGRAMACAO = "Linguagens de Programação"
    FRAMEWORKS_BIBLIOTECAS = "Frameworks & Bibliotecas"
    BANCO_DE_DADOS = "Banco de Dados"
    NUVEM_DEVOPS = "Nuvem & DevOps"
    SEGURANCA_INFORMACAO = "Segurança da Informação"
    REDES_INFRAESTRUTURA = "Redes & Infraestrutura"
    ANALISE_DADOS_BI = "Análise de Dados & BI"
    DESIGN_CRIATIVIDADE = "Design & Criatividade"
    MARKETING_VENDAS = "Marketing & Vendas"
    GESTAO_LIDERANCA = "Gestão & Liderança"
    FINANCAS_CONTABILIDADE = "Finanças & Contabilidade"
    ATENDIMENTO_CLIENTE = "Atendimento ao Cliente"
    METODOLOGIAS_PROCESSOS = "Metodologias & Processos"
    FERRAMENTAS_ESCRITORIO = "Ferramentas de Escritório"
    HABILIDADES_INTERPESSOAIS = "Habilidades Interpessoais"
    SAUDE_CUIDADOS = "Saúde & Cuidados"
    EDUCACAO_ENSINO = "Educação & Ensino"
    JURIDICO_COMPLIANCE = "Jurídico & Compliance"
    OUTRAS = "Outras"


class Situacao(str, enum.Enum):
    CONCLUIDO = "Concluído"
    EM_ANDAMENTO = "Em andamento"
    TRANCADO = "Trancado"
    INCOMPLETO = "Incompleto"
