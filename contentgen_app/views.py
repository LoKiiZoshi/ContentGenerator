from django.shortcuts import render
# contentgen_app/views.py


from .ai_generator import generate_text

def prompt_to_content_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        content = generate_text(prompt)
        return render(request, 'content_result.html', {'prompt': prompt, 'content': content})
    return render(request, 'text_input.html')
