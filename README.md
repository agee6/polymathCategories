# Python script for polymath

#### This python script pulls data from ebay categories api and store the information in an sql database. The information can then be rendered in HTML

## Documentation

#### There are commands the code can take from the shell, they are:

### --rebuild
#### this will trigger a call to the ebay API and rebuild the database

### --render <category_id>
#### this command will render an HTML page based on what category_id the user feeds it.

### for example:

```
$ python3 categories.py --rebuild
database built successfully
$ python3 categories.py --render 888
successfully rendered html file. You may now open 888.htmlin your browser
$ python3 categories.py --render 999999999
No category with ID:999999999
$ python3 categories.py --bananagram
Error: invalid command
```

#### Once you have successfully rendered an html file it should look like this:

![screen shot][screen]

[screen]: ScreenShot.png

## Database:
### the schema is a single table with five columns: "CategoryID", "CategoryName", "CategoryLevel", "BestOfferEnabled", and "Parent CategoryID".

## Next steps

#### If I were to put some more time into this I would do several things. One I would add some more pizzaz to the css. In particular I would make it somewhat like a drop down, that you could click on the items and have their children appear and disappear like a file tree in windows. Also right now I have a pretty basic schema. I believe I could make it faster by dividing things up into tables based on level, this would lead to small gains in render time, but an increase in rebuild speed which is already the slowest aspect. Finally, possibly most important of all I would add a lot more checks and catches to cover for things going wrong.
