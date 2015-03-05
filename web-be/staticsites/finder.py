from django.contrib.staticfiles.finders import BaseFinder, searched_locations
from django.contrib.staticfiles import utils
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage
from django.apps import apps
from collections import OrderedDict
import os.path
import os
import shutil
import re
import yaml
from jinja2 import Environment, PackageLoader
from jinjaext import markdown, media_url, full_url

class StaticSiteFinder(BaseFinder):
    """
    A static files finder that builds static sites using jinja/markdown
    Uses the STATIC_APPS setting to find the hyde sites
    """
    def __init__(self):
        try:
            self.applications = settings.STATIC_APPS
        except AttributeError:
            self.applications = []

        if not isinstance(self.applications, (list, tuple)):
            raise ImproperlyConfigured("STATIC_APPS should be list or tuple.")

        self.storages = OrderedDict()
        for app in self.applications:
            # Build all of the pages in the site to the staticsite directory
            path = os.path.join(settings.BASE_DIR, app, "staticsite")
            self.build_site(app, os.path.dirname(path))
            self.storages[app] = FileSystemStorage(location=path)

    def find(self, path, all=False):

        matches = []
        for loc in self.storages:
            path_gen = (part for part in path.split(os.path.sep) if part)
            current_part = next(path_gen)

            p = os.path.join(settings.BASE_DIR, loc, "deploy")
            if p not in searched_locations:
                searched_locations.append(path)

            while os.path.exists(os.path.join(p, current_part)):
                try:
                    current_part = next(path_gen)
                except StopIteration:
                    return os.path.join(p, current_part)

        return matches
    
    def list(self, ignore_patterns):
        for loc in self.storages:
            storage = self.storages[loc]
            for path in utils.get_files(storage, ignore_patterns):
                yield path, storage

    def build_site(self, app, path):
        env = Environment(loader=PackageLoader(app, 'templates'))
        env.filters["markdown"] = markdown
        env.globals["media_url"] = media_url(app)
        env.globals["full_url"] = full_url(app)

        target = os.path.join(path, "staticsite")
        # Clear everything in staticsite
        if os.path.exists(target):
          shutil.rmtree(target)
        os.mkdir(target)

        target = os.path.join(target, app)
        os.mkdir(target)


        content_path = os.path.join(path, "static-content") 
        site = {
          "static_url": settings.STATIC_URL
        }

        for dirpath, dirnames, filenames in os.walk(content_path):
          if dirpath == os.path.join(content_path, "media"):
            #copy whole directory, and continue
            shutil.copytree(dirpath, os.path.join(target, "media"))
            continue
          relpath = dirpath[len(content_path):]

          for d in dirnames:
            dpath = os.path.join(target, relpath, d)
            os.mkdir(dpath)
          for f in filenames:
            inpath = os.path.join(content_path, relpath, f)
            outpath = os.path.join(target, relpath, f)
            with open(inpath) as infile:
              lines = []
              start = infile.readline()
              if start != "---\n":
                shutil.copyfile(inpath, outpath)
                continue
              line = infile.readline()
              while line != "---\n":
                lines.append(line)
                line = infile.readline()
              frontmatter = "".join(lines)
              frontmatter = yaml.load(frontmatter)
              
              variables = {
                "resource":{
                  "meta":frontmatter
                },
                "site": site
              }

              lines = []
              for line in infile:
                lines.append(line)
              text = "".join(lines)
              t = env.from_string(text)
              with open(outpath, "w") as outfile:
                outfile.write(t.render(**variables))

