# -*- coding: utf-8 -*-
import logging
from tornado import gen
from tornado import web
import motor
from base.handlers import ListHandler, CreateHandler
from .models import NewsModel
from .forms import NewsForm

l = logging.getLogger(__name__)


class NewsListHandler(ListHandler):

    def initialize(self, **kwargs):
        super(NewsListHandler, self).initialize(**kwargs)
        self.model = NewsModel
        self.template_name = "news/list.html"


class NewsCreateHandler(CreateHandler):
    def initialize(self, **kwargs):
        super(NewsCreateHandler, self).initialize(**kwargs)
        self.template_name = "news/create.html"
        self.form_class = NewsForm
        self.success_url = self.reverse_url('news_list')

    @web.authenticated
    @gen.coroutine
    def get(self):
        yield super(NewsCreateHandler, self).get()

    @web.authenticated
    @gen.coroutine
    def post(self):
        yield super(NewsCreateHandler, self).post()

    @gen.coroutine
    def form_valid(self, form):
        obj = form.get_object()
        obj.author = self.current_user
        yield motor.Op(obj.insert, self.db)
        raise gen.Return(True)
