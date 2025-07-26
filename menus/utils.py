from django.contrib.postgres.search import SearchRank, SearchVector, SearchQuery, SearchHeadline
from menus.models import MenuItem


def q_search(query):
  if query.isdigit() and len(query) <= 5:
    return MenuItem.objects.filter(id=int(query))


  vector = SearchVector("name", "description")
  query = SearchQuery(query)

  result = (
        MenuItem.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )

  result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
  result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
  return result