"""Class to describe the 'UFRGS Entrance Exam and GPA Data'.

Persistent link: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/O35FW8

Data Description: Entrance exam scores of students applying to a university in Brazil
(Federal University of Rio Grande do Sul), along with the students' GPAs during the first three
semesters at university. In this dataset, each row contains anonymized information about an
applicant's scores on nine exams taken as part of the application process to the university, as
well as their corresponding GPA during the first three semesters at university.
The dataset has 43,303 rows, each corresponding to one student.
The columns correspond to:
1) Gender. 0 denotes female and 1 denotes male.
2) Score on physics exam
3) Score on biology exam
4) Score on history exam
5) Score on second language exam
6) Score on geography exam
7) Score on literature exam
8) Score on Portuguese essay exam
9) Score on math exam
10) Score on chemistry exam
11) Mean GPA during first three semesters at university, on a 4.0 scale.

We replace the mean GPA with a binary label Y representing whether the student’s GPA was above 3.0


```bibtex
@data{DVN/O35FW8_2019,
  author    = {Castro~da~Silva, Bruno},
  publisher = {Harvard Dataverse},
  title     = {{UFRGS Entrance Exam and GPA Data}},
  UNF       = {UNF:6:MQqEQGXiIfQTbS7q9QJ5uw==},
  year      = {2019},
  version   = {V1},
  doi       = {10.7910/DVN/O35FW8},
  url       = {https://doi.org/10.7910/DVN/O35FW8}
}
```
"""

from typing_extensions import Literal

from ..dataset import Dataset
from ..util import deprecated

__all__ = ["Admissions", "admissions"]

AdmissionsSplits = Literal["Gender"]


@deprecated
def Admissions(  # pylint: disable=invalid-name
    split: AdmissionsSplits = "Gender",
    discrete_only: bool = False,
    binarize_nationality: bool = False,
    binarize_race: bool = False,
) -> Dataset:
    """UFRGS Admissions dataset."""
    return admissions(split, discrete_only, binarize_nationality, binarize_race)


def admissions(
    split: AdmissionsSplits = "Gender",
    discrete_only: bool = False,
    binarize_nationality: bool = False,
    binarize_race: bool = False,
) -> Dataset:
    """UFRGS Admissions dataset."""
    features = [
        "gender",
        "physics",
        "biology",
        "history",
        "language",
        "geography",
        "literature",
        "essay",
        "math",
        "chemistry",
        "gpa",
    ]

    continuous_features = [
        "physics",
        "biology",
        "history",
        "language",
        "geography",
        "literature",
        "essay",
        "math",
        "chemistry",
    ]

    if split == "Gender":
        sens_attr_spec = "gender"
        s_prefix = ["gender"]
        class_label_spec = "gpa"
        class_label_prefix = ["gpa"]
    else:
        raise NotImplementedError

    name = f"Admissions {split}"

    return Dataset(
        name=name,
        num_samples=43_303,
        features=features,
        cont_features=continuous_features,
        sens_attr_spec=sens_attr_spec,
        class_label_spec=class_label_spec,
        filename_or_path="admissions.csv.zip",
        s_prefix=s_prefix,
        class_label_prefix=class_label_prefix,
        discrete_only=discrete_only,
    )