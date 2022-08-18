import os
import git
import sys

from logger import UPDATER_LOGGER

UPDATING_BRANCH: str = 'master'
CHECKOUT_WITH_FORCE: bool = False
SHOULD_PENDING_FOR_UPDATES: bool = (
    False
    if sys.argv[1:] and sys.argv[1] == 'skip_updates_pending'
    else True
)


class ProjectUpdater:

    __slots__ = 'repo', 'update_output',

    def __init__(self):
        self.repo = git.Repo(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), '..'
            )
        )
        self._fetch_remotes()
        self._checkout_to_updating_branch()
        self.update_output: str = ''

    def _fetch_remotes(self) -> None:
        UPDATER_LOGGER.info('PREPARING TO FETCH ALL REMOTES')
        for remote in self.repo.remotes:
            remote.fetch()

    def _checkout_to_updating_branch(self) -> None:
        if self.repo.active_branch.name != UPDATING_BRANCH:
            UPDATER_LOGGER.info(
                f'PROJECT WILL SWITCH TO "{UPDATING_BRANCH}" BRANCH FORCE={CHECKOUT_WITH_FORCE} (ACTIVE BRANCH: "{self.repo.active_branch.name}")'
            )
            self.repo.git.checkout(UPDATING_BRANCH, force=CHECKOUT_WITH_FORCE)

    def _updated(self) -> bool:
        return not self.repo.head.commit.diff()

    def _update_project(self) -> bool:
        self.repo.git.reset('--hard')
        self.update_output = self.repo.git.pull()
        return self.update_output == 'Already up to date.'

    def _restart_program(self) -> None:
        os.execl(
            sys.executable, sys.executable,
            *[*sys.argv, 'skip_updates_pending']
        )

    def pending_update(self) -> None:
        UPDATER_LOGGER.info(
            f'PENDING FOR UPDATE... (UPDATING BRANCH: "{UPDATING_BRANCH}")'
        )

        if self._updated():
            UPDATER_LOGGER.info('PROJECT ALREADY UPDATED')
            return

        if self._update_project() is False:
            UPDATER_LOGGER.error(
                self.update_output +
                '\nPROJECT WILL RESTART AS OLD VERSION...'
            )

        UPDATER_LOGGER.info(
            'PROJECT SUCCESSFULLY UPDATED. RESTARTING...'
        )
        self._restart_program()


if SHOULD_PENDING_FOR_UPDATES:
    try:
        ProjectUpdater().pending_update()
    except Exception as exception:
        UPDATER_LOGGER.error(
            f'CANNOT UPDATE PROJECT: {exception}', exc_info=True
        )
