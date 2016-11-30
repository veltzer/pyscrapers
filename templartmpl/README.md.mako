# **scrapers** project by ${tdefs.personal_fullname}

## What is it?

Scrapers for various stuff that I need off the web, maybe other people will like them too...:)

Currently I support downloading the public albums of a vk user.

## Installing

* Clone the repo
```bash
$ git clone https://github.com/veltzer/scrapers.git
```
* You need python3 installed. Usually it is but if it isn't:
```bash
$ sudo apt install python3
```
or
```bash
$ sudo yum install python3
```
* Install requirements using:
```bash
$ pip3 install --upgrade -r requirements.txt
```

## Running

```bash
  $ ./bin/scrape_vk_albums.py [user id in vk]
  $ ./bin/scrape_tg_albums.py [user id in travelgirls]
  $ ./bin/scrape_fb_albums.py [user id in facebook]
  $ ./bin/scrape_ig_albums.py [user id in instagram]
```
