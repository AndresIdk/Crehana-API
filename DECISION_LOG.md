# Decision Log - Task Manager API

Este documento es para dejar registradas algunas decisiones y motivos técnicos que tomé durante el desarrollo del proyecto. La idea es que cualquiera que revise esto entienda por qué están hechas ciertas cosas de determinada manera.

---

## 1. Estructura general

Quise organizar el proyecto siguiendo una estructura inspirada en Clean Architecture. Dividí el código en capas (`domain`, `application`, `infrastructure`, `api`) para separar responsabilidades y facilitar la mantenibilidad.

Sé que algunas partes podrían parecer sobreestructuradas o incluso innecesarias (por ejemplo, tener interfaces sin muchas implementaciones), pero la intención fue mostrar cómo se podrían inyectar distintas tecnologías sin tocar la lógica de negocio.

---

## 2. Soporte para múltiples bases de datos

Aunque el proyecto está conectado a PostgreSQL, dejé preparada toda la base para agregar soporte a MySQL. De hecho, los repositorios, interfaces y algunas configuraciones ya están pensadas para hacer el cambio sin afectar la capa de aplicación. No se completó del todo por temas de tiempo, pero el punto era mostrar la intención de desacoplamiento.

---

## 3. Autenticación con JWT

La autenticación la manejé con JWT para asegurar los endpoints de la API. Es una solución simple y estándar, que permite proteger rutas sin complicar demasiado el flujo.

---

## 4. Envío de correos (Resend)

Para las notificaciones por correo (como asignación de tareas), integré Resend.
Elegí este servicio porque es muy sencillo de usar y no requiere configurar un servidor SMTP.

Registré el dominio `jaimedev.site` y verifiqué los registros DNS para poder enviar desde `support@jaimedev.site`. Todo quedó listo para usarse.

---

## 5. Calidad de código

Todo esto está automatizado con un script (`lint.py`) y también hay hooks de pre-commit para que el código se mantenga limpio antes de cada commit.

---

## 6. Testing

Separé los tests en unitarios e integración. Hay un script para ejecutarlos (`run_tests.py`) que permite correr todos. También se puede correr todo el entorno de testing usando un profile de Docker Compose.

---

## 7. Docker y ambientes

El proyecto está containerizado, y hay varios perfiles en `docker-compose` para levantar diferentes entornos: desarrollo, testing, producción (simulado) y hasta uno con pgAdmin.
Esto permite probar el proyecto en distintas condiciones sin necesidad de tocar nada del código.

---

## 8. Configuraciones por ambiente

Usé archivos separados para configurar el entorno (`config_dev_postgres.py`, `config_prod_postgres.py`, etc.).
Dependiendo de la variable `APP_SETTINGS_MODULE`, el sistema carga la configuración correspondiente. Docker ya viene preconfigurado para el entorno de desarrollo, pero se puede cambiar fácilmente.

---

## 9. Otras consideraciones

- En algún momento pensé desplegar esto en una VPS privada con Nginx o Traefik, pero no llegué a implementarlo del todo.
- Algunas cosas pueden parecer innecesarias (como la capa para MySQL o algunos repositorios vacíos), pero están ahí con intención didáctica.
- El sistema de mappers se puede mejorar.
- En la capa de aplicación podrían agregarse más validaciones de negocio.
- También pensé en usar ramas de Git para simular entornos por configuración, pero decidí no complicarlo, lo importante es que se entienda el mensaje.
- No se preocupen por el acceso a resend, todo fue con este fin, sientanse libres de experimentar.
- No fueron 4-6 horas como se mencionaba en el paper 😅
- En mi maquina funciona (🙌).
---

## 10. Contacto

Si necesitan aclarar algo de lo que desarrollé, pueden escribirme directamente:

- +57 3043582857
- jaimenavarrou@gmail.com
