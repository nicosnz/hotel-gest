CREATE SCHEMA IF NOT EXISTS content;


CREATE TABLE content.roles (
    id UUID PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content.empleados (
    id UUID PRIMARY KEY,

    rol_id UUID NOT NULL REFERENCES content.roles(id),

    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,

    correo VARCHAR(150) UNIQUE,
    telefono VARCHAR(20) UNIQUE,

    fecha_contratacion DATE NOT NULL,

    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content.huespedes (
    id UUID PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,

    documento_identidad VARCHAR(30) UNIQUE NOT NULL,

    correo VARCHAR(150),
    telefono VARCHAR(20),

    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content.tipos_habitaciones (
    id UUID PRIMARY KEY,

    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,

    capacidad INTEGER NOT NULL,

    precio_por_noche NUMERIC(10,2) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE content.habitaciones (
    id UUID PRIMARY KEY,

    numero VARCHAR(10) NOT NULL UNIQUE,

    piso INTEGER NOT NULL,

    tipo_habitacion_id UUID NOT NULL
        REFERENCES content.tipos_habitaciones(id),

    estado VARCHAR(20) NOT NULL
        CHECK (estado IN (
            'DISPONIBLE',
            'OCUPADA',
            'RESERVADA',
            'MANTENIMIENTO'
        )),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content.reservas (
    id UUID PRIMARY KEY,

    habitacion_id UUID NOT NULL
        REFERENCES content.habitaciones(id),

   

    fecha_reserva TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    fecha_checkin_esperado DATE NOT NULL,
    fecha_checkout_esperado DATE NOT NULL,

    fecha_checkin_real TIMESTAMP,
    fecha_checkout_real TIMESTAMP,

    estado VARCHAR(20) NOT NULL
        CHECK (estado IN (
            'PENDIENTE',
            'CONFIRMADA',
            'CHECKIN',
            'FINALIZADA',
            'CANCELADA'
        )),

    observaciones TEXT,

    CONSTRAINT chk_fechas
    CHECK (
        fecha_checkout_esperado > fecha_checkin_esperado
    ),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content.reserva_huespedes (
    id UUID PRIMARY KEY,

    reserva_id UUID NOT NULL
        REFERENCES content.reservas(id)
        ON DELETE CASCADE,

    huesped_id UUID NOT NULL
        REFERENCES content.huespedes(id),

    es_titular BOOLEAN DEFAULT FALSE,

    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_reserva_huesped
    UNIQUE (reserva_id, huesped_id)
);
CREATE TABLE content.pagos (
    id UUID PRIMARY KEY,

    reserva_id UUID NOT NULL
        REFERENCES content.reservas(id),

    monto NUMERIC(10,2) NOT NULL,

    concepto VARCHAR(30) NOT NULL
        CHECK (concepto IN (
            'ADELANTO',
            'HOSPEDAJE',
            'SERVICIO',
            'REEMBOLSO',
            'PENALIZACION'
        )),
    metodo_pago VARCHAR(20) NOT NULL
        CHECK (metodo_pago IN (
            'EFECTIVO',
            'TARJETA',
            'TRANSFERENCIA',
            'QR'
        )),

    fecha_pago TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    estado VARCHAR(20) NOT NULL
        CHECK (estado IN (
            'PENDIENTE',
            'PAGADO',
            'REEMBOLSADO'
        )),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE content.servicios (
    id UUID PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    descripcion TEXT,

    precio NUMERIC(10,2) NOT NULL,

    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content.reserva_servicios (
    id UUID PRIMARY KEY,

    reserva_id UUID NOT NULL
        REFERENCES content.reservas(id),

    servicio_id UUID NOT NULL
        REFERENCES content.servicios(id),

    cantidad INTEGER NOT NULL
        CHECK (cantidad > 0),

    precio_unitario NUMERIC(10,2) NOT NULL,

    fecha_consumo TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE content.mantenimientos (
    id UUID PRIMARY KEY,

    habitacion_id UUID NOT NULL
        REFERENCES content.habitaciones(id),

    empleado_id UUID
        REFERENCES content.empleados(id),

    fecha_inicio TIMESTAMP NOT NULL,

    fecha_fin TIMESTAMP,

    descripcion TEXT NOT NULL,

    estado VARCHAR(20) NOT NULL
        CHECK (estado IN (
            'PROGRAMADO',
            'EN_PROCESO',
            'FINALIZADO'
        )),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
--  SEED: Hotel Management DB  (schema: content)
--  Datos realistas — Hotel "Las Américas", Santa Cruz, Bolivia
-- ============================================================

-- -------------------------------------------------------
-- 1. ROLES
-- -------------------------------------------------------
INSERT INTO content.roles (id, nombre) VALUES
  ('a1b2c3d4-0001-0001-0001-000000000001', 'Recepcionista'),
  ('a1b2c3d4-0001-0001-0001-000000000002', 'Ama de llaves'),
  ('a1b2c3d4-0001-0001-0001-000000000003', 'Mantenimiento'),
  ('a1b2c3d4-0001-0001-0001-000000000004', 'Gerente');

-- -------------------------------------------------------
-- 2. EMPLEADOS
-- -------------------------------------------------------
INSERT INTO content.empleados (id, rol_id, nombre, apellido, correo, telefono, fecha_contratacion, activo) VALUES
  ('b1000001-0000-0000-0000-000000000001',
   'a1b2c3d4-0001-0001-0001-000000000001',
   'Valentina', 'Quispe Mamani',
   'v.quispe@lasamericas.bo', '+591 76543210',
   '2021-03-15', TRUE),

  ('b1000001-0000-0000-0000-000000000002',
   'a1b2c3d4-0001-0001-0001-000000000001',
   'Carlos', 'Mendoza Vaca',
   'c.mendoza@lasamericas.bo', '+591 77812345',
   '2022-07-01', TRUE),

  ('b1000001-0000-0000-0000-000000000003',
   'a1b2c3d4-0001-0001-0001-000000000002',
   'Rosa', 'Terceros Suárez',
   'r.terceros@lasamericas.bo', '+591 71234567',
   '2020-01-10', TRUE),

  ('b1000001-0000-0000-0000-000000000004',
   'a1b2c3d4-0001-0001-0001-000000000003',
   'Juan Pablo', 'Ferrufino Ávila',
   'jp.ferrufino@lasamericas.bo', '+591 78901234',
   '2019-11-20', TRUE),

  ('b1000001-0000-0000-0000-000000000005',
   'a1b2c3d4-0001-0001-0001-000000000004',
   'Marcela', 'Orellana Pedraza',
   'm.orellana@lasamericas.bo', '+591 70000001',
   '2018-06-05', TRUE);

-- -------------------------------------------------------
-- 3. TIPOS DE HABITACIONES
-- -------------------------------------------------------
INSERT INTO content.tipos_habitaciones (id, nombre, descripcion, capacidad, precio_por_noche) VALUES
  ('c1000001-0000-0000-0000-000000000001',
   'Estándar Simple',
   'Habitación con cama matrimonial, TV, A/C y baño privado.',
   1, 180.00),

  ('c1000001-0000-0000-0000-000000000002',
   'Estándar Doble',
   'Habitación con dos camas simples, TV, A/C y baño privado.',
   2, 240.00),

  ('c1000001-0000-0000-0000-000000000003',
   'Suite Junior',
   'Sala de estar separada, cama king, jacuzzi y vista al jardín.',
   2, 420.00),

  ('c1000001-0000-0000-0000-000000000004',
   'Suite Ejecutiva',
   'Área de trabajo, sala, cama king, minibar y vista panorámica.',
   3, 650.00);

-- -------------------------------------------------------
-- 4. HABITACIONES
-- -------------------------------------------------------
INSERT INTO content.habitaciones (id, numero, piso, tipo_habitacion_id, estado) VALUES
  -- Piso 1: Estándar
  ('d1000001-0000-0000-0000-000000000001', '101', 1, 'c1000001-0000-0000-0000-000000000001', 'DISPONIBLE'),
  ('d1000001-0000-0000-0000-000000000002', '102', 1, 'c1000001-0000-0000-0000-000000000002', 'OCUPADA'),
  ('d1000001-0000-0000-0000-000000000003', '103', 1, 'c1000001-0000-0000-0000-000000000001', 'RESERVADA'),
  ('d1000001-0000-0000-0000-000000000004', '104', 1, 'c1000001-0000-0000-0000-000000000002', 'MANTENIMIENTO'),
  -- Piso 2: Mix
  ('d1000001-0000-0000-0000-000000000005', '201', 2, 'c1000001-0000-0000-0000-000000000002', 'DISPONIBLE'),
  ('d1000001-0000-0000-0000-000000000006', '202', 2, 'c1000001-0000-0000-0000-000000000003', 'OCUPADA'),
  -- Piso 3: Suites
  ('d1000001-0000-0000-0000-000000000007', '301', 3, 'c1000001-0000-0000-0000-000000000004', 'DISPONIBLE'),
  ('d1000001-0000-0000-0000-000000000008', '302', 3, 'c1000001-0000-0000-0000-000000000003', 'RESERVADA');

-- -------------------------------------------------------
-- 5. HUÉSPEDES
-- -------------------------------------------------------
INSERT INTO content.huespedes (id, nombre, apellido, documento_identidad, correo, telefono) VALUES
  ('e1000001-0000-0000-0000-000000000001',
   'Andrés', 'Salvatierra Rojas',
   'CI-5214789', 'andres.salvatierra@gmail.com', '+591 69871234'),

  ('e1000001-0000-0000-0000-000000000002',
   'Lucía', 'Peñaranda Vidal',
   'CI-8834512', 'lucia.penaranda@outlook.com', '+591 72345678'),

  ('e1000001-0000-0000-0000-000000000003',
   'Daniel', 'Morales Paz',
   'PAS-ARG-AA123456', 'd.morales@empresa.ar', '+54 9 11 5566 7788'),

  ('e1000001-0000-0000-0000-000000000004',
   'Sofía', 'Gutiérrez Herrera',
   'CI-3378821', 'sofia.gutierrez@hotmail.com', '+591 78234561'),

  ('e1000001-0000-0000-0000-000000000005',
   'Tomás', 'Baldivia Cuellar',
   'CI-9102345', NULL, '+591 76567890'),

  ('e1000001-0000-0000-0000-000000000006',
   'Camila', 'Ribera Antezana',
   'CI-6654321', 'c.ribera@ucb.edu.bo', '+591 71100234');

-- -------------------------------------------------------
-- 6. RESERVAS
-- -------------------------------------------------------
INSERT INTO content.reservas (
  id, habitacion_id,
  fecha_reserva, fecha_checkin_esperado, fecha_checkout_esperado,
  fecha_checkin_real, fecha_checkout_real,
  estado, observaciones
) VALUES
  -- Reserva 1: ya finalizada (hab 102)
  ('f1000001-0000-0000-0000-000000000001',
   'd1000001-0000-0000-0000-000000000002',
   '2025-05-20 10:00:00',
   '2025-05-22', '2025-05-25',
   '2025-05-22 13:30:00', '2025-05-25 11:00:00',
   'FINALIZADA', 'Cliente frecuente, se agradece atención especial.'),

  -- Reserva 2: en curso / checkin (hab 102, misma habitación nueva estadía)
  ('f1000001-0000-0000-0000-000000000002',
   'd1000001-0000-0000-0000-000000000002',
   '2025-06-01 09:15:00',
   '2025-06-03', '2025-06-07',
   '2025-06-03 14:00:00', NULL,
   'CHECKIN', NULL),

  -- Reserva 3: en curso / checkin (hab 202 - suite junior)
  ('f1000001-0000-0000-0000-000000000003',
   'd1000001-0000-0000-0000-000000000006',
   '2025-05-28 16:45:00',
   '2025-06-01', '2025-06-08',
   '2025-06-01 15:00:00', NULL,
   'CHECKIN', 'Viaje de negocios, requiere factura empresa.'),

  -- Reserva 4: pendiente / futura (hab 103)
  ('f1000001-0000-0000-0000-000000000004',
   'd1000001-0000-0000-0000-000000000003',
   '2025-06-02 11:00:00',
   '2025-06-10', '2025-06-12',
   NULL, NULL,
   'CONFIRMADA', 'Solicita cuna para bebé.'),

  -- Reserva 5: cancelada (hab 302 - suite junior)
  ('f1000001-0000-0000-0000-000000000005',
   'd1000001-0000-0000-0000-000000000008',
   '2025-05-15 08:30:00',
   '2025-05-30', '2025-06-02',
   NULL, NULL,
   'CANCELADA', 'Cancelación por fuerza mayor, sin cargo.');

-- -------------------------------------------------------
-- 7. RESERVA_HUÉSPEDES  (titular + acompañantes)
-- -------------------------------------------------------
INSERT INTO content.reserva_huespedes (id, reserva_id, huesped_id, es_titular) VALUES
  -- Reserva 1: Andrés titular
  ('aa000001-0000-0000-0000-000000000001',
   'f1000001-0000-0000-0000-000000000001',
   'e1000001-0000-0000-0000-000000000001', TRUE),

  -- Reserva 2: Lucía titular, Tomás acompañante
  ('aa000001-0000-0000-0000-000000000002',
   'f1000001-0000-0000-0000-000000000002',
   'e1000001-0000-0000-0000-000000000002', TRUE),
  ('aa000001-0000-0000-0000-000000000003',
   'f1000001-0000-0000-0000-000000000002',
   'e1000001-0000-0000-0000-000000000005', FALSE),

  -- Reserva 3: Daniel titular, Camila acompañante
  ('aa000001-0000-0000-0000-000000000004',
   'f1000001-0000-0000-0000-000000000003',
   'e1000001-0000-0000-0000-000000000003', TRUE),
  ('aa000001-0000-0000-0000-000000000005',
   'f1000001-0000-0000-0000-000000000003',
   'e1000001-0000-0000-0000-000000000006', FALSE),

  -- Reserva 4: Sofía titular
  ('aa000001-0000-0000-0000-000000000006',
   'f1000001-0000-0000-0000-000000000004',
   'e1000001-0000-0000-0000-000000000004', TRUE),

  -- Reserva 5: Andrés titular (la que canceló)
  ('aa000001-0000-0000-0000-000000000007',
   'f1000001-0000-0000-0000-000000000005',
   'e1000001-0000-0000-0000-000000000001', TRUE);

-- -------------------------------------------------------
-- 8. SERVICIOS
-- -------------------------------------------------------
INSERT INTO content.servicios (id, nombre, descripcion, precio, activo) VALUES
  ('ab000001-0000-0000-0000-000000000001',
   'Desayuno buffet',
   'Desayuno completo en restaurante, 07:00–10:00.',
   35.00, TRUE),

  ('ab000001-0000-0000-0000-000000000002',
   'Lavandería express',
   'Lavado y planchado en 4 horas.',
   55.00, TRUE),

  ('ab000001-0000-0000-0000-000000000003',
   'Transfer aeropuerto',
   'Traslado en vehículo privado al Aeropuerto Viru Viru.',
   120.00, TRUE),

  ('ab000001-0000-0000-0000-000000000004',
   'Minibar (recarga)',
   'Reposición de bebidas y snacks del minibar.',
   80.00, TRUE),

  ('ab000001-0000-0000-0000-000000000005',
   'Room service',
   'Servicio de comida a habitación (carta completa).',
   0.00, TRUE);  -- precio variable por ítem; se registra el monto real

-- -------------------------------------------------------
-- 9. RESERVA_SERVICIOS
-- -------------------------------------------------------
INSERT INTO content.reserva_servicios (
  id, reserva_id, servicio_id, cantidad, precio_unitario, fecha_consumo
) VALUES
  -- Reserva 1 (finalizada): desayunos x3 días, transfer de salida
  ('ac000001-0000-0000-0000-000000000001',
   'f1000001-0000-0000-0000-000000000001',
   'ab000001-0000-0000-0000-000000000001',
   3, 35.00, '2025-05-23 08:00:00'),

  ('ac000001-0000-0000-0000-000000000002',
   'f1000001-0000-0000-0000-000000000001',
   'ab000001-0000-0000-0000-000000000003',
   1, 120.00, '2025-05-25 10:00:00'),

  -- Reserva 2 (en curso): desayuno x2 personas, lavandería
  ('ac000001-0000-0000-0000-000000000003',
   'f1000001-0000-0000-0000-000000000002',
   'ab000001-0000-0000-0000-000000000001',
   2, 35.00, '2025-06-04 08:30:00'),

  ('ac000001-0000-0000-0000-000000000004',
   'f1000001-0000-0000-0000-000000000002',
   'ab000001-0000-0000-0000-000000000002',
   1, 55.00, '2025-06-04 10:00:00'),

  -- Reserva 3 (en curso): minibar, room service
  ('ac000001-0000-0000-0000-000000000005',
   'f1000001-0000-0000-0000-000000000003',
   'ab000001-0000-0000-0000-000000000004',
   1, 80.00, '2025-06-02 20:00:00'),

  ('ac000001-0000-0000-0000-000000000006',
   'f1000001-0000-0000-0000-000000000003',
   'ab000001-0000-0000-0000-000000000005',
   2, 65.00, '2025-06-03 21:30:00');

-- -------------------------------------------------------
-- 10. PAGOS
-- -------------------------------------------------------
INSERT INTO content.pagos (
  id, reserva_id, monto, concepto, metodo_pago, fecha_pago, estado
) VALUES
  -- Reserva 1 (finalizada): adelanto + liquidación final
  ('ad000001-0000-0000-0000-000000000001',
   'f1000001-0000-0000-0000-000000000001',
   180.00, 'ADELANTO', 'TARJETA',
   '2025-05-20 10:05:00', 'PAGADO'),

  ('ad000001-0000-0000-0000-000000000002',
   'f1000001-0000-0000-0000-000000000001',
   480.00, 'HOSPEDAJE', 'TRANSFERENCIA',  -- 3 noches × 180 - adelanto ya cobrado aparte
   '2025-05-25 11:10:00', 'PAGADO'),

  ('ad000001-0000-0000-0000-000000000003',
   'f1000001-0000-0000-0000-000000000001',
   225.00, 'SERVICIO', 'EFECTIVO',        -- desayunos + transfer
   '2025-05-25 11:10:00', 'PAGADO'),

  -- Reserva 2 (en curso): adelanto pagado, saldo pendiente
  ('ad000001-0000-0000-0000-000000000004',
   'f1000001-0000-0000-0000-000000000002',
   240.00, 'ADELANTO', 'QR',
   '2025-06-01 09:20:00', 'PAGADO'),

  ('ad000001-0000-0000-0000-000000000005',
   'f1000001-0000-0000-0000-000000000002',
   720.00, 'HOSPEDAJE', 'TARJETA',        -- saldo al hacer checkout (pendiente)
   '2025-06-03 14:05:00', 'PENDIENTE'),

  -- Reserva 3 (en curso): adelanto pagado
  ('ad000001-0000-0000-0000-000000000006',
   'f1000001-0000-0000-0000-000000000003',
   420.00, 'ADELANTO', 'TRANSFERENCIA',
   '2025-05-28 17:00:00', 'PAGADO'),

  -- Reserva 5 (cancelada): reembolso del adelanto
  ('ad000001-0000-0000-0000-000000000007',
   'f1000001-0000-0000-0000-000000000005',
   200.00, 'ADELANTO', 'TARJETA',
   '2025-05-15 08:35:00', 'REEMBOLSADO'),

  ('ad000001-0000-0000-0000-000000000008',
   'f1000001-0000-0000-0000-000000000005',
   200.00, 'REEMBOLSO', 'TARJETA',
   '2025-05-16 10:00:00', 'PAGADO');

-- -------------------------------------------------------
-- 11. MANTENIMIENTOS
-- -------------------------------------------------------
INSERT INTO content.mantenimientos (
  id, habitacion_id, empleado_id,
  fecha_inicio, fecha_fin, descripcion, estado
) VALUES
  -- Hab 104: en mantenimiento actualmente
  ('ae000001-0000-0000-0000-000000000001',
   'd1000001-0000-0000-0000-000000000004',
   'b1000001-0000-0000-0000-000000000004',
   '2025-06-03 08:00:00', NULL,
   'Reemplazo de grifo en ducha y revisión de instalación eléctrica del A/C.',
   'EN_PROCESO'),

  -- Hab 101: mantenimiento preventivo ya finalizado
  ('ae000001-0000-0000-0000-000000000002',
   'd1000001-0000-0000-0000-000000000001',
   'b1000001-0000-0000-0000-000000000004',
   '2025-05-10 09:00:00', '2025-05-10 13:00:00',
   'Revisión preventiva semestral: pintura, silicona de baño y limpieza de filtros de A/C.',
   'FINALIZADO'),

  -- Hab 302: mantenimiento programado antes de próxima reserva
  ('ae000001-0000-0000-0000-000000000003',
   'd1000001-0000-0000-0000-000000000008',
   NULL,   -- aún no asignado a empleado
   '2025-06-09 08:00:00', NULL,
   'Revisión del jacuzzi y cambio de luminarias LED en sala.',
   'PROGRAMADO');