import csv

def criar_toml_de_csv_corrigido(arquivo_csv_entrada, arquivo_toml_saida):
    """
    Converte um arquivo CSV estruturado para um arquivo TOML, lidando
    com codificação BOM e sendo mais flexível com a estrutura do arquivo.

    Argumentos:
        arquivo_csv_entrada (str): O caminho para o arquivo CSV de entrada.
        arquivo_toml_saida (str): O caminho para o arquivo TOML de saída.
    """
    try:
        # 1. Abre o arquivo com 'utf-8-sig' para remover o BOM automaticamente
        with open(arquivo_csv_entrada, mode='r', encoding='utf-8-sig') as arquivo_csv:
            leitor_csv = list(csv.reader(arquivo_csv))

            # 2. Processa as informações do sistema (primeiras 4 linhas)
            info_sistema = {linha[0]: linha[1] for linha in leitor_csv[:4]}

            conteudo_toml = f"""[system]
name = "{info_sistema.get('name', '')}"
version = "{info_sistema.get('version', '')}"
source = "{info_sistema.get('source', '')}"
description = "{info_sistema.get('description', '')}"

"""

            # 3. Encontra dinamicamente o cabeçalho dos dados (CODE,SUBJECT,...)
            indice_cabecalho = -1
            for i, linha in enumerate(leitor_csv):
                if linha and linha[0] == 'CODE':
                    indice_cabecalho = i
                    break
            
            if indice_cabecalho == -1:
                print("Erro: Cabeçalho 'CODE,SUBJECT,DESCRIPTION' não encontrado no arquivo CSV.")
                return

            # Mapeia os nomes das colunas para seus índices
            cabecalho_dados = {nome: i for i, nome in enumerate(leitor_csv[indice_cabecalho])}
            # Os dados começam na linha seguinte ao cabeçalho
            linhas_dados = leitor_csv[indice_cabecalho + 1:]

            # 4. Processa cada linha de dados
            for linha in linhas_dados:
                if not linha or not linha[0]:  # Pula linhas em branco
                    continue
                
                codigo = linha[cabecalho_dados['CODE']]
                assunto = linha[cabecalho_dados['SUBJECT']]
                descricao = linha[cabecalho_dados['DESCRIPTION']]

                # Constrói o nome da tabela TOML
                partes_codigo = codigo.split('-')
                if codigo == '0':
                    nome_tabela = 'Grupo0'
                else:
                    nome_tabela = f"Grupo0.{'.'.join(partes_codigo)}"

                # Monta a seção da tabela
                conteudo_toml += f"[{nome_tabela}]\n"
                conteudo_toml += f'code = "{codigo}"\n'
                if assunto:
                    conteudo_toml += f'subject = "{assunto}"\n'
                if descricao:
                    conteudo_toml += f'description = "{descricao}"\n'
                conteudo_toml += "\n"

        # 5. Escreve o resultado no arquivo de saída
        with open(arquivo_toml_saida, 'w', encoding='utf-8') as f:
            f.write(conteudo_toml)

        print(f"O arquivo '{arquivo_csv_entrada}' foi convertido com sucesso para '{arquivo_toml_saida}'.")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_csv_entrada}' não foi encontrado.")
    except IndexError:
        print("Erro: Ocorreu um problema ao ler a estrutura do arquivo CSV. Verifique se as linhas estão formatadas corretamente.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# --- Execução do Script ---
if __name__ == "__main__":
    arquivo_csv = 'nbr15965-classification.csv'
    arquivo_toml = 'nbr15965-classification.toml'

    criar_toml_de_csv_corrigido(arquivo_csv, arquivo_toml)
