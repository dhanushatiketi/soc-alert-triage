-- Initialize PostgreSQL database for SOC Alert Triage

-- Create schema
CREATE SCHEMA IF NOT EXISTS soc;

-- Set search path
ALTER DATABASE soc_alerts SET search_path = public, soc;

-- Log initialization
SELECT 'Database initialization completed' as status;