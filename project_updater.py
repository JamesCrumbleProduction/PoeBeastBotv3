import git
import os
import sys
import time

UPDATING_BRANCH: str = 'develop'

# i = 50

# print(f'start restarting -> i: {i}')
# time.sleep(10)
# os.execl(sys.executable, sys.executable, *sys.argv)

print(sys.executable, sys.argv)
repo = git.Repo(os.path.dirname(os.path.abspath(__file__)))

current = repo.head.commit

print(not repo.head.commit.diff('develop'))

if not repo.head.commit.diff('develop'):
    print("Repo not changed. Sleep mode activated.")
else:
    print("Repo changed! Activated.")


class ProjectUpdater:

    __slots__ = 'repo',

    def __init__(self):
        self.repo = git.Repo(
            os.path.dirname(os.path.abspath(__file__))
        )
        self._fetch_remotes()
        self._checkout_to_updating_brach()

    def _fetch_remotes(self) -> None:
        for remote in self.repo.remotes:
            remote.fetch()

    def _checkout_to_updating_brach(self) -> None:
        if self.repo.active_branch.name != UPDATING_BRANCH:
            self.repo.git.checkout(UPDATING_BRANCH)

    def _updated(self) -> bool:
        return not repo.head.commit.diff()

    def _update_project(self) -> bool:
        self.repo.git.reset('--hard')

    def _restart_program(self) -> None:
        os.execl(sys.executable, sys.executable, *sys.argv)

    def pending_update(self) -> None:
        if self._updated():
            return
