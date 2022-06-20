from biohub.subject.createSubject import CreateSubject

CreateSubject("subject_2", "/home/virtualvikings/Work/biohub/test/test_subjects")

from biohub.process.load import Load
from biohub.subject import Subject
from pathlib import Path

subject = Subject(path = "/home/virtualvikings/Work/biohub/test/test_subjects/subject_2/biohub_subject.xml")
Load().run(subject,
           Path("/home/virtualvikings/Work/biohub/test/test_raw/sample1_1.fq"),
           processAttrs = {"backgrounds" : ["load raw"]},
           fileAttrs = {"backgrounds" : ["raw", "single"]})

