from server.app import app
from flask import json
import fakeredis

r = fakeredis.FakeStrictRedis()
