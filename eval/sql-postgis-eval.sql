-- Complete this file by adding queries below each comment to perform the evaluation

------------------------------------------------------------------------------------------------------------------------
-- Using the airport table, compute the number of airports per country and type of airport,
-- and order the result by country and number of airports
[insert SQL query answer here]

--USING COPY to load data inside the tablemap_winnd_farm 
drop table if exists map_wind_farm;
create table map_wind_farm (
    id serial primary key ,
    facility_name text,
    facility text,
    facilitytype text,
    owner text,
    developer text,
    energypurchaser text,
    place text,
    generatingcapacity text,
    numberofunits text,
    commercialonlinedate text,
    windturbinemanufacturer text,
    facilitystatus text,
    coordinates text
);

COPY map_wind_farm(facility_name, facility, facilitytype, owner, developer,
                   energypurchaser, place, generatingcapacity, numberofunits,
                   commercialonlinedate, windturbinemanufacturer, facilitystatus, coordinates)
from '/data/map_wind_farm.csv'
with (format csv, header true);

--- Processing number of airports per country and type of airport
select count(*) as airport_country, iso_country, type
from airport
group by iso_country, type
order by iso_country, type desc; 

------------------------------------------------------------------------------------------------------------------------
-- Create a table containing all France airports by joining the airport and countries table spatially.
-- -> be cautious about tables spatial reference systems
-- SRS are not the same between tables: one must reproject one table to be able to work with data
-- for instance, reproject countries into 3857 SRID
[insert SQL query answer here]

-- Creation of the column geom inside table airport
alter table airport add column geom geometry(POINTZ, 3857);
update airport set geom = st_transform(
    st_setSRID(
        st_makePoint(longitude_deg,
            case when latitude_deg = -90 then -89.9 when latitude_deg = 90 then 89.9 else latitude_deg end,
            coalesce(elevation_ft * .3048, 0)), 4326), 3857);

-- Creation of the table france airports
drop table if exists france_airports; 
create table france_airports as (
	select a.*
from airport a join countries_inv c 
on st_intersects(a.geom, ST_Transform( st_setSRID(c.geom,4326), 3857))
where c.name = 'France'
	);
	
---***** Testify with the attribute join 
--This query returns 868 airports
select count(*) 
from france_airports;
-- using attribute join. This return 893
select count(*) 
from airport 
where iso_country = 'FR'; 




------------------------------------------------------------------------------------------------------------------------
-- Add a geometric column to the map_wind_farm table, with suitable geometric type and SRID (name this column “geom”)
-- 'coordinates' column gives us a point definition (2 coordinates)
-- in latitude/longitude format, but we want our geometry in SRID=3857:
-- lets create a POINT column in mercator SRS
[insert SQL query answer here]
select (regexp_split_to_array(replace(coordinates, '°', ''), ','))[1] as latitude, 
(regexp_split_to_array(replace(coordinates, '°', ''), ','))[2] as longitude 
from map_wind_farm ; 

-- Creation of the geom column 
alter table map_wind_farm add column geom geometry(POINT, 4326);

update map_wind_farm set geom =
st_setSRID(
 st_makePoint((regexp_split_to_array(replace(coordinates, '°', ''), ','))[2]::float, 
					 (regexp_split_to_array(replace(coordinates, '°', ''), ','))[1]::float), 
	4326); 

with point_table as (
	select st_setSRID(
 st_makePoint((regexp_split_to_array(replace(coordinates, '°', ''), ','))[2]::float, 
					 (regexp_split_to_array(replace(coordinates, '°', ''), ','))[1]::float), 
	4326) as geom1
from map_wind_farm) 
select st_transform(geom1 , 3857) as geom2
from point_table p;



------------------------------------------------------------------------------------------------------------------------
-- Populate the geom column by creating geometric objects based on column containing coordinates information
--  -> Use SQL functions to process data directly in the SELECT clause,
--  -> Functions like replace, regexp_split_to_array: use documentation to learn about these functions and how to use them
--  -> Use UPDATE command to populate the geom column
--  -> Use a join between the CTE creating the point and the map_wind_farm table
--  -> Use coordinate transformation in the query to store geometries in SRID 3857

-- lets create a Postgis POINT by parsing the coordinates column
-- coordinates as points: we look at the Postgis documentation to see a POINT geometry can be created based on x-y coordinates
-- (http://postgis.net/docs/ST_MakePoint.html)
-- By looking at the coordinates column, we see coordinates are decimal degrees with ° symbol:
-- 35.0861°, -118.3533°
-- to convert this column into 2 numnbers, we first remove the ° symbol, then parse the field on the comma into an array,
-- then create a postgis point from lonq and lat coordinates (x-y), and finally we transform this point to a POINT in SRID=3857 (mercator)
-- we first test our query in a select query
[insert SQL query answer here]

-- after a test with select, we can use update to update the table:
[insert SQL query answer here]


------------------------------------------------------------------------------------------------------------------------
-- Display the table in QGIS with countries table to check the position of map_wind_farm geometries
-- open qgis and load tables from postgis database. Add an OSM layer (QuickMapServices plugin) to check position of wind farms
-- [create screenshot img1.png to show qgis window with loaded tables]

------------------------------------------------------------------------------------------------------------------------
-- Create and use spatial index on the map_wind_farm and airport tables if they do not already exist, to speed-up the query
-- -> don't forget to analyse tables after index creation
create index on airport using gist(geom); 
create index on map_wind_farm using gist(geom); 

analyse airport; 
analyse map_wind_farm; 



------------------------------------------------------------------------------------------------------------------------
-- Using the map_wind_farm and airport tables, find the 3 farms closest to each US airport
-- -> Compute the distance in km between the airport and the farm
-- -> KNN query (as seen in slides)
-- -> Tables do not have the same SRID => need for reprojection
-- -> One must filter airports based on country (find the suitable column to filter on)
-- -> You can test parts of the final query in intermediate, smaller queries, then build the final query based on these steps

-- first filter on US airports: by looking at table values, we see the 'iso_country' column stores 2-letters country code
[insert SQL query answer here]
select * 
from airport 
where iso_country = 'US';

-- KNN SQL query to find wind farms close to each airport
[insert SQL query answer here]

select a.id as id_airport, m.id_wind,  a.iso_country,
       round(m.dist::numeric / 1000.0, 2) as dist_km
from airport a CROSS JOIN LATERAL (
    select f.id as id_wind, f.owner,
           a.geom <-> ST_Transform(f.geom, 3857)  as dist
    from map_wind_farm f
    where a.iso_country = 'US'
    order by a.geom <-> ST_Transform(f.geom, 3857) asc
    LIMIT 3
    ) as m;

-- In QGIS, display airport id = 20507, its 3 closest farms, and add an OSM base layer to check visually.

select a.id as id_airport, m.id_wind,  a.iso_country,
       round(m.dist::numeric / 1000.0, 2) as dist_km
from airport a CROSS JOIN LATERAL (
    select f.id as id_wind, f.owner,
           a.geom <-> ST_Transform(f.geom, 3857)  as dist
    from map_wind_farm f
    where a.id = '20507'
    order by a.geom <-> ST_Transform(f.geom, 3857) asc
    LIMIT 3
    ) as m;

	--as a
--order by id_wind, dist_km asc
--limit 3;

-- Use the distance tool to measure distance and compare with query result
-- load airport and map_wind_farm in QGIS from postgis database
-- create screenshot img2.png to show qgis window with loaded tables, OSM background, and distance tool
-- measuring one airport <-> wind farm distance

-- query to get the 3 closest windfarm from airport id=20507
[insert SQL query answer here]