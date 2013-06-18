drop table if exists schedule;
drop table if exists location;
drop table if exists valves;

create table schedule (
    schedule_id integer primary key autoincrement,
    valve integer not null,
    duration integer not null,
    start_time integer not null,
    sun integer default 0
    mon integer default 0,
    tue integer default 0,
    wed integer default 0,
    thu integer default 0,
    fri integer default 0,
    sat integer default 0
);

create table location (
    location_id integer primary key autoincrement,
    location_label text,
    street text,
    city text,
    state text,
    zip text
);

create table valves (
    valve_id integer primary key,
    valve_label text
);

insert into valves values (1,"Valve 1");
insert into valves values (2,"Valve 2");
insert into valves values (3,"Valve 3");
insert into valves values (4,"Valve 4");

