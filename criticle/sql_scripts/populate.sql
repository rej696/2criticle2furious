

insert into users (username, password, firstname, lastname, age, summary) 
values ('rej696', 'pbkdf2:sha256:150000$YwmgWhU8$a91240efa27793be07681104e7fe5116bc7e53dc4fb807792d349030bb3b2743', 'rowan', 'saunders', 24, 'hi i am rowan and this is my review shop');
insert into users (username, password, firstname, lastname, age, summary) 
values ('handjacobsanitiser', 'pbkdf2:sha256:150000$YwmgWhU8$a91240efa27793be07681104e7fe5116bc7e53dc4fb807792d349030bb3b2743', 'hal', 'smith', 23, 'Hi there Im using whatsapp');

insert into categories (media_type) values ('movies');

insert into movies (title, director, genre, summary) 
values ('pacific rim', 'guillermo del torro', 'action', 'Big robots fight aliens from the sea');
insert into movies (title, genre, summary)
values ('touching the void', 'docudrama', 'Brave man climbs down mountain, nearly dies, is cold');

insert into reviews (category_id, media_id, user_id, body, rating)
values (
    (select id from categories where media_type is 'movies'),
    (select id from movies where title is 'pacific rim'),
    (select id from users where username is 'rej696'),
    'Excelent movie, just the right amount of robot fighting, with plenty of cliche dialog. Idris Elba is a living legend',
    30
);
insert into reviews (category_id, media_id, user_id, body, rating) values (
    (select id from categories where media_type is 'movies'),
    (select id from movies where title is 'touching the void'),
    (select id from users where username is 'handjacobsanitiser'),
    'Thrilling!... and moving 😭',
    25
);


insert into categories (media_type) values ('books');

insert into books (title, author, genre, summary) values (
    'the three body problem',
    'cixin liu',
    'science fiction',
    'Humanity dicovers an ancient and dying alien race living in the alpha centuri star system'
);

insert into reviews (category_id, media_id, user_id, body, rating) values (
    (select id from categories where media_type is 'books'),
    (select id from books where title is 'the three body problem'),
    (select id from users where username is 'rej696'),
    'Excelent scifi epic, especially interesting to read scifi from different cultures (the book is translated from mandarin)',
    23
);

select rating from reviews 
where media_id = (select id from movies where title is 'pacific rim') 
and category_id = (select id from categories where media_type is 'movies');