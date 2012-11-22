## LazyLibrarian
#### Contributers 
* Current author: LibrarianMike  
* Original author: Mar2zz  
* Previous maintainer: itsmegb   

#### LazyLibrarian
LazyLibrarian is a program to follow authors and grab metadata for all your digital reading needs. 
It uses Goodreads.com (for author info and book info) websites as a source. License: GNU GPL v3 

Right now its capable of the following:  
* find authors and add them to the database  
* list all books of an author and add them as 'wanted'.  
* LazyLibrarian will search a nzb-file for that book (only Newznab and nzbmatrix are currently supported)  
* If a nzb is found it will be send to sabnzbd or saved in a blackhole where your downloadapp can pick it up.  
* When processing the downloaded books it will save a coverpicture (if available) and save all metadata into metadata.opf next to the bookfile (calibre compatible format)
* The new theme for the site allows it to be accessed (and usable) from devices with a smaller screen (such as an iPad)

##Screenshots
<img src="http://i.imgur.com/4sQDZ.png" width="600">
<img src="http://i.imgur.com/fr0yE.png" width="600">
<img src="http://i.imgur.com/AOgh1.png" width="600">

## Install:  
LazyLibrarian runs by default on port 8082 at http://hostname:8082/

Linux / Mac OS X:

* Install Python 2.6 or higher  
* Git clone/extract LL wherever you like  
* Run "python LazyLibrarian.py -daemon" to start in deamon mode  
* Set your username & password in the settings if you want.  
* Fill in all the config fields