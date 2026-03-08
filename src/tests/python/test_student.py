import pytest
import jutge_api_client as j


import re


@pytest.fixture(scope="module")
def jutge():
    client = j.JutgeApiClient()
    client.login("user1@jutge.org", "setzejutges")
    return client


# --- student.profile ---


def test_profile_get(jutge):
    profile = jutge.student.profile.get()
    assert isinstance(profile, j.Profile)
    assert re.fullmatch(r"[0-9a-f]{32}", profile.user_uid)
    assert isinstance(profile.email, str)
    assert profile.name == "User One"


def test_profile_get_avatar(jutge):
    _, avatar = jutge.student.profile.get_avatar()
    assert isinstance(avatar, j.Download)
    signature = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]
    assert avatar.data[:8] == bytes(signature), "Avatar is not a PNG"


def test_profile_update():
    updatable = j.JutgeApiClient()
    updatable.login("updatable@jutge.org", "setzejutges")
    # Save original profile
    original = updatable.student.profile.get()
    # Update name
    updatable.student.profile.update(
        j.NewProfile(
            name="Temp Name",
            birth_year=original.birth_year if original.birth_year is not None else 2000,
            nickname=original.nickname or "",
            webpage=original.webpage or "",
            affiliation=original.affiliation or "",
            description=original.description or "",
            country_id=original.country_id or "AD",
            timezone_id=original.timezone_id,
        )
    )
    updated = updatable.student.profile.get()
    assert updated.name == "Temp Name"
    # Restore original
    updatable.student.profile.update(
        j.NewProfile(
            name=original.name,
            birth_year=original.birth_year if original.birth_year is not None else 2000,
            nickname=original.nickname or "",
            webpage=original.webpage or "",
            affiliation=original.affiliation or "",
            description=original.description or "",
            country_id=original.country_id or "AD",
            timezone_id=original.timezone_id,
        )
    )
    restored = updatable.student.profile.get()
    assert restored.name == original.name


# --- student.keys ---


def test_keys_get(jutge):
    keys = jutge.student.keys.get()
    assert isinstance(keys, j.AllKeys)
    assert isinstance(keys.problems, list)
    assert isinstance(keys.enrolled_courses, list)
    assert isinstance(keys.available_courses, list)
    assert "C00001" in keys.enrolled_courses
    assert "C00002" in keys.available_courses
    assert "C00003" in keys.available_courses


def test_keys_get_problems(jutge):
    problems = jutge.student.keys.get_problems()
    assert isinstance(problems, list)
    assert len(problems) > 0
    assert all(isinstance(p, str) for p in problems)


def test_keys_get_enrolled_courses(jutge):
    courses = jutge.student.keys.get_enrolled_courses()
    assert isinstance(courses, list)
    assert "C00001" in courses


def test_keys_get_available_courses(jutge):
    courses = jutge.student.keys.get_available_courses()
    assert isinstance(courses, list)
    assert "C00002" in courses


def test_keys_get_lists(jutge):
    lists = jutge.student.keys.get_lists()
    assert isinstance(lists, list)
    assert all(isinstance(l, str) for l in lists)


# --- student.statuses ---


def test_statuses_get_all(jutge):
    statuses = jutge.student.statuses.get_all()
    assert isinstance(statuses, dict)
    assert "P68688" in statuses
    status = statuses["P68688"]
    assert isinstance(status, j.AbstractStatus)
    assert isinstance(status.nb_submissions, int)
    assert isinstance(status.status, str)


def test_statuses_get_for_abstract_problem(jutge):
    status = jutge.student.statuses.get_for_abstract_problem("P68688")
    assert isinstance(status, j.AbstractStatus)
    assert status.problem_nm == "P68688"
    assert isinstance(status.nb_submissions, int)
    assert isinstance(status.status, str)


def test_statuses_get_for_problem(jutge):
    status = jutge.student.statuses.get_for_problem("P68688_ca")
    assert isinstance(status, j.Status)
    assert status.problem_id == "P68688_ca"
    assert status.problem_nm == "P68688"
    assert isinstance(status.nb_submissions, int)
    assert isinstance(status.status, str)


# --- student.submissions ---


def test_submissions_get_all(jutge):
    subs = jutge.student.submissions.get_all()
    assert isinstance(subs, list)
    assert len(subs) >= 5
    assert all(isinstance(s, j.Submission) for s in subs)


def test_submissions_index_for_problem(jutge):
    index = jutge.student.submissions.index_for_problem("P68688_ca")
    assert isinstance(index, dict)
    for key, sub in index.items():
        assert isinstance(key, str)
        assert isinstance(sub, j.Submission)


def test_submissions_get(jutge):
    sub = jutge.student.submissions.get(
        j.GetGameResultIn(problem_id="P68688_ca", submission_id="S001")
    )
    assert isinstance(sub, j.Submission)
    assert sub.problem_id == "P68688_ca"
    assert sub.submission_id == "S001"


def test_submissions_get_code_as_b64(jutge):
    code = jutge.student.submissions.get_code_as_b64(
        j.GetGameResultIn(problem_id="P68688_ca", submission_id="S001")
    )
    assert isinstance(code, str)
    assert len(code) > 0


def test_submissions_get_analysis(jutge):
    analysis = jutge.student.submissions.get_analysis(
        j.GetGameResultIn(problem_id="P68688_ca", submission_id="S001")
    )
    assert isinstance(analysis, list)


# --- student.courses ---


def test_courses_index_enrolled(jutge):
    courses = jutge.student.courses.index_enrolled()
    assert isinstance(courses, dict)
    assert "instructor1:FAKE_COURSE1" in courses
    assert isinstance(courses["instructor1:FAKE_COURSE1"], j.BriefCourse)


def test_courses_index_available(jutge):
    courses = jutge.student.courses.index_available()
    assert isinstance(courses, dict)
    assert "instructor1:FAKE_COURSE2" in courses or "instructor1:FAKE_COURSE3" in courses


def test_courses_get_enrolled(jutge):
    course = jutge.student.courses.get_enrolled("instructor1:FAKE_COURSE1")
    assert isinstance(course, j.Course)
    assert course.course_nm == "FAKE_COURSE1"


def test_courses_get_available(jutge):
    course = jutge.student.courses.get_available("instructor1:FAKE_COURSE2")
    assert isinstance(course, j.Course)
    assert course.course_nm == "FAKE_COURSE2"


def test_courses_enroll_unenroll(jutge):
    # Enroll in FAKE_COURSE2
    jutge.student.courses.enroll("instructor1:FAKE_COURSE2")
    enrolled = jutge.student.courses.index_enrolled()
    assert "instructor1:FAKE_COURSE2" in enrolled
    # Unenroll to restore state
    jutge.student.courses.unenroll("instructor1:FAKE_COURSE2")
    enrolled = jutge.student.courses.index_enrolled()
    assert "instructor1:FAKE_COURSE2" not in enrolled


# --- student.dashboard ---


def test_dashboard_get_dashboard(jutge):
    dashboard = jutge.student.dashboard.get_dashboard()
    assert isinstance(dashboard, j.Dashboard)


def test_dashboard_get_stats(jutge):
    stats = jutge.student.dashboard.get_stats()
    assert isinstance(stats, dict)


def test_dashboard_get_level(jutge):
    level = jutge.student.dashboard.get_level()
    assert isinstance(level, str)


def test_dashboard_get_absolute_ranking(jutge):
    ranking = jutge.student.dashboard.get_absolute_ranking()
    assert isinstance(ranking, int)
    assert ranking > 0


def test_dashboard_get_heatmap_calendar(jutge):
    heatmap = jutge.student.dashboard.get_heatmap_calendar()
    assert isinstance(heatmap, list)


def test_dashboard_get_all_distributions(jutge):
    dists = jutge.student.dashboard.get_all_distributions()
    assert isinstance(dists, j.AllDistributions)


# --- student.awards ---


def test_awards_get_all(jutge):
    awards = jutge.student.awards.get_all()
    assert isinstance(awards, dict)
    assert "A00000001" in awards
    assert isinstance(awards["A00000001"], j.BriefAward)


def test_awards_get(jutge):
    award = jutge.student.awards.get("A00000001")
    assert isinstance(award, j.Award)
    assert award.award_id == "A00000001"
    assert award.title == "First AC"
    assert award.type == "solved"


# --- student.lists ---


def test_lists_get_all(jutge):
    lists = jutge.student.lists.get_all()
    assert isinstance(lists, dict)
    for key, brief in lists.items():
        assert isinstance(key, str)
        assert isinstance(brief, j.BriefList)


def test_lists_get(jutge):
    all_lists = jutge.student.lists.get_all()
    assert len(all_lists) > 0
    first_key = next(iter(all_lists))
    lst = jutge.student.lists.get(first_key)
    assert isinstance(lst, j.List)
