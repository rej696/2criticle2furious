

insert into users (username, firstname, lastname, age) 
values ('rej696', 'Rowan', 'Saunders', 24);
insert into users (username, firstname, lastname, age) 
values ('handjacobsanitiser', 'Hal', 'Smith', 23);

insert into categories (media_type) values ('movie');

insert into movies (title, director, genre, summary) 
values ('Pacific Rim', 'Guillermo Del Torro', 'Action', 'Big robots fight aliens from the sea');
insert into movies (title, genre, summary)
values ('Touching the Void', 'Docudrama', 'Brave man climbs down mountain, nearly dies, is cold');

insert into reviews (category_id, media_id, user_id, body, rating)
values (
    (select id from categories where media_type is 'movie'),
    (select id from movies where title is 'Pacific Rim'),
    (select id from users where username is 'rej696'),
    'Excelent movie, just the right amount of robot fighting, with plenty of cliche dialog. Idris Elba is a living legend',
    30
);
insert into reviews (category_id, media_id, user_id, body, rating) values (
    (select id from categories where media_type is 'movie'),
    (select id from movies where title is 'Touching the Void'),
    (select id from users where username is 'handjacobsanitiser'),
    'Thrilling!... and moving 😭',
    25
);


insert into categories (media_type) values ('book');

insert into books (title, author, genre, summary) values (
    'The Three Body Problem',
    'Cixin Liu',
    'Science Fiction',
    'Humanity dicovers an ancient and dying alien race living in the alpha centuri star system'
);

insert into reviews (category_id, media_id, user_id, body, rating) values (
    (select id from categories where media_type is 'book'),
    (select id from books where title is 'The Three Body Problem'),
    (select id from users where username is 'rej696'),
    'Excelent scifi epic, especially interesting to read scifi from different cultures (the book is translated from mandarin)',
    23
);

select rating from reviews 
where media_id = (select id from movies where title is 'Pacific Rim') 
and category_id = (select id from categories where media_type is 'movie');