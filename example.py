from flask import Flask, abort, request
from flask.ext.captain import Blueprint

app = Flask(__name__)


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


if __name__ == '__main__':
  app.register_blueprint(stripe_webhooks)
  app.run(debug=True)
