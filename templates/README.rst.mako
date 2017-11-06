# **pyscrapers** project by ${tdefs.personal_fullname}

## What is it?

Scrapers for various stuff that I need off the web, maybe other people will like them too...:)

Currently supports downloading photos from the following sites:
${tdefs.types}

## Installing

* Clone the repo
```bash
$ git clone https://github.com/veltzer/pyscrapers.git
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
  $ pyscrapers_photos --u [user_id] -t [type_of_site]
