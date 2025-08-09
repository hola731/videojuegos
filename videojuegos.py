import time
import statistics
from typing import List, Tuple

class TimingAttackDemo:
    """
    Demostración didáctica de un Timing Attack 
    
    Un timing attack es una técnica de criptoanálisis que explota las diferencias
    en el tiempo de ejecución de algoritmos para obtener información secreta.
    """
    
    def __init__(self, password_secreto: str = "SECRETO123"):
        self.password_secreto = password_secreto
        self.intentos_realizados = 0
        
    def comparar_vulnerable(self, intento: str) -> bool:
        """
        Función vulnerable a timing attack.
        
        Compara carácter por carácter y retorna False inmediatamente
        cuando encuentra una diferencia, revelando información sobre
        cuántos caracteres son correctos.
        """
        print(f"🔍 Comparando: '{intento}' vs '{self.password_secreto}'")
        
        for i, (caracter_real, caracter_intento) in enumerate(zip(self.password_secreto, intento)):
            if caracter_real != caracter_intento:
                print(f"   ❌ Diferencia en posición {i}: '{caracter_real}' != '{caracter_intento}'")
                return False
            # Simula procesamiento adicional por cada carácter correcto
            time.sleep(0.1)
            print(f"   ✅ Carácter {i} correcto: '{caracter_real}'")
        
        # Verifica longitud
        if len(intento) != len(self.password_secreto):
            print(f"   ❌ Longitud incorrecta: {len(intento)} vs {len(self.password_secreto)}")
            return False
            
        print("   🎉 ¡Contraseña correcta!")
        return True
    
    def comparar_segura(self, intento: str) -> bool:
        """
        Función segura contra timing attack.
        
        Siempre toma el mismo tiempo independientemente de la entrada.
        """
        print(f"🔒 Comparación segura: '{intento}' vs '{self.password_secreto}'")
        
        # Usa comparación constante en tiempo
        if len(intento) != len(self.password_secreto):
            time.sleep(0.5)  # Tiempo constante
            return False
        
        resultado = True
        for caracter_real, caracter_intento in zip(self.password_secreto, intento):
            if caracter_real != caracter_intento:
                resultado = False
            # Siempre toma el mismo tiempo
            time.sleep(0.1)
        
        # Tiempo adicional para mantener consistencia
        time.sleep(0.5)
        
        if resultado:
            print("   🎉 ¡Contraseña correcta!")
        else:
            print("   ❌ Contraseña incorrecta")
            
        return resultado
    
    def ataque_timing(self, caracteres_posibles: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") -> str:
        """
        Simula un timing attack para descubrir la contraseña.
        """
        print("\n🚨 INICIANDO TIMING ATTACK")
        print("=" * 50)
        
        password_descubierto = ""
        tiempos_por_caracter = {}
        
        # Para cada posición en la contraseña
        for posicion in range(len(self.password_secreto)):
            print(f"\n📍 Probando posición {posicion + 1}")
            
            mejor_caracter = None
            mejor_tiempo = 0
            
            # Probar cada carácter posible
            for caracter in caracteres_posibles:
                intento = password_descubierto + caracter + "X" * (len(self.password_secreto) - len(password_descubierto) - 1)
                
                # Medir tiempo de respuesta
                tiempo_inicio = time.time()
                self.comparar_vulnerable(intento)
                tiempo_fin = time.time()
                tiempo_respuesta = tiempo_fin - tiempo_inicio
                
                print(f"   '{caracter}' -> {tiempo_respuesta:.3f}s")
                
                # El carácter que toma más tiempo es probablemente el correcto
                if tiempo_respuesta > mejor_tiempo:
                    mejor_tiempo = tiempo_respuesta
                    mejor_caracter = caracter
            
            if mejor_caracter:
                password_descubierto += mejor_caracter
                print(f"   🎯 Carácter descubierto: '{mejor_caracter}' (tiempo: {mejor_tiempo:.3f}s)")
                tiempos_por_caracter[posicion] = mejor_tiempo
        
        print(f"\n🎉 Contraseña descubierta: '{password_descubierto}'")
        print(f"🔑 Contraseña real: '{self.password_secreto}'")
        print(f"✅ Ataque exitoso: {password_descubierto == self.password_secreto}")
        
        return password_descubierto
    
    def demostrar_diferencia(self):
        """
        Demuestra la diferencia entre implementaciones vulnerables y seguras.
        """
        print("\n📊 DEMOSTRACIÓN DE DIFERENCIAS")
        print("=" * 50)
        
        # Test con implementación vulnerable
        print("\n🔴 Implementación VULNERABLE:")
        intentos_vulnerables = ["A", "S", "SE", "SEC", "SECR", "SECRE", "SECRET", "SECRETO", "SECRETO1", "SECRETO12", "SECRETO123"]
        
        for intento in intentos_vulnerables:
            tiempo_inicio = time.time()
            self.comparar_vulnerable(intento)
            tiempo_fin = time.time()
            print(f"   Tiempo total: {tiempo_fin - tiempo_inicio:.3f}s\n")
        
        # Test con implementación segura
        print("\n🟢 Implementación SEGURA:")
        intentos_seguros = ["A", "S", "SE", "SEC", "SECR", "SECRE", "SECRET", "SECRETO", "SECRETO1", "SECRETO12", "SECRETO123"]
        
        for intento in intentos_seguros:
            tiempo_inicio = time.time()
            self.comparar_segura(intento)
            tiempo_fin = time.time()
            print(f"   Tiempo total: {tiempo_fin - tiempo_inicio:.3f}s\n")

def main():
    """
    Función principal para ejecutar la demostración.
    """
    print("🔐 DEMOSTRACIÓN DIDÁCTICA: TIMING ATTACK")
    print("=" * 60)
    print("""
    Esta demostración muestra cómo un atacante puede explotar
    las diferencias en tiempo de respuesta para descubrir información secreta.
    
    Conceptos clave:
    - Timing Attack: Ataque que explota diferencias temporales
    - Comparación vulnerable: Retorna inmediatamente al encontrar diferencias
    - Comparación segura: Tiempo constante independiente de la entrada
    """)
    
    # Crear instancia de la demostración
    demo = TimingAttackDemo("SECRETO123")
    
    # Mostrar diferencias entre implementaciones
    demo.demostrar_diferencia()
    
    # Ejecutar timing attack
    print("\n" + "=" * 60)
    input("Presiona Enter para ejecutar el timing attack...")
    demo.ataque_timing()
    
    print("\n" + "=" * 60)
    print("""
    🎓 LECCIONES APRENDIDAS:
    
    1. Las comparaciones carácter por carácter pueden revelar información
    2. Los tiempos de respuesta diferentes permiten ataques
    3. Las implementaciones seguras usan tiempo constante
    4. Siempre usar comparaciones seguras en aplicaciones reales
    
    💡 Mejores prácticas:
    - Usar funciones como hmac.compare_digest() en Python
    - Implementar comparaciones de tiempo constante
    - No revelar información a través de tiempos de respuesta
    """)

if __name__ == "__main__":
    main()