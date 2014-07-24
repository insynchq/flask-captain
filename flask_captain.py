from functools import wraps

from flask import Blueprint, request


class Captain(object):

  handlers = {}
  methods = ['GET', 'POST']

  def __init__(self, app=None, blueprint=None, url_prefix=None):
    self.app = app
    self.blueprint = blueprint or Blueprint('captain', __name__)
    self.url_prefix = url_prefix
    if app is not None:
      self.init_app(app)

  def init_app(self, app):
    self.blueprint.route(
      '/',
      methods=self.methods,
    )(self.event_callback)
    app.register_blueprint(
      self.blueprint,
      url_prefix=self.url_prefix,
    )
    app.extensions['flask-captain'] = self

  def event_callback(self):
    if request.json:
      return self.handle(request.json['type'])
    else:
      abort(406)

  def response_callback(self, event, values):
    success = all(
      [
        all(handlers.values()) for handlers in values.values()
      ]
    )
    if not success:
      abort(500)
    return ''

  def unhandled_callback(self, event):
    return ''

  def handle(self, event):
    values = {}
    event_handlers = self.handlers.get(event)
    if event_handlers:
      for handler in event_handlers:
        values.setdefault(event, {})[handler.__name__] = handler(event)
      return self.response_callback(event, values)
    else:
      return self.unhandled_callback(event)

  def event(self, f):
    self.event_callback = f
    return f

  def response(self, f):
    self.response_callback = f
    return f

  def unhandled(self, f):
    self.unhandled_callback = f
    return f

  def hook(self, event):
    def decorator(f):
      self.handlers.setdefault(event, []).append(f)
      return f
    return decorator

