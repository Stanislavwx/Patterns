
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .teachers import Teacher

@dataclass
class CourseWork:
    supervisor: Teacher
    title: str

    def submit(self, *args, **kwargs):
        raise NotImplementedError

@dataclass
class OnlineSubmission(CourseWork):
    submitted_file: Optional[str] = None
    def submit(self, filepath: str):
        self.submitted_file = filepath
        return True

@dataclass
class GitHubSubmission(CourseWork):
    repo_url: Optional[str] = None
    def submit(self, repo_url: str):
        if not repo_url.startswith("https://") or "/" not in repo_url:
            raise ValueError("Invalid repository URL")
        self.repo_url = repo_url
        return True

@dataclass
class OralDefense(CourseWork):
    scheduled_slot: Optional[str] = None
    def submit(self, requested_slot: str):
        self.scheduled_slot = requested_slot
        return True
