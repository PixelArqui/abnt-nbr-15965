import csv
import json

def convert_nbr_to_json(csv_filepath, json_filepath):
    tree = []
    nodes_map = {}
    metadata = {}
    
    # 1. Leitura com detecção automática do delimitador (vírgula ou ponto-e-vírgula)
    with open(csv_filepath, 'r', encoding='utf-8') as f:
        sample = f.read(1024)
        f.seek(0)
        try:
            # O Sniffer descobre automaticamente o formato do seu CSV
            delimiter = csv.Sniffer().sniff(sample, delimiters=';,').delimiter
        except csv.Error:
            delimiter = ';' # Fallback de segurança
            
        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)
        
    data_start = 0
    
    # 2. Processar metadados e encontrar onde a tabela começa
    for i, row in enumerate(rows):
        if not row: 
            continue
        # Identifica a linha de cabeçalho
        if row[0].strip().upper() == "CODE" or (len(row) > 1 and row[1].strip().upper() == "SUBJECT"):
            data_start = i + 1
            break
        elif len(row) >= 2 and row[0].strip():
            metadata[row[0].strip()] = row[1].strip()

    # 3. Processar dados da tabela mantendo a hierarquia
    for row in rows[data_start:]:
        if not row or not row[0].strip():
            continue
            
        code = row[0].strip()
        subject = row[1].strip() if len(row) > 1 else ""
        description = row[2].strip() if len(row) > 2 else ""
        
        # Identifica se o código original usa traço (-) ou ponto (.)
        separator = '-' if '-' in code else '.'
        parts = code.split(separator)
        
        # Remove os '00' do final
        active_parts = list(parts)
        while len(active_parts) > 1 and active_parts[-1] == '00':
            active_parts.pop()
            
        # Reconstrói o código limpo (ex: "0M")
        clean_code = separator.join(active_parts)
            
        node = {
            "code": clean_code,
            "subject": subject,
            "description": description,
            "children": []
        }
        
        path_tuple = tuple(active_parts)
        nodes_map[path_tuple] = node
        
        # Conecta pais e filhos
        if len(active_parts) == 1:
            tree.append(node)
        else:
            parent_tuple = tuple(active_parts[:-1])
            if parent_tuple in nodes_map:
                nodes_map[parent_tuple]['children'].append(node)
            else:
                tree.append(node)

    # 4. Montar e Salvar o JSON
    final_output = {
        "metadata": metadata,
        "classification": tree
    }

    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
        
    print(f"Sucesso! Arquivo lido com o separador '{delimiter}' e salvo em '{json_filepath}'.")

if __name__ == "__main__":
    convert_nbr_to_json("nbr15965-classification.csv", "nbr15965-classification.json")