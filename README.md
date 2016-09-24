# *scrapers* project by Mark Veltzer

## What is it?

Scrapers for various stuff that I need off the web, maybe other people will like them too...:)

Currently I support downloading the public albums of a vk user.

## Installing

* Clone the repo
  `$ git clone https://github.com/veltzer/scrapers.git`
* You need python3 installed. Usually it is but if it isn't:
  `$ sudo apt install python3`
  or
  `$ sudo yum install python3`
* Install requirements using:
  `$ pip3 install --upgrade -r requirements.txt`

## Running

  `$ ./bin/scrape_vk_albums.py [user_id_in_vk]`
