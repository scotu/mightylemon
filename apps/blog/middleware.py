import os
from blog.models import Blog
import settings


class BlogMiddleware:

    def process_request(self, request):
        """
        Sets request.blog to the first Blog. Lame.
        Multiple blogs is too ambitious for now.
        """
        try:
            request.blog = Blog.objects.all()[0]
        except IndexError:
            # Allow administration without a Blog
            # TODO use reverse to find admin urls
            if request.path.find('/admin') != 0:
                raise Exception("Blog not found! Add a blog in the admin please.")
            request.blog = None
        return None


class ThemeMiddleware:

    def process_request(self, request):
        """
        Determines the templates and static files from
        the individual Blog theme.

        Templates are loaded using a custom template loader where
        the theme_dirs can be set during the request.

        Static files are served (in debug-mode) via the Django view
        for static files using the theme directory.
        """
        # theme_dir is the path to all the theme files.
        # /templates and /static should be in this directory.
        theme_dir = os.path.join(settings.THEME_DIR, request.blog.theme)
        custom_path = request.blog.theme_path
        if custom_path:
            if os.path.exists(custom_path):
                theme_dir = custom_path
            else:
                print 'Using default theme since the theme path is not valid: %s' % request.blog.theme_path

        # templates
        from blog import templateloader
        templateloader.theme_template_dirs = (os.path.join(theme_dir, "templates"),)

        # static files
        if settings.DEBUG and request.path.find('/static/') == 0:
            # return view for serving static files
            from django.views.static import serve
            return serve(request, request.path, document_root=theme_dir)

        return None