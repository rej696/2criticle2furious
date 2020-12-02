-- Define database tables

-- Images table for referencing user and media profile pictures
create table images (
    id integer primary key autoincrement not null,
    title varchar(255),
    filepath varchar(255)
);

-- Media Database Tables

-- Movies table
create table movies (
    id integer primary key autoincrement not null,
    title varchar(255) not null,
    director varchar(255),
    genre varchar(255),
    summary text,
    image_id integer,
    foreign key (image_id) references images (id)
);

-- Books table
create table books (
    id integer primary key autoincrement not null,
    title varchar(255) not null,
    author varchar(255),
    genre varchar(255),
    summary text,
    image_id integer,
    foreign key (image_id) references images (id)
);

-- Categories Database
create table categories (
    id integer primary key autoincrement not null,
    media_type varchar(255) not null -- should reference the title of a media table
);

-- User Database
create table users (
    id integer primary key autoincrement not null,
    username varchar(255) unique not null,
    password varchar(255) not null,
    firstname varchar(255),
    lastname varchar(255),
    age integer,
    image_id integer
);

-- Review Map Database
create table reviews (
    id integer primary key autoincrement not null,
    category_id integer not null,
    media_id integer not null,
    user_id integer not null,
    body text,
    rating integer, -- enforce score out of 30
    foreign key (category_id) references categories(id),
    foreign key (user_id) references users(id)
);