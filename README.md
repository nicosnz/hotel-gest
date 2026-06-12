# Sistema de Gestión de Hotel

Software para la administración de servicios de un hotel.

## Pasos para usar el sistema

- Clonar el repositorio
- Renombrar el archivo `.env-template` a `.env`
- Ejecutar:

```bash
docker compose up -d --build
```

- Para ver /admin: `http://localhost:80/admin`
- Para ver /: `http://localhost:80/`

## Correr pruebas en SonarQube

- Ejecutar:

```bash
docker compose -f docker-compose.sonar.yml up -d
```

- Ir a: `http://localhost:9000`
- Login inicial: `admin` / `admin`
- Ejecutar el scanner:

```bash
docker run --rm `
  -v "${PWD}:/usr/src" `
  -e SONAR_HOST_URL="http://host.docker.internal:9000" `
  -e SONAR_TOKEN="<pega-tu-token-aqui>" `
  sonarsource/sonar-scanner-cli

```

- Volver a: `http://localhost:9000`

## Correr pruebas de estrés con JMeter

- Asegurarse que la app este corriendo:

```bash
docker compose up -d --build
```

- Ejecutar JMeter via Docker:

```bash
docker run --rm `
  -v "${PWD}/jmeter:/jmeter" `
  justb4/jmeter `
  -n -t /jmeter/test-plan.jmx `
  -l /jmeter/results-all.jtl `
  -e -o /jmeter/report

```

- Cuando termine, el reporte completo esta en `jmeter/report/index.html`

## Análisis de Vulnerabilidades mediante OWASP ZAP

- Scan de baseline:

```bash
docker run --rm `
  -v "${PWD}/zap-reports:/zap/wrk/:rw" `
  ghcr.io/zaproxy/zaproxy:stable `
  zap-baseline.py `
  -t http://host.docker.internal `
  -r zap-baseline.html `
  -I

```

- Scan de API:

```bash
docker run --rm `
  -v "${PWD}/zap-reports:/zap/wrk/:rw" `
  ghcr.io/zaproxy/zaproxy:stable `
  zap-api-scan.py `
  -t http://host.docker.internal/openapi.json `
  -f openapi `
  -r zap-api.html `
  -I

```

Los reportes quedan en `zap-reports/`
