from flask import abort, Flask, g, request
from flask_captain import Captain

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


captain = Captain(app)


@captain.hook('charge.succeeded')
def get_customer(event):
  g.customer = Customer.get(request.json['data']['object']['customer'])
  return True


@captain.hook('charge.succeeded')
def set_as_paid(event):
  return g.customer.set_as_paid()


@captain.hook('charge.succeeded')
def send_thanks_email(event):
  return g.customer.send_thanks_email()


if __name__ == '__main__':
  app.run(debug=True, port=2000)

