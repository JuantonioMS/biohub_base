from biohub.utils import GeneralClass


class Project(GeneralClass):


    def newId(self, buffer = []):
        return "bhPJ" + super().newId(buffer)


    def avoidAttrs(self):
        return super().avoidAttrs()