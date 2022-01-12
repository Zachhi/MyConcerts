
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

* Some way to compile and execute Java code
* SQL and PostgreSQL
* Access to Tamu network, either directly or through a VPN in order to access the database

### Installing and Executing

* Download the source code from github, or clone the repository into Visual Studio
* Change directory to <currentDir>/Reveilles-Reels/GUI
* Compile with `javac *.java`
* Execute with `java -cp ".;postgresql-42.2.8.jar" MainFile`. Use a `:` instead of a `;` if on Mac
* Type `V` for client view, or `A` for analyst view

## Authors

Zachary Chi - zachchi@tamu.edu
  
Emory Fields - emory.c.fields@tamu.edu
  
Morgan Roberts - morgan.roberts00@tamu.edu
  
Allison Edwards - allisone12@tamu.edu
  
Emma Haeussler - emmahaeussler@tamu.edu
  
## License

This project is licensed under the GNU General Public License v2.0 - see the LICENSE.md file for details
