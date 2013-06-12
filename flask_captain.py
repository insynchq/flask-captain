from flask import Blueprint as _Blueprint, jsonify


class Blueprint(_Blueprint):

  response_callback = None
  handlers = {}

  def handle_event(self, name):
    values = {}
    event_handlers = self.handlers[name]
    for handler in event_handlers:
      values.setdefault(name, {})[handler.__name__] = handler(name)
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
