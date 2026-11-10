#!/usr/bin/env python
"""
JobBridge — End-to-End Bot
==========================
Runs every major user flow automatically against the JS-driven frontend.
"""
from __future__ import annotations

import argparse
import sys
import time
import traceback
import uuid
from datetime import datetime
from pathlib import Path

from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
    expect,
    sync_playwright,
)

# ============================================================
# Configuration
# ============================================================
BASE_URL = "http://127.0.0.1:8000"
SCREENSHOT_DIR = Path(__file__).parent / "e2e_screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

DEFAULT_PASSWORD = "StrongPass!123"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
GREY = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"


# ============================================================
# Reporter
# ============================================================
class Reporter:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.failures: list[tuple[str, str]] = []
        self.start = time.time()

    def section(self, title: str) -> None:
        print(f"\n{BOLD}{CYAN}{'=' * 70}{RESET}")
        print(f"{BOLD}{CYAN}  {title}{RESET}")
        print(f"{BOLD}{CYAN}{'=' * 70}{RESET}")

    def test_start(self, name: str) -> None:
        print(f"\n{YELLOW}> {name}{RESET}")

    def test_pass(self, name: str) -> None:
        self.passed += 1
        print(f"{GREEN}  [PASS]  {name}{RESET}")

    def test_fail(self, name: str, error: str) -> None:
        self.failed += 1
        self.failures.append((name, error))
        print(f"{RED}  [FAIL]  {name}{RESET}")
        for line in error.strip().splitlines():
            print(f"{RED}          {line}{RESET}")

    def summary(self) -> int:
        elapsed = time.time() - self.start
        print(f"\n{BOLD}{CYAN}{'=' * 70}{RESET}")
        print(f"{BOLD}  SUMMARY{RESET}")
        print(f"{BOLD}{CYAN}{'=' * 70}{RESET}")
        print(f"  {GREEN}Passed:{RESET}  {self.passed}")
        print(f"  {RED}Failed:{RESET}  {self.failed}")
        print(f"  {GREY}Time:  {elapsed:.1f}s{RESET}")
        if self.failures:
            print(f"\n{BOLD}{RED}  Failures:{RESET}")
            for name, err in self.failures:
                first_line = err.strip().splitlines()[0] if err.strip() else "(no details)"
                print(f"    {RED}*{RESET} {name} -- {first_line}")
        print(f"{BOLD}{CYAN}{'=' * 70}{RESET}\n")
        return 0 if self.failed == 0 else 1


# ============================================================
# Helpers
# ============================================================
def unique_email(prefix: str) -> str:
    return f"{prefix}+{uuid.uuid4().hex[:8]}@jobbridge-test.local"


def screenshot(page: Page, name: str) -> Path | None:
    try:
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)[:80]
        stamp = datetime.now().strftime("%H%M%S")
        path = SCREENSHOT_DIR / f"{stamp}_{safe}.png"
        page.screenshot(path=str(path), full_page=True)
        print(f"{GREY}         [screenshot] {path.name}{RESET}")
        return path
    except Exception:
        return None


def body_contains(page: Page, text: str) -> None:
    expect(page.locator("body")).to_contain_text(text)


def body_not_contains(page: Page, text: str) -> None:
    expect(page.locator("body")).not_to_contain_text(text)


def wait_for_ready(page: Page) -> None:
    """Wait for the DOM to be loaded after a navigation / redirect."""
    page.wait_for_load_state("load")


def run_test(reporter: Reporter, name: str, fn, *args) -> bool:
    reporter.test_start(name)
    try:
        fn(*args)
        reporter.test_pass(name)
        return True
    except Exception as exc:  # noqa: BLE001
        err = "".join(traceback.format_exception_only(type(exc), exc))
        reporter.test_fail(name, err)
        for arg in args:
            if isinstance(arg, Page):
                screenshot(arg, name)
                break
        return False


# ============================================================
# Registration helpers (UPDATED for JS-driven forms)
# ============================================================
def register_candidate(page: Page) -> dict:
    email = unique_email("cand")
    page.goto(f"{BASE_URL}/accounts/register/candidate/")
    page.fill('input[name="first_name"]', "Test")
    page.fill('input[name="last_name"]', "Candidate")
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', DEFAULT_PASSWORD)
    page.fill('input[name="password_confirm"]', DEFAULT_PASSWORD)
    page.check('input[name="terms"]')
    
    # JS-based submission: click and wait for the redirect to /candidate/
    page.click('button[type="submit"]')
    page.wait_for_url(f"{BASE_URL}/candidate/", timeout=10000)
    wait_for_ready(page)
    return {"email": email, "password": DEFAULT_PASSWORD}


def register_employer(page: Page) -> dict:
    email = unique_email("emp")
    company = f"Test Co {uuid.uuid4().hex[:6]}"
    page.goto(f"{BASE_URL}/accounts/register/employer/")
    page.fill('input[name="first_name"]', "Test")
    page.fill('input[name="last_name"]', "Employer")
    page.fill('input[name="email"]', email)
    page.fill('input[name="company_name"]', company)
    page.fill('input[name="password"]', DEFAULT_PASSWORD)
    page.fill('input[name="password_confirm"]', DEFAULT_PASSWORD)
    page.check('input[name="terms"]')
    
    # JS-based submission: click and wait for the redirect to /employer/
    page.click('button[type="submit"]')
    page.wait_for_url(f"{BASE_URL}/employer/", timeout=10000)
    wait_for_ready(page)
    return {"email": email, "password": DEFAULT_PASSWORD, "company": company}


# ============================================================
# Candidate tests
# ============================================================
def test_candidate_signup(page: Page) -> None:
    register_candidate(page)
    body_contains(page, "Welcome")


def test_candidate_password_mismatch(page: Page) -> None:
    page.goto(f"{BASE_URL}/accounts/register/candidate/")
    page.fill('input[name="first_name"]', "Test")
    page.fill('input[name="last_name"]', "Mismatch")
    page.fill('input[name="email"]', unique_email("cand"))
    page.fill('input[name="password"]', "StrongPass!123")
    page.fill('input[name="password_confirm"]', "Different!456")
    page.check('input[name="terms"]')
    
    page.click('button[type="submit"]')
    
    # The JS form does not reload the page; it shows an inline alert
    # We wait for the specific alert div to have the error message
    expect(page.locator("#registerAlert")).to_contain_text("Passwords do not match")


def test_candidate_add_education(page: Page) -> None:
    register_candidate(page)
    page.goto(f"{BASE_URL}/candidate/education/")
    page.fill('input[name="degree"]', "BSc Computer Science")
    page.fill('input[name="institution"]', "Test University")
    page.fill('input[name="start_year"]', "2020")
    page.fill('input[name="end_year"]', "2024")
    page.fill('textarea[name="description"]', "Focused on distributed systems")
    page.click('button[type="submit"]')
    body_contains(page, "BSc Computer Science")
    body_contains(page, "Test University")


def test_candidate_delete_education(page: Page) -> None:
    register_candidate(page)
    page.goto(f"{BASE_URL}/candidate/education/")
    page.fill('input[name="degree"]', "Temp Degree")
    page.fill('input[name="institution"]', "Temp Uni")
    page.fill('input[name="start_year"]', "2019")
    page.fill('input[name="end_year"]', "2023")
    page.click('button[type="submit"]')
    body_contains(page, "Temp Degree")
    page.locator('form[action*="education/delete"] button').first.click()
    body_not_contains(page, "Temp Degree")


def test_candidate_add_experience(page: Page) -> None:
    register_candidate(page)
    page.goto(f"{BASE_URL}/candidate/experience/")
    page.fill('input[name="title"]', "Software Engineer")
    page.fill('input[name="company"]', "Acme Corp")
    page.fill('input[name="location"]', "Remote")
    page.fill('input[name="start_date"]', "2022-01-15")
    page.fill('textarea[name="description"]', "Built microservices")
    page.click('button[type="submit"]')
    body_contains(page, "Software Engineer")
    body_contains(page, "Acme Corp")


def test_candidate_add_skill(page: Page) -> None:
    register_candidate(page)
    page.goto(f"{BASE_URL}/candidate/skills/")
    page.fill('input[name="skill"]', "Python")
    page.click('button[type="submit"]')
    expect(page.locator(".skills-list")).to_contain_text("Python")


def test_candidate_update_profile(page: Page) -> None:
    register_candidate(page)
    page.goto(f"{BASE_URL}/candidate/profile/")
    page.fill('input[name="first_name"]', "UpdatedFirst")
    page.fill('input[name="last_name"]', "UpdatedLast")
    page.fill('input[name="phone"]', "+1-555-0100")
    page.fill('input[name="location"]', "New York, USA")
    page.fill('textarea[name="bio"]', "I build things on the web.")
    page.click('button[type="submit"]')
    body_contains(page, "Profile updated")


# ============================================================
# Employer tests
# ============================================================
def test_employer_signup(page: Page) -> None:
    register_employer(page)
    body_contains(page, "Welcome")


def test_employer_update_company(page: Page) -> None:
    register_employer(page)
    page.goto(f"{BASE_URL}/employer/company/")
    page.fill('input[name="name"]', "Updated Company")
    page.fill('input[name="website"]', "https://example.com")
    page.fill('input[name="industry"]', "Software")
    page.select_option('select[name="size"]', "51-200")
    page.fill('textarea[name="description"]', "We build things.")
    page.click('button[type="submit"]')
    body_contains(page, "Company updated")


def create_job(page: Page, title: str = "E2E Test Job") -> None:
    page.goto(f"{BASE_URL}/employer/jobs/create/")
    page.fill('input[name="title"]', title)
    page.select_option('select[name="job_type"]', "full_time")
    page.fill('input[name="location"]', "Remote")
    page.fill('textarea[name="description"]', "Job created by the E2E bot.")
    page.fill('textarea[name="requirements"]', "Python, Django")
    page.fill('textarea[name="responsibilities"]', "Build APIs.")
    page.click('button[type="submit"]')
    page.wait_for_url(f"{BASE_URL}/employer/jobs/", timeout=10000)
    wait_for_ready(page)


def test_employer_post_job(page: Page) -> None:
    register_employer(page)
    create_job(page, "E2E Test Job")
    body_contains(page, "E2E Test Job")


def test_employer_delete_job(page: Page) -> None:
    register_employer(page)
    create_job(page, "Temp Delete Job")
    body_contains(page, "Temp Delete Job")
    page.once("dialog", lambda d: d.accept())
    page.locator('form[action*="/delete/"] button').first.click()
    body_not_contains(page, "Temp Delete Job")


# ============================================================
# Full application pipeline
# ============================================================
def _get_csrf(page: Page) -> str | None:
    return next(
        (c["value"] for c in page.context.cookies() if c["name"] == "csrftoken"),
        None,
    )


def test_full_application_flow(emp_page: Page, cand_page: Page) -> None:
    job_title = f"Full Flow {uuid.uuid4().hex[:6]}"

    # ---- 1. Employer posts job ----
    emp_page.goto(f"{BASE_URL}/employer/jobs/create/")
    emp_page.fill('input[name="title"]', job_title)
    emp_page.select_option('select[name="job_type"]', "full_time")
    emp_page.fill('input[name="location"]', "Remote")
    emp_page.fill('textarea[name="description"]', "Job for the full E2E flow.")
    emp_page.click('button[type="submit"]')
    emp_page.wait_for_url(f"{BASE_URL}/employer/jobs/")
    wait_for_ready(emp_page)
    body_contains(emp_page, job_title)

    # ---- 2. Candidate sees it ----
    cand_page.goto(f"{BASE_URL}/jobs/")
    wait_for_ready(cand_page)
    body_contains(cand_page, job_title)

    # ---- 3. Candidate applies via API ----
    jobs_resp = cand_page.request.get(f"{BASE_URL}/api/")
    if not jobs_resp.ok:
        raise AssertionError(
            f"Jobs API returned {jobs_resp.status} — {jobs_resp.text()[:300]}"
        )
    jobs_json = jobs_resp.json()
    job = next((j for j in jobs_json["results"] if j["title"] == job_title), None)
    if not job:
        raise AssertionError(f"Job {job_title!r} not found in API")

    csrf = _get_csrf(cand_page)
    if not csrf:
        cand_page.goto(f"{BASE_URL}/candidate/")
        wait_for_ready(cand_page)
        csrf = _get_csrf(cand_page)
    if not csrf:
        raise AssertionError("No csrftoken cookie on candidate session")

    apply_resp = cand_page.request.post(
        f"{BASE_URL}/applications/api/",
        headers={
            "X-CSRFToken": csrf,
            "Referer": BASE_URL,
            "Origin": BASE_URL,
        },
        data={"job": job["id"], "cover_letter": "I'd love this role!"},
    )
    if not apply_resp.ok:
        raise AssertionError(
            f"Apply failed: {apply_resp.status} — {apply_resp.text()[:300]}"
        )
    application_id = apply_resp.json().get("id")
    if not application_id:
        raise AssertionError(
            f"Apply response missing 'id': {apply_resp.text()[:300]}"
        )

    # ---- 4. Candidate sees it in their applications ----
    cand_page.goto(f"{BASE_URL}/candidate/applications/")
    wait_for_ready(cand_page)
    body_contains(cand_page, job_title)

    # ---- 5. Employer sees the applicant ----
    emp_page.goto(f"{BASE_URL}/employer/applicants/")
    wait_for_ready(emp_page)
    body_contains(emp_page, "Test Candidate")
    body_contains(emp_page, job_title)

    # ---- 6. Open applicant detail page ----
    detail_url = f"{BASE_URL}/employer/applicants/{application_id}/"
    emp_page.goto(detail_url)
    wait_for_ready(emp_page)
    body_contains(emp_page, "Test Candidate")

    # ---- 7. Shortlist ----
    emp_page.locator('button[value="shortlist"]').click()
    emp_page.wait_for_url(detail_url)
    wait_for_ready(emp_page)
    body_contains(emp_page, "Applicant shortlisted")
    expect(emp_page.locator(".badge").first).to_contain_text("Shortlisted")

    # ---- 8. Confirm on shortlisted list ----
    emp_page.goto(f"{BASE_URL}/employer/shortlisted/")
    wait_for_ready(emp_page)
    body_contains(emp_page, "Test Candidate")

    # ---- 9. Schedule interview ----
    emp_page.goto(detail_url)
    wait_for_ready(emp_page)
    emp_page.locator('button[value="schedule_interview"]').click()
    emp_page.wait_for_url(detail_url)
    wait_for_ready(emp_page)
    body_contains(emp_page, "Interview scheduled")

    # ---- 10. Verify on interviews page ----
    emp_page.goto(f"{BASE_URL}/employer/interviews/")
    wait_for_ready(emp_page)
    body_contains(emp_page, "Test Candidate")
    body_contains(emp_page, job_title)


# ============================================================
# Test registry
# ============================================================
CANDIDATE_TESTS = [
    ("Candidate signup (success)",           test_candidate_signup),
    ("Candidate signup (password mismatch)", test_candidate_password_mismatch),
    ("Candidate add education",              test_candidate_add_education),
    ("Candidate delete education",           test_candidate_delete_education),
    ("Candidate add experience",             test_candidate_add_experience),
    ("Candidate add skill",                  test_candidate_add_skill),
    ("Candidate update profile",             test_candidate_update_profile),
]

EMPLOYER_TESTS = [
    ("Employer signup (success)", test_employer_signup),
    ("Employer update company",   test_employer_update_company),
    ("Employer post job",         test_employer_post_job),
    ("Employer delete job",       test_employer_delete_job),
]


# ============================================================
# Suites
# ============================================================
def run_candidate_suite(reporter: Reporter, browser) -> None:
    reporter.section("CANDIDATE FLOW")
    for name, fn in CANDIDATE_TESTS:
        ctx = browser.new_context()
        page = ctx.new_page()
        page.set_default_timeout(15_000)
        try:
            run_test(reporter, name, fn, page)
        finally:
            ctx.close()


def run_employer_suite(reporter: Reporter, browser) -> None:
    reporter.section("EMPLOYER FLOW")
    for name, fn in EMPLOYER_TESTS:
        ctx = browser.new_context()
        page = ctx.new_page()
        page.set_default_timeout(15_000)
        try:
            run_test(reporter, name, fn, page)
        finally:
            ctx.close()


def run_full_flow(reporter: Reporter, browser) -> None:
    reporter.section("FULL APPLICATION PIPELINE")
    name = "End-to-end: post -> apply -> shortlist -> interview"

    emp_ctx = browser.new_context()
    cand_ctx = browser.new_context()
    emp_page = emp_ctx.new_page()
    cand_page = cand_ctx.new_page()
    emp_page.set_default_timeout(15_000)
    cand_page.set_default_timeout(15_000)

    reporter.test_start(name)
    try:
        register_employer(emp_page)
        register_candidate(cand_page)
        test_full_application_flow(emp_page, cand_page)
        reporter.test_pass(name)
    except Exception as exc:  # noqa: BLE001
        err = "".join(traceback.format_exception_only(type(exc), exc))
        reporter.test_fail(name, err)
        screenshot(emp_page, "full_flow_employer_fail")
        screenshot(cand_page, "full_flow_candidate_fail")
    finally:
        emp_ctx.close()
        cand_ctx.close()


# ============================================================
# Main
# ============================================================
def main() -> int:
    global BASE_URL

    parser = argparse.ArgumentParser(description="JobBridge E2E bot")
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--slowmo", type=int, default=0)
    parser.add_argument("--only", choices=["candidate", "employer", "full"])
    parser.add_argument("--url", default=BASE_URL)
    args = parser.parse_args()

    BASE_URL = args.url.rstrip("/")

    reporter = Reporter()

    print(f"\n{BOLD}JobBridge E2E Bot{RESET}")
    print(f"{GREY}  Target:  {BASE_URL}{RESET}")
    print(f"{GREY}  Mode:    {'HEADED' if args.headed else 'HEADLESS'}{RESET}")
    if args.slowmo:
        print(f"{GREY}  Slowmo:  {args.slowmo}ms{RESET}")
    print(f"{GREY}  Output:  {SCREENSHOT_DIR}{RESET}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=not args.headed,
                slow_mo=args.slowmo,
            )
            try:
                if args.only in (None, "candidate"):
                    run_candidate_suite(reporter, browser)
                if args.only in (None, "employer"):
                    run_employer_suite(reporter, browser)
                if args.only in (None, "full"):
                    run_full_flow(reporter, browser)
            finally:
                browser.close()
    except PlaywrightTimeoutError as exc:
        print(f"\n{RED}Timed out: {exc}{RESET}")
        print(f"{YELLOW}Is the Django server running? -> python manage.py runserver{RESET}")
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"\n{RED}Unexpected error: {exc}{RESET}")
        traceback.print_exc()
        return 1

    return reporter.summary()


if __name__ == "__main__":
    sys.exit(main())