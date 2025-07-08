from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .ai_generator import generate_text
from .models import GeneratedContent

@csrf_exempt
def prompt_to_content_view(request):
    context = {}

    if request.method == 'POST':
        prompt = request.POST.get('prompt', '').strip()

        if prompt:
            # Create initial record with status pending
            record = GeneratedContent.objects.create(
                user=request.user if request.user.is_authenticated else None,
                prompt=prompt,
                status='pending'
            )

            try:
                content = generate_text(prompt)
                
                # Simulate counting tokens / words
                tokens_used = len(content.split())

                # Update the record
                record.content = content
                record.tokens_used = tokens_used
                record.status = 'success'
                record.metadata = {'model': 'gpt-4', 'temperature': 0.7}
                record.save()

                context.update({
                    'prompt': prompt,
                    'content': content,
                    'success': True,
                })
            except Exception as e:
                record.status = 'failed'
                record.metadata = {'error': str(e)}
                record.save()
                
                context.update({
                    'error': f"Error generating content: {e}",
                    'prompt': prompt
                })
        else:
            context['error'] = "Please enter a valid prompt."

    return render(request, 'text_input.html', context)
