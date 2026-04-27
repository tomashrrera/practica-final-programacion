Registros Diarios - Práctica Final Programación II


### Fecha: 2026-04-23
**Asistentes:** Tomas Herrera
**¿Qué hice ayer/hoy?**
- Adaptación del entorno de desarrollo profesional (WSL2, Ubuntu, Virtual Environment)
- Diseño e implementación de los modelos iniciales de SQLAlchemy (Book, User).
- Creación de iniciales pruebas unitarias inicial con Pytest.
- Configuración de .gitignore y manejo de ramas en Git.
**¿Qué haré ahora?**
- Implementar los primeros endpoints de la API con FastAPI siguiendo TDD.
**Bloqueos:**
- Problemas iniciales con permisos de Git y credenciales (Resuelto con PAT).

### Fecha: 23-04-2026
**Asistentes:** Tomas Herrera

**¿Qué hemos hecho hoy?**
- Configuración completa de CI/CD con GitHub Actions para ejecución de tests.
- Finalización de la capa de datos: se han implementado las relaciones entre Libros, Usuarios y Préstamos.
- Desarrollo de la API: endpoints CRUD operativos para libros y usuarios, y lógica de registro de préstamos.
- Integración del frontend: la interfaz de Streamlit ya consume datos de la API en lugar del CSV.
- Implementación de inyección de dependencias para las sesiones de la base de datos.

**Bloqueos:**
- Ninguno. El entorno de desarrollo es estable y todos los tests pasan (7/7).

### Fecha: 23-04-2026 (Actualización CI/CD)
**¿Qué hemos hecho ahora?**
- Depuración y corrección del pipeline de GitHub Actions para asegurar que los tests se ejecutan correctamente.
- Resolución de conflictos de importación ("shadowing") renombrando el directorio `fastapi/` a `api/`.
- Ajuste de versiones de `typing_extensions` para garantizar la compatibilidad de Pydantic V2 en el servidor de integración.

### Fecha: 26-04-2026 (Sesión de Refactorización)
**Asistentes:** Tomas Herrera

**¿Qué hemos hecho hoy?**
- Inicio formal del Sprint 2 enfocado en la modularización.
- Se ha descompuesto el servidor monolítico en routers especializados (`api/routers/`) siguiendo SRP.
- Centralización de dependencias en `api/dependencies.py` para limpiar las firmas de los endpoints.
- Resolución del conflicto crítico de nombres: se renombró definitivamente `fastapi/` a `api/` para evitar que Python sombreara la librería oficial, lo que impedía el arranque de Uvicorn.

**Bloqueos:**
- El sombreado (shadowing) de la carpeta `fastapi/` nos dio problemas de importación circulares y de ejecución, resuelto con el cambio de estructura.

### Fecha: 27-04-2026 (Sesión de Robustez y UX)
**Asistentes:** Tomas Herrera

**¿Qué hemos hecho hoy?**
- Finalización de Sprint 2.
- Implementación de un sistema de excepciones personalizadas en `api/exceptions.py` para capturar errores de negocio (libros no encontrados, ya prestados, etc.).
- Registro de manejadores globales en FastAPI para devolver respuestas JSON estandarizadas.
- Optimización de rendimiento en el frontend: creación de un cliente API centralizado con `@st.cache_data` para reducir la latitud y carga del servidor.
- Mejora de la UX en Streamlit: implementación de selectores dinámicos vinculados a la base de datos para facilitar la gestión de préstamos.

**Bloqueos:**
- Ajustes en la configuración de Docker para que los nuevos paths y el sistema de caching funcionen coordinados entre contenedores.
