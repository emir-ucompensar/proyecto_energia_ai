"""
integrales_numericas.py
=======================
Módulo para métodos de integración numérica: Regla del Trapecio y Regla de Simpson 1/3.
Implementa cálculo de integrales definidas con análisis de errores y métricas de convergencia.
"""

import numpy as np
from scipy import integrate


class IntegracionNumerica:
    """
    Marco de integración numérica para la función de consumo energético E(N).
    
    Proporciona métodos para:
    - Regla del Trapecio (convergencia O(h^2))
    - Regla de Simpson 1/3 (convergencia O(h^4))
    - Análisis de errores y validación de convergencia
    """
    
    def __init__(self, a=1.1, b=8.0):
        """
        Inicializar límites de integración.
        
        Parámetros:
        -----------
        a : float
            Límite inferior (default: 1.1 mil millones parámetros - TinyLLaMA)
        b : float
            Límite superior (default: 8.0 mil millones parámetros - LLaMA-3 8B)
        """
        self.a = a
        self.b = b
        self.resultados = []
    
    @staticmethod
    def funcion_energia(N):
        """
        Función polinomial de consumo energético E(N) - grado 4.
        
        E(N) = 0.0842*N^4 - 1.2156*N^3 + 6.8934*N^2 - 12.456*N + 11.234
        
        Parámetros:
        -----------
        N : float o array
            Parámetros del modelo en miles de millones
            
        Retorna:
        --------
        float o array
            Consumo energético en Wh
        """
        return 0.0842 * N**4 - 1.2156 * N**3 + 6.8934 * N**2 - 12.456 * N + 11.234
    
    @staticmethod
    def antiderivada_energia(N):
        """
        Antiderivada de E(N) para integración analítica.
        
        F(N) = 0.01684*N^5 - 0.3039*N^4 + 2.2978*N^3 - 6.228*N^2 + 11.234*N
        
        Parámetros:
        -----------
        N : float
            Parámetros del modelo en miles de millones
            
        Retorna:
        --------
        float
            Valor de la antiderivada
        """
        return (0.0842/5)*N**5 - (1.2156/4)*N**4 + (6.8934/3)*N**3 - (12.456/2)*N**2 + 11.234*N
    
    def integral_exacta(self):
        """
        Calcular integral exacta usando antiderivada (Teorema Fundamental del Cálculo).
        
        Retorna:
        --------
        float
            Valor exacto de la integral definida Z
        """
        return self.antiderivada_energia(self.b) - self.antiderivada_energia(self.a)
    
    def trapecio(self, n):
        """
        Aproximación por Regla del Trapecio.
        
        Fórmula:
        I_trap(n) = (h/2) * [f(x_0) + 2*sum(f(x_i)) + f(x_n)]
        
        Orden: O(h^2)
        
        Parámetros:
        -----------
        n : int
            Número de subintervalos
            
        Retorna:
        --------
        float
            Valor aproximado de la integral
        """
        h = (self.b - self.a) / n
        x = np.linspace(self.a, self.b, n + 1)
        y = self.funcion_energia(x)
        
        integral = (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
        return integral
    
    def simpson(self, n):
        """
        Aproximación por Regla de Simpson 1/3.
        
        Fórmula:
        I_simp(n) = (h/3) * [f(x_0) + 4*sum(f(x_impar)) + 2*sum(f(x_par)) + f(x_n)]
        
        Orden: O(h^4)
        Nota: n debe ser par
        
        Parámetros:
        -----------
        n : int
            Número de subintervalos (debe ser par)
            
        Retorna:
        --------
        float
            Valor aproximado de la integral
        """
        if n % 2 != 0:
            n += 1
        
        h = (self.b - self.a) / n
        x = np.linspace(self.a, self.b, n + 1)
        y = self.funcion_energia(x)
        
        integral = (h / 3) * (y[0] + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-1:2]) + y[-1])
        return integral
    
    def rectangulos(self, n, mode='mid'):
        """
        Aproximación por Método de Rectángulos (Sumas de Riemann).
        
        Fórmula:
        I_rect(n) = h * sum(f(x_i))
        
        donde x_i depende del modo:
        - 'left': extremo izquierdo
        - 'right': extremo derecho  
        - 'mid': punto medio (más preciso)
        
        Orden: O(h) para left/right, O(h^2) para mid
        
        Parámetros:
        -----------
        n : int
            Número de rectángulos/subintervalos
        mode : str
            Modo de evaluación: 'left', 'right', 'mid' (default: 'mid')
            
        Retorna:
        --------
        float
            Valor aproximado de la integral
        """
        h = (self.b - self.a) / n
        
        if mode == 'left':
            x = np.array([self.a + i * h for i in range(n)])
        elif mode == 'right':
            x = np.array([self.a + (i + 1) * h for i in range(n)])
        elif mode == 'mid':
            x = np.array([self.a + (i + 0.5) * h for i in range(n)])
        else:
            raise ValueError("mode debe ser 'left', 'right' o 'mid'")
        
        y = self.funcion_energia(x)
        integral = h * np.sum(y)
        return integral
    
    def calcular_error_relativo(self, i1, i2):
        """
        Calcular error relativo entre dos aproximaciones.
        
        Error_rel = |I_aprox(n) - I_aprox(2n)| / |I_aprox(2n)| * 100
        
        Parámetros:
        -----------
        i1 : float
            Primera aproximación
        i2 : float
            Segunda aproximación (típicamente con discretización más fina)
            
        Retorna:
        --------
        float
            Error relativo en porcentaje
        """
        if i2 == 0:
            return float('inf')
        return abs(i1 - i2) / abs(i2) * 100
    
    def analizar_convergencia_trapecio(self, valores_n):
        """
        Analizar convergencia de la Regla del Trapecio para múltiples valores de n.
        
        Parámetros:
        -----------
        valores_n : list
            Lista de valores de n a probar
            
        Retorna:
        --------
        dict
            Resultados con claves: n, integrales, errores_relativo, errores_absoluto
        """
        resultados = {
            'n': [],
            'integrales': [],
            'errores_relativo': [],
            'errores_absoluto': []
        }
        
        exact = self.integral_exacta()
        prev_integral = None
        
        for n in valores_n:
            integral = self.trapecio(n)
            error_abs = abs(integral - exact)
            
            resultados['n'].append(n)
            resultados['integrales'].append(integral)
            resultados['errores_absoluto'].append(error_abs)
            
            if prev_integral is not None:
                error_rel = self.calcular_error_relativo(prev_integral, integral)
                resultados['errores_relativo'].append(error_rel)
            else:
                resultados['errores_relativo'].append(None)
            
            prev_integral = integral
        
        return resultados
    
    def analizar_convergencia_simpson(self, valores_n):
        """
        Analizar convergencia de la Regla de Simpson 1/3 para múltiples valores de n.
        
        Parámetros:
        -----------
        valores_n : list
            Lista de valores de n a probar
            
        Retorna:
        --------
        dict
            Resultados con claves: n, integrales, errores_relativo, errores_absoluto
        """
        resultados = {
            'n': [],
            'integrales': [],
            'errores_relativo': [],
            'errores_absoluto': []
        }
        
        exact = self.integral_exacta()
        prev_integral = None
        
        for n in valores_n:
            integral = self.simpson(n)
            error_abs = abs(integral - exact)
            
            resultados['n'].append(n)
            resultados['integrales'].append(integral)
            resultados['errores_absoluto'].append(error_abs)
            
            if prev_integral is not None:
                error_rel = self.calcular_error_relativo(prev_integral, integral)
                resultados['errores_relativo'].append(error_rel)
            else:
                resultados['errores_relativo'].append(None)
            
            prev_integral = integral
        
        return resultados
    
    def analizar_convergencia_rectangulos(self, valores_n, mode='mid'):
        """
        Analizar convergencia del Método de Rectángulos para múltiples valores de n.
        
        Parámetros:
        -----------
        valores_n : list
            Lista de valores de n a probar
        mode : str
            Modo de evaluación: 'left', 'right', 'mid'
            
        Retorna:
        --------
        dict
            Resultados con claves: n, integrales, errores_relativo, errores_absoluto
        """
        resultados = {
            'n': [],
            'integrales': [],
            'errores_relativo': [],
            'errores_absoluto': []
        }
        
        exact = self.integral_exacta()
        prev_integral = None
        
        for n in valores_n:
            integral = self.rectangulos(n, mode)
            error_abs = abs(integral - exact)
            
            resultados['n'].append(n)
            resultados['integrales'].append(integral)
            resultados['errores_absoluto'].append(error_abs)
            
            if prev_integral is not None:
                error_rel = self.calcular_error_relativo(prev_integral, integral)
                resultados['errores_relativo'].append(error_rel)
            else:
                resultados['errores_relativo'].append(None)
            
            prev_integral = integral
        
        return resultados
    
    def generar_reporte(self, metodo, valores_n, mode='mid'):
        """
        Generar reporte exhaustivo de convergencia.
        
        Parámetros:
        -----------
        metodo : str
            'trapecio', 'simpson' o 'rectangulos'
        valores_n : list
            Lista de valores de n
        mode : str
            Para 'rectangulos': 'left', 'right' o 'mid'
            
        Retorna:
        --------
        dict
            Resultados completos del análisis con metadatos
        """
        if metodo.lower() == 'trapecio':
            datos = self.analizar_convergencia_trapecio(valores_n)
            orden = 2
        elif metodo.lower() == 'simpson':
            datos = self.analizar_convergencia_simpson(valores_n)
            orden = 4
        elif metodo.lower() == 'rectangulos':
            datos = self.analizar_convergencia_rectangulos(valores_n, mode)
            orden = 2 if mode == 'mid' else 1
        else:
            raise ValueError("Metodo debe ser 'trapecio', 'simpson' o 'rectangulos'")
        
        exact = self.integral_exacta()
        
        reporte = {
            'metodo': metodo,
            'orden_convergencia': orden,
            'integral_exacta': exact,
            'datos': datos,
            'intervalo': (self.a, self.b),
            'funcion': 'E(N) = 0.0842*N^4 - 1.2156*N^3 + 6.8934*N^2 - 12.456*N + 11.234'
        }
        
        if metodo.lower() == 'rectangulos':
            reporte['mode'] = mode
        
        return reporte


if __name__ == '__main__':
    # Ejemplo de uso
    integ = IntegracionNumerica()
    
    print("Integral Exacta (Teorema Fundamental):", integ.integral_exacta())
    print("\nTrapecio (n=100):", integ.trapecio(100))
    print("Simpson (n=100):", integ.simpson(100))
    print("Rectángulos Mid (n=100):", integ.rectangulos(100, 'mid'))
    print("Rectángulos Left (n=100):", integ.rectangulos(100, 'left'))
    print("Rectángulos Right (n=100):", integ.rectangulos(100, 'right'))
