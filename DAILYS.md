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