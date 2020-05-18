"""
Download course material from drumeo
"""

import json
import logging
import os

import lxml.html

from pyscrapers.core.utils import download_url, download_video_if_wider

# this means that we can use regular expression functions like 'match'
# by specifying 're:match' in our xpath expressions
ns = lxml.etree.FunctionNamespace("http://exslt.org/regular-expressions")
ns.prefix = 're'


def get_number_of_pages(courses: bool, session) -> int:
    """
    Get the number of pages for all courses or pages
    :param courses:
    :param session:
    :return:
    """
    if courses:
        url = "https://www.drumeo.com/laravel/public/members-area/json/lesson-group/courses?page=1"
    else:
        url = "https://www.drumeo.com/laravel/public/members-area/json/lesson-group/library?page=1"
    result = session.get(url)
    assert result.status_code == 200
    content = result.content.decode()
    obj = json.loads(content)
    d_page_count = obj["pageCount"]
    return d_page_count


class Course:
    """
    This is an object representing one course
    """
    def __init__(self):
        """
        constructor
        """
        self.number = 0
        self.instructor = None
        self.name = None
        self.diff = None
        self.lessons = []
        self.resources = None
        self.videos = []

    def __repr__(self):
        """
        nice representation of this object
        :return:
        """
        return ",".join([
            self.number, self.name, self.instructor, self.diff,
            str(self.lessons), str(self.resources),
            str(self.videos)])

    def add_lesson(self, lesson):
        """
        Add a lesson to the course
        :param lesson:
        :return:
        """
        self.lessons.append(lesson)

    def add_video(self, video, quality):
        """
        Add a video to the course
        :param video:
        :param quality:
        :return:
        """
        self.videos.append((video, quality))


def get_url(courses: bool, page: int) -> str:
    if courses:
        url = "https://www.drumeo.com/laravel/public/members-area/json/lesson-group/courses?page={}".format(page)
    else:
        url = "https://www.drumeo.com/laravel/public/members-area/json/lesson-group/library?page={}".format(page)
    return url


def get_members_url(courses: bool, number: int) -> str:
    if courses:
        url = "https://www.drumeo.com/members/lessons/courses/{}".format(number)
    else:
        url = "https://www.drumeo.com/members/lessons/library/{}".format(number)
    return url


def get_link_re(courses: bool) -> str:
    if courses:
        link_re = r"https://www.drumeo.com/laravel/public/members/lessons/courses/\d+"
    else:
        link_re = r"https://www.drumeo.com/laravel/public/members/lessons/library/\d+"
    return link_re


def get_courses(pages, courses: bool, session):
    """
    Download the list of all the courses
    :param pages:
    :param courses:
    :param session:
    :return:
    """
    collected_courses = []
    for page in range(1, pages + 1):
        result = session.get(get_url(courses, page))
        assert result.status_code == 200
        for lesson_list in json.loads(result.content.decode())["lessonsHtml"]:
            course = Course()
            root = lxml.html.fromstring(lesson_list)
            links = root.xpath('//a[re:match(@href,"{}")]'.format(get_link_re(courses)))
            assert len(links) == 2, len(links)
            course.number = links[0].get('href').split("/")[-1]
            titles = root.xpath('//h2[@class="card-title"]')
            assert len(titles) == 1
            course.name = titles[0].text
            instructors = root.xpath('//p[@class="card-sub-title card-instructor"]')
            assert len(instructors) == 1
            course.instructor = instructors[0].text
            diffs = root.xpath('//h3[@class="card-difficulty"]')
            assert len(diffs) == 1
            course.diff = diffs[0].text.strip()
            collected_courses.append(course)
    return collected_courses


def get_course_details(course: Course, courses: bool, session):
    """
    Populate the Course type object
    :param course:
    :param courses:
    :param session:
    :return:
    """
    result = session.get(get_members_url(courses, course.number))
    assert result.status_code == 200
    content = result.content.decode()
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
        get_videos(root, course, session)


def get_course_urls(course, courses: bool, session):
    if not courses:
        return
    logger = logging.getLogger(__name__)
    logger.info("doing course [%s]", course)
    for lesson in course.lessons:
        if courses:
            url = "https://www.drumeo.com/members/lessons/courses/{}".format(lesson)
        else:
            url = "https://www.drumeo.com/members/lessons/library/{}".format(lesson)
        result = session.get(url)
        assert result.status_code == 200
        content = result.content.decode()
        print(content)
        root = lxml.html.fromstring(content)
        get_videos(root, course, session)


def get_videos(root, course, session):
    """
    Get all the videos pertaining to a certain course
    :param root:
    :param course:
    :param session:
    :return:
    """
    logger = logging.getLogger(__name__)
    videos = root.xpath('//div[@data-video-load-url]')
    for video in videos:
        video_url = video.get('data-video-load-url')
        logger.info("url for video info is [%s]", video_url)
        result = session.get(video_url)
        assert result.status_code == 200
        content = result.content.decode()
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


def download_course(course, session):
    """
    Download a course
    :param course:
    :param session:
    :return:
    """
    folder_name = os.path.join("drumeo", course.number)
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)
    details = os.path.join(folder_name, "details.txt")
    if not os.path.isfile(details):
        with open(details, "wt") as file_handle:
            print("course_number: {}".format(course.number), file=file_handle)
            print("course_name: {}".format(course.name), file=file_handle)
            print("course_difficulty: {}".format(course.diff), file=file_handle)
            print("instructor: {}".format(course.instructor), file=file_handle)
    if course.resources is not None:
        download_url(course.resources, os.path.join(folder_name, "resources.zip"), session)
    for i, (video, quality) in enumerate(course.videos):
        download_video_if_wider(session, video, os.path.join(folder_name, "{}.mp4".format(i)), width=int(quality))
