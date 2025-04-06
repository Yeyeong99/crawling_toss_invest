from django.shortcuts import render, redirect
from .models import Comment, CommentAnalysis
from .crawling import crawl_and_save_comments

# Create your views here.
def index(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        if not Comment.objects.filter(company_name=company_name).exists():
            crawl_and_save_comments(company_name)
    else:
        company_name = request.GET.get('company_name')

    comments = Comment.objects.filter(company_name=company_name)
    
    analysis = CommentAnalysis.objects.filter(company_name=company_name).order_by('-created_at').first()
    
    context = {
        'company_name': company_name,
        'comments': comments,
        'analysis': analysis,
    }
    return render(request, 'crawlings/stock_finder.html', context)


def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    company_name = comment.company_name
    comment.delete()
    return redirect(f'/crawlings/?company_name={company_name}')