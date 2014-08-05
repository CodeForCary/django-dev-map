-- These steps are required to setup the permit database
CREATE EXTENSION postgis;
CREATE EXTENSION unaccent;
ALTER FUNCTION unaccent(text) IMMUTABLE;
