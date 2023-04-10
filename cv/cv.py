from pylatex import Document, Section, Subsection, Command
from pylatex.utils import bold

# Create document
doc = Document()

# Add header
doc.preamble.append(Command('title', 'My Fancy CV'))
doc.preamble.append(Command('author', 'John Doe'))
doc.preamble.append(Command('date', ''))

# Begin document
doc.append(Section('Personal Information'))
doc.append('Address: 123 Main Street, Anytown USA\n')
doc.append('Phone: (555) 555-5555\n')
doc.append('Email: johndoe@email.com\n')

# Add education
doc.append(Section('Education'))
with doc.create(Subsection('Bachelor of Science in Computer Science')):
    doc.append(bold('University of XYZ\n'))
    doc.append('Graduated: May 2020\n')
with doc.create(Subsection('Master of Science in Data Science')):
    doc.append(bold('University of ABC\n'))
    doc.append('Graduated: May 2022\n')

# Add work experience
doc.append(Section('Work Experience'))
with doc.create(Subsection('Software Developer')):
    doc.append(bold('ABC Company\n'))
    doc.append('May 2022 - Present\n')
    doc.append('Developed software for clients using Python and Django\n')
with doc.create(Subsection('Data Analyst Intern')):
    doc.append(bold('XYZ Corporation\n'))
    doc.append('May 2021 - August 2021\n')
    doc.append('Analyzed data using SQL and Python\n')

# Add skills
doc.append(Section('Skills'))
doc.append('Python, Django, SQL, Data Analysis, Machine Learning')

# Generate PDF
doc.generate_pdf('cv', clean_tex=False)

