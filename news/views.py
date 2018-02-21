from django.shortcuts import render, redirect
"""
The HttpResponse is a class of the django.http module that is
responsible for returning a response to the user
"""
from django.http import Http404  # HttpResponse
from .models import Article
import datetime as dt

# Create your views here.

"""
We define the function that will render our welcome message to the templates.

This function takes in the argument 'request'.

This argument contains the information of the current web request
that has triggered this view and is an instance of the
'django.http.HttpRequest' class.

This means that request is an parameter that passes in a request
object as an argument.


"""


def welcome(request):
    # return HttpResponse('Welcome to Moringa Tribune')
    return render(request, 'welcome.html')


def news_today(request):
    """
    We call our 'todays_news' function that returns news aricles
    published today.
    """
    date = dt.date.today()
    news = Article.todays_news()
    return render(request, 'all-news/todays-news.html',
                  {"date": date, "news": news})


"""
Below we define the view function to display news from a past date.
"""


def past_days_news(request, past_date):
    try:
        # Converts data from the string Url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_today)

    return render(request, 'all-news/past-news.html', {"date": date})


def article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except DoesNotExist:
        raise Http404()

    return render(request, 'all-news/article.html', {"article": article})


def search_results(request):
    """
    This function defines our search results view.

    We first check if the article query exists in our request.GET object
    and then check if it has a value.

    We then get the search term using the get method called on the
    request.GET object.

    Next we call the search_by_title method class method we created in
    our models and pass in the user input.

    We then render a HTML template and pass in the list of articles found
    by our method and the search_term itself
    """
    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',
                      {"message": message, "articles": searched_articles})
    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html', {"message": message})
