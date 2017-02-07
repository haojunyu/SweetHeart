from . import main
#from .. import db
from ..models import *

@main.route('/', methods=['GET', 'POST'])
def index():
  return 'hello world!'
