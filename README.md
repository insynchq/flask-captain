# Flask-Captain

Easy webhooks handling with Flask

So you're using a web service and it supports webhooks with events you might
care about like when you get your money or when an order has been received.
You might also be using Python and Flask is your web framework of choice.
How do you create the server that handles those webhooks you want?

It usually ends up like this:

```python
from flask import Flask, jsonify, request


class Customer(object):
  def __init__(self, customer_id):
    self.customer_id = customer_id

  @classmethod
  def get(cls, customer_id):
    return cls(customer_id)

  def set_as_paid(self):
    print "Customer %r marked as paid" % self.customer_id
    return True

  def send_thanks_email(self):
    print "Sending thanks email to customer %r" % self.customer_id
    return True
    

app = Flask(__name__)


@app.route('/')
def stripe_webhooks():
  if request.json:
    event = request.json['type']
    if event == 'charge.succeeded':
      customer_id = request.json['data']['object']['customer']
      customer = Customer.get(customer_id)
      customer.set_as_paid()
      customer.send_thanks_email()
    elif ...
      # other events
  else:
    abort(400)

if __name__ == '__main__':
  app.run(debug=True)

```

You define a single route and build a colossal if-else block.
It's easier to look at in this example but try adding a few more
event types and you lose DRYness and readability quickly.

Enter Flask-Captain.

Flask-Captain extends the `Blueprint` class with
some added methods to make webhooks handling easier.

```python
from flask.ext.captain import Blueprint

stripe_webhooks = Blueprint('stripe_webhooks', __name__)


@stripe_webhooks.route('/', methods=['POST'])
def handle():
  if request.json:
    return stripe_webhooks.handle_event('stripe.' + request.json['type'])
  else:
    abort(400)


@stripe_webhooks.hook('stripe.charge.succeeded')
def get_customer(event):
  g.customer = Customer.get(request.json['data']['object']['customer'])
  return True


@stripe_webhooks.hook('stripe.charge.succeeded')
def set_as_paid(event):
  return g.customer.set_as_paid()


@stripe_webhooks.hook('stripe.charge.succeeded')
def send_thanks_email(event):
  return g.customer.send_thanks_email()


@stripe_webhooks.hook('stripe.other.event')
@stripe_webhooks.hook('stripe.another.event')
def do_something(event):
  # You can inspect `event` when adding multiple
  # events to a single handler
  return True


if __name__ == '__main__':
  app.register_blueprint(stripe_webhooks)
  app.run(debug=True)

```
