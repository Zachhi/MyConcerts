
# MyConcerts

A movie recommendation software created in a team of 5 that recommends movies to clients based on different parameters. There is both a client and an analyst side. The client side uses a clients data to analyze their watch history and preferences. The analyst side is for people who want to analyze what movies are popular and what movies they should create more of. Implemented using Java, Java Swing, SQL, and PostgreSQL. Waterfall methodology was used in planning and executing this project. 

Data is pulled from 5 different csv files, each with 500,000 lines of data. Data is pulled, formatted, and stored into an online database using java and SQL. The data is then  fetched from the online database using java and SQL in order to give the correct analysis and results.

Recommendations are based on many things, such as the client's top rated directors, movies, genres, similar movies, etc. Also based on movies other client's who watched
similar movies like, and more. There are many different utilities, such as a "movies to stay away from" and a "director's choice" section. The analyst side has a lot of ways
to analyze movies, such as determining what actors have chemistry, what movies have a cult following, and more.

I just moved this to my main github account instead of my school one.

## Demo

https://www.youtube.com/watch?v=bvd4KsevTKk


### Dependencies

* Some way to compile and execute Python code
* SQL
* Javascript, HTML, CSS, and Bootstrap are used. You do not need to worry about anything to use these though

### Installing and Executing

* Download the source code from github, or clone the repository
* Change directory to <currentDir>/concerts
* Run `pip install django` (if you don't already have Django)
* Run `pip install -r requirements.txt` (this will install all required libraries)
* Run `python manage.py runserver`
* A url will print, follow this url and you are done

## Authors

Zachary Chi - zachchi@tamu.edu
  
Emory Fields - emory.c.fields@tamu.edu
  
Morgan Roberts - morgan.roberts00@tamu.edu
  
Allison Edwards - allisone12@tamu.edu
  
Emma Haeussler - emmahaeussler@tamu.edu
  
## License

This project is licensed under the MIT License - see the LICENSE.md file for details
