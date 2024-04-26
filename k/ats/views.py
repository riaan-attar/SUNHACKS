from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
import tempfile
import docx2txt
import fitz  # PyMuPDF
from .models import Applicant
import google.generativeai as genai
import re


def home(request):
    return render(request,"index.html")

def signup(request):
    return render (request,"login.html")

def submit_application(request):
    if request.method != 'POST':
        return HttpResponse('Invalid request method', status=405)

    name = request.POST.get('name')
    phone = request.post.get('phone')
    email = request.POST.get('email')
    resume_file = request.FILES.get('resume')

    # Validate inputs
    if not (name and email and resume_file and phone):
        return redirect(request,ocr)

    # Check if the uploaded file is an image
    if resume_file.content_type.startswith('image'):
        return HttpResponse('Uploaded file is an image, text extraction is not supported for images', status=400)

    # Extract text from resume file
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

    # Create new Applicant instance and save to database
    new_applicant = Applicant(name=name, email=email,  resume_file=resume_file,phone = phone)
    new_applicant.save()

    return HttpResponse('Application submitted successfully', status=200)

def ocr(request):
    

    return