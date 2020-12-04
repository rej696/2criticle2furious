# 2criticle2furious

## Requirements
### Must:
- Media (Book/Movie/Music) Database: Have a database of Media information for each media type (category) (e.g for books: System ID, Author, Title, Genre, Publish Date, Edition,  ISBN, Blurb/Summary, Image ID)

- User Database: Have a database of Customer information: Name, Address, (Bank details, Age, Bio, Profile Image ID).

- Review Map Database: Customer Media (Book/Movie) Map (Category: Media ID: Customer ID: Star Rating: Comment)

- Category Database: If having different media types available (i.e. movies, and books) need to have a database that maps the media type to their respective media databases (ID: Category Name: Database ID)

- User stories: 
    - add new entry to Media Database;
    - register user in User Database; 
    - create review in Review Map Database; 
    - modify review in Review Map Database;
    - remove review in Review Map Database; 
    - list/search media functions:
    - List all media data (all entries in all Media Databases in all Category Database); 
    - List all entries in Category (data in single Media Database);
    - List all with title/other attribute (in Category) (data in single Media Database);
    - List all reviews in Category (data in Review Map Database with given Category).
    - List reviews in Category for User ID (data in Review Map Database with given Category and User ID/User-name)

- Have a central feed with most recent reviews/activity of (followed) user profiles


### Should:
- Have a distinct profile page for each media
- Have user profiles
- Have basic cross-device compatibility.

### Could:
- Be able to export data to csv for analysis (i.e. take movie watchlist and rankings of current user, or export movie rankings from multiple users)
- Implement recommendations based on previous user ratings
- Create new categories of media (i.e. dynamically create database table with user defined headings (from a list of predefined categories)
- Upload images (e.g. book/movie covers) when creating new media entries.
- Users can upload profile pictures.
- Users should be able to follow/friend other user profiles
- Database for mapping between user id and id of user to follow
- User should be able to switch between public profile and private (only followers can see posted reviews)
- Optimise cross-device compatibility.
