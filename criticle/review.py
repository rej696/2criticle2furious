class Review:

    def __init__(self, db, review_raw):
        category_id = review_raw['category_id']
        self.category = db.execute('select media_type from categories where id is ?', (category_id,)).fetchone()[0]
        self.rating = review_raw['rating']
        self.body = review_raw['body']
        media_id = review_raw['media_id']
        self.title = db.execute(f'select title from {self.category} where id is ?', (media_id,)).fetchone()[0]
        user_id = review_raw['user_id']
        self.user = db.execute('select username from users where id is ?', (user_id,)).fetchone()[0]

        self.capitalise_attributes()
    
    def capitalise_attributes(self):
        pass
        # self.category = self.category.title()
        # self.title = self.title.title()
