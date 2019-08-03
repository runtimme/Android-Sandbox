from lib.model.Analysis import Analysis

import base64

import jinja2

class ReportGenerator:

    @staticmethod
    def b64encode(text):
        return base64.b64encode(text).decode('utf8')

    def generate(self, param,searchpath="./"):
        templateLoader = jinja2.FileSystemLoader(searchpath=searchpath)
        templateEnv = jinja2.Environment(loader=templateLoader)

        templateEnv.filters['b64encode'] = ReportGenerator.b64encode

        TEMPLATE_FILE = "templates/index.jinja"
        template = templateEnv.get_template(TEMPLATE_FILE)

        outputText = template.render(param=param)

        path = f"{searchpath}/reports/{param.uuid}.html"
        f = open(path,"w")
        f.write(outputText)
        f.close()
        return path