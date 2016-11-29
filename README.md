# *scrapers* project by Mark Veltzer


Scrapers for various stuff that I need off the web, maybe other people will like them too...:)

Currently I support downloading the public albums of a vk user.


* Clone the repo
  `$ git clone https://github.com/veltzer/scrapers.git`
* You need python3 installed. Usually it is but if it isn't:
  `$ sudo apt install python3`
  or
  `$ sudo yum install python3`
* Install requirements using:
  `$ pip3 install --upgrade -r requirements.txt`


  `$ ./bin/scrape_vk_albums.py [user id in vk]`
  `$ ./bin/scrape_tg_albums.py [user id in travelgirls]`
  `$ ./bin/scrape_fb_albums.py [user id in facebook]`
  `$ ./bin/scrape_ig_albums.py [user id in instagram]`
