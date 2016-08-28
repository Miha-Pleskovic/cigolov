#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import jinja2
import webapp2
import sys

reload(sys)
sys.setdefaultencoding("utf8")

template_dir = os.path.join(os.path.dirname(__file__), "html")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))
#--------------------------------------------------------------------

hair_color = {"črna": "CCAGCAATCGC",
              "rjava": "GCCAGTGCCG",
              "blond": "TTAGCTATCGC"}

face_shape = {"kvadratna": "GCCACGG",
              "okrogla": "ACCACAA",
              "ovalna": "AGGCCTCA"}

eye_color = {"modre": "TTGTGGTGGC",
             "zelene": "GGGAGGTGGC",
             "rjave": "AAGTAGTGAC"}

gender = {"ženska": "TGAAGGACCTTC",
          "moški": "TGCAGGAACTTC"}

race = {"bel": "AAAACCTCA",
        "temnopolt": "CGACTACAG",
        "azijec": "CGCGGGCCG"}

class Suspect(object):
    def __init__(self, name, gender, race, hair_color, eye_color, face_shape):
        self.name = name
        self.gender = gender
        self.race = race
        self.hair_color = hair_color
        self.eye_color = eye_color
        self.face_shape = face_shape

suspects_list = []

eva = Suspect("Eva", "ženska", "bel", "blond", "modre", "ovalna")
larisa = Suspect("Larisa", "ženska", "bel", "rjava", "rjave", "ovalna")
matej = Suspect("Matej", "moški", "bel", "črna", "modre", "ovalna")
miha = Suspect("Miha", "moški", "bel", "rjava", "zelene", "kvadratna")

suspects_list.append(eva)
suspects_list.append(larisa)
suspects_list.append(matej)
suspects_list.append(miha)


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("dna-forensics.html")

    def post(self):
        culprit_gender = "<pre>Spol:          NEZNAN</pre>"
        culprit_race = "<pre>Rasa:          NEZNANA</pre>"
        culprit_hair_color = "<pre>Barva las:     NEZNANA</pre>"
        culprit_eye_color = "<pre>Barva oči:     NEZNANA</pre>"
        culprit_face_shape = "<pre>Oblika obraza: NEZNANA</pre>"
        dna = self.request.get("script")
        culprit = []

        for item in gender:
            if gender[item] in dna:
                culprit_gender = "<pre>Spol:          " + item + "</pre>"
                culprit.append(item)

        for item in race:
            if race[item] in dna:
                culprit_race = "<pre>Rasa:          " + item + "</pre>"
                culprit.append(item)

        for item in hair_color:
            if hair_color[item] in dna:
                culprit_hair_color = "<pre>Barva las:     " + item + "</pre>"
                culprit.append(item)

        for item in eye_color:
            if eye_color[item] in dna:
                culprit_eye_color = "<pre>Barva oči:     " + item + "</pre>"
                culprit.append(item)

        for item in face_shape:
            if face_shape[item] in dna:
                culprit_face_shape = "<pre>Oblika obraza: " + item + "</pre>"
                culprit.append(item)

        self.write(culprit_gender + "<br>")
        self.write(culprit_race + "<br>")
        self.write(culprit_hair_color + "<br>")
        self.write(culprit_eye_color + "<br>")
        self.write(culprit_face_shape + "<br>")
        self.write("<br>")

        for suspect in suspects_list:
            if suspect.gender == culprit[0] and suspect.race == culprit[1] and suspect.hair_color == culprit[2] and suspect.eye_color == culprit[3] and suspect.face_shape == culprit[4]:
                self.write("DNK POVEZAVA NAJDENA!<br>")
                self.write(suspect.name)


app = webapp2.WSGIApplication([
    webapp2.Route("/", MainHandler)
], debug=True)
