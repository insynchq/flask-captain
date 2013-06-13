from flask import (
  Blueprint as _Blueprint,
  jsonify,
)


class Blueprint(_Blueprint):

  handlers = {}
  response_callback = None
  unhandled_callback = None

  def handle(self, event):
    values = {}
    event_handlers = self.handlers.get(event)
    if event_handlers:
      for handler in event_handlers:
        values.setdefault(event, {})[handler.__name__] = handler(event)
      if self.response_callback:
        return self.response_callback(event, values)
      else:
        success = all(
          [
            all(handlers.values()) for handlers in values.values()
          ]
        )
        return jsonify(success=success), 200 if success else 500
    else:
      if self.unhandled_callback:
        return self.unhandled_callback(event)
      else:
        return jsonify(success=True)

  def hook(self, event):
    def wrapper(f):
      self.handlers.setdefault(event, []).append(f)
      return f
    return wrapper

  def response(self, f):
    self.response_callback = f
    return f

  def unhandled(self, f):
    self.unhandled_callback = f
    return f
