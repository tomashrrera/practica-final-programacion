# Library Management System 📚 (Proyecto Final)

Este proyecto consiste en un sistema integral de gestión bibliotecaria desarrollado bajo los estándares de **Ingeniería del Software**. Se ha transformado un esqueleto inicial ineficiente en una aplicación robusta, escalable y profesional, aplicando principios **SOLID**, metodologías **XP (Extreme Programming)** y conceptos avanzados de **Python**.

## 🚀 Arquitectura del Sistema

El sistema utiliza una arquitectura desacoplada basada en microservicios, asegurando que cada capa sea independiente:

*   **Backend**: Desarrollado con **FastAPI**, utilizando un sistema de rutas modular y persistencia de datos mediante **SQLAlchemy 2.x**.
*   **Frontend**: Interfaz de usuario interactiva construida con **Streamlit**, que se comunica exclusivamente a través de la API REST para evitar acoplamiento con la base de datos.
*   **Infraestructura**: Orquestación completa mediante **Docker** y **Docker Compose**.
*   **CI/CD**: Integración continua configurada con **GitHub Actions** para garantizar que cada cambio pase una suite de pruebas automatizadas.

---

## 🛡️ Principios SOLID Aplicados

El diseño del código se rige por los principios SOLID para garantizar la mantenibilidad a largo plazo:

1.  **SRP (Single Responsibility Principle)**:
    *   Hemos separado estrictamente las responsabilidades: los modelos (`models.py`) definen la estructura, los esquemas (`schemas.py`) gestionan la validación con Pydantic, y los routers gestionan la lógica de transporte.
2.  **OCP (Open/Closed Principle)**:
    *   La implementación de un **Manejador Global de Excepciones** y el uso de **APIRouter** permiten extender la funcionalidad del sistema (añadir nuevos módulos o tipos de error) sin necesidad de modificar el código base del servidor central.
3.  **LSP (Liskov Substitution Principle)**:
    *   Todas nuestras excepciones personalizadas heredan de una clase base común `LibraryException`. Esto permite que el sistema de manejo de errores trate cualquier excepción de negocio de forma uniforme sin romper el flujo de la aplicación.
4.  **ISP (Interface Segregation Principle)**:
    *   La API está dividida en interfaces específicas (`books`, `users`, `loans`). El frontend solo consume los servicios que necesita, evitando la dependencia de una interfaz monolítica innecesaria.
5.  **DIP (Dependency Inversion Principle)**:
    *   Utilizamos **Inyección de Dependencias** mediante el sistema `Depends()` de FastAPI. La lógica de los endpoints no depende de la creación manual de sesiones de base de datos, sino de una abstracción inyectada, facilitando el testing y el cambio de proveedores de datos.

---

## 🐍 Ingeniería de Software Avanzada

Para alcanzar el grado de excelencia técnica (**Sobresaliente**), hemos implementado:

*   **Decoradores Propios**: Implementación de `@log_execution_time` para monitorizar y registrar el rendimiento de los endpoints críticos en los logs del sistema.
*   **Properties (@property)**: Uso de propiedades pythonicas en los modelos de SQLAlchemy para calcular estados en tiempo real (ej. `User.active_loans_count`) sin almacenar datos redundantes en la base de datos.
*   **Generadores (yield)**: Sistema de sembrado de datos (`api/utils/seeder.py`) que utiliza generadores para procesar y cargar registros de prueba de forma eficiente, optimizando el uso de memoria.
*   **Context Managers**: Gestión segura y eficiente de los recursos y sesiones de la base de datos mediante bloques `try...finally` y generadores.

---

## 🛠️ Instalación y Ejecución

El sistema está completamente dockerizado para evitar problemas de "funciona en mi máquina".

### 1. Arrancar el entorno
Ejecuta el siguiente comando en la raíz del proyecto:
```bash
sudo docker-compose up --build
```
*   **API (Backend)**: Acceso a la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs)
*   **Frontend**: Acceso a la aplicación en [http://localhost:8501](http://localhost:8501)

### 2. Ejecutar Pruebas (Pytest)
Para verificar la integridad del sistema localmente:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
pytest tests/
```

---

## 📈 Metodología XP (Extreme Programming)
*   **TDD**: Desarrollo guiado por pruebas, asegurando una cobertura robusta antes de cada implementación.
*   **Refactorización Continua**: Evolución constante del código para eliminar deuda técnica (ej. migración de CSV a DB y modularización de la API).
*   **Pair Programming**: Trabajo colaborativo reflejado en el historial de commits.
*   **Registros Diarios**: Documentación transparente del progreso y bloqueos en `DAILYS.md`.
