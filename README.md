# Flask-Canvas

Easy webhooks handling with Flask

## Example

```python

from flask import Flask, abort, request
from flask.ext.captain import Captain

app = Flask(__name__)
captain = Captain(app)


@captain.route('/stripe', methods=['POST'])
def stripe():
  if request.json:
    return captain.handle_event('stripe.' + request.json['type'])
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


@captain.hook('stripe.charge.succeeded')
def set_as_paid():
  customer_id = request.json['data']['object']['customer']
  return Customer.get(customer_id).set_as_paid()


@captain.hook('stripe.charge.succeeded')
def send_thanks_email():
  customer_id = request.json['data']['object']['customer']
  return Customer.get(customer_id).send_thanks_email()


if __name__ == '__main__':
  app.run(debug=True)

```
