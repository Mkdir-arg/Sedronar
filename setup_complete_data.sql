-- ========================================
-- SISOC - Script completo de datos maestros
-- ========================================

USE sedronar;

-- ========================================
-- 1. DATOS BÁSICOS DEL SISTEMA
-- ========================================

-- Sexos
INSERT IGNORE INTO core_sexo (id, sexo) VALUES 
(1, 'Femenino'),
(2, 'Masculino'),
(3, 'X');

-- Días de la semana
INSERT IGNORE INTO core_dia (id, nombre) VALUES 
(1, 'Lunes'),
(2, 'Martes'),
(3, 'Miércoles'),
(4, 'Jueves'),
(5, 'Viernes'),
(6, 'Sábado'),
(7, 'Domingo');

-- Meses
INSERT IGNORE INTO core_mes (id, nombre) VALUES 
(1, 'Enero'),
(2, 'Febrero'),
(3, 'Marzo'),
(4, 'Abril'),
(5, 'Mayo'),
(6, 'Junio'),
(7, 'Julio'),
(8, 'Agosto'),
(9, 'Septiembre'),
(10, 'Octubre'),
(11, 'Noviembre'),
(12, 'Diciembre');

-- Turnos
INSERT IGNORE INTO core_turno (id, nombre) VALUES 
(1, 'Mañana'),
(2, 'Tarde'),
(3, 'Noche');

-- ========================================
-- 2. UBICACIONES GEOGRÁFICAS
-- ========================================

-- Provincias principales
INSERT IGNORE INTO core_provincia (id, nombre) VALUES 
(1, 'Buenos Aires'),
(2, 'Catamarca'),
(3, 'Chaco'),
(4, 'Chubut'),
(5, 'Córdoba'),
(6, 'Corrientes'),
(7, 'Entre Ríos'),
(8, 'Formosa'),
(9, 'Jujuy'),
(10, 'La Pampa'),
(11, 'La Rioja'),
(12, 'Mendoza'),
(13, 'Misiones'),
(14, 'Neuquén'),
(15, 'Río Negro'),
(16, 'Salta'),
(17, 'San Juan'),
(18, 'San Luis'),
(19, 'Santa Cruz'),
(20, 'Santa Fe'),
(21, 'Santiago del Estero'),
(22, 'Tierra del Fuego'),
(23, 'Tucumán'),
(24, 'Ciudad Autónoma de Buenos Aires');

-- Municipios principales
INSERT IGNORE INTO core_municipio (id, nombre, provincia_id) VALUES 
(1, 'Ciudad Autónoma de Buenos Aires', 24),
(2, 'La Plata', 1),
(3, 'Mar del Plata', 1),
(4, 'Bahía Blanca', 1),
(5, 'Córdoba', 5),
(6, 'Rosario', 20),
(7, 'Mendoza', 12),
(8, 'Tucumán', 23),
(9, 'Salta', 16),
(10, 'Santa Fe', 20),
(11, 'Corrientes', 6),
(12, 'Posadas', 13),
(13, 'Neuquén', 14),
(14, 'Paraná', 7),
(15, 'Formosa', 8);

-- Localidades principales
INSERT IGNORE INTO core_localidad (id, nombre, municipio_id) VALUES 
(1, 'Centro', 1),
(2, 'Palermo', 1),
(3, 'Belgrano', 1),
(4, 'San Telmo', 1),
(5, 'Casco Urbano', 2),
(6, 'Centro', 3),
(7, 'Centro', 4),
(8, 'Nueva Córdoba', 5),
(9, 'Centro', 6),
(10, 'Ciudad', 7),
(11, 'Centro', 8),
(12, 'Centro', 9),
(13, 'Centro', 10),
(14, 'Centro', 11),
(15, 'Centro', 12);

-- ========================================
-- 3. INSTITUCIONES DE LA RED SEDRONAR
-- ========================================

INSERT IGNORE INTO core_institucion (id, tipo, nombre, provincia_id, municipio_id, localidad_id, direccion, telefono, email, activo, nro_registro, resolucion, fecha_alta, descripcion, estado_registro, fecha_aprobacion, creado, modificado) VALUES 
(1, 'DTC', 'DTC Buenos Aires Centro', 24, 1, 1, 'Av. Corrientes 1234', '011-4567-8901', 'dtc.bsas.centro@sedronar.gob.ar', 1, 'DTC-001-2024', 'Res. 123/2024', '2024-01-15', 'Dispositivo Territorial Comunitario en el centro de CABA', 'APROBADO', '2024-01-15', NOW(), NOW()),
(2, 'CAAC', 'CAAC La Plata', 1, 2, 5, 'Calle 7 entre 47 y 48', '0221-456-7890', 'caac.laplata@sedronar.gob.ar', 1, 'CAAC-001-2024', 'Res. 124/2024', '2024-01-15', 'Casa de Atención y Acompañamiento Comunitario', 'APROBADO', '2024-01-15', NOW(), NOW()),
(3, 'CAI', 'CAI Buenos Aires Sur', 24, 1, 4, 'Ramón Carrillo 375', '011-4305-0061', 'cai.bsas.sur@sedronar.gob.ar', 1, 'CAI-001-2024', 'Res. 125/2024', '2024-01-15', 'Centro de Asistencia Inmediata', 'APROBADO', '2024-01-15', NOW(), NOW()),
(4, 'DTC', 'DTC Córdoba Capital', 5, 5, 8, 'Av. Colón 1456', '0351-234-5678', 'dtc.cordoba@sedronar.gob.ar', 1, 'DTC-002-2024', 'Res. 126/2024', '2024-01-15', 'Dispositivo Territorial Comunitario Córdoba', 'APROBADO', '2024-01-15', NOW(), NOW()),
(5, 'CAAC', 'CAAC Rosario', 20, 6, 9, 'Bv. Oroño 789', '0341-567-8901', 'caac.rosario@sedronar.gob.ar', 1, 'CAAC-002-2024', 'Res. 127/2024', '2024-01-15', 'Casa de Atención y Acompañamiento Comunitario Rosario', 'APROBADO', '2024-01-15', NOW(), NOW()),
(6, 'CCC', 'CCC Mendoza', 12, 7, 10, 'San Martín 234', '0261-345-6789', 'ccc.mendoza@sedronar.gob.ar', 1, 'CCC-001-2024', 'Res. 128/2024', '2024-01-15', 'Casa Comunitaria Convivencial Mendoza', 'APROBADO', '2024-01-15', NOW(), NOW()),
(7, 'CT', 'CT Tucumán', 23, 8, 11, 'Av. Independencia 567', '0381-456-7890', 'ct.tucuman@sedronar.gob.ar', 1, 'CT-001-2024', 'Res. 129/2024', '2024-01-15', 'Comunidad Terapéutica Tucumán', 'APROBADO', '2024-01-15', NOW(), NOW()),
(8, 'IC', 'IC Salta Norte', 16, 9, 12, 'Av. San Martín 890', '0387-567-8901', 'ic.salta@sedronar.gob.ar', 1, 'IC-001-2024', 'Res. 130/2024', '2024-01-15', 'Institución Conveniada Salta', 'APROBADO', '2024-01-15', NOW(), NOW());

-- ========================================
-- 4. GRUPOS DE USUARIOS DEL SISTEMA
-- ========================================

INSERT IGNORE INTO auth_group (name) VALUES 
('Administrador'),
('Responsable'),
('Operador'),
('Supervisor'),
('Consulta'),
('EncargadoInstitucion'),
('EncargadoDispositivo'),
('Profesional');

-- ========================================
-- 5. USUARIOS DEL SISTEMA
-- ========================================

-- Superusuario admin
INSERT IGNORE INTO auth_user (username, first_name, last_name, email, is_staff, is_active, is_superuser, password, date_joined) VALUES
('admin', 'Administrador', 'Principal', 'admin@sisoc.gov.ar', 1, 1, 1, 'pbkdf2_sha256$600000$admin$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW());

-- Administradores (3 usuarios)
INSERT IGNORE INTO auth_user (username, first_name, last_name, email, is_staff, is_active, is_superuser, password, date_joined) VALUES
('admin1', 'Juan', 'Pérez', 'admin1@sisoc.gov.ar', 1, 1, 0, 'pbkdf2_sha256$600000$admin123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW()),
('admin2', 'María', 'González', 'admin2@sisoc.gov.ar', 1, 1, 0, 'pbkdf2_sha256$600000$admin123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW()),
('admin3', 'Carlos', 'López', 'admin3@sisoc.gov.ar', 1, 1, 0, 'pbkdf2_sha256$600000$admin123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW());

-- Responsables (3 usuarios)
INSERT IGNORE INTO auth_user (username, first_name, last_name, email, is_staff, is_active, is_superuser, password, date_joined) VALUES
('resp1', 'Ana', 'Martínez', 'resp1@sisoc.gov.ar', 0, 1, 0, 'pbkdf2_sha256$600000$resp123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW()),
('resp2', 'Luis', 'Rodríguez', 'resp2@sisoc.gov.ar', 0, 1, 0, 'pbkdf2_sha256$600000$resp123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW()),
('resp3', 'Carmen', 'Silva', 'resp3@sisoc.gov.ar', 0, 1, 0, 'pbkdf2_sha256$600000$resp123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW());

-- Operadores (3 usuarios)
INSERT IGNORE INTO auth_user (username, first_name, last_name, email, is_staff, is_active, is_superuser, password, date_joined) VALUES
('oper1', 'Diego', 'Fernández', 'oper1@sisoc.gov.ar', 0, 1, 0, 'pbkdf2_sha256$600000$oper123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW()),
('oper2', 'Laura', 'Morales', 'oper2@sisoc.gov.ar', 0, 1, 0, 'pbkdf2_sha256$600000$oper123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW()),
('oper3', 'Roberto', 'Castro', 'oper3@sisoc.gov.ar', 0, 1, 0, 'pbkdf2_sha256$600000$oper123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW());

-- Supervisores (3 usuarios)
INSERT IGNORE INTO auth_user (username, first_name, last_name, email, is_staff, is_active, is_superuser, password, date_joined) VALUES
('super1', 'Patricia', 'Herrera', 'super1@sisoc.gov.ar', 0, 1, 0, 'pbkdf2_sha256$600000$super123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW()),
('super2', 'Miguel', 'Vargas', 'super2@sisoc.gov.ar', 0, 1, 0, 'pbkdf2_sha256$600000$super123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW()),
('super3', 'Elena', 'Jiménez', 'super3@sisoc.gov.ar', 0, 1, 0, 'pbkdf2_sha256$600000$super123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW());

-- Consulta (3 usuarios)
INSERT IGNORE INTO auth_user (username, first_name, last_name, email, is_staff, is_active, is_superuser, password, date_joined) VALUES
('cons1', 'Fernando', 'Ruiz', 'cons1@sisoc.gov.ar', 0, 1, 0, 'pbkdf2_sha256$600000$cons123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW()),
('cons2', 'Gabriela', 'Torres', 'cons2@sisoc.gov.ar', 0, 1, 0, 'pbkdf2_sha256$600000$cons123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW()),
('cons3', 'Andrés', 'Mendoza', 'cons3@sisoc.gov.ar', 0, 1, 0, 'pbkdf2_sha256$600000$cons123$VQiX8tqvP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKzP8DjQzKz', NOW());

-- ========================================
-- 6. ASIGNACIÓN DE USUARIOS A GRUPOS
-- ========================================

-- Administradores
INSERT IGNORE INTO auth_user_groups (user_id, group_id)
SELECT u.id, g.id FROM auth_user u, auth_group g 
WHERE u.username IN ('admin1', 'admin2', 'admin3') AND g.name = 'Administrador';

-- Responsables
INSERT IGNORE INTO auth_user_groups (user_id, group_id)
SELECT u.id, g.id FROM auth_user u, auth_group g 
WHERE u.username IN ('resp1', 'resp2', 'resp3') AND g.name = 'Responsable';

-- Operadores
INSERT IGNORE INTO auth_user_groups (user_id, group_id)
SELECT u.id, g.id FROM auth_user u, auth_group g 
WHERE u.username IN ('oper1', 'oper2', 'oper3') AND g.name = 'Operador';

-- Supervisores
INSERT IGNORE INTO auth_user_groups (user_id, group_id)
SELECT u.id, g.id FROM auth_user u, auth_group g 
WHERE u.username IN ('super1', 'super2', 'super3') AND g.name = 'Supervisor';

-- Consulta
INSERT IGNORE INTO auth_user_groups (user_id, group_id)
SELECT u.id, g.id FROM auth_user u, auth_group g 
WHERE u.username IN ('cons1', 'cons2', 'cons3') AND g.name = 'Consulta';

-- ========================================
-- 7. PERFILES DE USUARIO
-- ========================================

INSERT IGNORE INTO users_profile (user_id, dark_mode, es_usuario_provincial, provincia_id, rol)
SELECT u.id, 1, 1, 1, 
    CASE 
        WHEN u.username = 'admin' THEN 'Superadministrador'
        WHEN u.username LIKE 'admin%' THEN 'Administrador del Sistema'
        WHEN u.username LIKE 'resp%' THEN 'Responsable de Legajos'
        WHEN u.username LIKE 'oper%' THEN 'Operador de Campo'
        WHEN u.username LIKE 'super%' THEN 'Supervisor Regional'
        WHEN u.username LIKE 'cons%' THEN 'Usuario de Consulta'
    END
FROM auth_user u 
WHERE u.username IN ('admin', 'admin1', 'admin2', 'admin3', 'resp1', 'resp2', 'resp3', 
                     'oper1', 'oper2', 'oper3', 'super1', 'super2', 'super3',
                     'cons1', 'cons2', 'cons3');

-- ========================================
-- 8. PROFESIONALES
-- ========================================

INSERT IGNORE INTO legajos_profesional (usuario_id, matricula, rol, creado, modificado)
SELECT u.id, 
    CASE 
        WHEN u.username LIKE 'resp%' THEN CONCAT('MP-', LPAD(SUBSTRING(u.username, 5), 4, '0'))
        WHEN u.username LIKE 'oper%' THEN CONCAT('OP-', LPAD(SUBSTRING(u.username, 5), 4, '0'))
        WHEN u.username LIKE 'super%' THEN CONCAT('SP-', LPAD(SUBSTRING(u.username, 6), 4, '0'))
    END,
    CASE 
        WHEN u.username LIKE 'resp%' THEN 'Psicólogo/a'
        WHEN u.username LIKE 'oper%' THEN 'Operador/a Social'
        WHEN u.username LIKE 'super%' THEN 'Supervisor/a'
    END,
    NOW(), NOW()
FROM auth_user u 
WHERE u.username LIKE 'resp%' OR u.username LIKE 'oper%' OR u.username LIKE 'super%';

-- ========================================
-- 9. CIUDADANOS DE EJEMPLO
-- ========================================

INSERT IGNORE INTO legajos_ciudadano (dni, nombre, apellido, fecha_nacimiento, genero, telefono, email, domicilio, activo, creado, modificado) VALUES
('12345678', 'Juan Carlos', 'Rodríguez', '1985-03-15', 'M', '011-1234-5678', 'juan.rodriguez@email.com', 'Av. Corrientes 1234, CABA', 1, NOW(), NOW()),
('23456789', 'María Elena', 'González', '1990-07-22', 'F', '011-2345-6789', 'maria.gonzalez@email.com', 'Calle Falsa 123, La Plata', 1, NOW(), NOW()),
('34567890', 'Carlos Alberto', 'Fernández', '1978-11-08', 'M', '0351-345-6789', 'carlos.fernandez@email.com', 'San Martín 456, Córdoba', 1, NOW(), NOW()),
('45678901', 'Ana Sofía', 'Martínez', '1995-01-30', 'F', '0341-456-7890', 'ana.martinez@email.com', 'Bv. Oroño 789, Rosario', 1, NOW(), NOW()),
('56789012', 'Roberto Luis', 'Castro', '1982-09-12', 'M', '0261-567-8901', 'roberto.castro@email.com', 'Las Heras 321, Mendoza', 1, NOW(), NOW());

-- ========================================
-- 10. DATOS PARA CHATBOT
-- ========================================

INSERT IGNORE INTO chatbot_knowledgebase (pregunta, respuesta, categoria, activo, creado, modificado) VALUES
('¿Qué es SEDRONAR?', 'SEDRONAR es la Secretaría de Políticas Integrales sobre Drogas de la Nación Argentina, encargada de diseñar e implementar políticas públicas en materia de prevención del consumo problemático de drogas.', 'Institucional', 1, NOW(), NOW()),
('¿Dónde puedo pedir ayuda?', 'Puedes acercarte a cualquiera de nuestros dispositivos territoriales: DTC, CAAC, CAI o CCC. También puedes llamar a la línea gratuita 141 las 24 horas.', 'Ayuda', 1, NOW(), NOW()),
('¿Qué es un DTC?', 'Un Dispositivo Territorial Comunitario (DTC) es un espacio de atención integral que brinda acompañamiento y tratamiento a personas con consumo problemático de sustancias.', 'Dispositivos', 1, NOW(), NOW()),
('¿Qué es una CAAC?', 'Una Casa de Atención y Acompañamiento Comunitario (CAAC) es un dispositivo residencial que ofrece alojamiento transitorio y tratamiento integral.', 'Dispositivos', 1, NOW(), NOW()),
('¿Cómo funciona el tratamiento?', 'El tratamiento es integral, gratuito y voluntario. Incluye atención médica, psicológica, social y actividades comunitarias adaptadas a cada persona.', 'Tratamiento', 1, NOW(), NOW());

-- ========================================
-- 11. VERIFICACIÓN FINAL
-- ========================================

SELECT '========================================' as info;
SELECT 'RESUMEN DE DATOS CREADOS:' as info;
SELECT '========================================' as info;

SELECT 'UBICACIONES:' as categoria, COUNT(*) as cantidad FROM core_provincia
UNION ALL
SELECT 'MUNICIPIOS:', COUNT(*) FROM core_municipio
UNION ALL
SELECT 'LOCALIDADES:', COUNT(*) FROM core_localidad
UNION ALL
SELECT 'DISPOSITIVOS:', COUNT(*) FROM core_dispositivored
UNION ALL
SELECT 'GRUPOS:', COUNT(*) FROM auth_group
UNION ALL
SELECT 'USUARIOS:', COUNT(*) FROM auth_user
UNION ALL
SELECT 'PERFILES:', COUNT(*) FROM users_profile
UNION ALL
SELECT 'PROFESIONALES:', COUNT(*) FROM legajos_profesional
UNION ALL
SELECT 'CIUDADANOS:', COUNT(*) FROM legajos_ciudadano;

SELECT '========================================' as info;
SELECT 'CREDENCIALES DE ACCESO:' as info;
SELECT '========================================' as info;
SELECT 'Superusuario: admin / admin123' as credenciales;
SELECT 'Administradores: admin1, admin2, admin3 / admin123' as credenciales;
SELECT 'Responsables: resp1, resp2, resp3 / resp123' as credenciales;
SELECT 'Operadores: oper1, oper2, oper3 / oper123' as credenciales;
SELECT 'Supervisores: super1, super2, super3 / super123' as credenciales;
SELECT 'Consulta: cons1, cons2, cons3 / cons123' as credenciales;
SELECT '========================================' as info;

SELECT 'SISTEMA LISTO PARA USAR!' as resultado;