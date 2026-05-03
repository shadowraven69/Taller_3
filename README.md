# Mesa de Servicios para Laboratorios

## 1. Información General
- **Nombre del proyecto:** API Mesa de Servicios para Laboratorios Universitarios
- **Integrantes del equipo:** Breidys Julieth Patiño Medina, Juan Fernando Ducuara Cadavid, Steven Pajaro Garcia.
- **Asignatura:** Aplicaciones y servicios WEB (ISW4245).
- **Fecha:** 2 de Mayo del 2026.

## 2. Descripción del Sistema
Este proyecto es una API REST desarrollada con FastAPI que permite gestionar las solicitudes de servicios en los laboratorios de una universidad.

### Entidades implementadas
- **Usuarios:** Gestión de personas que interactúan con el sistema, incluyendo autenticación mediante contraseñas cifradas con bcrypt.
- **Laboratorios:** Catálogo de laboratorios disponibles.
- **Servicios:** Tipos de soporte técnico ofrecidos.
- **Tickets:** Registro de solicitudes, controlando transiciones de estado desde `solicitado` hasta `terminado`.


### Arquitectura
La arquitectura sigue el patrón MVC adaptado para APIs, separando:
- **Modelos (models.py):** Representan las entidades de base de datos usando SQLAlchemy.
- **Esquemas (schemas.py):** Validaciones Pydantic para los datos de entrada/salida.
- **Enrutadores (routers/):** Endpoints agrupados por recurso.
- **Autenticación (auth.py):** Lógica de generación de tokens JWT y dependencias para validación de scopes.

## 3. Configuración del Entorno
Para configurar el entorno y ejecutar el proyecto localmente, sigue estos pasos:

1. Clonar el repositorio.
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   venv\Scripts\activate     
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Configurar el archivo `.env` en la raíz del proyecto. Debe contener las siguientes variables (no incluir valores reales en producción):
   - `DATABASE_URL` (cadena de conexión de PostgreSQL)
   - `SECRET_KEY` (llave para firmar el JWT)
   - `ALGORITHM` (algoritmo, típicamente HS256)
   - `ACCESS_TOKEN_EXPIRE_MINUTES` (tiempo de expiración del token)
5. Ejecutar la aplicación:
   ```bash
   uvicorn main:app --reload
   ```

## 4. Configuración de la Base de Datos
El proyecto utiliza PostgreSQL como base de datos.
La conexión se realiza utilizando el esquema `jwt_grupo_6` a través de la configuración de SQLAlchemy en `database.py`. No se utiliza el schema `public`.

## 5. Endpoints Implementados

| Método | Ruta | Descripción | Scope Requerido | Rol Autorizado |
|---|---|---|---|---|
| POST | `/usuarios/` | Registrar usuario nuevo | Ninguno | Todos |
| GET | `/usuarios/` | Listar usuarios | `usuarios:gestionar` | admin |
| GET | `/usuarios/{id}` | Obtener usuario específico | `usuarios:gestionar` | admin |
| POST | `/auth/token` | Iniciar sesión y obtener JWT | Ninguno | Todos |
| POST | `/laboratorios/` | Crear laboratorio | Autenticado | Todos |
| GET | `/laboratorios/` | Listar laboratorios | Autenticado | Todos |
| POST | `/servicios/` | Crear servicio | Autenticado | Todos |
| GET | `/servicios/` | Listar servicios | Autenticado | Todos |
| POST | `/tickets/` | Crear ticket | `tickets:crear` | solicitante, admin |
| GET | `/tickets/` | Listar tickets | `tickets:ver_propios` | Todos (varía visibilidad) |
| GET | `/tickets/{id}` | Ver detalle de ticket | `tickets:ver_propios` | Todos (varía visibilidad) |
| PATCH| `/tickets/{id}/estado` | Actualizar estado | Varía según transición | Varía según transición |

## 6. Evidencias de Funcionamiento
> **Nota:** Agregar en esta sección las capturas de pantalla tomadas desde Swagger (http://localhost:8000/docs) validando cada escenario de la tabla de la Actividad 5, así como las pruebas de Autenticación y Autorización.

## 7. Control de Versiones
- **Repositorio:** [URL de GitHub]
- **Aportes:**
  - **[Integrante 1]:** [Descripción del aporte, ej. Modelos y Configuración Inicial]
  - **[Integrante 2]:** [Descripción del aporte, ej. Autenticación y JWT]
  - **[Integrante 3]:** [Descripción del aporte, ej. Autorización y Reglas de Negocio]

## 8. Conclusiones
- **Aprendizajes:** Implementación efectiva de seguridad en FastAPI y control fino de permisos usando scopes.
- **Dificultades:** Manejo de transiciones de estado complejas y validación de relaciones entre usuarios y tickets.
- **Soluciones:** Creación de lógica robusta en el endpoint PATCH y configuración adecuada de `SecurityScopes`.
