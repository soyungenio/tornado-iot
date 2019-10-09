create table device
(
    id         serial                                             not null
        constraint device_pkey
            primary key
);

create table report
(
    id         serial                                             not null
        constraint report_pkey
            primary key,
    created_at timestamp with time zone default CURRENT_TIMESTAMP not null,
    report     varchar(32)                                        not null,
    device_id integer
        constraint device_device_id_fkey
            references device
            on update restrict on delete restrict
);

alter table device
    owner to postgres;

alter table report
    owner to postgres;