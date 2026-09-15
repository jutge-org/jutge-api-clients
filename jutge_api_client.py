"""
This file has been automatically generated at 2025-10-07T13:36:19.405Z

Name:    Jutge API
Version: 2.0.0

Description:

Jutge API

"""


# In order to use this module, you should install its dependencies using pip:
# python3 -m pip install requests requests-toolbelt pyyaml rich pydantic
# A recent version of Python (3.11 or newer) is required.


# pyright: reportUnusedVariable=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownArgumentType=false

# pylint: disable=line-too-long, too-many-lines, unused-variable, fixme, redefined-builtin, too-many-instance-attributes, too-few-public-methods, too-many-locals

from __future__ import annotations

import json
import os
import re
from typing import Any, Type, Optional, BinaryIO
from pydantic import BaseModel, TypeAdapter, Field
from pydantic_core import to_jsonable_python
from requests_toolbelt.multipart import decoder  # type: ignore
from rich import print
import yaml
import requests


# Models


class CredentialsIn(BaseModel):
    """
    No description yet
    """

    email: str
    password: str


class ExamCredentialsIn(BaseModel):
    """
    No description yet
    """

    email: str
    password: str
    exam: str
    exam_password: str


class CredentialsOut(BaseModel):
    """
    No description yet
    """

    token: str
    expiration: str
    user_uid: str
    error: str


class Time(BaseModel):
    """
    No description yet
    """

    full_time: str
    int_timestamp: int
    float_timestamp: float
    time: str
    date: str


class HomepageStats(BaseModel):
    """
    No description yet
    """

    users: int
    problems: int
    submissions: int
    exams: int
    contests: int


type ColorMapping = dict[str, dict[str, str]]


class ApiVersion(BaseModel):
    """
    No description yet
    """

    version: str
    mode: str
    gitHash: str
    gitBranch: str
    gitDate: str


class RequestInformation(BaseModel):
    """
    No description yet
    """

    url: str
    ip: str
    domain: str


class Language(BaseModel):
    """
    No description yet
    """

    language_id: str  # Id of the language
    eng_name: str  # English name of the language
    own_name: str  # Name of the language in its own language


class Country(BaseModel):
    """
    No description yet
    """

    country_id: str  # Id of the country
    eng_name: str  # English name of the country


class Compiler(BaseModel):
    """
    No description yet
    """

    compiler_id: str  # Id of the compiler
    name: str
    language: str
    extension: str
    description: Optional[str] = Field(default=None)
    version: Optional[str] = Field(default=None)
    flags1: Optional[str] = Field(default=None)
    flags2: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    warning: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)


class Driver(BaseModel):
    """
    No description yet
    """

    driver_id: str  # Id of the driver


class Verdict(BaseModel):
    """
    No description yet
    """

    verdict_id: str  # Id of the verdict
    name: str
    description: str
    emoji: str


class Proglang(BaseModel):
    """
    No description yet
    """

    proglang_id: str  # Id of the proglang


class AllTables(BaseModel):
    """
    No description yet
    """

    languages: dict[str, Language]
    countries: dict[str, Country]
    compilers: dict[str, Compiler]
    drivers: dict[str, Driver]
    verdicts: dict[str, Verdict]
    proglangs: dict[str, Proglang]


class BriefAbstractProblem(BaseModel):
    """
    No description yet
    """

    problem_nm: str
    author: Optional[str] = Field(default=None)
    author_email: Optional[str] = Field(default=None)
    public: Optional[int] = Field(default=None)
    official: Optional[int] = Field(default=None)
    compilers: Optional[str] = Field(default=None)
    driver_id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    deprecation: Optional[str] = Field(default=None)
    created_at: str
    updated_at: str


class BriefProblem(BaseModel):
    """
    No description yet
    """

    problem_id: str
    problem_nm: str
    language_id: str
    title: str
    original_language_id: str
    translator: Optional[str] = Field(default=None)
    translator_email: Optional[str] = Field(default=None)
    checked: Optional[int] = Field(default=None)


type BriefProblemDict = dict[str, BriefProblem]


class AbstractProblem(BaseModel):
    """
    No description yet
    """

    problem_nm: str
    author: Optional[str] = Field(default=None)
    author_email: Optional[str] = Field(default=None)
    public: Optional[int] = Field(default=None)
    official: Optional[int] = Field(default=None)
    compilers: Optional[str] = Field(default=None)
    driver_id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    deprecation: Optional[str] = Field(default=None)
    created_at: str
    updated_at: str
    problems: BriefProblemDict


class AbstractProblemSuppl(BaseModel):
    """
    No description yet
    """

    compilers_with_ac: list[str]
    proglangs_with_ac: list[str]


class ProblemSuppl(BaseModel):
    """
    No description yet
    """

    compilers_with_ac: list[str]
    proglangs_with_ac: list[str]
    official_solution_checks: dict[str, bool]
    handler: Any


class Problem(BaseModel):
    """
    No description yet
    """

    problem_id: str
    problem_nm: str
    language_id: str
    title: str
    original_language_id: str
    translator: Optional[str] = Field(default=None)
    translator_email: Optional[str] = Field(default=None)
    checked: Optional[int] = Field(default=None)
    abstract_problem: BriefAbstractProblem


class Testcase(BaseModel):
    """
    No description yet
    """

    name: str
    input_b64: str
    correct_b64: str


class ProblemRich(BaseModel):
    """
    No description yet
    """

    problem_id: str
    problem_nm: str
    language_id: str
    title: str
    original_language_id: str
    translator: Optional[str] = Field(default=None)
    translator_email: Optional[str] = Field(default=None)
    checked: Optional[int] = Field(default=None)
    abstract_problem: BriefAbstractProblem
    sample_testcases: list[Testcase]
    html_statement: str


class AllKeys(BaseModel):
    """
    No description yet
    """

    problems: list[str]
    enrolled_courses: list[str]
    available_courses: list[str]
    lists: list[str]


class Profile(BaseModel):
    """
    No description yet
    """

    user_uid: str
    email: str
    name: str
    username: Optional[str] = Field(default=None)
    nickname: Optional[str] = Field(default=None)
    webpage: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    affiliation: Optional[str] = Field(default=None)
    birth_year: Optional[int] = Field(default=None)
    max_subsxhour: int
    max_subsxday: int
    administrator: int
    instructor: int
    parent_email: Optional[str] = Field(default=None)
    country_id: Optional[str] = Field(default=None)
    timezone_id: str
    compiler_id: Optional[str] = Field(default=None)
    language_id: Optional[str] = Field(default=None)


class NewProfile(BaseModel):
    """
    No description yet
    """

    name: str
    birth_year: int
    nickname: str
    webpage: str
    affiliation: str
    description: str
    country_id: str
    timezone_id: str


class NewPassword(BaseModel):
    """
    No description yet
    """

    oldPassword: str
    newPassword: str


class DateValue(BaseModel):
    """
    No description yet
    """

    date: int
    value: int


type HeatmapCalendar = list[DateValue]

type Distribution = dict[str, int]


class AllDistributions(BaseModel):
    """
    No description yet
    """

    verdicts: Distribution
    compilers: Distribution
    proglangs: Distribution
    submissions_by_hour: Distribution
    submissions_by_weekday: Distribution


class Dashboard(BaseModel):
    """
    No description yet
    """

    stats: Distribution
    heatmap: HeatmapCalendar
    distributions: AllDistributions


class Submission(BaseModel):
    """
    No description yet
    """

    problem_id: str
    submission_id: str
    compiler_id: str
    annotation: Optional[str] = Field(default=None)
    state: str
    time_in: str
    veredict: Optional[str] = Field(default=None)
    veredict_info: Optional[str] = Field(default=None)
    veredict_publics: Optional[str] = Field(default=None)
    ok_publics_but_wrong: int


class NewSubmissionIn(BaseModel):
    """
    No description yet
    """

    problem_id: str
    compiler_id: str
    annotation: str


class NewSubmissionOut(BaseModel):
    """
    No description yet
    """

    submission_id: str


class SubmissionAnalysis(BaseModel):
    """
    No description yet
    """

    testcase: str
    execution: str
    verdict: str


class TestcaseAnalysis(BaseModel):
    """
    No description yet
    """

    testcase: str
    execution: str
    verdict: str
    input_b64: str
    output_b64: str
    expected_b64: str


class PublicProfile(BaseModel):
    """
    No description yet
    """

    email: str
    name: str
    username: Optional[str] = Field(default=None)


class BriefCourse(BaseModel):
    """
    No description yet
    """

    course_nm: str
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    annotation: Optional[str] = Field(default=None)
    public: int
    official: int


class Course(BaseModel):
    """
    No description yet
    """

    course_nm: str
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    annotation: Optional[str] = Field(default=None)
    public: int
    official: int
    owner: PublicProfile
    lists: list[str]


class ListItem(BaseModel):
    """
    No description yet
    """

    problem_nm: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class BriefList(BaseModel):
    """
    No description yet
    """

    list_nm: str
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    annotation: Optional[str] = Field(default=None)
    public: int
    official: int


class List(BaseModel):
    """
    No description yet
    """

    list_nm: str
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    annotation: Optional[str] = Field(default=None)
    public: int
    official: int
    items: list[ListItem]
    owner: PublicProfile


class ReadyExam(BaseModel):
    """
    No description yet
    """

    exam_key: str  # Unique key for the exam, in the format "username:exam_nm"
    title: str
    place: str
    description: str
    exp_time_start: str
    running_time: int
    contest: bool


class RunningExamProblem(BaseModel):
    """
    No description yet
    """

    problem_nm: str
    icon: Optional[str] = Field(default=None)
    caption: Optional[str] = Field(default=None)
    weight: Optional[int] = Field(default=None)


class RunningExamDocument(BaseModel):
    """
    No description yet
    """

    document_nm: str
    title: str
    description: str


class RunningExam(BaseModel):
    """
    No description yet
    """

    title: str
    description: str
    instructions: str
    time_start: Optional[str] = Field(default=None)
    exp_time_start: str
    running_time: int
    contest: int
    problems: list[RunningExamProblem]
    compilers: list[str]
    documents: list[RunningExamDocument]


class AbstractStatus(BaseModel):
    """
    No description yet
    """

    problem_nm: str
    nb_submissions: int
    nb_pending_submissions: int
    nb_accepted_submissions: int
    nb_rejected_submissions: int
    nb_scored_submissions: int
    status: str


class Status(BaseModel):
    """
    No description yet
    """

    problem_id: str
    problem_nm: str
    nb_submissions: int
    nb_pending_submissions: int
    nb_accepted_submissions: int
    nb_rejected_submissions: int
    nb_scored_submissions: int
    status: str


class Award(BaseModel):
    """
    No description yet
    """

    award_id: str
    time: str
    type: str
    icon: str
    title: str
    info: str
    youtube: Optional[str] = Field(default=None)
    submission: Optional[Submission] = Field(default=None)


class BriefAward(BaseModel):
    """
    No description yet
    """

    award_id: str
    time: str
    type: str
    icon: str
    title: str
    info: str
    youtube: Optional[str] = Field(default=None)


class Document(BaseModel):
    """
    No description yet
    """

    document_nm: str  # Document name
    title: str  # The title of the document
    description: str = Field(default="", description="The description of the document")
    created_at: str  # The date when the document was created
    updated_at: str  # The date when the document was last updated


class DocumentCreation(BaseModel):
    """
    No description yet
    """

    document_nm: str  # Document name
    title: str  # The title of the document
    description: str = Field(default="", description="The description of the document")


type DocumentUpdate = DocumentCreation


class InstructorBriefList(BaseModel):
    """
    No description yet
    """

    list_nm: str  # The name of the list
    title: str  # The title of the list
    description: str = Field(default="", description="The description of the list")
    annotation: str = Field(default="", description="Additional private annotations for the list")
    official: int = Field(default=0, description="Indicates if the list is official (1) or not (0) TODO")
    public: int = Field(default=0, description="Indicates if the list is public (1) or private (0) TODO")
    created_at: str  # Creation date of the list
    updated_at: str  # Last update date of the list


class InstructorListItem(BaseModel):
    """
    Provide a problem_nm or a description, not both or none
    """

    problem_nm: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


type InstructorListItems = list[InstructorListItem]


class InstructorList(BaseModel):
    """
    No description yet
    """

    list_nm: str  # The name of the list
    title: str  # The title of the list
    description: str = Field(default="", description="The description of the list")
    annotation: str = Field(default="", description="Additional private annotations for the list")
    official: int = Field(default=0, description="Indicates if the list is official (1) or not (0) TODO")
    public: int = Field(default=0, description="Indicates if the list is public (1) or private (0) TODO")
    created_at: str  # Creation date of the list
    updated_at: str  # Last update date of the list
    items: InstructorListItems


class InstructorListCreation(BaseModel):
    """
    No description yet
    """

    list_nm: str  # The name of the list
    title: str  # The title of the list
    description: str = Field(default="", description="The description of the list")
    annotation: str = Field(default="", description="Additional private annotations for the list")
    official: int = Field(default=0, description="Indicates if the list is official (1) or not (0) TODO")
    public: int = Field(default=0, description="Indicates if the list is public (1) or private (0) TODO")
    items: InstructorListItems


type InstructorListUpdate = InstructorListCreation


class InstructorBriefCourse(BaseModel):
    """
    No description yet
    """

    course_nm: str  # The name of the course
    title: str  # The title of the course
    description: str = Field(default="", description="The description of the course")
    annotation: str = Field(default="", description="Additional private annotations for the course")
    official: int = Field(default=0, description="Indicates if the course is official (1) or not (0) TODO")
    public: int = Field(default=0, description="Indicates if the course is public (1) or private (0) TODO")
    created_at: str  # Creation date of the course
    updated_at: str  # Last update date of the course


class CourseMembers(BaseModel):
    """
    No description yet
    """

    invited: list[str]
    enrolled: list[str]
    pending: list[str]


class InstructorCourse(BaseModel):
    """
    No description yet
    """

    course_nm: str  # The name of the course
    title: str  # The title of the course
    description: str = Field(default="", description="The description of the course")
    annotation: str = Field(default="", description="Additional private annotations for the course")
    official: int = Field(default=0, description="Indicates if the course is official (1) or not (0) TODO")
    public: int = Field(default=0, description="Indicates if the course is public (1) or private (0) TODO")
    created_at: str  # Creation date of the course
    updated_at: str  # Last update date of the course
    lists: list[str]
    students: CourseMembers
    tutors: CourseMembers


class StudentProfile(BaseModel):
    """
    No description yet
    """

    name: str  # The name of the student
    email: str  # The email of the student


class InstructorCourseCreation(BaseModel):
    """
    No description yet
    """

    course_nm: str  # The name of the course
    title: str  # The title of the course
    description: str = Field(default="", description="The description of the course")
    annotation: str = Field(default="", description="Additional private annotations for the course")
    official: int = Field(default=0, description="Indicates if the course is official (1) or not (0) TODO")
    public: int = Field(default=0, description="Indicates if the course is public (1) or private (0) TODO")
    lists: list[str]
    students: CourseMembers
    tutors: CourseMembers


type InstructorCourseUpdate = InstructorCourseCreation


class InstructorExamCourse(BaseModel):
    """
    No description yet
    """

    course_nm: str
    title: str


type InstructorExamDocument = RunningExamDocument


class InstructorExamCompiler(BaseModel):
    """
    No description yet
    """

    compiler_id: str
    name: str


class InstructorExamProblem(BaseModel):
    """
    No description yet
    """

    problem_nm: str
    weight: Optional[float] = Field(default=1)
    icon: Optional[str] = Field(default=None)
    caption: Optional[str] = Field(default=None)


class InstructorExamStudent(BaseModel):
    """
    No description yet
    """

    email: str
    name: Optional[str] = Field(default=None)
    code: Optional[str] = Field(default=None)
    restricted: int = Field(default=0)
    annotation: Optional[str] = Field(default=None)
    result: Optional[str] = Field(default=None)
    finished: int = Field(default=0)
    banned: int = Field(default=0)
    reason_ban: Optional[str] = Field(default=None)
    inc: Optional[int] = Field(default=None)
    reason_inc: Optional[str] = Field(default=None)
    taken_exam: int = Field(default=0)
    emergency_password: Optional[str] = Field(default=None)
    invited: int = Field(default=0)


class InstructorExamCreation(BaseModel):
    """
    No description yet
    """

    exam_nm: str
    course_nm: str
    title: str
    exp_time_start: str


class InstructorExamUpdate(BaseModel):
    """
    No description yet
    """

    exam_nm: str
    course_nm: str
    title: str
    place: str = Field(default="")
    code: str
    description: str = Field(default="")
    time_start: Optional[str] = Field(default=None)
    exp_time_start: str
    running_time: int
    visible_submissions: int = Field(default=0)
    started_by: Optional[str] = Field(default=None)
    contest: int = Field(default=0)
    instructions: str = Field(default="")
    avatars: Optional[str] = Field(default=None)
    anonymous: int = Field(default=1)


class InstructorNewExamStudent(BaseModel):
    """
    No description yet
    """

    email: str
    invited: int = Field(default=0)
    restricted: int = Field(default=0)
    code: str = Field(default="")
    emergency_password: str = Field(default="")
    annotation: str = Field(default="")


class InstructorExamSubmissionsOptions(BaseModel):
    """
    No description yet
    """

    problems: str = Field(default="all", description="Comma-separated list of problem names (without language). Use `all` to include all problems.")
    include_source: bool = Field(default=True, description="Include source code")
    include_pdf: bool = Field(default=True, description="Include source code formated in PDF")
    include_metadata: bool = Field(default=True, description="Include metadata in the code")
    only_last: bool = Field(default=True, description="Only include last submission of each problem for each student")
    font_size: float = Field(default=10, description="Font size on the PDF")
    layout: str = Field(default="vertical", description="Layout (vertical|horizontal|double)")
    obscure_private_testcases_names: bool = Field(default=False, description="Obscure private testcases names")


class Pack(BaseModel):
    """
    No description yet
    """

    message: str
    href: str


class InstructorBriefExam(BaseModel):
    """
    No description yet
    """

    exam_nm: str
    title: str
    place: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    code: Optional[str] = Field(default=None)
    time_start: Optional[str] = Field(default=None)
    exp_time_start: str
    running_time: int
    visible_submissions: int
    started_by: Optional[str] = Field(default=None)
    contest: int
    instructions: Optional[str] = Field(default=None)
    avatars: Optional[str] = Field(default=None)
    anonymous: int
    course: InstructorExamCourse
    created_at: str
    updated_at: str


class InstructorExam(BaseModel):
    """
    No description yet
    """

    exam_nm: str
    title: str
    place: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    code: Optional[str] = Field(default=None)
    time_start: Optional[str] = Field(default=None)
    exp_time_start: str
    running_time: int
    visible_submissions: int
    started_by: Optional[str] = Field(default=None)
    contest: int
    instructions: Optional[str] = Field(default=None)
    avatars: Optional[str] = Field(default=None)
    anonymous: int
    course: InstructorExamCourse
    created_at: str
    updated_at: str
    documents: list[RunningExamDocument]
    compilers: list[InstructorExamCompiler]
    problems: list[InstructorExamProblem]
    students: list[InstructorExamStudent]


class ExamStatisticsEntry(BaseModel):
    """
    No description yet
    """

    minute: int
    ok: int
    ko: int


class ExamStatistics(BaseModel):
    """
    No description yet
    """

    submissions: dict[str, dict[str, float]]
    statuses: dict[str, dict[str, float]]
    timeline: list[ExamStatisticsEntry]
    compilers: dict[str, dict[str, float]]
    proglangs: dict[str, dict[str, float]]


class RankingResult(BaseModel):
    """
    No description yet
    """

    problem_nm: str
    submissions: int
    verdict: Optional[str] = Field(default=None)
    score: float
    time: float
    penalty: float
    wrongs: float


class RankingRow(BaseModel):
    """
    No description yet
    """

    position: Optional[int] = Field(default=None)
    name: str
    avatar: Optional[str] = Field(default=None)
    score: float
    time: float
    invited: bool
    submissions: int
    rankingResults: list[RankingResult]


type Ranking = list[RankingRow]


class WebStream(BaseModel):
    """
    No description yet
    """

    title: str
    id: str


class SubmissionQuery(BaseModel):
    """
    No description yet
    """

    email: str
    problem_nm: str
    problem_id: str
    time: str
    ip: str
    verdict: str


type SubmissionsQuery = list[SubmissionQuery]

type TagsDict = dict[str, list[str]]


class InstructorEntry(BaseModel):
    """
    No description yet
    """

    username: str
    name: str
    email: str


type InstructorEntries = list[InstructorEntry]


class UserCreation(BaseModel):
    """
    No description yet
    """

    email: str
    name: str
    username: str
    password: str
    administrator: float = Field(default=0)
    instructor: float = Field(default=0)


class UserEmailAndName(BaseModel):
    """
    No description yet
    """

    email: str
    name: str


type UsersEmailsAndNames = list[UserEmailAndName]


class ProfileForAdmin(BaseModel):
    """
    No description yet
    """

    user_id: str
    user_uid: str
    email: str
    name: str
    username: Optional[str] = Field(default=None)
    nickname: Optional[str] = Field(default=None)
    webpage: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    affiliation: Optional[str] = Field(default=None)
    birth_year: Optional[int] = Field(default=None)
    max_subsxhour: int
    max_subsxday: int
    administrator: int
    instructor: int
    parent_email: Optional[str] = Field(default=None)
    country_id: Optional[str] = Field(default=None)
    timezone_id: str
    compiler_id: Optional[str] = Field(default=None)
    language_id: Optional[str] = Field(default=None)
    locked: int
    banned: int
    nb_bans: int
    reason: Optional[str] = Field(default=None)
    creation_date: str


class FreeDiskSpaceItem(BaseModel):
    """
    No description yet
    """

    disk: str
    filesystem: str
    size: str
    used: str
    available: str
    use: str
    mounted: str


type NullableFreeDiskSpaceItem = Optional[FreeDiskSpaceItem]

type FreeDiskSpace = dict[str, NullableFreeDiskSpaceItem]


class RecentConnectedUsers(BaseModel):
    """
    No description yet
    """

    latest_hour: int
    latest_day: int
    latest_week: int
    latest_month: int
    latest_year: int


class RecentSubmissions(BaseModel):
    """
    No description yet
    """

    latest_01_minutes: int
    latest_05_minutes: int
    latest_15_minutes: int
    latest_60_minutes: int


class RecentLoadAverages(BaseModel):
    """
    No description yet
    """

    latest_01_minutes: float
    latest_05_minutes: float
    latest_15_minutes: float


class SubmissionsHistograms(BaseModel):
    """
    No description yet
    """

    latest_hour: list[int]
    latest_day: list[int]


class Zombies(BaseModel):
    """
    No description yet
    """

    ies: int
    pendings: int


class AdminDashboard(BaseModel):
    """
    No description yet
    """

    free_disk_space: FreeDiskSpace
    recent_load_averages: RecentLoadAverages
    recent_connected_users: RecentConnectedUsers
    recent_submissions: RecentSubmissions
    submissions_histograms: SubmissionsHistograms
    zombies: Zombies


class UpcomingExam(BaseModel):
    """
    No description yet
    """

    exam_nm: str
    title: str
    username: str
    email: str
    exp_time_start: str
    running_time: int
    students: int
    name: str
    contest: int


type UpcomingExams = list[UpcomingExam]


class SubmissionQueueItem(BaseModel):
    """
    No description yet
    """

    submission_uid: str
    submission_id: str
    problem_id: str
    compiler_id: str
    time_in: str
    exam_id: Optional[str] = Field(default=None)
    veredict: Optional[str] = Field(default=None)
    user_id: str
    user__name: str
    problem__title: str


type SubmissionQueueItems = list[SubmissionQueueItem]


class QueueQuery(BaseModel):
    """
    No description yet
    """

    verdicts: list[str]
    limit: int


class UserRankingEntry(BaseModel):
    """
    No description yet
    """

    user_id: str
    nickname: Optional[str] = Field(default=None)
    email: str
    name: str
    problems: int


type UserRanking = list[UserRankingEntry]


class DateRange(BaseModel):
    """
    No description yet
    """

    start: str
    end: str


class ProblemSummary(BaseModel):
    """
    No description yet
    """

    summary_1s: str  # One sentence summary
    summary_1p: str  # One paragraph summary
    keywords: str  # Comma separated keywords
    model: str  # system/model
    duration: float  # Time in seconds to generate


class AbstractProblemTag(BaseModel):
    """
    No description yet
    """

    tags: str  # Comma separated tags
    model: str  # system/model
    duration: float  # Time in seconds to generate


class TwoFloats(BaseModel):
    """
    No description yet
    """

    a: float  # A first real number
    b: float  # A second real number


class TwoInts(BaseModel):
    """
    No description yet
    """

    a: int  # A first integer
    b: int  # A second integer


class Name(BaseModel):
    """
    No description yet
    """

    name: str  # A string


class SomeType(BaseModel):
    """
    No description yet
    """

    a: str = Field(default="foo", description="A string")
    b: int = Field(default=1, description="An integer")
    c: bool = Field(default=True, description="A boolean")
    d: bool  # Another boolean


# exceptions
class UnauthorizedException(Exception):
    """Class UnauthorizedException"""


class InfoException(Exception):
    """Class InfoException"""


class NotFoundException(Exception):
    """Class NotFoundException"""


class InputException(Exception):
    """Class InputException"""


class ProtocolException(Exception):
    """Class ProtocolException"""


class Download(BaseModel):
    """Class for downloaded files (ofiles)"""

    data: bytes
    name: str
    type: str

    def write(self, path: str) -> None:
        """Write the content of the download to the file at the given path."""

        with open(path, "wb") as file:
            file.write(self.data)


def _build(x: Any, t: Any) -> Any:
    try:
        return t.model_validate(x)
    except Exception:
        try:
            return TypeAdapter(t).validate_python(x)
        except Exception:
            return x


def _debuild(x: Any) -> Any:
    if isinstance(x, BaseModel):
        return x.model_dump()
    if isinstance(x, list):
        return [_debuild(v) for v in x]
    if isinstance(x, dict):
        return {k: _debuild(v) for k, v in x.items()}
    return x


def _raise_exception(error: dict[str, Any], operation_id: str | None) -> None:
    # TODO: do something with operation_id
    message = error.get("message", "Unknown error")
    if error["name"] == "UnauthorizedError":
        raise UnauthorizedException(message)
    if error["name"] == "InfoError":
        raise InfoException(message)
    if error["name"] == "NotFoundError":
        raise NotFoundException(message)
    if error["name"] == "InputError":
        raise InputException(message)
    raise Exception("Unknown error")


class Util:
    """
    Utility class with static methods to convert between JSON and YAML formats.
    """

    @staticmethod
    def from_json[T](s: str, t: Type[T]) -> T:
        """Parse a JSON string into a Python object"""

        return TypeAdapter(t).validate_json(s)

    @staticmethod
    def to_json(obj: Any) -> str:
        """Convert a Python object into a JSON string"""

        return json.dumps(obj, default=to_jsonable_python, ensure_ascii=False)

    @staticmethod
    def json_to_yaml(s: str) -> str:
        """Convert a JSON string into a YAML string"""

        return yaml.dump(json.loads(s), allow_unicode=True, indent=4)

    @staticmethod
    def yaml_to_json(s: str) -> str:
        """Convert a YAML string into a JSON string"""

        return json.dumps(yaml.safe_load(s), ensure_ascii=False)

    @staticmethod
    def to_yaml(obj: Any) -> str:
        """Convert a Python object into a YAML string"""
        return Util.json_to_yaml(Util.to_json(obj))

    @staticmethod
    def from_yaml[T](s: str, t: Type[T]) -> T:
        """Convert a YAML string into a Python object"""
        return Util.from_json(Util.yaml_to_json(s), t)


class JutgeApiClient:
    """
    Client to interact with the Jutge API.
    """

    JUTGE_API_URL: str = os.environ.get("JUTGE_API_URL", "https://api.jutge.org/api")

    _meta: Any | None = None

    clients: ModuleClients
    auth: ModuleAuth
    misc: ModuleMisc
    tables: ModuleTables
    problems: ModuleProblems
    student: ModuleStudent
    instructor: ModuleInstructor
    admin: ModuleAdmin
    testing: ModuleTesting

    def __init__(self):
        self.clients = ModuleClients(self)
        self.auth = ModuleAuth(self)
        self.misc = ModuleMisc(self)
        self.tables = ModuleTables(self)
        self.problems = ModuleProblems(self)
        self.student = ModuleStudent(self)
        self.instructor = ModuleInstructor(self)
        self.admin = ModuleAdmin(self)
        self.testing = ModuleTesting(self)

    def execute(self, func: str, input: Any, ifiles: list[BinaryIO] | None = None) -> tuple[Any, list[Download]]:
        """Function that sends a request to the API and returns the response"""

        data = {"func": func, "input": input, "meta": self._meta}
        files = {}
        if ifiles is not None:
            for i, ifile in enumerate(ifiles):
                files["file_" + str(i)] = ifile
        response = requests.post(self.JUTGE_API_URL, data={"data": json.dumps(data)}, files=files)
        content_type = response.headers.get("content-type", "").split(";")[0].lower()
        if content_type != "multipart/form-data":
            raise ProtocolException("The content type is not multipart/form-data")

        ofiles = []
        answer = None
        multipart_data = decoder.MultipartDecoder.from_response(response)

        for part in multipart_data.parts:

            def get(x: bytes) -> str:
                """Helper function to get a header from a part and decode it without warnings"""
                return part.headers.get(x, "").decode("utf-8")  # type: ignore

            if b"Content-Type" in part.headers:
                filenames = re.findall('filename="(.+)"', get(b"Content-Disposition"))
                if len(filenames) != 1:
                    raise ProtocolException("The part does not have a filename")
                filename = filenames[0]
                type = get(b"Content-Type")
                ofiles.append(Download(data=part.content, name=filename, type=type))
            else:
                if answer is not None:
                    raise ProtocolException("There are multiple parts with JSON content")
                answer = json.loads(part.content)

        if not isinstance(answer, dict):
            raise ProtocolException("The answer is not an object")

        output = answer.get("output", None)
        operation_id = answer.get("operation_id", None)

        if "error" in answer:
            _raise_exception(answer["error"], operation_id)

        return output, ofiles

    def login(self, email: str, password: str) -> CredentialsOut:
        """
        Simple login to the API.

        Attempts to login with the provided email and password.
            - If successful, it returns the credentials and sets the _meta attribute so that the following requests are authenticated.
            - If not, it raises an UnauthorizedException exception.
        """

        input = {"email": email, "password": password}
        credentials_out, _ = self.execute("auth.login", input)
        if credentials_out["error"] != "":
            raise UnauthorizedException(credentials_out["error"])
        self._meta = {
            "token": credentials_out["token"],
            "exam": None,
        }
        return CredentialsOut(**credentials_out)

    def logout(self, silent: bool = False) -> None:
        """
        Simple logout from the API.
        """

        try:
            self.execute("auth.logout", None)
        except UnauthorizedException:
            pass
        except Exception as e:
            if not silent:
                print("[red]Error at log out[/red]")
            else:
                raise e
        finally:
            self._meta = None
            if not silent:
                print("[green]Logged out[/green]")


class ModuleClients:
    """
    Module to download clients.
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def python(self) -> Download:
        """
        Get Python client.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("clients.python", None)

        return ofiles[0]


class ModuleAuth:
    """
    Module to provide authentication functions.
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def login(self, data: CredentialsIn) -> CredentialsOut:
        """
            Login: Get an access token.

            🔐 Authenticated

        On success, token is a valid token and error is empty. On failure, token is empty and error is a message.
        """

        output, ofiles = self._root.execute("auth.login", _debuild(data))
        result = _build(output, CredentialsOut)
        return result

    def logout(self) -> None:
        """
        Logout: Discard the access token.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("auth.logout", None)
        result = _build(output, None)
        return result

    def login_exam(self, data: ExamCredentialsIn) -> CredentialsOut:
        """
            Login to an exam: Get an access token for an exam.

            🔐 Authenticated

        On success, token is a valid token and error is empty. On failure, token is empty and error is a message.
        """

        output, ofiles = self._root.execute("auth.loginExam", _debuild(data))
        result = _build(output, CredentialsOut)
        return result


class ModuleMisc:
    """
    Module with miscellaneous endpoints
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get_api_version(self) -> ApiVersion:
        """
        Get version information of the API.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("misc.getApiVersion", None)
        result = _build(output, ApiVersion)
        return result

    def get_request_information(self) -> RequestInformation:
        """
        Get requestion information.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("misc.getRequestInformation", None)
        result = _build(output, RequestInformation)
        return result

    def get_fortune(self) -> str:
        """
        Get a fortune message.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("misc.getFortune", None)
        result = _build(output, str)
        return result

    def get_time(self) -> Time:
        """
        Get server time.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("misc.getTime", None)
        result = _build(output, Time)
        return result

    def get_homepage_stats(self) -> HomepageStats:
        """
        Get homepage stats.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("misc.getHomepageStats", None)
        result = _build(output, HomepageStats)
        return result

    def get_logo(self) -> Download:
        """
        Get Jutge.org logo as a PNG file.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("misc.getLogo", None)

        return ofiles[0]

    def get_avatar_packs(self) -> list[str]:
        """
            Returns all packs of avatars.

            🔐 Authenticated

        Avatars are used in exams and contests to identify students or participants.
        """

        output, ofiles = self._root.execute("misc.getAvatarPacks", None)
        result = _build(output, list[str])
        return result

    def get_exam_icons(self) -> TagsDict:
        """
            Returns all exam icons.

            🔐 Authenticated

        Exam icon are used in exams and contests to identify problems.
        """

        output, ofiles = self._root.execute("misc.getExamIcons", None)
        result = _build(output, TagsDict)
        return result

    def get_colors(self) -> ColorMapping:
        """
            Returns color mappings using colornames notation.

            🔐 Authenticated

        Color mappings may be used to colorize keys in the frontends. Color names are as defined in https://github.com/timoxley/colornames
        """

        output, ofiles = self._root.execute("misc.getColors", None)
        result = _build(output, ColorMapping)
        return result

    def get_hex_colors(self) -> ColorMapping:
        """
            Returns color mappings using hexadecimal color notation.

            🔐 Authenticated

        Color mappings may be used to colorize keys in the frontends.
        """

        output, ofiles = self._root.execute("misc.getHexColors", None)
        result = _build(output, ColorMapping)
        return result

    def get_demos_for_compiler(self, compiler_id: str) -> dict[str, str]:
        """
        Returns code demos for a given compiler as a dictionary of base64 codes indexed by problem_nm.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("misc.getDemosForCompiler", _debuild(compiler_id))
        result = _build(output, dict[str, str])
        return result


class ModuleTables:
    """
    Module with quite static tables
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get(self) -> AllTables:
        """
            Returns all tables.

            🔐 Authenticated

        Returns all compilers, countries, drivers, languages, proglangs, and verdicts in a single request. This data does not change often, so you should only request it once per session.
        """

        output, ofiles = self._root.execute("tables.get", None)
        result = _build(output, AllTables)
        return result

    def get_languages(self) -> dict[str, Language]:
        """
            Returns all languages.

            🔐 Authenticated

        Returns all languages as a dictionary of objects, indexed by id.
        """

        output, ofiles = self._root.execute("tables.getLanguages", None)
        result = _build(output, dict[str, Language])
        return result

    def get_countries(self) -> dict[str, Country]:
        """
            Returns all countries.

            🔐 Authenticated

        Returns all countries as a dictionary of objects, indexed by id.
        """

        output, ofiles = self._root.execute("tables.getCountries", None)
        result = _build(output, dict[str, Country])
        return result

    def get_compilers(self) -> dict[str, Compiler]:
        """
            Returns all compilers.

            🔐 Authenticated

        Returns all compilers as a dictionary of objects, indexed by id.
        """

        output, ofiles = self._root.execute("tables.getCompilers", None)
        result = _build(output, dict[str, Compiler])
        return result

    def get_drivers(self) -> dict[str, Driver]:
        """
            Returns all drivers.

            🔐 Authenticated

        Returns all drivers as a dictionary of objects, indexed by id.
        """

        output, ofiles = self._root.execute("tables.getDrivers", None)
        result = _build(output, dict[str, Driver])
        return result

    def get_verdicts(self) -> dict[str, Verdict]:
        """
            Returns all verdicts.

            🔐 Authenticated

        Returns all verdicts as a dictionary of objects, indexed by id.
        """

        output, ofiles = self._root.execute("tables.getVerdicts", None)
        result = _build(output, dict[str, Verdict])
        return result

    def get_proglangs(self) -> dict[str, Proglang]:
        """
            Returns all proglangs.

            🔐 Authenticated

        Returns all proglangs (porgramming languages) as a dictionary of objects, indexed by id.
        """

        output, ofiles = self._root.execute("tables.getProglangs", None)
        result = _build(output, dict[str, Proglang])
        return result


class ModuleProblems:
    """
        Module with endpoints related to problems.

    There are two types of problems: *abstract problems* and *problems*. An abstract
    problem is a group of problems. A problem is an instance of an abstract problem
    in a particular language. Abstract problems are identified by a `problem_nm` (such
    as 'P68688'), while problems are identified by a `problem_id` including its
    `language_id` (such as 'P68688_en'). Abstract problems have a list of problems,
    while problems have an abstract problem. Abstract problems have an author, while
    problems have a translator.

    Available problems depend on the actor issuing the request. For example, non
    authenticated users can only access public problems, while authenticated
    users can potentially access more problems.

    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get_all_abstract_problems(self) -> dict[str, AbstractProblem]:
        """
            Get all available abstract problems.

            🔐 Authenticated

        Includes problems.
        """

        output, ofiles = self._root.execute("problems.getAllAbstractProblems", None)
        result = _build(output, dict[str, AbstractProblem])
        return result

    def get_abstract_problems(self, problem_nms: str) -> dict[str, AbstractProblem]:
        """
            Get available abstract problems whose keys are in `problem_nms`.

            🔐 Authenticated

        Includes problems.
        """

        output, ofiles = self._root.execute("problems.getAbstractProblems", _debuild(problem_nms))
        result = _build(output, dict[str, AbstractProblem])
        return result

    def get_abstract_problems_in_list(self, list_key: str) -> dict[str, AbstractProblem]:
        """
            Get available abstract problems that belong to a list.

            🔐 Authenticated

        Includes problems.
        """

        output, ofiles = self._root.execute("problems.getAbstractProblemsInList", _debuild(list_key))
        result = _build(output, dict[str, AbstractProblem])
        return result

    def get_abstract_problem(self, problem_nm: str) -> AbstractProblem:
        """
            Get an abstract problem.

            🔐 Authenticated

        Includes problems
        """

        output, ofiles = self._root.execute("problems.getAbstractProblem", _debuild(problem_nm))
        result = _build(output, AbstractProblem)
        return result

    def get_abstract_problem_suppl(self, problem_nm: str) -> AbstractProblemSuppl:
        """
            Get supplementary information of an abstract problem.

            🔐 Authenticated

        Includes accepted compilers and accepted proglangs
        """

        output, ofiles = self._root.execute("problems.getAbstractProblemSuppl", _debuild(problem_nm))
        result = _build(output, AbstractProblemSuppl)
        return result

    def get_problem(self, problem_id: str) -> Problem:
        """
            Get a problem.

            🔐 Authenticated

        Includes abstract problem.
        """

        output, ofiles = self._root.execute("problems.getProblem", _debuild(problem_id))
        result = _build(output, Problem)
        return result

    def get_problem_rich(self, problem_id: str) -> ProblemRich:
        """
            Get a problem with more infos.

            🔐 Authenticated

        Includes abstract problem, which includes statements, testcases, etc.
        """

        output, ofiles = self._root.execute("problems.getProblemRich", _debuild(problem_id))
        result = _build(output, ProblemRich)
        return result

    def get_problem_suppl(self, problem_id: str) -> ProblemSuppl:
        """
            Get supplementary information of a problem.

            🔐 Authenticated

        Includes accepted compilers, accepted proglangs, official solutions
        checks and handler specifications
        """

        output, ofiles = self._root.execute("problems.getProblemSuppl", _debuild(problem_id))
        result = _build(output, ProblemSuppl)
        return result

    def get_sample_testcases(self, problem_id: str) -> list[Testcase]:
        """
        Get sample testcases of a problem.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("problems.getSampleTestcases", _debuild(problem_id))
        result = _build(output, list[Testcase])
        return result

    def get_public_testcases(self, problem_id: str) -> list[Testcase]:
        """
            Get public testcases of a problem.

            🔐 Authenticated

        Public testcases are like sample testcases, but are not meant to be show
        in the problem statatement, because of their long length.
        """

        output, ofiles = self._root.execute("problems.getPublicTestcases", _debuild(problem_id))
        result = _build(output, list[Testcase])
        return result

    def get_html_statement(self, problem_id: str) -> str:
        """
            Get Html statement of a problem.

            🔐 Authenticated

        We are working on this, please provide feedback.
        """

        output, ofiles = self._root.execute("problems.getHtmlStatement", _debuild(problem_id))
        result = _build(output, str)
        return result

    def get_text_statement(self, problem_id: str) -> str:
        """
        Get Text statement of a problem.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("problems.getTextStatement", _debuild(problem_id))
        result = _build(output, str)
        return result

    def get_markdown_statement(self, problem_id: str) -> str:
        """
        Get Markdown statement of a problem.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("problems.getMarkdownStatement", _debuild(problem_id))
        result = _build(output, str)
        return result

    def get_pdf_statement(self, problem_id: str) -> Download:
        """
        Get PDF statement of a problem.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("problems.getPdfStatement", _debuild(problem_id))

        return ofiles[0]

    def get_zip_statement(self, problem_id: str) -> Download:
        """
        Get ZIP archive of a problem. This includes the PDF statement and sample testcases.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("problems.getZipStatement", _debuild(problem_id))

        return ofiles[0]

    def get_templates(self, problem_id: str) -> list[str]:
        """
        Get list of template files of a problem (`main.*`, `code.*`, `public.tar`, etc.).

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("problems.getTemplates", _debuild(problem_id))
        result = _build(output, list[str])
        return result

    def get_template(self, problem_id: str, template: str) -> Download:
        """
        Get a template file of a problem.

        🔐 Authenticated
        """

        data = {"problem_id": problem_id, "template": template}
        output, ofiles = self._root.execute("problems.getTemplate", _debuild(data))

        return ofiles[0]


class ModuleStudent:
    """
    These operations are available to all users, provided they are authenticated.
    """

    _root: JutgeApiClient

    keys: ModuleStudentKeys
    profile: ModuleStudentProfile
    dashboard: ModuleStudentDashboard
    submissions: ModuleStudentSubmissions
    courses: ModuleStudentCourses
    lists: ModuleStudentLists
    exam: ModuleStudentExam
    statuses: ModuleStudentStatuses
    awards: ModuleStudentAwards

    def __init__(self, root: JutgeApiClient):
        self._root = root
        self.keys = ModuleStudentKeys(root)
        self.profile = ModuleStudentProfile(root)
        self.dashboard = ModuleStudentDashboard(root)
        self.submissions = ModuleStudentSubmissions(root)
        self.courses = ModuleStudentCourses(root)
        self.lists = ModuleStudentLists(root)
        self.exam = ModuleStudentExam(root)
        self.statuses = ModuleStudentStatuses(root)
        self.awards = ModuleStudentAwards(root)


class ModuleStudentKeys:
    """
    This module exposes all valid keys for problems, courses and lists that a user can access.
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get(self) -> AllKeys:
        """
        Get problem, courses (as enrolled and available) and list keys.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.keys.get", None)
        result = _build(output, AllKeys)
        return result

    def get_problems(self) -> list[str]:
        """
        Get problem keys.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.keys.getProblems", None)
        result = _build(output, list[str])
        return result

    def get_enrolled_courses(self) -> list[str]:
        """
        Get enrolled course keys.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.keys.getEnrolledCourses", None)
        result = _build(output, list[str])
        return result

    def get_available_courses(self) -> list[str]:
        """
        Get available course keys.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.keys.getAvailableCourses", None)
        result = _build(output, list[str])
        return result

    def get_lists(self) -> list[str]:
        """
        Get list keys.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.keys.getLists", None)
        result = _build(output, list[str])
        return result


class ModuleStudentProfile:
    """
    This module exposes the user profile.
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get(self) -> Profile:
        """
            Get the profile.

            🔐 Authenticated

        In case of exams, some fields are not nullified to avoid cheating.
        """

        output, ofiles = self._root.execute("student.profile.get", None)
        result = _build(output, Profile)
        return result

    def get_avatar(self) -> Download:
        """
        Returns the avatar as a PNG file.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.profile.getAvatar", None)

        return ofiles[0]

    def update(self, data: NewProfile) -> None:
        """
        Update the profile

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.profile.update", _debuild(data))
        result = _build(output, None)
        return result

    def update_avatar(self, ifile: BinaryIO) -> None:
        """
        Update the avatar with new PNG.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.profile.updateAvatar", None, [ifile])
        result = _build(output, None)
        return result

    def update_password(self, data: NewPassword) -> None:
        """
            Update password.

            🔐 Authenticated

        Receives the old password and the new one, and changes the password if the old one is correct and the new one strong enough.
        """

        output, ofiles = self._root.execute("student.profile.updatePassword", _debuild(data))
        result = _build(output, None)
        return result


class ModuleStudentDashboard:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get_absolute_ranking(self) -> int:
        """
        Get the ranking of the user over all users in the system.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.dashboard.getAbsoluteRanking", None)
        result = _build(output, int)
        return result

    def get_all_distributions(self) -> AllDistributions:
        """
        Get all distributions.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.dashboard.getAllDistributions", None)
        result = _build(output, AllDistributions)
        return result

    def get_compilers_distribution(self) -> Distribution:
        """
        Get compilers distribution.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.dashboard.getCompilersDistribution", None)
        result = _build(output, Distribution)
        return result

    def get_dashboard(self) -> Dashboard:
        """
        Get dashboard.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.dashboard.getDashboard", None)
        result = _build(output, Dashboard)
        return result

    def get_heatmap_calendar(self) -> HeatmapCalendar:
        """
        Get heatmap calendar of submissions.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.dashboard.getHeatmapCalendar", None)
        result = _build(output, HeatmapCalendar)
        return result

    def get_proglangs_distribution(self) -> Distribution:
        """
        Get programming languages distribution.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.dashboard.getProglangsDistribution", None)
        result = _build(output, Distribution)
        return result

    def get_stats(self) -> Distribution:
        """
        Get dashboard stats.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.dashboard.getStats", None)
        result = _build(output, Distribution)
        return result

    def get_level(self) -> str:
        """
        Get fancy Jutge level.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.dashboard.getLevel", None)
        result = _build(output, str)
        return result

    def get_submissions_by_hour(self) -> Distribution:
        """
        Get submissions by hour distribution.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.dashboard.getSubmissionsByHour", None)
        result = _build(output, Distribution)
        return result

    def get_submissions_by_week_day(self) -> Distribution:
        """
        Get submissions by weekday distribution.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.dashboard.getSubmissionsByWeekDay", None)
        result = _build(output, Distribution)
        return result

    def get_verdicts_distribution(self) -> Distribution:
        """
        Get verdicts distribution.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.dashboard.getVerdictsDistribution", None)
        result = _build(output, Distribution)
        return result


class ModuleStudentSubmissions:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def index_for_abstract_problem(self, problem_nm: str) -> dict[str, dict[str, Submission]]:
        """
            Get index of all submissions for an abstract problem.

            🔐 Authenticated

        Grouped by problem.
        """

        output, ofiles = self._root.execute("student.submissions.indexForAbstractProblem", _debuild(problem_nm))
        result = _build(output, dict[str, dict[str, Submission]])
        return result

    def index_for_problem(self, problem_id: str) -> dict[str, Submission]:
        """
        Get index of all submissions for a problem.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.submissions.indexForProblem", _debuild(problem_id))
        result = _build(output, dict[str, Submission])
        return result

    def get_all(self) -> list[Submission]:
        """
            Get all submissions.

            🔐 Authenticated

        Flat array of submissions in chronological order.
        """

        output, ofiles = self._root.execute("student.submissions.getAll", None)
        result = _build(output, list[Submission])
        return result

    def submit(self, problem_id: str, compiler_id: str, code: str, annotation: str) -> str:
        """
        Submit a solution to the Judge, easy interface.

        🔐 Authenticated
        """

        data = {"problem_id": problem_id, "compiler_id": compiler_id, "code": code, "annotation": annotation}
        output, ofiles = self._root.execute("student.submissions.submit", _debuild(data))
        result = _build(output, str)
        return result

    def submit_full(self, data: NewSubmissionIn, ifile: BinaryIO) -> NewSubmissionOut:
        """
        Submit a solution to the Judge, full interface.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.submissions.submitFull", _debuild(data), [ifile])
        result = _build(output, NewSubmissionOut)
        return result

    def get(self, problem_id: str, submission_id: str) -> Submission:
        """
        Get a submission.

        🔐 Authenticated
        """

        data = {"problem_id": problem_id, "submission_id": submission_id}
        output, ofiles = self._root.execute("student.submissions.get", _debuild(data))
        result = _build(output, Submission)
        return result

    def get_code_as_b64(self, problem_id: str, submission_id: str) -> str:
        """
        Get code for a submission as a string in base64.

        🔐 Authenticated
        """

        data = {"problem_id": problem_id, "submission_id": submission_id}
        output, ofiles = self._root.execute("student.submissions.getCodeAsB64", _debuild(data))
        result = _build(output, str)
        return result

    def get_code_metrics(self, problem_id: str, submission_id: str) -> Any:
        """
            Get code metrics for a submission as JSON.

            🔐 Authenticated
            ❌ Warning: TODO: add more documentation

        See https://github.com/jutge-org/jutge-code-metrics for details.
        """

        data = {"problem_id": problem_id, "submission_id": submission_id}
        output, ofiles = self._root.execute("student.submissions.getCodeMetrics", _debuild(data))
        result = _build(output, Any)
        return result

    def get_awards(self, problem_id: str, submission_id: str) -> list[str]:
        """
        Get list of awards ids for a submission.

        🔐 Authenticated
        """

        data = {"problem_id": problem_id, "submission_id": submission_id}
        output, ofiles = self._root.execute("student.submissions.getAwards", _debuild(data))
        result = _build(output, list[str])
        return result

    def get_analysis(self, problem_id: str, submission_id: str) -> list[SubmissionAnalysis]:
        """
        Get analysis of a submission.

        🔐 Authenticated
        """

        data = {"problem_id": problem_id, "submission_id": submission_id}
        output, ofiles = self._root.execute("student.submissions.getAnalysis", _debuild(data))
        result = _build(output, list[SubmissionAnalysis])
        return result

    def get_testcase_analysis(self, problem_id: str, submission_id: str, testcase: str) -> TestcaseAnalysis:
        """
        Get a (public) testcase analysis of a submission.

        🔐 Authenticated
        """

        data = {"problem_id": problem_id, "submission_id": submission_id, "testcase": testcase}
        output, ofiles = self._root.execute("student.submissions.getTestcaseAnalysis", _debuild(data))
        result = _build(output, TestcaseAnalysis)
        return result


class ModuleStudentCourses:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def index_available(self) -> dict[str, BriefCourse]:
        """
        Get index of all available courses.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.courses.indexAvailable", None)
        result = _build(output, dict[str, BriefCourse])
        return result

    def index_enrolled(self) -> dict[str, BriefCourse]:
        """
        Get index of all enrolled courses.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.courses.indexEnrolled", None)
        result = _build(output, dict[str, BriefCourse])
        return result

    def get_available(self, course_key: str) -> Course:
        """
            Get an available course.

            🔐 Authenticated

        Includes owner and lists.
        """

        output, ofiles = self._root.execute("student.courses.getAvailable", _debuild(course_key))
        result = _build(output, Course)
        return result

    def get_enrolled(self, course_key: str) -> Course:
        """
            Get an enrolled course.

            🔐 Authenticated

        Includes owner and lists.
        """

        output, ofiles = self._root.execute("student.courses.getEnrolled", _debuild(course_key))
        result = _build(output, Course)
        return result

    def enroll(self, course_key: str) -> None:
        """
        Enroll in an available course.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.courses.enroll", _debuild(course_key))
        result = _build(output, None)
        return result

    def unenroll(self, course_key: str) -> None:
        """
        Unenroll from an enrolled course.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.courses.unenroll", _debuild(course_key))
        result = _build(output, None)
        return result


class ModuleStudentLists:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get_all(self) -> dict[str, BriefList]:
        """
        Get all lists.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.lists.getAll", None)
        result = _build(output, dict[str, BriefList])
        return result

    def get(self, list_key: str) -> List:
        """
            Get a list.

            🔐 Authenticated

        Includes items, owner.
        """

        output, ofiles = self._root.execute("student.lists.get", _debuild(list_key))
        result = _build(output, List)
        return result


class ModuleStudentExam:
    """
    ‼️ The state of this module is UNDER CONSTRUCTION. It is not ready for production use. The output of some function is capped if the exam has not started yet.
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get_ready_exams(self) -> list[ReadyExam]:
        """
            Get list of ready exams.

            🔐 Authenticated

        An exam is ready if the current time is between its expected start time minus two days and its expected end time plus two days. Exams are sorted by their distance to the current time and by title order in case of ties.
        """

        output, ofiles = self._root.execute("student.exam.getReadyExams", None)
        result = _build(output, list[ReadyExam])
        return result

    def get(self) -> RunningExam:
        """
        Get current exam.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.exam.get", None)
        result = _build(output, RunningExam)
        return result

    def get_document(self, document_nm: str) -> RunningExamDocument:
        """
        Get a document in an exam.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.exam.getDocument", _debuild(document_nm))
        result = _build(output, RunningExamDocument)
        return result

    def get_document_pdf(self, document_nm: str) -> Download:
        """
        Get PDF of a document in an exam.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.exam.getDocumentPdf", _debuild(document_nm))

        return ofiles[0]

    def get_ranking(self) -> Ranking:
        """
        Get ranking of the current contest.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.exam.getRanking", None)
        result = _build(output, Ranking)
        return result


class ModuleStudentStatuses:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get_all(self) -> dict[str, AbstractStatus]:
        """
        Get statuses for all abstract problems.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.statuses.getAll", None)
        result = _build(output, dict[str, AbstractStatus])
        return result

    def get_for_abstract_problem(self, problem_nm: str) -> AbstractStatus:
        """
        Get status for an abstract problem.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.statuses.getForAbstractProblem", _debuild(problem_nm))
        result = _build(output, AbstractStatus)
        return result

    def get_for_problem(self, problem_id: str) -> Status:
        """
        Get status for a problem.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.statuses.getForProblem", _debuild(problem_id))
        result = _build(output, Status)
        return result


class ModuleStudentAwards:
    """
    This module is not yet finished.
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get_all(self) -> dict[str, BriefAward]:
        """
        Get all awards.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.awards.getAll", None)
        result = _build(output, dict[str, BriefAward])
        return result

    def get(self, award_id: str) -> Award:
        """
        Get an award.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("student.awards.get", _debuild(award_id))
        result = _build(output, Award)
        return result


class ModuleInstructor:
    """
    This module is meant to be used by instructors
    """

    _root: JutgeApiClient

    documents: ModuleInstructorDocuments
    lists: ModuleInstructorLists
    courses: ModuleInstructorCourses
    exams: ModuleInstructorExams
    problems: ModuleInstructorProblems
    queries: ModuleInstructorQueries
    tags: ModuleInstructorTags

    def __init__(self, root: JutgeApiClient):
        self._root = root
        self.documents = ModuleInstructorDocuments(root)
        self.lists = ModuleInstructorLists(root)
        self.courses = ModuleInstructorCourses(root)
        self.exams = ModuleInstructorExams(root)
        self.problems = ModuleInstructorProblems(root)
        self.queries = ModuleInstructorQueries(root)
        self.tags = ModuleInstructorTags(root)


class ModuleInstructorDocuments:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def index(self) -> dict[str, Document]:
        """
        Get index of all documents.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.documents.index", None)
        result = _build(output, dict[str, Document])
        return result

    def get(self, document_nm: str) -> Document:
        """
            Get a document.

            🔐 Authenticated

        The PDF file is not included in the response.
        """

        output, ofiles = self._root.execute("instructor.documents.get", _debuild(document_nm))
        result = _build(output, Document)
        return result

    def get_pdf(self, document_nm: str) -> Download:
        """
        Get PDF of a document.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.documents.getPdf", _debuild(document_nm))

        return ofiles[0]

    def create(self, data: DocumentCreation, ifile: BinaryIO) -> None:
        """
        Create a new document.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.documents.create", _debuild(data), [ifile])
        result = _build(output, None)
        return result

    def update(self, data: DocumentCreation, ifile: BinaryIO) -> None:
        """
        Update a document.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.documents.update", _debuild(data), [ifile])
        result = _build(output, None)
        return result

    def remove(self, document_nm: str) -> None:
        """
        Remove a document.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.documents.remove", _debuild(document_nm))
        result = _build(output, None)
        return result


class ModuleInstructorLists:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def index(self) -> dict[str, InstructorBriefList]:
        """
        Get index of all lists.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.lists.index", None)
        result = _build(output, dict[str, InstructorBriefList])
        return result

    def get(self, list_nm: str) -> InstructorList:
        """
        Get a list.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.lists.get", _debuild(list_nm))
        result = _build(output, InstructorList)
        return result

    def create(self, data: InstructorListCreation) -> None:
        """
        Create a new list.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.lists.create", _debuild(data))
        result = _build(output, None)
        return result

    def update(self, data: InstructorListCreation) -> None:
        """
        Update an existing list.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.lists.update", _debuild(data))
        result = _build(output, None)
        return result

    def remove(self, list_nm: str) -> None:
        """
        Delete an existing list.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.lists.remove", _debuild(list_nm))
        result = _build(output, None)
        return result

    def get_archived(self) -> list[str]:
        """
            Get the list of lists that are archived.

            🔐 Authenticated

        At some point, endpoints related to archiving lists should change as the archive bit will be an attribute of each list.
        """

        output, ofiles = self._root.execute("instructor.lists.getArchived", None)
        result = _build(output, list[str])
        return result

    def archive(self, list_nm: str) -> None:
        """
        Archive a list.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.lists.archive", _debuild(list_nm))
        result = _build(output, None)
        return result

    def unarchive(self, list_nm: str) -> None:
        """
        Unarchive a list.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.lists.unarchive", _debuild(list_nm))
        result = _build(output, None)
        return result


class ModuleInstructorCourses:
    """

    This module manages the courses that an instructor is teaching. It allows the instructor to manage the course, including getting and updating its lists, students and tutors. It can also send invites to pending students and tutors.

    The course name is a unique slug for the course. It is used to reference the course in the system.

    The course title is the human-readable title of the course.

    The course description is a human-readable description of the course.

    Students and tutors are managed in three lists: invited, enrolled and pending. These contains the emails of these users. Invited students and tutors are those who have been invited to the course. Enrolled students and tutors are those who have accepted the invitation and are part of the course. Pending students and tutors are those who have been invited to join the course but have not yet accepted. Enrolled and pending students and tutors are managed by the system and cannot not be modified directly.

    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def index(self) -> dict[str, InstructorBriefCourse]:
        """
        Get index of all courses.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.courses.index", None)
        result = _build(output, dict[str, InstructorBriefCourse])
        return result

    def get(self, course_nm: str) -> InstructorCourse:
        """
        Get a course.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.courses.get", _debuild(course_nm))
        result = _build(output, InstructorCourse)
        return result

    def create(self, data: InstructorCourseCreation) -> None:
        """
            Create a new course.

            🔐 Authenticated

        Only invited students and tutors are taken into account. Enrolled and pending students and tutors are ignored, as these are managed by the system.
        """

        output, ofiles = self._root.execute("instructor.courses.create", _debuild(data))
        result = _build(output, None)
        return result

    def update(self, data: InstructorCourseCreation) -> None:
        """
            Update an existing course.

            🔐 Authenticated

        Only invited students and tutors are taken into account. Enrolled and pending students and tutors are ignored, as these are managed by the system.
        """

        output, ofiles = self._root.execute("instructor.courses.update", _debuild(data))
        result = _build(output, None)
        return result

    def remove(self, course_nm: str) -> None:
        """
            Delete an existing course.

            🔐 Authenticated

        A course should not be deleted. Ask a system administrator to remove it if you really need it.
        """

        output, ofiles = self._root.execute("instructor.courses.remove", _debuild(course_nm))
        result = _build(output, None)
        return result

    def send_invite_to_students(self, course_nm: str) -> None:
        """
            Send invite email to pending students in the course.

            🔐 Authenticated

        Please do not abuse.
        """

        output, ofiles = self._root.execute("instructor.courses.sendInviteToStudents", _debuild(course_nm))
        result = _build(output, None)
        return result

    def send_invite_to_tutors(self, course_nm: str) -> None:
        """
            Send invite email to pending tutors in the course.

            🔐 Authenticated

        Please do not abuse.
        """

        output, ofiles = self._root.execute("instructor.courses.sendInviteToTutors", _debuild(course_nm))
        result = _build(output, None)
        return result

    def get_student_profiles(self, course_nm: str) -> dict[str, StudentProfile]:
        """
        Get the profiles of the students enrolled in the course.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.courses.getStudentProfiles", _debuild(course_nm))
        result = _build(output, dict[str, StudentProfile])
        return result

    def get_tutor_profiles(self, course_nm: str) -> dict[str, StudentProfile]:
        """
        Get the profiles of the tutors enrolled in the course.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.courses.getTutorProfiles", _debuild(course_nm))
        result = _build(output, dict[str, StudentProfile])
        return result

    def get_archived(self) -> list[str]:
        """
            Get the list of courses that are archived.

            🔐 Authenticated

        At some point, endpoints related to archiving courses should change as the archive bit will be an attribute of each course.
        """

        output, ofiles = self._root.execute("instructor.courses.getArchived", None)
        result = _build(output, list[str])
        return result

    def archive(self, course_nm: str) -> None:
        """
        Archive a course.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.courses.archive", _debuild(course_nm))
        result = _build(output, None)
        return result

    def unarchive(self, course_nm: str) -> None:
        """
        Unarchive a course.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.courses.unarchive", _debuild(course_nm))
        result = _build(output, None)
        return result


class ModuleInstructorExams:
    """


    This module manages the exams that an instructor is teaching. It allows the instructor to manage the exam, including getting and updating its documents, problems, students and submissions.

    Exams objects are quite complex. Thus, this interface is also a bit complex. Each part of an exam can be get or updated in a separate endpoint. The main endpoint is the get endpoint, which returns the full exam object.


    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def index(self) -> dict[str, InstructorBriefExam]:
        """
        Get index of all exams.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.exams.index", None)
        result = _build(output, dict[str, InstructorBriefExam])
        return result

    def get(self, exam_nm: str) -> InstructorExam:
        """
        Get an exam.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.exams.get", _debuild(exam_nm))
        result = _build(output, InstructorExam)
        return result

    def get_documents(self, exam_nm: str) -> list[RunningExamDocument]:
        """
        Get documents of an exam.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.exams.getDocuments", _debuild(exam_nm))
        result = _build(output, list[RunningExamDocument])
        return result

    def get_problems(self, exam_nm: str) -> list[InstructorExamProblem]:
        """
        Get problems of an exam.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.exams.getProblems", _debuild(exam_nm))
        result = _build(output, list[InstructorExamProblem])
        return result

    def get_students(self, exam_nm: str) -> list[InstructorExamStudent]:
        """
        Get students of an exam.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.exams.getStudents", _debuild(exam_nm))
        result = _build(output, list[InstructorExamStudent])
        return result

    def get_student(self, exam_nm: str, email: str) -> InstructorExamStudent:
        """
        Get an student of an exam.

        🔐 Authenticated
        """

        data = {"exam_nm": exam_nm, "email": email}
        output, ofiles = self._root.execute("instructor.exams.getStudent", _debuild(data))
        result = _build(output, InstructorExamStudent)
        return result

    def get_submissions(self, exam_nm: str, options: InstructorExamSubmissionsOptions) -> WebStream:
        """
            Get submissions of an exam as a webstream.

            🔐 Authenticated

        Meant for real-time streaming of submissions, most instructors will possibly prefer getSubmissionsPack.
        """

        data = {"exam_nm": exam_nm, "options": options}
        output, ofiles = self._root.execute("instructor.exams.getSubmissions", _debuild(data))
        result = _build(output, WebStream)
        return result

    def get_submissions_pack(self, exam_nm: str, options: InstructorExamSubmissionsOptions) -> Pack:
        """
            Get submissions of an exam as a pack.

            🔐 Authenticated

        This endpoint will prepare the pack in the background and return a link to download it later. Packs take some time to be prepared, and are deleted after 24 hours. This is the preferred endpoint for most instructors, as it is simpler to use than getSubmissions.
        """

        data = {"exam_nm": exam_nm, "options": options}
        output, ofiles = self._root.execute("instructor.exams.getSubmissionsPack", _debuild(data))
        result = _build(output, Pack)
        return result

    def get_statistics(self, exam_nm: str) -> ExamStatistics:
        """
        Get statistics of an exam.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.exams.getStatistics", _debuild(exam_nm))
        result = _build(output, ExamStatistics)
        return result

    def create(self, data: InstructorExamCreation) -> None:
        """
        Create a new exam.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.exams.create", _debuild(data))
        result = _build(output, None)
        return result

    def update(self, data: InstructorExamUpdate) -> None:
        """
        Update an existing exam.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.exams.update", _debuild(data))
        result = _build(output, None)
        return result

    def update_documents(self, exam_nm: str, document_nms: list[str]) -> None:
        """
        Update documents of an exam.

        🔐 Authenticated
        """

        data = {"exam_nm": exam_nm, "document_nms": document_nms}
        output, ofiles = self._root.execute("instructor.exams.updateDocuments", _debuild(data))
        result = _build(output, None)
        return result

    def update_compilers(self, exam_nm: str, compiler_ids: list[str]) -> None:
        """
        Update compilers of an exam.

        🔐 Authenticated
        """

        data = {"exam_nm": exam_nm, "compiler_ids": compiler_ids}
        output, ofiles = self._root.execute("instructor.exams.updateCompilers", _debuild(data))
        result = _build(output, None)
        return result

    def update_problems(self, exam_nm: str, problems: list[InstructorExamProblem]) -> None:
        """
        Update problems of an exam.

        🔐 Authenticated
        """

        data = {"exam_nm": exam_nm, "problems": problems}
        output, ofiles = self._root.execute("instructor.exams.updateProblems", _debuild(data))
        result = _build(output, None)
        return result

    def update_students(self, exam_nm: str, students: list[InstructorExamStudent]) -> None:
        """
        Update students of an exam.

        🔐 Authenticated
        """

        data = {"exam_nm": exam_nm, "students": students}
        output, ofiles = self._root.execute("instructor.exams.updateStudents", _debuild(data))
        result = _build(output, None)
        return result

    def add_students(self, exam_nm: str, students: list[InstructorExamStudent]) -> None:
        """
        Add students to an exam.

        🔐 Authenticated
        """

        data = {"exam_nm": exam_nm, "students": students}
        output, ofiles = self._root.execute("instructor.exams.addStudents", _debuild(data))
        result = _build(output, None)
        return result

    def remove_students(self, exam_nm: str, emails: list[str]) -> None:
        """
        Remove students from an exam.

        🔐 Authenticated
        """

        data = {"exam_nm": exam_nm, "emails": emails}
        output, ofiles = self._root.execute("instructor.exams.removeStudents", _debuild(data))
        result = _build(output, None)
        return result

    def remove(self, exam_nm: str) -> None:
        """
            Delete an existing exam.

            🔐 Authenticated

        Note: An exam can only be deleted if it has not started.
        """

        output, ofiles = self._root.execute("instructor.exams.remove", _debuild(exam_nm))
        result = _build(output, None)
        return result

    def get_archived(self) -> list[str]:
        """
            Get the list of exams that are archived.

            🔐 Authenticated

        At some point, endpoints related to archiving exams should change as the archive bit will be an attribute of each exam.
        """

        output, ofiles = self._root.execute("instructor.exams.getArchived", None)
        result = _build(output, list[str])
        return result

    def archive(self, exam_nm: str) -> None:
        """
        Archive an exam.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.exams.archive", _debuild(exam_nm))
        result = _build(output, None)
        return result

    def unarchive(self, exam_nm: str) -> None:
        """
        Unarchive an exam.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.exams.unarchive", _debuild(exam_nm))
        result = _build(output, None)
        return result

    def get_ranking(self, exam_nm: str) -> Ranking:
        """
            Get the ranking.

            🔐 Authenticated

        Under development.
        """

        output, ofiles = self._root.execute("instructor.exams.getRanking", _debuild(exam_nm))
        result = _build(output, Ranking)
        return result


class ModuleInstructorProblems:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get_own_problems(self) -> list[str]:
        """
        Get the list of own problems.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.problems.getOwnProblems", None)
        result = _build(output, list[str])
        return result

    def get_own_problems_with_passcode(self) -> list[str]:
        """
        Get the list of own problems that have a passcode.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.problems.getOwnProblemsWithPasscode", None)
        result = _build(output, list[str])
        return result

    def get_passcode(self, problem_nm: str) -> str:
        """
            Get the passcode of a problem.

            🔐 Authenticated

        Returns an empty string if the problem has no passcode.
        """

        output, ofiles = self._root.execute("instructor.problems.getPasscode", _debuild(problem_nm))
        result = _build(output, str)
        return result

    def set_passcode(self, problem_nm: str, passcode: str) -> None:
        """
            Set or update the passcode of a problem.

            🔐 Authenticated

        The passcode must be at least 8 characters long and contain only alphanumeric characters. The passcode will be stored in the database in plain text.
        """

        data = {"problem_nm": problem_nm, "passcode": passcode}
        output, ofiles = self._root.execute("instructor.problems.setPasscode", _debuild(data))
        result = _build(output, None)
        return result

    def remove_passcode(self, problem_nm: str) -> None:
        """
        Remove passcode of a problem.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.problems.removePasscode", _debuild(problem_nm))
        result = _build(output, None)
        return result

    def share_passcode(self, problem_nm: str, emails: list[str]) -> None:
        """
            Share passcode to a list of users identified by their email.

            🔐 Authenticated

        No emails are sent. Emails that are not registered in the system are ignored.
        """

        data = {"problem_nm": problem_nm, "emails": emails}
        output, ofiles = self._root.execute("instructor.problems.sharePasscode", _debuild(data))
        result = _build(output, None)
        return result

    def deprecate(self, problem_nm: str, reason: str) -> None:
        """
        Deprecate a problem.

        🔐 Authenticated
        """

        data = {"problem_nm": problem_nm, "reason": reason}
        output, ofiles = self._root.execute("instructor.problems.deprecate", _debuild(data))
        result = _build(output, None)
        return result

    def undeprecate(self, problem_nm: str) -> None:
        """
        Undeprecate a problem.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.problems.undeprecate", _debuild(problem_nm))
        result = _build(output, None)
        return result

    def download(self, problem_nm: str) -> Download:
        """
            Download a problem as a ZIP file.

            🔐 Authenticated

        Quick and dirty implementation, should be improved. Returns a ZIP file with the abstract problem and all its problems.
        """

        output, ofiles = self._root.execute("instructor.problems.download", _debuild(problem_nm))

        return ofiles[0]

    def legacy_create(self, passcode: str, ifile: BinaryIO) -> str:
        """
            Create a problem from a ZIP archive using old PHP code.

            🔐 Authenticated

        At some point, this endpoint will be deprecated. It is a bit slow (about one minute). Returns the problem_nm of the new problem. Does not provide any feedback.
        """

        output, ofiles = self._root.execute("instructor.problems.legacyCreate", _debuild(passcode), [ifile])
        result = _build(output, str)
        return result

    def legacy_update(self, problem_nm: str, ifile: BinaryIO) -> None:
        """
            Update a problem from a ZIP archive using old PHP code.

            🔐 Authenticated

        At some point, this endpoint will be deprecated. Does not provide any feedback.
        """

        output, ofiles = self._root.execute("instructor.problems.legacyUpdate", _debuild(problem_nm), [ifile])
        result = _build(output, None)
        return result

    def legacy_create_with_terminal(self, passcode: str, ifile: BinaryIO) -> WebStream:
        """
            Create a problem from a ZIP archive using old PHP code using terminal streaming.

            🔐 Authenticated

        At some point, this endpoint will be deprecated. Returns a Terminal from which the problem feedback is streamed.
        """

        output, ofiles = self._root.execute("instructor.problems.legacyCreateWithTerminal", _debuild(passcode), [ifile])
        result = _build(output, WebStream)
        return result

    def legacy_update_with_terminal(self, problem_nm: str, ifile: BinaryIO) -> WebStream:
        """
            Update a problem from a ZIP archive using old PHP code using terminal streaming.

            🔐 Authenticated

        At some point, this endpoint will be deprecated. Returns an id from which the problem feedback is streamed under /terminals.
        """

        output, ofiles = self._root.execute("instructor.problems.legacyUpdateWithTerminal", _debuild(problem_nm), [ifile])
        result = _build(output, WebStream)
        return result


class ModuleInstructorQueries:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get_course_problem_submissions(self, course_nm: str, problem_nm: str) -> SubmissionsQuery:
        """
            Get submissions for a problem in a course.

            🔐 Authenticated

        Returns a list of submissions for a given problem for all students of a given course. Each submission includes the email, time, problem name, problem id, verdict, and IP address. The list is ordered by email and time. Known as ricard01 in the past.
        """

        data = {"course_nm": course_nm, "problem_nm": problem_nm}
        output, ofiles = self._root.execute("instructor.queries.getCourseProblemSubmissions", _debuild(data))
        result = _build(output, SubmissionsQuery)
        return result

    def get_course_list_submissions(self, course_nm: str, list_nm: str) -> SubmissionsQuery:
        """
            Get submissions for all problems in a list in a course.

            🔐 Authenticated

        Returns a list of submissions for all problems in a given list for all students of a given course. Each submission includes the email, time, problem name, problem id, verdict, and IP address. The list is ordered by email, problem id and time. Known as ricard02 in the past.
        """

        data = {"course_nm": course_nm, "list_nm": list_nm}
        output, ofiles = self._root.execute("instructor.queries.getCourseListSubmissions", _debuild(data))
        result = _build(output, SubmissionsQuery)
        return result


class ModuleInstructorTags:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def index(self) -> list[str]:
        """
        Get list of all tags.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.tags.index", None)
        result = _build(output, list[str])
        return result

    def get_dict(self) -> TagsDict:
        """
        Get all tags with their problems.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.tags.getDict", None)
        result = _build(output, TagsDict)
        return result

    def get(self, tag: str) -> list[str]:
        """
        Get all problems with a given tag.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("instructor.tags.get", _debuild(tag))
        result = _build(output, list[str])
        return result


class ModuleAdmin:
    """
    Module with administration endpoints. Not meant for regular users. It still lacks lots of endpoints
    """

    _root: JutgeApiClient

    instructors: ModuleAdminInstructors
    users: ModuleAdminUsers
    dashboard: ModuleAdminDashboard
    queue: ModuleAdminQueue
    tasks: ModuleAdminTasks
    stats: ModuleAdminStats
    problems: ModuleAdminProblems

    def __init__(self, root: JutgeApiClient):
        self._root = root
        self.instructors = ModuleAdminInstructors(root)
        self.users = ModuleAdminUsers(root)
        self.dashboard = ModuleAdminDashboard(root)
        self.queue = ModuleAdminQueue(root)
        self.tasks = ModuleAdminTasks(root)
        self.stats = ModuleAdminStats(root)
        self.problems = ModuleAdminProblems(root)


class ModuleAdminInstructors:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get(self) -> InstructorEntries:
        """
        Get instructors.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.instructors.get", None)
        result = _build(output, InstructorEntries)
        return result

    def add(self, email: str, username: str) -> None:
        """
        Add an instructor.

        🔐 Authenticated
        """

        data = {"email": email, "username": username}
        output, ofiles = self._root.execute("admin.instructors.add", _debuild(data))
        result = _build(output, None)
        return result

    def remove(self, email: str) -> None:
        """
        Remove an instructor.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.instructors.remove", _debuild(email))
        result = _build(output, None)
        return result


class ModuleAdminUsers:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def count(self) -> int:
        """
        Count users

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.users.count", None)
        result = _build(output, int)
        return result

    def create(self, data: UserCreation) -> None:
        """
        Create a user

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.users.create", _debuild(data))
        result = _build(output, None)
        return result

    def remove(self, email: str) -> None:
        """
        Remove a user

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.users.remove", _debuild(email))
        result = _build(output, None)
        return result

    def set_password(self, email: str, password: str, message: str) -> None:
        """
        Set a password for a user

        🔐 Authenticated
        """

        data = {"email": email, "password": password, "message": message}
        output, ofiles = self._root.execute("admin.users.setPassword", _debuild(data))
        result = _build(output, None)
        return result

    def get_profiles(self, data: str) -> list[ProfileForAdmin]:
        """
        Get all profiles of users whose email or name contains a specific string

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.users.getProfiles", _debuild(data))
        result = _build(output, list[ProfileForAdmin])
        return result

    def get_all_with_email(self, data: str) -> UsersEmailsAndNames:
        """
        Get all users (well, just email and name) whose email contains a specific string

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.users.getAllWithEmail", _debuild(data))
        result = _build(output, UsersEmailsAndNames)
        return result

    def get_spam_users(self) -> list[str]:
        """
        Get a list of emails of spam users

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.users.getSpamUsers", None)
        result = _build(output, list[str])
        return result

    def remove_spam_users(self, data: list[str]) -> None:
        """
        Remove spam users

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.users.removeSpamUsers", _debuild(data))
        result = _build(output, None)
        return result


class ModuleAdminDashboard:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get_all(self) -> AdminDashboard:
        """
        Get all admin dashboard items.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.dashboard.getAll", None)
        result = _build(output, AdminDashboard)
        return result

    def get_free_disk_space(self) -> FreeDiskSpace:
        """
        Get free disk space.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.dashboard.getFreeDiskSpace", None)
        result = _build(output, FreeDiskSpace)
        return result

    def get_recent_connected_users(self) -> RecentConnectedUsers:
        """
        Get recent connected users.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.dashboard.getRecentConnectedUsers", None)
        result = _build(output, RecentConnectedUsers)
        return result

    def get_recent_load_averages(self) -> RecentLoadAverages:
        """
        Get recent load averages.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.dashboard.getRecentLoadAverages", None)
        result = _build(output, RecentLoadAverages)
        return result

    def get_recent_submissions(self) -> RecentSubmissions:
        """
        Get recent submissions.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.dashboard.getRecentSubmissions", None)
        result = _build(output, RecentSubmissions)
        return result

    def get_submissions_histograms(self) -> SubmissionsHistograms:
        """
        Get submissions histograms.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.dashboard.getSubmissionsHistograms", None)
        result = _build(output, SubmissionsHistograms)
        return result

    def get_zombies(self) -> Zombies:
        """
        Get zombies.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.dashboard.getZombies", None)
        result = _build(output, Zombies)
        return result

    def get_upcoming_exams(self, daysBefore: int, daysAfter: int) -> UpcomingExams:
        """
        Get upcoming exams

        🔐 Authenticated
        """

        data = {"daysBefore": daysBefore, "daysAfter": daysAfter}
        output, ofiles = self._root.execute("admin.dashboard.getUpcomingExams", _debuild(data))
        result = _build(output, UpcomingExams)
        return result

    def get_p_m2_status(self) -> Any:
        """
            Get PM2 status

            🔐 Authenticated

        This endpoint retrieves the status of PM2 processes as reported by `pm2 jlist`.
        """

        output, ofiles = self._root.execute("admin.dashboard.getPM2Status", None)
        result = _build(output, Any)
        return result


class ModuleAdminQueue:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get_queue(self, data: QueueQuery) -> SubmissionQueueItems:
        """
            Get the lattest submissions from the queue in descending chronological order for a certain verdict.

            🔐 Authenticated

        The `limit` parameter tells the number of submissions to retrieve. The `verdicts` parameter is an array of verdicts to filter the submissions. If no verdicts are provided, all submissions will be retrieved.
        """

        output, ofiles = self._root.execute("admin.queue.getQueue", _debuild(data))
        result = _build(output, SubmissionQueueItems)
        return result


class ModuleAdminTasks:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def purge_auth_tokens(self) -> None:
        """
            Purge expired access tokens.

            🔐 Authenticated

        Purge expired access tokens (call it from time to time, it does not hurt)
        """

        output, ofiles = self._root.execute("admin.tasks.purgeAuthTokens", None)
        result = _build(output, None)
        return result

    def clear_caches(self) -> None:
        """
        Clear all memoization caches.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.tasks.clearCaches", None)
        result = _build(output, None)
        return result

    def fatalize_i_es(self) -> None:
        """
        Fatalize IE submissions.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.tasks.fatalizeIEs", None)
        result = _build(output, None)
        return result

    def fatalize_pendings(self) -> None:
        """
        Fatalize pending submissions.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.tasks.fatalizePendings", None)
        result = _build(output, None)
        return result

    def resubmit_i_es(self) -> None:
        """
        Resubmit IE submissions.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.tasks.resubmitIEs", None)
        result = _build(output, None)
        return result

    def resubmit_pendings(self) -> None:
        """
        Resubmit pending submissions.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.tasks.resubmitPendings", None)
        result = _build(output, None)
        return result


class ModuleAdminStats:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get_counters(self) -> dict[str, float]:
        """
        Get counters.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getCounters", None)
        result = _build(output, dict[str, float])
        return result

    def get_distribution_of_verdicts(self) -> dict[str, float]:
        """
        Get distribution of verdicts.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfVerdicts", None)
        result = _build(output, dict[str, float])
        return result

    def get_distribution_of_verdicts_by_year(self) -> list[dict[str, float]]:
        """
        Get distribution of verdicts by year.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfVerdictsByYear", None)
        result = _build(output, list[dict[str, float]])
        return result

    def get_distribution_of_compilers(self) -> dict[str, float]:
        """
        Get distribution of compilers.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfCompilers", None)
        result = _build(output, dict[str, float])
        return result

    def get_distribution_of_proglangs(self) -> dict[str, float]:
        """
        Get distribution of proglangs.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfProglangs", None)
        result = _build(output, dict[str, float])
        return result

    def get_distribution_of_users_by_year(self) -> dict[str, float]:
        """
        Get distribution of registered users by year.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfUsersByYear", None)
        result = _build(output, dict[str, float])
        return result

    def get_distribution_of_users_by_country(self) -> dict[str, float]:
        """
        Get distribution of registered users by country.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfUsersByCountry", None)
        result = _build(output, dict[str, float])
        return result

    def get_distribution_of_users_by_submissions(self, data: int) -> dict[str, float]:
        """
        Get distribution of registered users by submissions using a custom bucket size.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfUsersBySubmissions", _debuild(data))
        result = _build(output, dict[str, float])
        return result

    def get_ranking_of_users(self, limit: int) -> UserRanking:
        """
        Get ranking of users.

        🔐 Authenticated
        ❌ Warning: Input type is not correct
        """

        output, ofiles = self._root.execute("admin.stats.getRankingOfUsers", _debuild(limit))
        result = _build(output, UserRanking)
        return result

    def get_distribution_of_submissions_by_hour(self) -> dict[str, float]:
        """
        Get distribution of submissions by hour.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfSubmissionsByHour", None)
        result = _build(output, dict[str, float])
        return result

    def get_distribution_of_submissions_by_proglang(self) -> dict[str, float]:
        """
        Get distribution of submissions by proglang.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfSubmissionsByProglang", None)
        result = _build(output, dict[str, float])
        return result

    def get_distribution_of_submissions_by_compiler(self) -> dict[str, float]:
        """
        Get distribution of submissions by compiler.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfSubmissionsByCompiler", None)
        result = _build(output, dict[str, float])
        return result

    def get_distribution_of_submissions_by_weekday(self) -> dict[str, float]:
        """
        Get distribution of submissions by weekday.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfSubmissionsByWeekday", None)
        result = _build(output, dict[str, float])
        return result

    def get_distribution_of_submissions_by_year(self) -> dict[str, float]:
        """
        Get distribution of submissions by year.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfSubmissionsByYear", None)
        result = _build(output, dict[str, float])
        return result

    def get_distribution_of_submissions_by_year_for_proglang(self, proglang: str) -> dict[str, float]:
        """
        Get distribution of submissions by year for a proglang.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfSubmissionsByYearForProglang", _debuild(proglang))
        result = _build(output, dict[str, float])
        return result

    def get_distribution_of_submissions_by_day(self) -> dict[str, float]:
        """
        Get distribution of submissions by day.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfSubmissionsByDay", None)
        result = _build(output, dict[str, float])
        return result

    def get_heatmap_calendar_of_submissions(self, data: DateRange) -> Any:
        """
        Get heatmap calendar of submissions.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getHeatmapCalendarOfSubmissions", _debuild(data))
        result = _build(output, Any)
        return result

    def get_distribution_of_domains(self) -> dict[str, float]:
        """
        Get distribution of domains of users' emails.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.stats.getDistributionOfDomains", None)
        result = _build(output, dict[str, float])
        return result


class ModuleAdminProblems:
    """
    No description yet
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def get_solutions(self, problem_id: str) -> list[str]:
        """
        Get list of proglangs for which the problem has an official solution.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.problems.getSolutions", _debuild(problem_id))
        result = _build(output, list[str])
        return result

    def get_solution_as_b64(self, problem_id: str, proglang: str) -> str:
        """
        Get official solution for a problem in proglang as a string in base64.

        🔐 Authenticated
        """

        data = {"problem_id": problem_id, "proglang": proglang}
        output, ofiles = self._root.execute("admin.problems.getSolutionAsB64", _debuild(data))
        result = _build(output, str)
        return result

    def get_solution_as_file(self, problem_id: str, proglang: str) -> Download:
        """
        Get official solution for a problem in proglang as a file.

        🔐 Authenticated
        """

        data = {"problem_id": problem_id, "proglang": proglang}
        output, ofiles = self._root.execute("admin.problems.getSolutionAsFile", _debuild(data))

        return ofiles[0]

    def set_problem_summary(self, problem_id: str, summary: ProblemSummary) -> None:
        """
        Set summary for a problem.

        🔐 Authenticated
        """

        data = {"problem_id": problem_id, "summary": summary}
        output, ofiles = self._root.execute("admin.problems.setProblemSummary", _debuild(data))
        result = _build(output, None)
        return result

    def get_problem_summary(self, problem_id: str) -> Optional[ProblemSummary]:
        """
        Get summary for a problem.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.problems.getProblemSummary", _debuild(problem_id))
        result = _build(output, Optional[ProblemSummary])
        return result

    def get_problems_with_summary(self) -> list[str]:
        """
        Get list of problems with summary.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.problems.getProblemsWithSummary", None)
        result = _build(output, list[str])
        return result

    def get_problems_without_summary(self) -> list[str]:
        """
        Get list of problems without summary.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("admin.problems.getProblemsWithoutSummary", None)
        result = _build(output, list[str])
        return result

    def set_abstract_problem_tag(self, problem_nm: str, tag: AbstractProblemTag) -> None:
        """
        Set AI tags for an abstract problem.

        🔐 Authenticated
        """

        data = {"problem_nm": problem_nm, "tag": tag}
        output, ofiles = self._root.execute("admin.problems.setAbstractProblemTag", _debuild(data))
        result = _build(output, None)
        return result


class ModuleTesting:
    """
    Module with testing endpoints. Not meant for regular users.
    """

    _root: JutgeApiClient

    check: ModuleTestingCheck
    playground: ModuleTestingPlayground

    def __init__(self, root: JutgeApiClient):
        self._root = root
        self.check = ModuleTestingCheck(root)
        self.playground = ModuleTestingPlayground(root)


class ModuleTestingCheck:
    """
    This module is intended for internal use and contains functions to check the actor of the query. General public should not rely on it.
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def check_user(self) -> None:
        """
        Checks that query actor is a user.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.check.checkUser", None)
        result = _build(output, None)
        return result

    def check_instructor(self) -> None:
        """
        Checks that query actor is an instructor.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.check.checkInstructor", None)
        result = _build(output, None)
        return result

    def check_admin(self) -> None:
        """
        Checks that query actor is an admin.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.check.checkAdmin", None)
        result = _build(output, None)
        return result

    def throw_error(self, exception: str) -> None:
        """
        Throw an exception of the given type.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.check.throwError", _debuild(exception))
        result = _build(output, None)
        return result


class ModuleTestingPlayground:
    """
    This module is intended for internal use. General users should not rely on it.
    """

    _root: JutgeApiClient

    def __init__(self, root: JutgeApiClient):
        self._root = root

    def upload(self, data: Name, ifile: BinaryIO) -> str:
        """
        Upload a file.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.playground.upload", _debuild(data), [ifile])
        result = _build(output, str)
        return result

    def negate(self, ifile: BinaryIO) -> Download:
        """
        Get negative of an image.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.playground.negate", None, [ifile])

        return ofiles[0]

    def download(self, data: Name) -> Download:
        """
        Download a file.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.playground.download", _debuild(data))

        return ofiles[0]

    def download2(self, data: Name) -> tuple[str, Download]:
        """
        Download a file with a string.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.playground.download2", _debuild(data))
        result = _build(output, str)
        return result, ofiles[0]

    def ping(self) -> str:
        """
        Ping the server to get a pong string.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.playground.ping", None)
        result = _build(output, str)
        return result

    def to_upper_case(self, s: str) -> str:
        """
        Returns the given string in uppercase.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.playground.toUpperCase", _debuild(s))
        result = _build(output, str)
        return result

    def add2i(self, data: TwoInts) -> int:
        """
        Returns the sum of two integers.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.playground.add2i", _debuild(data))
        result = _build(output, int)
        return result

    def add2f(self, data: TwoFloats) -> float:
        """
        Returns the sum of two floats.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.playground.add2f", _debuild(data))
        result = _build(output, float)
        return result

    def inc(self, data: TwoInts) -> TwoInts:
        """
        increment two numbers.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.playground.inc", _debuild(data))
        result = _build(output, TwoInts)
        return result

    def add3i(self, a: int, b: int, c: int) -> int:
        """
        Returns the sum of three integers.

        🔐 Authenticated
        """

        data = {"a": a, "b": b, "c": c}
        output, ofiles = self._root.execute("testing.playground.add3i", _debuild(data))
        result = _build(output, int)
        return result

    def something(self, data: SomeType) -> SomeType:
        """
        Returns a type with defaults.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.playground.something", _debuild(data))
        result = _build(output, SomeType)
        return result

    def clock(self) -> WebStream:
        """
        Get a webstream with clok data.

        🔐 Authenticated
        """

        output, ofiles = self._root.execute("testing.playground.clock", None)
        result = _build(output, WebStream)
        return result
