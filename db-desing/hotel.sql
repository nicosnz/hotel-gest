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

    -- empleado_id UUID NOT NULL
    --     REFERENCES empleados(id),

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
    reserva_id UUID NOT NULL
        REFERENCES content.reservas(id)
        ON DELETE CASCADE,

    huesped_id UUID NOT NULL
        REFERENCES content.huespedes(id),

    es_titular BOOLEAN DEFAULT FALSE,

    PRIMARY KEY (reserva_id, huesped_id),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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