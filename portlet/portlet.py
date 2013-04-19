import uuid

class BasePortlet(object):
    def __init__(self, template):
        self.tpl_vars = {}
        self.template = template

    def execute(self):
        """Function for whether this portlet should render."""
        return True
  
    def __call__(self, render_func):
        if not self.execute():
            return ''

        return self._execution_complete(render_func)

    def _execution_complete(self, render_func):
        return render_func(self.template, self.tpl_vars)

class Portlet(BasePortlet):
    PREFIX_CSS_CLASS = 'portlet'
    """Base Class for generating chunks of HTML content"""
    def __init__(self, template, css_class=None):
        css_class = css_class or []
        if isinstance(css_class, basestring):
            css_class = [css_class.split(' ')]

        self.css_class = set(css_class)
        self._id = self.html_id()

        super(BasePortlet, self).__init__(template)

    def _execution_complete(self, render_func):
        content = BasePortlet._execution_complete(self, render_func)

        css_class = self.PREFIX_CSS_CLASS
        if self.css_class:
            css_class = '{} {}' % (css_class, ' '.join(self.css_class))

        return '<div class="{}" id="{}">{}</div>'.format(css_class, self._id, content)

    @classmethod
    def html_id(cls, prefix='portlet_'):
        return '{}{}'.format(prefix, uuid.uuid4().hex)

class AsyncPortlet(Portlet):
    def __call__(self, render_func, callback):
        def execute_cb(result):
            if result:
                callback(self._execution_complete(render_func))
            else:
                callback('')

        self.execute(execute_cb)
