# Sistema Integral de Seguimiento y Orientación Ciudadana
## Documentación Completa de Funcionalidades

---

## Tabla de Contenidos

1. [Visión General del Sistema](#visión-general-del-sistema)
2. [Arquitectura y Tecnologías](#arquitectura-y-tecnologías)
3. [Módulos del Sistema](#módulos-del-sistema)
4. [Gestión de Usuarios y Permisos](#gestión-de-usuarios-y-permisos)
5. [Funcionalidades por Rol](#funcionalidades-por-rol)
6. [Sistema de Notificaciones y Alertas](#sistema-de-notificaciones-y-alertas)
7. [APIs y Integraciones](#apis-y-integraciones)
8. [Seguridad y Auditoría](#seguridad-y-auditoría)
9. [Reportes y Métricas](#reportes-y-métricas)
10. [Configuración y Administración](#configuración-y-administración)

---

## Visión General del Sistema

Este es un sistema integral desarrollado para SEDRONAR (Secretaría de Políticas Integrales sobre Drogas) que permite la gestión completa de ciudadanos, legajos de atención, seguimientos, derivaciones y comunicación en tiempo real. El sistema está diseñado para facilitar el trabajo de profesionales en el área de prevención y asistencia en consumos problemáticos.

### Objetivos Principales
- **Centralizar** la información de ciudadanos y sus tratamientos
- **Facilitar** el seguimiento integral de casos
- **Optimizar** la comunicación entre dispositivos de la red
- **Automatizar** procesos administrativos y alertas
- **Garantizar** la confidencialidad y seguridad de los datos
- **Proporcionar** herramientas de análisis y reportes

---

## Arquitectura y Tecnologías

### Stack Tecnológico
- **Backend**: Django 4.2 (Python)
- **Base de Datos**: MySQL 8.0
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS, Alpine.js
- **Contenedores**: Docker + Docker Compose
- **APIs**: Django REST Framework
- **Documentación**: Swagger/OpenAPI 3.0
- **Testing**: pytest
- **IA**: OpenAI GPT-3.5-turbo (Chatbot)

### Arquitectura del Sistema
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Base de       │
│   (Templates)   │◄──►│   (Django)      │◄──►│   Datos (MySQL) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│   APIs REST     │◄─────────────┘
                        │   (DRF)         │
                        └─────────────────┘
                                 │
                        ┌─────────────────┐
                        │   Integraciones │
                        │   - RENAPER     │
                        │   - OpenAI      │
                        │   - WebSockets  │
                        └─────────────────┘
```

---

## Módulos del Sistema

### 1. **Módulo Core (Núcleo)**

**Descripción General**: El módulo Core constituye la base fundamental del sistema, proporcionando la infraestructura esencial para el funcionamiento de todos los demás módulos. Este módulo centraliza la gestión de datos maestros, configuraciones globales y servicios transversales que son utilizados por toda la aplicación.

#### Funcionalidades:

##### **Gestión Geográfica**
**Descripción**: Esta funcionalidad permite administrar la estructura territorial completa de Argentina, organizando la información geográfica en tres niveles jerárquicos: provincias, municipios y localidades. Sirve como base para la ubicación y organización territorial de ciudadanos, instituciones y dispositivos de la red SEDRONAR. Los usuarios pueden crear, editar y mantener actualizada toda la información geográfica, asegurando que los registros de ciudadanos e instituciones estén correctamente geolocalizados para facilitar la coordinación territorial y la generación de reportes por región.

##### **Instituciones de la Red**
**Descripción**: Esta funcionalidad gestiona el registro completo de todos los dispositivos y instituciones que forman parte de la red SEDRONAR. Permite el alta, modificación y administración de diferentes tipos de instituciones (DTC, CAAC, CCC, CAI, etc.), incluyendo sus datos de contacto, ubicación, servicios que prestan, capacidad de atención y estado de habilitación. El sistema controla el proceso completo de registro institucional, desde la solicitud inicial hasta la aprobación final, gestionando la documentación requerida y los estados del trámite. Esta funcionalidad es crucial para mantener actualizado el mapa de recursos disponibles en la red.

##### **Datos de Referencia**
**Descripción**: Esta funcionalidad mantiene todos los catálogos y datos maestros que son utilizados como referencia en todo el sistema. Incluye la gestión de tipos de sexo, días de la semana, meses, turnos de trabajo, y otros datos estructurados que garantizan la consistencia y estandarización de la información. Estos catálogos son fundamentales para la integridad de los datos y facilitan la generación de reportes estadísticos confiables.

##### **Auditoría**
**Descripción**: Esta funcionalidad implementa un sistema completo de trazabilidad que registra automáticamente todas las acciones realizadas por los usuarios en el sistema. Captura información detallada sobre quién realizó cada acción, cuándo se ejecutó, qué datos se modificaron y desde qué ubicación se accedió. Este sistema es esencial para el cumplimiento de normativas de protección de datos, investigación de incidentes de seguridad, y mantenimiento de la integridad del sistema. Permite generar reportes de auditoría y realizar seguimientos detallados de la actividad del sistema.

##### **Configuración Global**
**Descripción**: Esta funcionalidad centraliza la administración de todos los parámetros y configuraciones que afectan el comportamiento global del sistema. Incluye la configuración de integraciones externas (RENAPER, OpenAI), parámetros de seguridad, configuraciones de notificaciones, límites del sistema y otras variables que determinan cómo opera SISOC. Solo usuarios con permisos administrativos pueden acceder a estas configuraciones, garantizando la estabilidad y seguridad del sistema.

#### Modelos Principales:
- `Provincia`: Divisiones administrativas principales
- `Municipio`: Subdivisiones por provincia
- `Localidad`: Localidades específicas por municipio
- `Institucion`: Dispositivos de la red SEDRONAR (DTC, CAAC, CCC, CAI, etc.)
- `DocumentoRequerido`: Documentación necesaria para registro de instituciones

#### Tipos de Instituciones:
- **DTC**: Dispositivo Territorial Comunitario
- **CAAC**: Casa de Atención y Acompañamiento Comunitario
- **CCC**: Casa Comunitaria Convivencial
- **CAI**: Centro de Asistencia Inmediata
- **IC**: Institución Conveniada
- **CT**: Comunidad Terapéutica

### 2. **Módulo Users (Usuarios)**

**Descripción General**: El módulo Users gestiona todo lo relacionado con la autenticación, autorización y administración de usuarios del sistema. Proporciona un sistema robusto de seguridad que controla el acceso a las funcionalidades según roles y permisos específicos, garantizando que cada usuario acceda únicamente a la información y funciones que le corresponden según su función en la organización.

#### Funcionalidades:

##### **Autenticación**
**Descripción**: Esta funcionalidad implementa un sistema seguro de inicio y cierre de sesión que valida la identidad de los usuarios antes de permitir el acceso al sistema. Incluye mecanismos de validación de credenciales, control de intentos fallidos, gestión de sesiones activas y logout automático por inactividad. El sistema registra todos los intentos de acceso para auditoría y seguridad, y puede integrarse con sistemas de autenticación externa si es necesario. Garantiza que solo usuarios autorizados puedan acceder a la información sensible del sistema.

##### **Gestión de Perfiles**
**Descripción**: Esta funcionalidad permite administrar información adicional y específica de cada usuario más allá de los datos básicos de autenticación. Incluye la gestión de datos personales, información de contacto, preferencias del sistema, configuraciones específicas del rol, y metadatos relacionados con la actividad del usuario. Los perfiles pueden incluir información sobre la provincia de trabajo, dispositivo de pertenencia, especialización profesional y otras características relevantes para la operación del sistema.

##### **Roles y Permisos**
**Descripción**: Esta funcionalidad implementa un sistema granular de control de acceso basado en roles que determina qué acciones puede realizar cada usuario en el sistema. Define diferentes niveles de acceso (Administrador, Responsable, Operador, Supervisor, etc.) y asigna permisos específicos para cada funcionalidad. El sistema permite crear grupos de usuarios con permisos similares, facilitando la administración masiva de accesos. Los permisos se pueden configurar a nivel de módulo, funcionalidad e incluso registro individual, proporcionando un control muy fino sobre la seguridad del sistema.

##### **Usuarios Provinciales**
**Descripción**: Esta funcionalidad permite gestionar usuarios que tienen alcance y responsabilidades específicas a nivel provincial. Facilita la administración descentralizada del sistema, permitiendo que supervisores provinciales gestionen usuarios y dispositivos de su jurisdicción. Incluye la asignación automática de permisos basados en la provincia, filtrado automático de información por región, y generación de reportes provinciales. Esta funcionalidad es clave para la operación federal del sistema.

##### **Configuración Personal**
**Descripción**: Esta funcionalidad permite a cada usuario personalizar su experiencia en el sistema según sus preferencias individuales. Incluye opciones como modo oscuro/claro, idioma de la interfaz, configuración de notificaciones, layout de pantallas, y otras preferencias de usabilidad. Los usuarios pueden configurar alertas personalizadas, definir vistas predeterminadas y ajustar la interfaz para optimizar su productividad. Estas configuraciones se almacenan por usuario y se mantienen entre sesiones.

#### Modelos Principales:
- `User`: Usuario base de Django extendido
- `Profile`: Perfil adicional con configuraciones específicas

#### Roles del Sistema:
- **Administrador**: Acceso completo al sistema
- **Responsable**: Gestión de legajos y equipos
- **Operador**: Atención directa de ciudadanos
- **Supervisor**: Supervisión y reportes
- **EncargadoInstitucion**: Gestión de instituciones específicas

### 3. **Módulo Legajos (Gestión de Casos)**

**Descripción General**: El módulo Legajos constituye el corazón operativo del sistema, diseñado para gestionar de manera integral todos los aspectos relacionados con la atención de ciudadanos en situación de consumo problemático. Este módulo permite crear, mantener y hacer seguimiento de casos individuales desde el primer contacto hasta el cierre del tratamiento, garantizando continuidad en la atención y trazabilidad completa del proceso terapéutico.

#### Funcionalidades Principales:

##### **Gestión de Ciudadanos**
**Descripción**: Esta funcionalidad permite crear y mantener un registro completo de todos los ciudadanos que acceden a los servicios de la red SEDRONAR. El sistema facilita el alta de nuevos ciudadanos capturando datos demográficos esenciales como DNI, nombre, apellido, fecha de nacimiento, género, información de contacto y domicilio. La integración con RENAPER permite validar automáticamente la identidad y obtener datos oficiales, reduciendo errores y agilizando el proceso de registro. Incluye un potente sistema de búsqueda que permite localizar ciudadanos por múltiples criterios (DNI, nombre, apellido, etc.) y filtros avanzados para segmentar la población. Mantiene un historial completo de todas las interacciones del ciudadano con el sistema, proporcionando una vista integral de su trayectoria en la red de atención.

##### **Legajos de Atención**
**Descripción**: Esta funcionalidad gestiona la creación y administración de casos individuales de atención para cada ciudadano. Cada legajo representa un episodio de atención específico y contiene toda la información clínica, social y administrativa relacionada. El sistema permite abrir nuevos legajos, asignar responsables profesionales, definir niveles de confidencialidad y controlar el estado del caso a lo largo del tiempo. Los estados del legajo (Abierto, En Seguimiento, Derivado, Cerrado) reflejan la situación actual del caso y determinan las acciones disponibles. La funcionalidad incluye controles de calidad que verifican la completitud de la información antes de permitir cambios de estado, garantizando que todos los casos mantengan estándares mínimos de documentación.

##### **Evaluación Inicial**
**Descripción**: Esta funcionalidad estructura y estandariza el proceso de evaluación clínico-psicosocial que se realiza al inicio de cada caso. Proporciona formularios estructurados para registrar la situación de consumo actual, antecedentes médicos y psiquiátricos, condición socioeconómica, red de apoyo familiar y social, y otros factores relevantes para el tratamiento. Incluye la aplicación de instrumentos de tamizaje validados como ASSIST (para consumo de sustancias) y PHQ-9 (para depresión), que proporcionan mediciones objetivas del estado del ciudadano. El sistema identifica automáticamente factores de riesgo críticos como riesgo suicida o situaciones de violencia, generando alertas inmediatas para los responsables del caso. Esta evaluación sirve como línea de base para el seguimiento posterior y la medición de resultados.

##### **Planes de Intervención**
**Descripción**: Esta funcionalidad permite diseñar y gestionar planes terapéuticos individualizados para cada ciudadano. Los profesionales pueden definir objetivos específicos, medibles y temporalizados, establecer actividades concretas para alcanzar esas metas, y asignar responsables para cada intervención. El sistema controla la vigencia de los planes, alertando cuando es necesario realizar revisiones o actualizaciones. Incluye indicadores de éxito que permiten medir el progreso hacia los objetivos planteados. Los planes pueden incluir diferentes tipos de actividades como entrevistas individuales, terapia grupal, talleres, visitas domiciliarias, y coordinaciones con otros servicios. La funcionalidad facilita el trabajo interdisciplinario permitiendo que múltiples profesionales contribuyan al plan de un mismo ciudadano.

##### **Seguimientos y Contactos**
**Descripción**: Esta funcionalidad registra y organiza todos los contactos e intervenciones realizadas con cada ciudadano a lo largo de su tratamiento. Permite documentar diferentes tipos de contacto (entrevistas presenciales, llamadas telefónicas, visitas domiciliarias, talleres grupales, etc.) con información detallada sobre la duración, contenido, adherencia del ciudadano, acuerdos alcanzados y próximos pasos. El sistema puede adjuntar documentos, grabaciones o fotografías relacionadas con cada contacto. Incluye funcionalidades de programación que permiten agendar contactos futuros y generar recordatorios automáticos. La información de seguimiento es crucial para evaluar la evolución del caso y tomar decisiones clínicas informadas.

##### **Derivaciones**
**Descripción**: Esta funcionalidad gestiona el proceso completo de transferencia de casos entre diferentes dispositivos de la red SEDRONAR. Permite solicitar derivaciones cuando un ciudadano requiere un nivel de atención diferente o servicios especializados no disponibles en el dispositivo actual. El sistema clasifica las derivaciones por nivel de urgencia (baja, media, alta) y controla su estado (pendiente, aceptada, rechazada) facilitando el seguimiento del proceso. Incluye mecanismos de comunicación entre dispositivos para coordinar la transferencia y garantizar continuidad en la atención. Las derivaciones pueden ser internas (dentro de la misma provincia) o interprovinciales, con flujos específicos para cada caso.

##### **Eventos Críticos**
**Descripción**: Esta funcionalidad registra y gestiona situaciones de alto riesgo o impacto que requieren atención inmediata y seguimiento especial. Incluye diferentes tipos de eventos como sobredosis, crisis agudas, situaciones de violencia, internaciones de emergencia, intentos de suicidio, entre otros. Cuando se registra un evento crítico, el sistema genera alertas automáticas a los responsables del caso y supervisores, facilitando una respuesta rápida y coordinada. Cada evento se documenta detalladamente incluyendo circunstancias, acciones tomadas, personas notificadas y seguimiento posterior. Esta información es crucial para la gestión de riesgos y la mejora continua de los protocolos de atención.

#### Modelos Principales:
- `Ciudadano`: Datos personales y demográficos
- `LegajoAtencion`: Caso individual de atención
- `EvaluacionInicial`: Evaluación clínico-psicosocial
- `PlanIntervencion`: Plan terapéutico estructurado
- `SeguimientoContacto`: Registro de contactos
- `Derivacion`: Transferencias entre dispositivos
- `EventoCritico`: Eventos de alto impacto
- `Consentimiento`: Consentimientos informados

### 4. **Módulo Contactos (Red Familiar y Social)**

**Descripción General**: El módulo Contactos está diseñado para mapear y gestionar toda la red de apoyo social y familiar que rodea a cada ciudadano en tratamiento. Reconociendo que el éxito de las intervenciones depende en gran medida del entorno social del individuo, este módulo permite identificar, registrar y coordinar con todos los actores relevantes en el proceso de recuperación, desde familiares directos hasta profesionales de otros servicios.

#### Funcionalidades:

##### **Vínculos Familiares**
**Descripción**: Esta funcionalidad permite mapear y gestionar las relaciones familiares del ciudadano, creando un genograma digital que identifica todos los vínculos significativos. El sistema registra diferentes tipos de relaciones (padre, madre, hermanos, pareja, hijos, etc.) y caracteriza cada vínculo según su rol en el tratamiento. Permite identificar quiénes conviven con el ciudadano, quiénes pueden ser contactos de emergencia, y quiénes participan activamente como referentes en el proceso terapéutico. La funcionalidad incluye la capacidad de vincular familiares que también son ciudadanos registrados en el sistema, facilitando el abordaje familiar integral. Registra información sobre la calidad de las relaciones, conflictos existentes, y recursos de apoyo disponibles en la familia.

##### **Profesionales Tratantes**
**Descripción**: Esta funcionalidad gestiona el equipo interdisciplinario de profesionales que participan en la atención de cada ciudadano. Permite registrar psicólogos, psiquiatras, médicos, trabajadores sociales, operadores socio-terapéuticos, y otros profesionales involucrados, definiendo el rol específico de cada uno en el tratamiento. El sistema identifica al responsable principal del caso y coordina las intervenciones del equipo. Incluye información sobre la institución de pertenencia de cada profesional, fechas de asignación y desasignación, y observaciones sobre su participación. Esta funcionalidad es esencial para garantizar la coordinación entre profesionales y evitar duplicación de esfuerzos o intervenciones contradictorias.

##### **Dispositivos Vinculados**
**Descripción**: Esta funcionalidad mantiene un historial completo de todos los dispositivos e instituciones por los que ha pasado el ciudadano durante su trayectoria en la red SEDRONAR. Registra fechas de admisión y egreso, motivos de derivación, estado de la admisión (activo, egresado, derivado, abandono), y referentes en cada dispositivo. Esta información es crucial para entender la trayectoria del ciudadano, identificar patrones de adherencia o abandono, y coordinar con dispositivos previos cuando es necesario. Permite generar reportes sobre la utilización de servicios y facilita la planificación de recursos en la red.

##### **Contactos de Emergencia**
**Descripción**: Esta funcionalidad gestiona una lista priorizada de personas que pueden ser contactadas en situaciones de emergencia o crisis. Incluye información detallada de contacto (teléfonos múltiples, emails, direcciones), disponibilidad horaria, relación con el ciudadano, y instrucciones especiales para cada contacto. El sistema permite definir diferentes niveles de prioridad y especificar qué tipo de situaciones ameritan contactar a cada persona. Esta funcionalidad es crítica para la respuesta rápida en crisis y para mantener informada a la red de apoyo sobre la evolución del tratamiento.

##### **Historial de Contactos**
**Descripción**: Esta funcionalidad registra de manera detallada todos los contactos realizados con familiares, referentes y otros miembros de la red de apoyo del ciudadano. Documenta el tipo de contacto (llamada, reunión, visita), participantes, duración, motivo, contenido de la conversación, acuerdos alcanzados y próximos pasos. Permite adjuntar documentos o grabaciones cuando corresponde. Esta información es valiosa para evaluar el nivel de apoyo familiar, identificar conflictos o resistencias, y planificar intervenciones familiares. El historial facilita la continuidad cuando cambian los profesionales responsables del caso.

#### Modelos Principales:
- `VinculoFamiliar`: Relaciones familiares entre ciudadanos
- `ProfesionalTratante`: Profesionales asignados al caso
- `DispositivoVinculado`: Historial de admisiones
- `ContactoEmergencia`: Contactos para situaciones críticas
- `HistorialContacto`: Registro detallado de todos los contactos

### 5. **Módulo Chatbot (Asistente Virtual)**

**Descripción General**: El módulo Chatbot incorpora inteligencia artificial al sistema para proporcionar asistencia automatizada a los usuarios del sistema. Utilizando tecnología de procesamiento de lenguaje natural, este asistente virtual puede responder consultas, proporcionar información sobre procedimientos, ayudar con la navegación del sistema y ofrecer soporte técnico básico, mejorando la experiencia del usuario y reduciendo la carga de trabajo del personal de soporte.

#### Funcionalidades:

##### **Chat Inteligente**
**Descripción**: Esta funcionalidad proporciona una interfaz de chat conversacional que permite a los usuarios interactuar con un asistente virtual inteligente. El sistema utiliza procesamiento de lenguaje natural para comprender las consultas de los usuarios y generar respuestas apropiadas y contextuales. El chatbot puede ayudar con preguntas sobre cómo usar el sistema, explicar procedimientos, proporcionar información sobre políticas y protocolos de SEDRONAR, y guiar a los usuarios a través de procesos complejos. La interfaz es intuitiva y accesible desde cualquier parte del sistema, proporcionando ayuda inmediata cuando los usuarios la necesitan.

##### **Integración OpenAI**
**Descripción**: Esta funcionalidad integra el sistema con la API de OpenAI GPT-3.5-turbo para proporcionar capacidades avanzadas de generación de texto y comprensión de lenguaje natural. La integración permite que el chatbot genere respuestas coherentes, contextualmente apropiadas y en lenguaje natural a las consultas de los usuarios. El sistema está configurado con prompts específicos que orientan al modelo hacia el contexto de SEDRONAR y las necesidades particulares del sistema. Incluye controles de costo y uso para gestionar el consumo de la API de manera eficiente.

##### **Base de Conocimiento**
**Descripción**: Esta funcionalidad mantiene una base de conocimiento estructurada con información específica sobre SEDRONAR, sus procedimientos, políticas, y el funcionamiento del sistema. La base de conocimiento se organiza por categorías temáticas y puede ser actualizada por administradores para mantener la información actualizada. El chatbot utiliza esta información para proporcionar respuestas precisas y actualizadas sobre temas específicos de la organización. La base de conocimiento incluye preguntas frecuentes, guías paso a paso, definiciones de términos técnicos, y otra información relevante para los usuarios del sistema.

##### **Historial de Conversaciones**
**Descripción**: Esta funcionalidad mantiene un registro completo de todas las conversaciones que cada usuario ha tenido con el chatbot. Permite a los usuarios revisar conversaciones anteriores, continuar discusiones previas, y acceder a información proporcionada en sesiones pasadas. El historial facilita el seguimiento de consultas complejas que requieren múltiples interacciones y permite al chatbot proporcionar respuestas más personalizadas basadas en el contexto de conversaciones anteriores. Los administradores pueden analizar el historial para identificar patrones en las consultas y mejorar la base de conocimiento.

##### **Sistema de Feedback**
**Descripción**: Esta funcionalidad permite a los usuarios evaluar la calidad y utilidad de las respuestas del chatbot, proporcionando un mecanismo de mejora continua. Los usuarios pueden calificar respuestas, proporcionar comentarios específicos, y reportar respuestas incorrectas o inapropiadas. El sistema recopila y analiza este feedback para identificar áreas de mejora, ajustar la base de conocimiento, y refinar los prompts utilizados con la IA. Esta retroalimentación es esencial para mantener la calidad del servicio y adaptar el chatbot a las necesidades cambiantes de los usuarios.

##### **Panel de Administración**
**Descripción**: Esta funcionalidad proporciona herramientas administrativas para gestionar y configurar el chatbot. Permite a los administradores actualizar la base de conocimiento, revisar y analizar conversaciones, configurar parámetros del sistema, y monitorear el rendimiento del chatbot. Incluye estadísticas sobre uso, satisfacción de usuarios, temas más consultados, y otras métricas relevantes. El panel permite realizar ajustes en tiempo real para mejorar la experiencia del usuario y optimizar el funcionamiento del asistente virtual.

#### Modelos Principales:
- `Conversation`: Conversaciones por usuario
- `Message`: Mensajes individuales
- `ChatbotKnowledge`: Base de conocimiento
- `ChatbotFeedback`: Evaluación de respuestas

### 6. **Módulo Conversaciones (Chat Ciudadano-Operador)**

**Descripción General**: El módulo Conversaciones facilita la comunicación directa en tiempo real entre ciudadanos y operadores del sistema SEDRONAR. Este módulo democratiza el acceso a la orientación y consulta, permitiendo que cualquier persona pueda contactar con profesionales de la red sin barreras administrativas, proporcionando un canal de comunicación inmediato y accesible para consultas, orientación y seguimiento.

#### Funcionalidades:

##### **Chat Público**
**Descripción**: Esta funcionalidad proporciona un canal de comunicación abierto y accesible que permite a cualquier ciudadano iniciar una conversación con operadores de SEDRONAR sin necesidad de registro previo o autenticación. El sistema está diseñado para ser completamente accesible desde cualquier dispositivo con conexión a internet, eliminando barreras tecnológicas y administrativas. La interfaz es simple e intuitiva, optimizada para usuarios que pueden no estar familiarizados con tecnologías complejas. Esta funcionalidad es crucial para el primer contacto y la captación temprana de personas que necesitan orientación o asistencia.

##### **Modalidades**
**Descripción**: Esta funcionalidad ofrece dos modalidades de conversación para adaptarse a diferentes necesidades y niveles de confianza de los usuarios. La modalidad anónima permite a los ciudadanos hacer consultas sin proporcionar información personal, ideal para primeras consultas o cuando existe resistencia a identificarse. La modalidad personal requiere que el ciudadano proporcione su DNI, lo que permite a los operadores acceder a información previa si existe y brindar un servicio más personalizado. El sistema permite la transición de conversaciones anónimas a personales durante la misma sesión si el ciudadano decide proporcionar su identificación.

##### **Asignación Automática**
**Descripción**: Esta funcionalidad implementa un sistema inteligente de distribución de conversaciones que asigna automáticamente las consultas entrantes a operadores disponibles. El sistema considera factores como la carga de trabajo actual de cada operador, su especialización, disponibilidad horaria, y rendimiento histórico. Incluye un sistema de cola que gestiona los tiempos de espera y prioriza las conversaciones según urgencia. Los operadores pueden configurar su disponibilidad y capacidad máxima de conversaciones simultáneas. El sistema también permite la reasignación manual de conversaciones cuando es necesario.

##### **Gestión de Estados**
**Descripción**: Esta funcionalidad controla el ciclo de vida completo de cada conversación, desde su inicio hasta su cierre. Las conversaciones pasan por diferentes estados: pendiente (esperando asignación), activa (en curso con un operador asignado), y cerrada (finalizada). El sistema registra automáticamente los cambios de estado y los tiempos asociados, proporcionando métricas valiosas sobre la eficiencia del servicio. Los operadores pueden cerrar conversaciones cuando se resuelve la consulta, y el sistema puede cerrar automáticamente conversaciones inactivas después de un período determinado.

##### **Métricas de Rendimiento**
**Descripción**: Esta funcionalidad recopila y analiza métricas detalladas sobre el rendimiento del servicio de chat, incluyendo tiempos de espera, tiempos de respuesta, duración de conversaciones, y niveles de satisfacción de los usuarios. Genera reportes automáticos que permiten a los supervisores monitorear la calidad del servicio, identificar cuellos de botella, y tomar decisiones informadas sobre asignación de recursos. Las métricas se pueden segmentar por operador, período de tiempo, tipo de consulta, y otros criterios relevantes para el análisis.

##### **Sistema de Prioridades**
**Descripción**: Esta funcionalidad permite clasificar las conversaciones según su nivel de urgencia, asegurando que las situaciones críticas reciban atención prioritaria. El sistema puede detectar automáticamente palabras clave que indican urgencia (crisis, emergencia, riesgo, etc.) y escalar la prioridad de la conversación. Los operadores también pueden ajustar manualmente la prioridad basada en su evaluación de la situación. Las conversaciones de alta prioridad se asignan inmediatamente a operadores disponibles y generan alertas para supervisores cuando es necesario.

#### Modelos Principales:
- `Conversacion`: Sesiones de chat
- `Mensaje`: Mensajes intercambiados
- `ColaAsignacion`: Sistema de asignación automática
- `MetricasOperador`: Rendimiento de operadores
- `HistorialAsignacion`: Registro de asignaciones

### 7. **Módulo Portal (Portal Público)**

**Descripción General**: El módulo Portal proporciona una interfaz pública que permite a instituciones externas interactuar con SEDRONAR para solicitar su incorporación a la red de dispositivos. Este módulo facilita el proceso de expansión de la red al automatizar los trámites de registro y proporcionar transparencia en el proceso de evaluación y aprobación de nuevas instituciones.

#### Funcionalidades:

##### **Registro de Instituciones**
**Descripción**: Esta funcionalidad permite a organizaciones interesadas en formar parte de la red SEDRONAR completar el proceso de solicitud de registro de manera digital. Proporciona formularios estructurados que capturan toda la información necesaria sobre la institución, incluyendo datos legales, ubicación, servicios que presta, capacidad de atención, recursos humanos, y infraestructura disponible. El sistema guía a los solicitantes a través del proceso paso a paso, validando la información en tiempo real y proporcionando retroalimentación sobre requisitos faltantes. Incluye la capacidad de guardar borradores y continuar el proceso en múltiples sesiones.

##### **Consulta de Trámites**
**Descripción**: Esta funcionalidad proporciona transparencia en el proceso de evaluación permitiendo a las instituciones solicitantes consultar el estado actual de su trámite de registro. Los usuarios pueden ver en qué etapa se encuentra su solicitud, qué documentos han sido revisados, si existen observaciones o requerimientos adicionales, y cuáles son los próximos pasos en el proceso. El sistema envía notificaciones automáticas por email cuando hay cambios en el estado del trámite, manteniendo a los solicitantes informados sobre el progreso de su solicitud.

##### **Creación de Usuarios**
**Descripción**: Esta funcionalidad permite a los encargados de instituciones crear cuentas de usuario que les darán acceso al sistema una vez que su institución sea aprobada. El proceso incluye la validación de identidad, configuración de credenciales seguras, y asignación de permisos apropiados. Los usuarios creados quedan en estado pendiente hasta que la institución sea aprobada oficialmente. Esta funcionalidad agiliza el proceso de incorporación al eliminar pasos administrativos adicionales una vez que la institución es aceptada en la red.

##### **Documentación**
**Descripción**: Esta funcionalidad gestiona la carga y validación de todos los documentos requeridos para el registro de instituciones. Proporciona una lista clara de documentos necesarios según el tipo de institución, permite la carga de archivos en múltiples formatos, y valida que los documentos cumplan con los requisitos técnicos. El sistema organiza los documentos por categorías y mantiene un registro de versiones cuando se requieren actualizaciones. Los evaluadores pueden revisar los documentos, agregar observaciones, y solicitar correcciones o documentos adicionales a través del sistema.licitudes
- **Creación de Usuarios**: Registro para encargados de instituciones
- **Documentación**: Carga de documentos requeridos

### 8. **Módulo Dashboard (Tablero Principal)**

#### Funcionalidades:
- **Métricas en Tiempo Real**: Estadísticas del sistema
- **Actividad Diaria**: Resumen de acciones del día
- **Alertas Activas**: Notificaciones pendientes
- **Gráficos y Reportes**: Visualización de datos
- **Accesos Rápidos**: Enlaces a funciones principales

### 9. **Módulo Configuración**

#### Funcionalidades:
- **Gestión de Dispositivos**: CRUD de instituciones
- **Configuración Geográfica**: Provincias, municipios, localidades
- **Parámetros del Sistema**: Configuraciones globales
- **Tipos de Datos**: Catálogos y referencias

### 10. **Módulo Trámites**

#### Funcionalidades:
- **Gestión de Solicitudes**: Seguimiento de trámites
- **Estados de Trámites**: Control de flujo de procesos
- **Notificaciones**: Comunicación automática de estados

---

## Gestión de Usuarios y Permisos

### Sistema de Roles

#### **Administrador del Sistema**
- Acceso completo a todas las funcionalidades
- Gestión de usuarios y permisos
- Configuración del sistema
- Acceso a auditoría completa

#### **Responsable de Dispositivo**
- Gestión completa de legajos de su dispositivo
- Asignación de casos a operadores
- Supervisión de equipos
- Reportes y métricas

#### **Operador Socioterapéutico**
- Gestión de legajos asignados
- Registro de seguimientos
- Comunicación con ciudadanos
- Derivaciones

#### **Supervisor Provincial**
- Vista consolidada de su provincia
- Reportes provinciales
- Supervisión de dispositivos

#### **Encargado de Institución**
- Gestión de su institución específica
- Solicitudes de registro
- Actualización de datos institucionales

### Permisos Granulares
- **Por Módulo**: Acceso específico a cada funcionalidad
- **Por Acción**: Ver, crear, editar, eliminar
- **Por Datos**: Filtros por provincia, dispositivo, etc.
- **Por Confidencialidad**: Niveles de acceso a información sensible

---

## Funcionalidades por Rol

### **Ciudadano (Sin Autenticación)**
- Acceso al chat público
- Consulta de información general
- Solicitud de orientación
- Evaluación de satisfacción

### **Operador Socioterapéutico**
- **Gestión de Legajos**:
  - Crear y editar legajos asignados
  - Registrar evaluaciones iniciales
  - Crear planes de intervención
  - Registrar seguimientos y contactos
  
- **Comunicación**:
  - Chat con ciudadanos
  - Responder conversaciones asignadas
  - Coordinar con otros profesionales
  
- **Derivaciones**:
  - Solicitar derivaciones
  - Recibir y evaluar derivaciones
  - Seguimiento de transferencias

### **Responsable de Dispositivo**
- **Supervisión de Equipo**:
  - Asignar legajos a operadores
  - Supervisar carga de trabajo
  - Revisar calidad de registros
  
- **Gestión de Casos**:
  - Aprobar derivaciones
  - Cerrar legajos
  - Gestionar eventos críticos
  
- **Reportes**:
  - Métricas del dispositivo
  - Reportes de actividad
  - Indicadores de calidad

### **Supervisor Provincial**
- **Vista Consolidada**:
  - Estadísticas provinciales
  - Comparativas entre dispositivos
  - Identificación de tendencias
  
- **Coordinación**:
  - Facilitar derivaciones interprovinciales
  - Coordinar recursos
  - Planificación estratégica

### **Administrador del Sistema**
- **Configuración Global**:
  - Parámetros del sistema
  - Gestión de usuarios
  - Configuración de dispositivos
  
- **Mantenimiento**:
  - Monitoreo del sistema
  - Gestión de backups
  - Actualizaciones y parches
  
- **Auditoría**:
  - Revisión de logs
  - Análisis de seguridad
  - Cumplimiento normativo

---

## Sistema de Notificaciones y Alertas

### **Alertas Automáticas**

#### **Alertas de Riesgo**
- **Riesgo Suicida**: Notificación inmediata a responsables
- **Situación de Violencia**: Activación de protocolos
- **Riesgo Alto**: Seguimiento prioritario
- **Eventos Críticos**: Notificación en tiempo real

#### **Alertas de Proceso**
- **Sin Contacto Prolongado**: Ciudadanos sin seguimiento
- **Sin Evaluación Inicial**: Legajos sin evaluación
- **Sin Plan de Intervención**: Casos sin planificación
- **Derivaciones Pendientes**: Transferencias sin respuesta
- **Planes Vencidos**: Revisión de planes de intervención

#### **Alertas Administrativas**
- **Documentación Faltante**: Consentimientos, documentos
- **Usuarios Inactivos**: Control de accesos
- **Capacidad de Dispositivos**: Sobrecarga de casos

### **Sistema de Notificaciones**
- **En Tiempo Real**: WebSockets para notificaciones inmediatas
- **Por Email**: Notificaciones importantes por correo
- **En Pantalla**: Alertas visuales en la interfaz
- **Móviles**: Notificaciones push (futuro)

### **Configuración de Alertas**
- **Por Rol**: Diferentes alertas según el rol
- **Por Dispositivo**: Alertas específicas del dispositivo
- **Personalizables**: Usuarios pueden configurar preferencias
- **Escalamiento**: Alertas que escalan si no se atienden

---

## APIs y Integraciones

### **API REST Completa**

#### **Documentación Interactiva**
- **Swagger UI**: `/api/docs/` - Interfaz interactiva
- **ReDoc**: `/api/redoc/` - Documentación detallada
- **Schema JSON**: `/api/schema/` - Esquema OpenAPI

#### **Endpoints Principales**

##### **Core API** (`/api/core/`)
```
GET    /api/core/provincias/           # Listar provincias
GET    /api/core/municipios/           # Listar municipios
GET    /api/core/localidades/          # Listar localidades
CRUD   /api/core/dispositivos/         # Gestión de dispositivos
```

##### **Legajos API** (`/api/legajos/`)
```
CRUD   /api/legajos/ciudadanos/        # Gestión de ciudadanos
CRUD   /api/legajos/legajos/           # Gestión de legajos
POST   /api/legajos/legajos/{id}/cerrar/     # Cerrar legajo
POST   /api/legajos/legajos/{id}/reabrir/    # Reabrir legajo
CRUD   /api/legajos/seguimientos/      # Seguimientos
CRUD   /api/legajos/derivaciones/      # Derivaciones
CRUD   /api/legajos/eventos/           # Eventos críticos
```

##### **Chatbot API** (`/api/chatbot/`)
```
CRUD   /api/chatbot/conversations/     # Conversaciones
POST   /api/chatbot/conversations/{id}/send/  # Enviar mensaje
CRUD   /api/chatbot/knowledge/         # Base de conocimiento
POST   /api/chatbot/feedback/          # Feedback
```

##### **Users API** (`/api/users/`)
```
CRUD   /api/users/users/               # Gestión de usuarios
GET    /api/users/users/me/            # Perfil actual
POST   /api/users/users/change_password/  # Cambiar contraseña
CRUD   /api/users/groups/              # Grupos y permisos
```

### **Integraciones Externas**

#### **RENAPER (Registro Nacional de Personas)**
- **Validación de Identidad**: Verificación automática de DNI
- **Datos Demográficos**: Obtención de datos oficiales
- **Modo Test**: Simulación para desarrollo y testing

#### **OpenAI GPT-3.5-turbo**
- **Chatbot Inteligente**: Respuestas contextuales
- **Base de Conocimiento**: Información específica de SEDRONAR
- **Procesamiento de Lenguaje Natural**: Comprensión de consultas

#### **Servicios de Email**
- **Notificaciones**: Envío automático de alertas
- **Confirmaciones**: Registro de acciones importantes
- **Reportes**: Envío programado de reportes

### **Características de la API**
- **Autenticación**: Basada en sesiones Django
- **Paginación**: Resultados paginados automáticamente
- **Filtrado**: Filtros avanzados por múltiples campos
- **Búsqueda**: Búsqueda de texto completo
- **Ordenamiento**: Ordenamiento por cualquier campo
- **Versionado**: Control de versiones de API
- **Rate Limiting**: Control de límites de uso

---

## Seguridad y Auditoría

### **Seguridad de Datos**

#### **Autenticación y Autorización**
- **Autenticación Robusta**: Validación de credenciales
- **Sesiones Seguras**: Gestión segura de sesiones
- **Permisos Granulares**: Control de acceso específico
- **Expiración de Sesiones**: Timeout automático

#### **Protección de Datos**
- **Encriptación**: Datos sensibles encriptados
- **HTTPS**: Comunicación segura
- **Validación de Entrada**: Prevención de inyecciones
- **Sanitización**: Limpieza de datos de entrada

#### **Cumplimiento Normativo**
- **Ley de Protección de Datos**: Cumplimiento de normativas
- **Consentimientos Informados**: Registro de autorizaciones
- **Confidencialidad**: Niveles de acceso a información
- **Derecho al Olvido**: Capacidad de anonimizar datos

### **Sistema de Auditoría**

#### **Registro de Acciones**
- **Todas las Operaciones**: Log completo de acciones
- **Identificación de Usuario**: Quién realizó cada acción
- **Timestamp**: Cuándo se realizó cada acción
- **Detalles de Cambios**: Qué se modificó exactamente

#### **Tipos de Logs**
- **Acciones de Usuario**: Login, logout, operaciones CRUD
- **Cambios de Datos**: Modificaciones en registros
- **Accesos a Información**: Consultas y visualizaciones
- **Errores del Sistema**: Fallos y excepciones
- **Descargas de Archivos**: Control de acceso a documentos

#### **Monitoreo y Alertas**
- **Actividad Sospechosa**: Detección de patrones anómalos
- **Intentos de Acceso**: Fallos de autenticación
- **Cambios Críticos**: Modificaciones importantes
- **Accesos Fuera de Horario**: Actividad inusual

### **Backup y Recuperación**
- **Backups Automáticos**: Respaldo programado de datos
- **Versionado**: Múltiples versiones de respaldo
- **Recuperación Rápida**: Procedimientos de restauración
- **Testing de Backups**: Verificación periódica

---

## Reportes y Métricas

### **Dashboard Ejecutivo**

#### **Métricas en Tiempo Real**
- **Ciudadanos Activos**: Total de ciudadanos en el sistema
- **Legajos Abiertos**: Casos activos por dispositivo
- **Actividad Diaria**: Seguimientos y contactos del día
- **Alertas Pendientes**: Notificaciones sin atender
- **Usuarios Conectados**: Actividad en tiempo real

#### **Indicadores de Gestión**
- **Tiempo de Respuesta**: Métricas de atención
- **Adherencia al Tratamiento**: Seguimiento de planes
- **Derivaciones**: Flujo entre dispositivos
- **Eventos Críticos**: Incidencias por período
- **Satisfacción**: Evaluaciones de ciudadanos

### **Reportes Operativos**

#### **Por Dispositivo**
- **Carga de Trabajo**: Legajos por operador
- **Productividad**: Seguimientos por período
- **Calidad**: Completitud de registros
- **Tiempos**: Métricas de atención
- **Resultados**: Objetivos alcanzados

#### **Por Provincia**
- **Cobertura**: Ciudadanos atendidos por región
- **Recursos**: Utilización de dispositivos
- **Derivaciones**: Flujo interprovincial
- **Tendencias**: Evolución temporal
- **Comparativas**: Benchmarking entre provincias

### **Reportes Clínicos**

#### **Epidemiológicos**
- **Perfiles de Consumo**: Patrones identificados
- **Factores de Riesgo**: Análisis de vulnerabilidades
- **Efectividad**: Resultados de intervenciones
- **Seguimiento**: Evolución de casos
- **Prevención**: Indicadores preventivos

#### **De Calidad**
- **Adherencia a Protocolos**: Cumplimiento de procedimientos
- **Tiempos de Atención**: Métricas de respuesta
- **Completitud**: Calidad de registros
- **Satisfacción**: Evaluación de servicios
- **Mejora Continua**: Identificación de oportunidades

### **Exportación y Distribución**
- **Formatos Múltiples**: PDF, Excel, CSV
- **Programación**: Reportes automáticos
- **Distribución**: Envío por email
- **Personalización**: Reportes a medida
- **Visualización**: Gráficos y dashboards

---

## Configuración y Administración

### **Configuración del Sistema**

#### **Parámetros Globales**
- **Configuración de Base de Datos**: Conexiones y pools
- **Configuración de Email**: Servidores SMTP
- **Configuración de APIs**: Keys y endpoints externos
- **Configuración de Seguridad**: Políticas y timeouts
- **Configuración de Logs**: Niveles y rotación

#### **Gestión de Dispositivos**
- **Alta de Instituciones**: Registro en la red
- **Configuración de Servicios**: Tipos de atención
- **Asignación de Usuarios**: Personal por dispositivo
- **Configuración de Alertas**: Notificaciones específicas
- **Métricas Personalizadas**: KPIs por dispositivo

### **Administración de Usuarios**

#### **Gestión de Cuentas**
- **Creación de Usuarios**: Alta individual o masiva
- **Asignación de Roles**: Permisos por función
- **Configuración de Perfiles**: Datos adicionales
- **Gestión de Contraseñas**: Políticas de seguridad
- **Activación/Desactivación**: Control de accesos

#### **Grupos y Permisos**
- **Definición de Roles**: Permisos por función
- **Asignación Masiva**: Gestión eficiente
- **Herencia de Permisos**: Jerarquías organizacionales
- **Permisos Temporales**: Accesos por tiempo limitado
- **Auditoría de Permisos**: Control de cambios

### **Mantenimiento del Sistema**

#### **Monitoreo**
- **Estado del Sistema**: Salud de servicios
- **Rendimiento**: Métricas de performance
- **Uso de Recursos**: CPU, memoria, disco
- **Conectividad**: Estado de integraciones
- **Errores**: Detección y alertas

#### **Actualizaciones**
- **Versionado**: Control de releases
- **Despliegue**: Procedimientos automatizados
- **Rollback**: Capacidad de reversión
- **Testing**: Validación pre-producción
- **Documentación**: Registro de cambios

### **Configuración de Integraciones**

#### **RENAPER**
- **Credenciales**: Configuración de acceso
- **Endpoints**: URLs de servicios
- **Modo Test**: Simulación para desarrollo
- **Rate Limiting**: Control de consultas
- **Fallback**: Procedimientos alternativos

#### **OpenAI**
- **API Keys**: Configuración de acceso
- **Modelos**: Selección de GPT
- **Prompts**: Personalización de contexto
- **Límites**: Control de uso y costos
- **Monitoreo**: Seguimiento de consumo

---

## Casos de Uso Principales

### **Flujo de Atención Ciudadana**

1. **Primer Contacto**
   - Ciudadano accede al chat público
   - Operador recibe y atiende consulta
   - Se evalúa necesidad de seguimiento

2. **Registro en el Sistema**
   - Validación de identidad con RENAPER
   - Creación de perfil de ciudadano
   - Apertura de legajo de atención

3. **Evaluación Inicial**
   - Aplicación de tamizajes
   - Identificación de riesgos
   - Mapeo de red de apoyo

4. **Plan de Intervención**
   - Definición de objetivos
   - Programación de actividades
   - Asignación de responsables

5. **Seguimiento Continuo**
   - Contactos programados
   - Registro de evolución
   - Ajuste de planes

6. **Derivación (si necesario)**
   - Evaluación de necesidades
   - Solicitud a dispositivo especializado
   - Transferencia de información

7. **Cierre del Caso**
   - Evaluación de objetivos
   - Registro de resultados
   - Seguimiento post-cierre

### **Gestión de Crisis**

1. **Detección de Evento Crítico**
   - Registro inmediato del evento
   - Clasificación por tipo y gravedad
   - Activación de alertas automáticas

2. **Respuesta Inmediata**
   - Notificación a responsables
   - Activación de protocolos
   - Coordinación de recursos

3. **Seguimiento Post-Crisis**
   - Evaluación de impacto
   - Ajuste de planes
   - Refuerzo de red de apoyo

### **Coordinación de Red**

1. **Identificación de Necesidades**
   - Análisis de capacidades
   - Detección de brechas
   - Planificación de recursos

2. **Derivaciones Estratégicas**
   - Optimización de derivaciones
   - Balanceo de carga
   - Especialización de servicios

3. **Monitoreo de Calidad**
   - Seguimiento de indicadores
   - Identificación de mejoras
   - Capacitación continua

---

## Beneficios del Sistema

### **Para Ciudadanos**
- **Acceso Fácil**: Chat público sin barreras
- **Atención Personalizada**: Seguimiento individual
- **Confidencialidad**: Protección de datos personales
- **Continuidad**: Historial completo de atención
- **Calidad**: Protocolos estandarizados

### **Para Profesionales**
- **Herramientas Integrales**: Todo en una plataforma
- **Información Centralizada**: Acceso completo al historial
- **Alertas Inteligentes**: Notificaciones relevantes
- **Colaboración**: Trabajo en equipo facilitado
- **Eficiencia**: Automatización de procesos

### **Para Gestores**
- **Visibilidad**: Métricas en tiempo real
- **Control**: Seguimiento de procesos
- **Planificación**: Datos para toma de decisiones
- **Calidad**: Monitoreo de estándares
- **Optimización**: Identificación de mejoras

### **Para la Organización**
- **Estandarización**: Procesos unificados
- **Escalabilidad**: Crecimiento sostenible
- **Cumplimiento**: Adherencia a normativas
- **Innovación**: Incorporación de tecnologías
- **Impacto**: Medición de resultados

---

## Roadmap y Evolución

### **Funcionalidades Futuras**
- **Aplicación Móvil**: App nativa para profesionales
- **Inteligencia Artificial**: Análisis predictivo de riesgos
- **Telemedicina**: Consultas remotas integradas
- **Blockchain**: Trazabilidad de datos sensibles
- **IoT**: Integración con dispositivos de monitoreo

### **Mejoras Continuas**
- **Performance**: Optimización de consultas
- **UX/UI**: Mejora de experiencia de usuario
- **Integraciones**: Nuevos servicios externos
- **Reportes**: Dashboards más sofisticados
- **Seguridad**: Fortalecimiento continuo

---

## Conclusión

SISOC representa una solución integral y moderna para la gestión de casos en el ámbito de prevención y asistencia en consumos problemáticos. Su arquitectura modular, funcionalidades completas y enfoque en la seguridad lo convierten en una herramienta fundamental para optimizar la atención ciudadana y mejorar los resultados de las intervenciones.

El sistema no solo digitaliza procesos existentes, sino que introduce nuevas capacidades como la inteligencia artificial, las alertas automáticas y la coordinación en tiempo real, posicionando a SEDRONAR a la vanguardia tecnológica en el sector público.

---

**Documento generado**: Noviembre 2024  
**Versión del Sistema**: v1.0  
**Última actualización**: 31/10/2024