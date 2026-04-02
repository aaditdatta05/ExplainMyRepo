from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["ui"])


@router.get("/", response_class=HTMLResponse)
def ui_index() -> str:
    return """
<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>ExplainMyRepo</title>
</head>
<body>
  <h1>ExplainMyRepo</h1>
  <p>Submit a GitHub repository URL to analyze.</p>
      <form method=\"post\" action=\"/analyze/form\">
    <label for=\"repository_url\">Repository URL</label>
    <input id=\"repository_url\" name=\"repository_url\" type=\"url\" />
        <button type=\"submit\">Analyze</button>
  </form>
</body>
</html>
"""
