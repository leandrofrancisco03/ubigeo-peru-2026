import pandas as pd
import re
import os
import json
import yaml

# ==========================================
# FASE 0: FUNCIONES DE LIMPIEZA Y PREPARACIÓN
# ==========================================
def limpiar_texto(texto):
    if pd.isna(texto):
        return texto
    
    # 1. Convertir a string y a mayúsculas
    texto = str(texto).upper()
    
    # 2. Eliminar espacios al inicio y al final
    texto = texto.strip()
    
    # 3. Eliminar espacios dobles o triples entre palabras
    texto = re.sub(r'\s+', ' ', texto)
    
    # 4. Quitar tildes de las vocales (Mantenemos la Ñ intacta)
    reemplazos = {'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}
    for acentuada, sin_acento in reemplazos.items():
        texto = texto.replace(acentuada, sin_acento)
        
    return texto

def crear_estructura_directorios():
    carpetas = ['csv', 'json', 'php_arrays', 'sql', 'xml', 'yaml']
    for carpeta in carpetas:
        os.makedirs(carpeta, exist_ok=True)
    print("Directorios creados/verificados correctamente.")

# ==========================================
# FUNCIONES DE EXPORTACIÓN POR FORMATO
# ==========================================
def exportar_csv(df, filename):
    df.to_csv(f'csv/{filename}.csv', index=False, encoding='utf-8-sig')

def exportar_json(df, filename):
    with open(f'json/{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(df.to_dict(orient='records'), f, ensure_ascii=False, indent=4)

def exportar_yaml(df, filename):
    with open(f'yaml/{filename}.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(df.to_dict(orient='records'), f, allow_unicode=True, sort_keys=False)

def exportar_php(df, variable_name, filename):
    with open(f'php_arrays/{filename}.php', 'w', encoding='utf-8') as f:
        f.write("<?php\n")
        f.write(f"${variable_name} = [\n")
        for row in df.to_dict(orient='records'):
            f.write("    [\n")
            for k, v in row.items():
                val = str(v).replace("'", "\\'")
                f.write(f"        '{k}' => '{val}',\n")
            f.write("    ],\n")
        f.write("];\n")

def exportar_sql(df, table_name, filename):
    with open(f'sql/{filename}.sql', 'w', encoding='utf-8') as f:
        # Se asume que la estructura de la tabla ya existe, insertamos los datos en bloque
        columnas = ", ".join([f"`{col}`" for col in df.columns])
        f.write(f"INSERT INTO `{table_name}` ({columnas}) VALUES\n")
        
        filas = []
        for row in df.itertuples(index=False):
            valores = ", ".join([f"'{str(v).replace(chr(39), chr(39)+chr(39))}'" for v in row])
            filas.append(f"({valores})")
            
        f.write(",\n".join(filas) + ";\n")

def exportar_xml(df, root_node, item_node, filename):
    with open(f'xml/{filename}.xml', 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(f"<{root_node}>\n")
        for row in df.to_dict(orient='records'):
            f.write(f"    <{item_node}>\n")
            for k, v in row.items():
                # Escapar caracteres especiales para XML si es necesario
                val = str(v).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                f.write(f"        <{k}>{val}</{k}>\n")
            f.write(f"    </{item_node}>\n")
        f.write(f"</{root_node}>\n")

# ==========================================
# LECTURA Y PROCESAMIENTO DE DATOS
# ==========================================
print("Iniciando proceso...")
crear_estructura_directorios()

print("Leyendo archivo original...")
# Leemos el Excel tal como lo tienes ahora (los títulos ya están en la fila 1)
df_master = pd.read_excel('3908763-directorio-nacional-de-municipalidades-provinciales-y-distritales-mayo-2026 (1).xlsx', dtype={'Ubigeo': str})
df_master.columns = df_master.columns.str.strip()

# SALVAVIDAS: Eliminamos cualquier fila vacía o fantasma que no tenga Ubigeo
df_master.dropna(subset=['Ubigeo'], inplace=True)
df_master = df_master[df_master['Ubigeo'].str.strip() != '']

# Aseguramos que el Ubigeo tenga siempre 6 dígitos (rellenando con ceros si hiciera falta)
df_master['Ubigeo'] = df_master['Ubigeo'].str.zfill(6)

print("Aplicando limpieza de datos...")
columnas_clave = ['Departamento', 'Provincia', 'Distrito']
for col in columnas_clave:
    if col in df_master.columns:
        df_master[col] = df_master[col].apply(limpiar_texto)

# ==========================================
# FASE 1: DEPARTAMENTOS (Primeros 2 dígitos)
# ==========================================
print("Estructurando Departamentos...")
df_dept = df_master[['Ubigeo', 'Departamento']].copy()
df_dept['id'] = df_dept['Ubigeo'].str[:2]
df_dept = df_dept[['id', 'Departamento']].drop_duplicates().sort_values('id').reset_index(drop=True)
df_dept.rename(columns={'Departamento': 'name'}, inplace=True)

# ==========================================
# FASE 2: PROVINCIAS (Primeros 4 dígitos)
# ==========================================
print("Estructurando Provincias...")
df_prov = df_master[['Ubigeo', 'Provincia']].copy()
df_prov['id'] = df_prov['Ubigeo'].str[:4]
df_prov['name'] = df_prov['Provincia']
df_prov['department_id'] = df_prov['Ubigeo'].str[:2]
df_prov = df_prov[['id', 'name', 'department_id']].drop_duplicates().sort_values('id').reset_index(drop=True)

# ==========================================
# FASE 3: DISTRITOS (6 dígitos)
# ==========================================
print("Estructurando Distritos...")
df_dist = df_master[['Ubigeo', 'Distrito']].copy()
df_dist['id'] = df_dist['Ubigeo']
df_dist['name'] = df_dist['Distrito']
df_dist['province_id'] = df_dist['Ubigeo'].str[:4]
df_dist['department_id'] = df_dist['Ubigeo'].str[:2]
df_dist = df_dist[['id', 'name', 'province_id', 'department_id']].drop_duplicates().sort_values('id').reset_index(drop=True)

# ==========================================
# FASE 4: EXPORTACIÓN MASIVA A FORMATOS
# ==========================================
print("Generando archivos de exportación en múltiples formatos...")

año_export = "2026"
archivos = [
    (df_dept, f'ubigeo_peru_{año_export}_departamentos', 'departments', 'departamentos', 'departamento'),
    (df_prov, f'ubigeo_peru_{año_export}_provincias', 'provinces', 'provincias', 'provincia'),
    (df_dist, f'ubigeo_peru_{año_export}_distritos', 'districts', 'distritos', 'distrito')
]

for df, filename, english_table, xml_root, xml_item in archivos:
    # 1. CSV
    exportar_csv(df, filename)
    # 2. JSON
    exportar_json(df, filename)
    # 3. YAML
    exportar_yaml(df, filename)
    # 4. PHP Arrays
    exportar_php(df, english_table, filename) 
    # 5. SQL 
    exportar_sql(df, english_table, filename)
    # 6. XML
    exportar_xml(df, xml_root, xml_item, filename)

print("¡Listo! Todo el contenido ha sido procesado y distribuido en las carpetas correspondientes.")