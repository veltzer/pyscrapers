import json
import os
import shelve

import browser_cookie3
import requests
import logging
import lxml.html


from pyscrapers.utils import download_url, download_video_if_wider

# set up the logger
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)

# load cookies from browser
cookies = browser_cookie3.firefox()

# this means that we can use regular expression functions like 'match'
# by specifying 're:match' in our xpath expressions
ns = lxml.etree.FunctionNamespace("http://exslt.org/regular-expressions")
ns.prefix = 're'


def get_number_of_pages():
    url = "https://www.drumeo.com/laravel/public/members-area/json/lesson-group/courses?page=1"
    r = requests.get(url, cookies=cookies)
    assert r.status_code == 200
    content = r.content.decode()
    o = json.loads(content)
    d_page_count = o["pageCount"]
    return d_page_count


class Course:
    def __init__(self):
        self.number = None
        self.instructor = None
        self.name = None
        self.diff = None
        self.lessons = []
        self.resources = None
        self.videos = []

    def __repr__(self):
        return ",".join([self.number, self.name, self.instructor, self.diff, str(self.lessons), str(self.resources),
                        str(self.videos)])

    def add_lesson(self, lesson):
        self.lessons.append(lesson)

    def add_video(self, video, quality):
        self.videos.append((video, quality))


def get_courses(pages):
    courses = []
    for i in range(1, pages + 1):
        url = "https://www.drumeo.com/laravel/public/members-area/json/lesson-group/courses?page={}".format(i)
        r = requests.get(url, cookies=cookies)
        assert r.status_code == 200
        content = r.content.decode()
        o = json.loads(content)
        d_lessons = o["lessonsHtml"]
        for l in d_lessons:
            root = lxml.html.fromstring(l)
            # pyscrapers.utils.print_element(root)
            link_re = r"https://www.drumeo.com/laravel/public/members/lessons/courses/\d+"
            links = root.xpath('//a[re:match(@href,"{}")]'.format(link_re))
            assert len(links) == 2, len(links)
            course_number = links[0].get('href').split("/")[-1]
            titles = root.xpath('//h2[@class="card-title"]')
            assert len(titles) == 1
            title = titles[0].text
            instructors = root.xpath('//p[@class="card-sub-title card-instructor"]')
            assert len(instructors) == 1
            instructor = instructors[0].text
            diffs = root.xpath('//h3[@class="card-difficulty"]')
            assert len(diffs) == 1
            diff = diffs[0].text.strip()
            c = Course()
            c.instructor = instructor
            c.name = title
            c.number = course_number
            c.diff = diff
            courses.append(c)
    return courses


def get_course_details(course: Course):
    url = "https://www.drumeo.com/members/lessons/courses/{}".format(course.number)
    r = requests.get(url, cookies=cookies)
    assert r.status_code == 200
    content = r.content.decode()
    root = lxml.html.fromstring(content)
    lessons = root.xpath('//a[@class="course-lesson"]')
    for lesson in lessons:
        lesson_num = lesson.get('href').split('/')[-1]
        course.add_lesson(lesson_num)
    resources = root.xpath('//a[re:match(text(), "All Course Resources")]')
    if len(resources) == 1:
        resource = resources[0].get('href')
        course.resources = "http:"+resource


def get_course_urls(course):
    logger.info("doing course [%s]", course)
    for lesson in course.lessons:
        url = "https://www.drumeo.com/members/lessons/courses/{}".format(lesson)
        r = requests.get(url, cookies=cookies)
        assert r.status_code == 200
        content = r.content.decode()
        root = lxml.html.fromstring(content)
        videos = root.xpath('//div[@data-video-load-url]')
        assert len(videos) == 1
        video = videos[0].get('data-video-load-url')
        logger.info("url for video info is [%s]", video)
        r = requests.get(video, cookies=cookies)
        assert r.status_code == 200
        content = r.content.decode()
        data = json.loads(content)
        if 'error' in data:
            logger.info("error [%s]", data['error'])
            raise ValueError("errors, try later")
        if 'video-quality-urls' not in data:
            logger.info("did not find video-quality-urls")
            continue
        video_urls = data['video-quality-urls']
        quality_numbers = sorted([int(x) for x in video_urls.keys()])
        best_vid_key = str(quality_numbers[-1])
        # print(quality_numbers, best_vid_key)
        best_vid = video_urls[best_vid_key]
        course.add_video(best_vid, best_vid_key)


def download_course(course):
    folder_name = os.path.join("drumeo", course.number)
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    details = os.path.join(folder_name, "details.txt")
    if not os.path.isfile(details):
        with open(details, "wt") as file_handle:
            print("course_number: {}".format(course.number), file=file_handle)
            print("course_name: {}".format(course.name), file=file_handle)
            print("course_difficulty: {}".format(course.diff), file=file_handle)
            print("instructor: {}".format(course.instructor), file=file_handle)
    if course.resources is not None:
        download_url(course.resources, os.path.join(folder_name, "resources.zip"))
    for i, (video, quality) in enumerate(course.videos):
        download_video_if_wider(video, os.path.join(folder_name, "{}.mp4".format(i)), width=int(quality))


def main():
    pages = get_number_of_pages()
    courses = get_courses(pages)
    reload = set()
    with shelve.open("cache.db") as d:
        for i, course in enumerate(courses):
            logger.info("course number [%s]", i)
            if course.number in d and course.number not in reload:
                courses[i] = d[course.number]
                logger.info("got from cache [%s]", courses[i])
            else:
                get_course_details(course)
                get_course_urls(course)
                d[course.number] = course
            download_course(courses[i])

if __name__ == '__main__':
    main()
