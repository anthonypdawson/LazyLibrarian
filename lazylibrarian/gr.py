import time, threading, urllib, urllib2, sys, re
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

import lazylibrarian
from lazylibrarian import logger, formatter, database

class GoodReads:
    # http://www.goodreads.com/api/

    def __init__(self, name=None, type=None):
        self.name = {"id": name}
        self.type = type
        self.params = {"key":  lazylibrarian.GR_API}

    def find_author_id(self):

        URL = 'http://www.goodreads.com/api/author_url/?' + urllib.urlencode(self.name) + '&' + urllib.urlencode(self.params)
        logger.info("Searching for author with name: %s" % self.name)

        try:
            sourcexml = ElementTree.parse(urllib2.urlopen(URL, timeout=20))
        except (urllib2.URLError, IOError, EOFError), e:
            logger.error("Error fetching authorid: ", e)
        
        rootxml = sourcexml.getroot()
        resultxml = rootxml.getiterator('author')
        authorlist = []

        if not len(rootxml):
            logger.info('No authors found with name: %s' % self.name)
            return authorlist
        else:
            for author in resultxml:
                authorid = author.attrib.get("id")
                logger.info('Found author: %s with GoodReads-id: %s' % (author[0].text, authorid))

            time.sleep(5)
            authorlist = self.get_author_info(authorid)
        
        return authorlist

    def get_author_info(self, authorid=None):

        URL = 'http://www.goodreads.com/author/show/' + authorid + '.xml?' + urllib.urlencode(self.params)
        sourcexml = ElementTree.parse(urllib2.urlopen(URL, timeout=20))
        rootxml = sourcexml.getroot()
        resultxml = rootxml.find('author')
        author_dict = {}

        if not len(rootxml):
            logger.info('No author found with ID: ' + authorid)

        else:
            logger.info("Processing info for authorID: %s" % authorid)

            author_dict = {
                'authorid':   resultxml[0].text,
                'authorlink':   resultxml.find('link').text,
                'authorimg':  resultxml.find('image_url').text,
                'authorborn':   resultxml.find('born_at').text,
                'authordeath':  resultxml.find('died_at').text,
                'totalbooks':   resultxml.find('works_count').text
                }
        return author_dict

    def get_author_books(self, authorid=None):

        URL = 'http://www.goodreads.com/author/list/' + authorid + '.xml?' + urllib.urlencode(self.params)
        sourcexml = ElementTree.parse(urllib2.urlopen(URL, timeout=20))
        rootxml = sourcexml.getroot()
        resultxml = rootxml.getiterator('book')
        books_dict = []

        if not len(rootxml):
            logger.info('No books found for author with ID: %s' % authorid)

        else:
            logger.info("Processing books for author with ID: %s" % authorid)

            resultsCount = 0
            removedResults = 0

			#CANT FIND ANY OF THE BOOKS ATTRIBUTES: SEE URL http://www.goodreads.com/author/list/4399719.xml?key=ckvsiSDsuqh7omh74ZZ6Q
            for book in resultxml:
	                #logger.info("Found %s " % book.find('description').text)
	
	                #if (book.find('publication_day').text == None):
	                    #pubday = "01"
	                #else:
	                    #pubday = book.find('publication_day').text
	
	                #if (book.find('publication_month').text == None):
	                    #pubmonth = "01"
	                #else:
	                    #pubmonth = book.find('publication_month').text
	
	                if (book.find('publication_year').text == None):
	                    pubyear = "0000"
	                else:
	                    pubyear = book.find('publication_year').text

	                authorNameResult = book.find('./authors/author/name').text
	
	                try:
	                    bookimg = book.find('image_url').text
	                    if (bookimg == 'http://www.goodreads.com/assets/nocover/111x148.png'):
	                    	bookimg = 'images/nocover.png'
	                except KeyError:
	                    bookimg = 'images/nocover.png'
	                except AttributeError:
	                    bookimg = 'images/nocover.png'
	
	                #pubdate = ''.join([pubyear, '-', pubmonth, '-', pubday])
	                
	                if not (re.match('[^\w-]', book.find('title').text)): #remove books with bad caracters in title
	                	if not pubyear == "0000":
	                		books_dict.append({
	                    		'authorname': authorNameResult,
                        		'bookid': book.find('id').text,
                        		'bookname': book.find('title').text,
                        		'booksub': "",
                        		'bookisbn': book.find('isbn').text,
                        		'bookpub': book.find('publisher').text,
                        		'bookdate': pubyear,
                        		'booklang': "en", #No language attribute provided by goodreads, put default as english
                        		'booklink': book.find('link').text,
                        		'bookrate': float(book.find('average_rating').text),
                        		'bookimg': bookimg,
                        		'bookpages': book.find('num_pages').text,
                        		'bookgenre': "",
                        		'bookdesc': book.find('description').text
	                			})
	                		resultsCount = resultsCount + 1
	                else:
						removedResults = removedResults + 1
					
        logger.info("Removed %s non-english and no publication year results for author" % removedResults)
					
	                #logger.info("Found %s " % book.tag)
	                #logger.info("Found %s " % book.find('title').text)
        logger.info("Found %s books for author" % resultsCount)
        return books_dict
		
    def find_results(self, authorname=None):
		resultlist = []
		logger.info(authorname)
		url = urllib.quote_plus(authorname)
		set_url = 'http://www.goodreads.com/search.xml?q=' + url + '&' + urllib.urlencode(self.params)

		logger.info('Searching for author at: %s' % set_url)

		try:
			sourcexml = ElementTree.parse(urllib2.urlopen(set_url, timeout=20))
			rootxml = sourcexml.getroot()
			resultxml = rootxml.getiterator('work')
			author_dict = []
			resultcount = 0
			for author in resultxml:
				bookdate = "0001-01-01"
				#try:
					#if (author.find('original_publication_day').text == None):
						#pubday = "01"
					#else:
						#pubday = author.find('original_publication_day').text

						#if (author.find('original_publication_month').text == None):
							#pubmonth = "01"
						#else:
							#pubmonth = author.find('original_publication_month').text

						#if (author.find('original_publication_year').text == None):
							#pubyear = "0001"
						#else:
							#pubyear = author.find('original_publication_year').text

						#bookdate = ''.join([pubyear, '-', pubmonth, '-', pubday])

				#except KeyError:
					#bookdate = "0001-01-01"
						
				if (author.find('original_publication_year').text == None):
					bookdate = "0000"
				else:
					bookdate = author.find('original_publication_year').text
		
				authorNameResult = author.find('./best_book/author/name').text
				booksub = ""
				bookpub = ""
				booklang = "en"
				
				try:
					bookimg = author.find('./best_book/image_url').text
					if (bookimg == 'http://www.goodreads.com/assets/nocover/111x148.png'):
						bookimg = 'images/nocover.png'
				except KeyError:
					bookimg = 'images/nocover.png'
				except AttributeError:
					bookimg = 'images/nocover.png'

				try:
					bookrate = author.find('average_rating').text
				except KeyError:
					bookrate = 0

				bookpages = '0'
				bookgenre = ''
				bookdesc = 'Not available'
				
				bookisbn = author.find('./best_book/id').text
				
				if (author.find('./best_book/title').text == None):
					bookTitle = ""
				else:
					bookTitle = author.find('./best_book/title').text

				resultlist.append({
					'authorname': author.find('./best_book/author/name').text,
					'bookid': author.find('./best_book/id').text,
					'authorid' : author.find('./best_book/author/id').text,
					'bookname': bookTitle.encode("ascii", "ignore"),
					'booksub': booksub,
					'bookisbn': bookisbn,
					'bookpub': bookpub,
					'bookdate': bookdate,
					'booklang': booklang,
					'booklink': '/',
					'bookrate': float(bookrate),
					'bookimg': bookimg,
					'bookpages': bookpages,
					'bookgenre': bookgenre,
					'bookdesc': bookdesc
				})

				resultcount = resultcount+1

	        except urllib2.HTTPError, err:               	
	        	if err.code == 404:
		        	logger.info('Received a 404 error when searching for author')
		        if err.code == 403:
		            	logger.info('Access to api is denied: usage exceeded')
		        else:
		                logger.info('An unexpected error has occurred when searching for an author')

	        logger.info('Found %s results' % (resultcount))

		return resultlist


