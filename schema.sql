drop table if exists schedule;
drop table if exists location;
drop table if exists valves;

create table schedule (
    id integer primary key autoincrement,
    valve integer not null,
    duration integer not null,
    start_time integer not null,
    sun integer default 0,
    mon integer default 0,
    tue integer default 0,
    wed integer default 0,
    thu integer default 0,
    fri integer default 0,
    sat integer default 0
);

insert into schedule values (null,1,10,1010,1,1,1,1,1,1,1);
insert into schedule values (null,2,10,1010,1,1,1,1,1,1,1);
insert into schedule values (null,3,10,1010,1,1,1,1,1,1,1);
insert into schedule values (null,4,10,1010,1,1,1,1,1,1,1);

create table valves (
    id integer primary key,
    gpio_id integer,
    label text
);

insert into valves values (1,24,"Valve 1");
insert into valves values (2,23,"Valve 2");
insert into valves values (3,22,"Valve 3");
insert into valves values (4,18,"Valve 4");

create table location (
    id integer primary key default 1,
    label text,
    street text,
    city text,
    state text,
    zip text
);

insert into location values (1, 'Home','8085 Chestnut Glen Ave', 'Las Vegas', 'NV', '89131');

create table network_settings (
    ip string,
    ssid string,
    username string,
    password string
);

create table water_group (
    water_group string,
    days_of_week string
    district string
)
