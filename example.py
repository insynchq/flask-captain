from flask import Flask, abort, request
from flask.ext.captain import Blueprint

app = Flask(__name__)
stripe = Blueprint('stripe', __name__)


@stripe.route('/', methods=['POST'])
def stripe_webhooks():
  if request.json:
    return stripe.handle_event('stripe.' + request.json['type'])
  else:
    abort(400)


class Customer(object):
  def __init__(self, customer_id):
    self.customer_id = customer_id

  @classmethod
  def get(cls, customer_id):
    return cls(customer_id)

  def set_as_paid(self):
    print "Customer %r marked as paid" % self.customer_id

  def send_thanks_email(self):
    print "Sending thanks email to customer %r" % self.customer_id


@stripe.hook('stripe.charge.succeeded')
def set_as_paid():
  customer_id = request.json['data']['object']['customer']
  return Customer.get(customer_id).set_as_paid()


@stripe.hook('stripe.charge.succeeded')
def send_thanks_email():
  customer_id = request.json['data']['object']['customer']
  return Customer.get(customer_id).send_thanks_email()


if __name__ == '__main__':
  app.register_blueprint(stripe)
  app.run(debug=True)
