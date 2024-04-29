from django.shortcuts import render
from ats.models import Applicant,keyword

from decimal import Decimal
from django.db.models import F
from ats.models import Applicant, keyword
from decimal import Decimal

from django.shortcuts import render
from .models import Applicant

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
import tempfile


from .models import Applicant, keyword
import google.ai.generativelanguage as glm
import google.generativeai as genai
from ats.models import Applicant, keyword


def home(request):
    return render(request, "index.html")

def signup(request):
    return render(request,"login.html")

def hrn(request):
    return render(request , "main.html")

def resume(request):
    return render(request,"resume.html")

def thank(request):
    return render(request,"thankyou.html")


# Configure the Generative AI API with your API ke
# Print the extracted text
import io
import PyPDF2
import pathlib
import google.ai.generativelanguage as glm
import google.generativeai as genai
from django.shortcuts import render
from django.http import HttpResponse
from .models import Applicant, keyword

def resume(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        resume_file = request.FILES.get('resume')

        # Assuming you have saved the uploaded resume as 'resume.pdf'
        pdf_path = 'resume.pdf'

        # Extract text from the resume PDF
        resume_text = extract_text_from_pdf(pdf_path)

        # Provide your API key here
        api_key = "AIzaSyCO_iR3zrQIuFbsy_wGyFOOfhaXr38Ogjc"
        genai.configure(api_key=api_key)

        # Create a GenerativeModel instance
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"FIND ALL THE SKILLS, KEYWORDS IN ABOVE RESUME TEXT {resume_text} THE OUTPUT SHOULD CONTAIN ONLY THE LIST OF SKILLS WHICH I WILL BE STORING IN PYTHON LIST, THE SECOND LAST ELEMENT OF LIST MUST CONTAIN THE FLOAT VALUE OF CGPA, AND LAST VALUE MUST CONTAIN THE TOTAL SUMMATION OF THE EXPERIENCE GIVEN IN RESUME")
        
        # Extracting the text from the response
        text = response._result.candidates[0].content.parts[0].text

        # Now process the extracted keywords
        keywords_list = text.split(',')  # Assuming keywords are separated by comma
        keywords_objects = []
        for keyword_str in keywords_list:
            keyword_str = keyword_str.strip()  # Remove leading/trailing whitespaces
            keyword_obj, created = Keyword.objects.get_or_create(word=keyword_str)
            keywords_objects.append(keyword_obj)

        # Create Applicant instance and save
        applicant = Applicant.objects.create(
            name=name,
            email=email,
            phone=phone,
            resume=resume_file,
            jd=0  # You might need to adjust this field
        )
        applicant.keywords.add(*keywords_objects)  # Add extracted keywords to the applicant
        return redirect('thank')

    return render(request, 'resume.html')


import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf_reader.numPages
        for page_num in range(num_pages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
    return text
# def submit_application(request):
#     if request.method == 'POST':
#         # Get form data
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         resume_file = request.FILES.get('resume')

#         content_type = resume_file.content_type
#         if content_type.startswith('image/'):

            

        

#         # Validate inputs
#         if not (name and email and resume_file and phone):
#             return HttpResponse('Input form is incomplete', status=400)

#         # Extract text from resume file
#         text, content_type = extract_text_from_resume(resume_file)

#         # Call AI function to analyze text
#         if content_type == 'text':
#             keywords_list = get_ai_response(text)
#         else:
#             keywords_list = []

#         # Store extracted information in models
#         new_applicant = Applicant.objects.create(name=name, email=email, phone=phone, resume=resume_file)
#         new_applicant.save()
#         add_keywords_to_applicant(new_applicant, keywords_list)

#         # Create context
#         context = {
#             'name': name,
#             'phone': phone,
#             'email': email,
#             'resume_file': resume_file,
#             'text': text,
#             'keywords_list': keywords_list,
#         }

#         return render(request, "resume.html", context)
#     else:
#         # Render form template
#         return render(request, "submit_application_form.html")

# def extract_text_from_pdf(resume_file):
#     content_type = resume_file.content_type
#     if content_type.startswith('image/'):
#         # Placeholder for image to text conversion
#         return "", 'image'
#     elif content_type == 'application/pdf':
#         return convert_pdf_to_text(resume_file), 'text'
#     elif content_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
#         return convert_doc_to_text(resume_file), 'text'
#     else:
#         # Unsupported file format
#      return None, 'unsupported'

# def convert_pdf_to_text(pdf_file):
#     text = ""
#     with pdf_file.open() as f:
#         pdf_reader = PyPDF2.PdfFileReader(f)
#         for page_num in range(pdf_reader.numPages):
#             text += pdf_reader.getPage(page_num).extractText()
#     return text

# def convert_doc_to_text(doc_file):
#     if doc_file.content_type == 'application/msword':
#         doc = docx.Document(io.BytesIO(doc_file.read()))
#     else:
#         doc = docx.Document(doc_file)
#     text = ""
#     for paragraph in doc.paragraphs:
#         text += paragraph.text + "\n"
#     return text

# def get_ai_response(resume_text):
#     # AI response logic
#     api_key = "YOUR_API_KEY"  # Replace with your actual API key

#     # Configure the Generative AI API with your API key
#     genai.configure(api_key=api_key)

#     # Create a GenerativeModel instance
#     model = genai.GenerativeModel('gemini-pro')

#     # Generate content using the model
#     response = model.generate_content(f"FIND ALL THE  SKILLS , KEYWORDS IN ABOVE RESUME TEXT {resume_text} the OUTPUT SHOULD CONTAIN ONLY THE LIST OF SKILLS WHICH I WILL BE STORING IN PYTHON LIST, THE SECOND LAST ELEMENT OF LIST MUST CONTAIN THE FLOAT VALUE OF CGPA, AND LAST VALUE MUST CONTAIN THE TOTAL SUMMATION OF THE EXPIRIENCE GIVEN IN RESUME ")

#     # Process the response
#     for chunk in response:
#         # Handle the response chunk
#         extracted_text = chunk

#     # Extracting the text from the response
#     text = response._result.candidates[0].content.parts[0].text
#     exp = text.pop()
#     cgpa = text.pop()
#     text = text

#     # Return the extracted text
#     return text , cgpa,exp

def add_keywords_to_applicant(applicant, keywords_list):
    for keyword_text in keywords_list:
        keyword_obj, created = keyword.objects.get_or_create(word=keyword_text)
        applicant.keywords.add(keyword_obj)

           

        



def hrn(request):
    if request.method == 'POST':
        admin_keywords = request.POST.getlist('keywords')  # Assuming the keywords are submitted as a list
        applicants = Applicant.objects.all()

        # Calculate matching score for each applicant
        for applicant in applicants:
            applicant.matching_score = calculate_matching_score(applicant.keywords.split(','), admin_keywords)

        # Sort applicants based on matching score
        sorted_applicants = sorted(applicants, key=lambda x: x.matching_score, reverse=True)

        return render(request, 'main.html', {'applicants': sorted_applicants})

    return render(request, 'main.html')

from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.conf import settings

def upload(request):
    if request.method == 'POST':
        # Retrieve form data
        full_name = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('number')
        resume_file = request.FILES.get('resume')

        # Store the resume file in the media directory
        if resume_file:
            file_path = default_storage.save(resume_file.name, resume_file)
            # You can also save the file path in your database if needed
            # For example:
            # Resume.objects.create(full_name=full_name, email=email, phone_number=phone_number, resume=file_path)
        
        # Redirect to a success page or do any further processing
        return redirect('thank.html')

    return render(request, 'your_template.html')
def process_keywords(request):
    if request.method == 'POST':
        keywords = request.POST.get('TAGS', '')  # Get the value of the input field with name 'TAGS'
        keyword_list = keywords.split(',')  # Split the input string into a list of keywords
        return keyword_list

# scored_applicants = search_and_update_scores(keywords, cgpa, exp)

# Print details of top scoring applicants
# for applicant, score in scored_applicants:
#     print(f"Name: {applicant.name}, Email: {applicant.email}, Score: {score}, Resume: {applicant.resume_file.url}"  