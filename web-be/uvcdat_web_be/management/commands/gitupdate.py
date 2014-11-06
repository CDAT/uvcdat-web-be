from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import git
import os
import os.path

class Command(BaseCommand):
    args = ''
    help = 'updates all submodules'

    def handle(self, *args, **options):
        base = settings.BASE_DIR
        self.stdout.write(os.path.dirname(base))

        repo = git.Repo(os.path.dirname(base))
        sms = repo.submodules
        for sm in sms:
            self.stdout.write(sm.name)
            sm.update()

            #git submodule update --init --recursive
        
