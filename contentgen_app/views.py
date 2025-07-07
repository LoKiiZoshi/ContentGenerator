# contentgen_app/views.py

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .ai_generator import generate_text

@csrf_exempt  # only for quick testing; remove in production if using {% csrf_token %} in your form
def prompt_to_content_view(request):
    """
    View to handle user input of a prompt and generate content using the AI generator.
    """
    context = {}

    if request.method == 'POST':
        prompt = request.POST.get('prompt', '').strip()

        if prompt:
            try:
                content = generate_text(prompt)
                context.update({
                    'prompt': prompt,
                    'content': content,
                    'success': True,
                })
            except Exception as e:
                # Safely handle errors in generation
                context.update({
                    'error': f"Error generating content: {e}",
                    'prompt': prompt
                })
        else:
            context['error'] = "Please enter a valid prompt."

    return render(request, 'text_input.html', context)
