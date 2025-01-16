from django.shortcuts import render, redirect,get_object_or_404
from .models import Task
from .forms import TaskForm
import pyjokes
from django.http import JsonResponse
import pyttsx3
from django.http import HttpResponse
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import joblib  # Load the model if hosted locally
import json
from django.http import JsonResponse
from googletrans import Translator  # For translation functionality

# View for displaying tasks
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# View for adding a task
def add_task(request, task_id=None):
    
    # If task_id is provided, get the task to edit
    if task_id:
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(request.POST or None, instance=task)  # Pre-populate the form if editing
    else:
        form = TaskForm(request.POST or None)  # For new task

    # If it's a POST request, validate and save the form
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to task list after saving

    return render(request, 'tasks/add_task.html', {'form': form, 'task_id': task_id})  # Pass form and task_id

# View for deleting a task
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('task_list')

# View for marking a task as completed
def mark_completed(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')


def pop_jokes(request):
    joke =  pyjokes.get_joke()
    # print(joke)
    return JsonResponse({'joke': joke})



# module for text to speech
def text_speech(request):
    engine = pyttsx3.init()

    # Set voice rate
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 120)

    # Set voice type
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Index 1 for female voice

    # Get text from the GET request
    text = request.GET.get('text', 'Hi, how can I help you?')  # Default text if not provided

    if text:
        engine.say(text)
    else:
        engine.say("Hi, how can I help you?")

    engine.runAndWait()

    return redirect('task_list')



# Load GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

def generate_task_description(title, category):
    # Combine the inputs into a prompt
    prompt = f"Generate a detailed task description for a task titled '{title}' in the category '{category}':\n"

    # Tokenize the input
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    # Generate text
    output = model.generate(
        input_ids,
        max_length=100,  # Max tokens in the output
        num_return_sequences=3,  # Number of outputs
        no_repeat_ngram_size=2,  # Avoid repeated phrases
        temperature=0.9,  # Adjust creativity (higher = more creative)
        top_k=50,  # Consider only top-k words for sampling
        num_beams=5,  # Use beam search with 5 beams
    )

    # Decode the generated text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Alternatively, integrate with an API like OpenAI for hosted models.




def generate_description(request):
    if request.method == "POST":
        try:
            # Parse the JSON body of the request
            data = json.loads(request.body)

            # Extract title and category from the parsed data
            title = data.get("title", "")
            category = data.get("category", "")

            # Ensure that both title and category are provided
            if not title or not category:
                return JsonResponse({"error": "Both title and category are required"}, status=400)

            # Call the text generation function
            description = generate_task_description(title, category)

            return JsonResponse({"description": description})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)


# View for transloter
def translator(request):
    translation = None
    if request.method == "POST":
        text_to_translate = request.POST.get('text_to_translate', '')
        target_language = request.POST.get('target_language', 'en')

        if text_to_translate:
            translator = Translator()
            translation = translator.translate(text_to_translate, dest=target_language)

    return render(request, 'tasks/translator.html')
