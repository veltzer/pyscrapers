import json
import logging
import os
from typing import IO

import lxml.html
import requests

from pyscrapers.core.utils import download_url, download_video_if_wider

# this means that we can use regular expression functions like 'match'
# by specifying 're:match' in our xpath expressions
ns = lxml.etree.FunctionNamespace("http://exslt.org/regular-expressions")
ns.prefix = 're'


def get_number_of_pages(courses: bool, cookies) -> int:
    if courses:
        url = "https://www.drumeo.com/laravel/public/members-area/json/lesson-group/courses?page=1"
    else:
        url = "https://www.drumeo.com/laravel/public/members-area/json/lesson-group/library?page=1"
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


def get_courses(pages, courses: bool, cookies):
    collected_courses = []
    for i in range(1, pages + 1):
        if courses:
            url = "https://www.drumeo.com/laravel/public/members-area/json/lesson-group/courses?page={}".format(i)
        else:
            url = "https://www.drumeo.com/laravel/public/members-area/json/lesson-group/library?page={}".format(i)
        r = requests.get(url, cookies=cookies)
        assert r.status_code == 200
        content = r.content.decode()
        o = json.loads(content)
        d_lessons = o["lessonsHtml"]
        for lesson_list in d_lessons:
            root = lxml.html.fromstring(lesson_list)
            # pyscrapers.utils.print_element(root)
            if courses:
                link_re = r"https://www.drumeo.com/laravel/public/members/lessons/courses/\d+"
            else:
                link_re = r"https://www.drumeo.com/laravel/public/members/lessons/library/\d+"
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
            collected_courses.append(c)
    return collected_courses


def get_course_details(course: Course, courses: bool, cookies):
    if courses:
        url = "https://www.drumeo.com/members/lessons/courses/{}".format(course.number)
    else:
        url = "https://www.drumeo.com/members/lessons/library/{}".format(course.number)
    r = requests.get(url, cookies=cookies)
    assert r.status_code == 200
    content = r.content.decode()
    root = lxml.html.fromstring(content)
    if courses:
        class_text = "course-lesson"
    else:
        class_text = "event-toggle download-lesson"
    lessons = root.xpath('//a[@class="{}"]'.format(class_text))
    for lesson in lessons:
        lesson_num = lesson.get('href').split('/')[-1]
        course.add_lesson(lesson_num)
    resources = root.xpath('//a[re:match(text(), "All Course Resources")]')
    if len(resources) == 1:
        resource = resources[0].get('href')
        course.resources = "http:"+resource
    if not courses:
        get_videos(root, course, cookies)


def get_course_urls(course, courses: bool, cookies):
    if not courses:
        return
    logger = logging.getLogger(__name__)
    logger.info("doing course [%s]", course)
    for lesson in course.lessons:
        if courses:
            url = "https://www.drumeo.com/members/lessons/courses/{}".format(lesson)
        else:
            url = "https://www.drumeo.com/members/lessons/library/{}".format(lesson)
        r = requests.get(url, cookies=cookies)
        assert r.status_code == 200
        content = r.content.decode()
        print(content)
        root = lxml.html.fromstring(content)
        get_videos(root, course, cookies)


def get_videos(root, course, cookies):
    logger = logging.getLogger(__name__)
    videos = root.xpath('//div[@data-video-load-url]')
    for video in videos:
        video_url = video.get('data-video-load-url')
        logger.info("url for video info is [%s]", video_url)
        r = requests.get(video_url, cookies=cookies)
        assert r.status_code == 200
        content = r.content.decode()
        data = json.loads(content)
        if 'error' in data:
            logger.info("error [%s]", data['error'])
            raise ValueError("errors, try later")
        if 'video-quality-urls' not in data:
            logger.info("did not find video-quality-urls")
            return
        video_urls = data['video-quality-urls']
        quality_numbers = sorted([int(x) for x in video_urls.keys()])
        best_vid_key = str(quality_numbers[-1])
        # print(quality_numbers, best_vid_key)
        best_vid = video_urls[best_vid_key]
        course.add_video(best_vid, best_vid_key)


def download_course(course):
    folder_name = os.path.join("drumeo", course.number)
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)
    details = os.path.join(folder_name, "details.txt")
    if not os.path.isfile(details):
        with open(details, "wt") as file_handle:  # type: IO[str]
            print("course_number: {}".format(course.number), file=file_handle)
            print("course_name: {}".format(course.name), file=file_handle)
            print("course_difficulty: {}".format(course.diff), file=file_handle)
            print("instructor: {}".format(course.instructor), file=file_handle)
    if course.resources is not None:
        download_url(course.resources, os.path.join(folder_name, "resources.zip"))
    for i, (video, quality) in enumerate(course.videos):
        download_video_if_wider(video, os.path.join(folder_name, "{}.mp4".format(i)), width=int(quality))
