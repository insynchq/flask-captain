from functools import partial

from flask import Blueprint as _Blueprint, jsonify


class Blueprint(_Blueprint):

  response_callback = None
  handlers = {}

  def handle_event(self, name):
    values = {}
    event_handlers = self.handlers[name]
    for handler in event_handlers:
      args = [name] if len(event_handlers) > 2 else []
      values.setdefault(name, {})[handler.__name__] = handler(*args)
    return self._make_response(values)

  def _make_response(self, values):
    if self.response_callback:
      return self.response_callback(values)
    else:
      success = True
      for handler_values in values:
        if success and not all(handler_values):
          success = False
      return jsonify(success=success), 200 if success else 500

  def response(self, f):
    self.response_callback = f
    return f

  def hook(self, name):
    def wrapper(f):
      self.handlers.setdefault(name, []).append(f)
      return f
    return wrapper


class Captain(Blueprint, object):

  def __init__(self, *args, **kwargs):
    args = list(args)

    if len(args) in (1, 3):
      app = args.pop(0)
    else:
      app = kwargs.pop('app', None)

    self.app = app

    if len(args) < 2:
      kwargs.setdefault('name', 'webhooks')
      kwargs.setdefault('import_name', __name__)

    super(Captain, self).__init__(*args, **kwargs)

    if app:
      self.init_app(app)

  def init_app(self, app):
    app.before_first_request(partial(self.register_blueprint, app))

  def register_blueprint(self, app, *args, **kwargs):
    kwargs.setdefault('url_prefix', '/webhooks')
    app.register_blueprint(self, *args, **kwargs)
