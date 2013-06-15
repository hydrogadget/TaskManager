drop table if exists schedule;

create table schedule (
    schedule_id integer primary key autoincrement,
    valve integer not null,
    duration integer not null,
    start_time integer not null,
    mon integer default 0,
    tue integer default 0,
    wed integer default 0,
    thu integer default 0,
    fri integer default 0,
    sat integer default 0,
    sun integer default 0
);
