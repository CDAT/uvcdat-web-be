import misaka

__markdown_flags__ = misaka.EXT_NO_INTRA_EMPHASIS | misaka.EXT_TABLES | misaka.EXT_FENCED_CODE | misaka.EXT_AUTOLINK | misaka.EXT_STRIKETHROUGH | misaka.EXT_LAX_HTML_BLOCKS | misaka.EXT_SPACE_HEADERS | misaka.EXT_SUPERSCRIPT

def markdown(string):
  return misaka.html(string, extensions = __markdown_flags__)


from django.conf import settings
import os.path
def media_url(app):
  def f(string):
    return os.path.join(settings.STATIC_URL, app, "media")
  return f
