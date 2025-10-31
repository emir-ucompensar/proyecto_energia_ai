"""
config.py
=========
Archivo de configuración centralizado para todos los scripts de análisis gráfico.
Permite modificar parámetros sin alterar la lógica de los scripts.

Autor: Emir Alejandro Chía
Fecha: Octubre 2025
"""

import numpy as np
import pandas as pd

# =============================================================================
# CONFIGURACIÓN DE DATOS EXPERIMENTALES
# =============================================================================

# Datos de modelos LLM evaluados localmente
MODELOS = {
    'nombres': ['Phi-3 Mini', 'LLaMA-3 8B', 'Mistral-7B', 'Gemma-2B', 'TinyLLaMA'],
    'nombres_cortos': ['Phi-3', 'LLaMA-3', 'Mistral', 'Gemma', 'TinyLLaMA'],
    'parametros': [3.8, 8.0, 7.0, 2.0, 1.1],  # Billones de parámetros
    'tokens_por_seg': [23.4, 17.1, 19.8, 31.2, 38.9],  # tokens/s
    'latencia': [0.42, 0.68, 0.59, 0.37, 0.31],  # segundos
    'potencia_gpu': [96, 110, 104, 88, 82],  # Watts
    'ram_usada': [14.2, 16.8, 15.9, 12.3, 10.8],  # GiB
    'vram_usada': [4.9, 5.6, 5.3, 4.1, 3.8],  # GiB
    'energia_total': [14.8, 18.3, 16.9, 13.2, 11.7],  # Wh (10 min test)
}

# Calcular eficiencia (tokens/Wh)
MODELOS['eficiencia'] = [
    (MODELOS['tokens_por_seg'][i] * 600) / MODELOS['energia_total'][i]
    for i in range(len(MODELOS['nombres']))
]

# =============================================================================
# CONFIGURACIÓN DE SIMULACIÓN DE POTENCIA EN EL TIEMPO
# =============================================================================

# Duración de la simulación (segundos)
DURACION_SIMULACION = 600  # 10 minutos

# Número de puntos de muestreo
NUM_PUNTOS = 600  # 1 punto por segundo

# Parámetros para perfiles de potencia dinámicos
PERFIL_CONFIG = {
    'warmup_time': 30,  # Tiempo de calentamiento en segundos
    'variacion_max': 0.10,  # Variación máxima ±10% de la potencia nominal
    'frecuencia_oscilacion': 0.05,  # Frecuencia de oscilación (Hz)
}

# =============================================================================
# CONFIGURACIÓN DE MÉTODOS NUMÉRICOS
# =============================================================================

# Número de subintervalos para integración numérica
N_INTERVALOS = [10, 20, 50, 100, 200, 500, 1000]

# Límites de integración para ejemplos
A_LIMITE_INFERIOR = 0
B_LIMITE_SUPERIOR = 10

# =============================================================================
# CONFIGURACIÓN DE AJUSTE DE CURVAS (REGRESIÓN)
# =============================================================================

# Grado máximo de polinomio para ajuste
GRADO_POLINOMIO_MAX = 5

# Tipos de funciones para probar en el ajuste
TIPOS_AJUSTE = ['polinomial', 'exponencial', 'potencial', 'logaritmica']

# Umbral de R² mínimo aceptable
R2_MINIMO = 0.80

# =============================================================================
# CONFIGURACIÓN DE VISUALIZACIÓN
# =============================================================================

# Tamaño de figuras (pulgadas)
TAMANO_FIGURA = (12, 8)
TAMANO_FIGURA_GRANDE = (14, 10)

# DPI para guardar imágenes
DPI = 300

# Colores personalizados (paleta profesional)
COLORES = {
    'principal': '#2E86AB',      # Azul
    'secundario': '#A23B72',     # Magenta
    'terciario': '#F18F01',      # Naranja
    'cuaternario': '#C73E1D',    # Rojo
    'quinario': '#6A994E',       # Verde
    'trapecio': '#3A86FF',       # Azul claro
    'simpson': '#FB5607',        # Naranja brillante
    'analitico': '#06A77D',      # Verde agua
    'pareto': '#D62828',         # Rojo brillante
}

# Estilo de gráficos
ESTILO_GRAFICOS = 'seaborn-v0_8-darkgrid'  # Estilo matplotlib

# Formato de exportación de figuras
FORMATOS_EXPORTACION = ['png', 'pdf']  # Guardar en ambos formatos

# =============================================================================
# CONFIGURACIÓN DE RUTAS
# =============================================================================

# Directorios de salida organizados
DIR_BASE = '../figuras/'
DIR_PNG = '../figuras/png/'
DIR_PDF = '../figuras/pdf/'
DIR_RESULTADOS = '../figuras/resultados/'

# Directorio de salida por defecto (PNG para LaTeX)
DIR_SALIDA = DIR_PNG

# Prefijo para nombres de archivos
PREFIJO_ARCHIVOS = 'grafico_'

# =============================================================================
# CONFIGURACIÓN MATEMÁTICA
# =============================================================================

# Semilla para reproducibilidad de simulaciones estocásticas
SEMILLA_ALEATORIA = 42

# Precisión numérica
PRECISION_DECIMAL = 4

# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def configurar_semilla():
    """Configura la semilla aleatoria para reproducibilidad."""
    np.random.seed(SEMILLA_ALEATORIA)

def obtener_color(indice):
    """Obtiene un color de la paleta basado en el índice."""
    colores_lista = list(COLORES.values())
    return colores_lista[indice % len(colores_lista)]

def formatear_numero(numero, decimales=PRECISION_DECIMAL):
    """Formatea un número con la precisión configurada."""
    return round(numero, decimales)

def guardar_figura(fig, nombre_base, dpi=DPI):
    """
    Guarda una figura en PNG y PDF en sus respectivos directorios.
    
    Args:
        fig: Figura de matplotlib a guardar
        nombre_base: Nombre base del archivo (sin extensión ni prefijo)
        dpi: Resolución para PNG (default: 300)
    
    Returns:
        dict: Rutas de los archivos guardados
    """
    import os
    
    # Crear directorios si no existen
    os.makedirs(DIR_PNG, exist_ok=True)
    os.makedirs(DIR_PDF, exist_ok=True)
    
    # Construir nombres de archivo completos
    nombre_completo = f"{PREFIJO_ARCHIVOS}{nombre_base}"
    
    rutas = {}
    
    # Guardar PNG
    ruta_png = os.path.join(DIR_PNG, f"{nombre_completo}.png")
    fig.savefig(ruta_png, dpi=dpi, bbox_inches='tight', format='png')
    rutas['png'] = ruta_png
    print(f"[OK] PNG guardado: {ruta_png}")
    
    # Guardar PDF
    ruta_pdf = os.path.join(DIR_PDF, f"{nombre_completo}.pdf")
    fig.savefig(ruta_pdf, bbox_inches='tight', format='pdf')
    rutas['pdf'] = ruta_pdf
    print(f"[OK] PDF guardado: {ruta_pdf}")
    
    return rutas

def obtener_dataframe_modelos():
    """
    Convierte los datos de MODELOS a un DataFrame de pandas.
    
    Returns:
        pd.DataFrame: DataFrame con todos los datos de modelos
    """
    df = pd.DataFrame({
        'Modelo': MODELOS['nombres'],
        'Nombre_Corto': MODELOS['nombres_cortos'],
        'Parametros_B': MODELOS['parametros'],
        'Tokens_por_Segundo': MODELOS['tokens_por_seg'],
        'Latencia_s': MODELOS['latencia'],
        'Potencia_GPU_W': MODELOS['potencia_gpu'],
        'RAM_Usada_GiB': MODELOS['ram_usada'],
        'VRAM_Usada_GiB': MODELOS['vram_usada'],
        'Energia_Total_Wh': MODELOS['energia_total'],
        'Eficiencia_tokens_Wh': MODELOS['eficiencia']
    })
    return df

def exportar_estadisticas_csv(df, nombre_archivo='estadisticas_modelos.csv'):
    """
    Exporta estadísticas del DataFrame a CSV.
    
    Args:
        df: DataFrame de pandas
        nombre_archivo: Nombre del archivo CSV
    """
    import os
    
    # Crear directorio de resultados si no existe
    os.makedirs(DIR_RESULTADOS, exist_ok=True)
    
    # Calcular estadísticas descriptivas
    estadisticas = df.describe()
    
    # Guardar en CSV
    ruta_csv = os.path.join(DIR_RESULTADOS, nombre_archivo)
    estadisticas.to_csv(ruta_csv)
    print(f"[OK] Estadísticas exportadas: {ruta_csv}")
    
    return ruta_csv

def calcular_estadisticas_avanzadas(df):
    """
    Calcula estadísticas avanzadas del DataFrame.
    
    Args:
        df: DataFrame de pandas
        
    Returns:
        dict: Diccionario con estadísticas
    """
    estadisticas = {
        'total_modelos': len(df),
        'energia_total': df['Energia_Total_Wh'].sum(),
        'energia_promedio': df['Energia_Total_Wh'].mean(),
        'energia_std': df['Energia_Total_Wh'].std(),
        'eficiencia_promedio': df['Eficiencia_tokens_Wh'].mean(),
        'eficiencia_max': df['Eficiencia_tokens_Wh'].max(),
        'eficiencia_min': df['Eficiencia_tokens_Wh'].min(),
        'modelo_mas_eficiente': df.loc[df['Eficiencia_tokens_Wh'].idxmax(), 'Modelo'],
        'modelo_menos_eficiente': df.loc[df['Eficiencia_tokens_Wh'].idxmin(), 'Modelo'],
        'correlacion_tamano_energia': df['Parametros_B'].corr(df['Energia_Total_Wh']),
    }
    return estadisticas

# =============================================================================
# CONFIGURACIÓN DE HARDWARE
# =============================================================================

HARDWARE_INFO = {
    'gpu': 'NVIDIA GTX 1660 Ti (6 GB GDDR6)',
    'cpu': 'AMD Ryzen 7 5800X (8c/16t)',
    'ram': '32 GiB DDR4 3200 MHz',
    'so': 'Ubuntu 22.04 LTS',
}

# =============================================================================
# METADATOS
# =============================================================================

METADATA = {
    'proyecto': 'Evaluación del consumo energético en procesos industriales asociados a centros de datos de IA generativa',
    'institucion': 'Fundación Universitaria Compensar',
    'fecha': 'Octubre 2025',
}

if __name__ == '__main__':
    print("=" * 70)
    print(f"{METADATA['proyecto']}")
    print("=" * 70)
    print(f"\nConfiguración cargada exitosamente.")
    print(f"\nModelos configurados: {len(MODELOS['nombres'])}")
    print(f"Duración de simulación: {DURACION_SIMULACION} segundos")
    print(f"Puntos de muestreo: {NUM_PUNTOS}")
    print(f"Hardware: {HARDWARE_INFO['gpu']}")
    configurar_semilla()
    print(f"Semilla aleatoria configurada: {SEMILLA_ALEATORIA}")
