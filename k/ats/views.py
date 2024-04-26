from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
import tempfile
import docx2txt
import fitz  # PyMuPDF
from .models import Applicant, Keyword
import google.ai.generativelanguage as glm
import google.generativeai as genai


def home(request):
    return render(request, "index.html")


def submit_application(request):
    if request.method != 'POST':
        return HttpResponse('Invalid request method', status=405)

    name = request.POST.get('name')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    resume_file = request.FILES.get('resume')

    # Validate inputs
    if not (name and email and resume_file and phone):
        return HttpResponse('Input form is incomplete', status=400)

    # Check if the uploaded file is an image
    if resume_file.content_type.startswith('image'):
        # Image processing logic
        api_key = "AIzaSyCO_iR3zrQIuFbsy_wGyFOOfhaXr38Ogjc"

        # Configure the Generative AI API with your API key
        genai.configure(api_key=api_key)

        # Create a GenerativeModel instance
        model = genai.GenerativeModel('gemini-pro-vision')

        # Read the image data from the file
        image_data = resume_file.read()

        # Generate content using the model
        response = model.generate_content(
            glm.Content(
                parts=[
                    glm.Part(text="EXTRACT SKILLS , KEYWORDS IN ABOVE RESUME IMAGE the OUTPUT SHOULD CONTAIN ONLY THE LIST OF SKILLS WHICH I WILL BE STORING IN PYTHON LIST, THE SECOND LAST ELEMENT OF LIST MUST CONTAIN THE FLOAT VALUE OF CGPA, AND LAST VALUE MUST CONTAIN THE TOTAL SUMMATION OF THE EXPERIENCE GIVEN IN RESUME "),
                    glm.Part(
                        inline_data=glm.Blob(
                            mime_type=resume_file.content_type,
                            data=image_data
                        )
                    ),
                ],
            ),
            stream=True
        )

        # Process the response
        extracted_text = ''
        for chunk in response:
            # Handle the response chunk
            extracted_text += chunk

        # Call get_ai_response function
        keywords_list = get_ai_response(extracted_text)

        # Create new Applicant instance and save to database
        new_applicant = Applicant(name=name, email=email, resume_file=resume_file, phone=phone)
        new_applicant.save()
        add_keywords_to_applicant(new_applicant, keywords_list)
        return render(request," thankyou.html")
        
    else:
        # Extract text from non-image resume file
        if resume_file.content_type == 'application/pdf':
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in resume_file.chunks():
                    temp_file.write(chunk)
                temp_file.close()
                doc = fitz.open(temp_file.name)
                resume_text = "".join(page.get_text() for page in doc)
                os.unlink(temp_file.name)
        elif resume_file.content_type in [
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        ]:
            resume_text = docx2txt.process(resume_file)
        else:
            return HttpResponse('Unsupported file format', status=400)

        # Call get_ai_response function
        keywords_list = get_ai_response(resume_text)
        exp = keywords_list.pop()
        cgpa = keywords_list.pop()


        # Create new Applicant instance and save to database
        new_applicant = Applicant(name=name, email=email, resume_file=resume_file, phone=phone,exp =exp,cgpa=cgpa)
        new_applicant.save()
        add_keywords_to_applicant(new_applicant, keywords_list)

        return HttpResponse('Application submitted successfully', status=200)


def get_ai_response(resume_text):
    # AI response logic
    api_key = "AIzaSyCO_iR3zrQIuFbsy_wGyFOOfhaXr38Ogjc"

    # Configure the Generative AI API with your API key
    genai.configure(api_key=api_key)

    # Create a GenerativeModel instance
    model = genai.GenerativeModel('gemini-pro')

    # Generate content using the model
    response = model.generate_content(f"FIND ALL THE SKILLS, KEYWORDS IN ABOVE RESUME TEXT {resume_text} THE OUTPUT SHOULD CONTAIN ONLY THE LIST OF SKILLS WHICH I WILL BE STORING IN PYTHON LIST, THE SECOND LAST ELEMENT OF LIST MUST CONTAIN THE FLOAT VALUE OF CGPA, AND LAST VALUE MUST CONTAIN THE TOTAL SUMMATION OF THE EXPERIENCE GIVEN IN RESUME ")

    # Process the response
    for chunk in response:
        # Handle the response chunk
        extracted_text = chunk

    # Extracting the text from the response
    text = response._result.candidates[0].content.parts[0].text
    
    return text


def add_keywords_to_applicant(applicant, keywords_list):
    for keyword_text in keywords_list:
        keyword_obj, created = Keyword.objects.get_or_create(word=keyword_text)
        applicant.keywords.add(keyword_obj)
    return None




def hr_view(request):
    return render(request, "example_template.html")
