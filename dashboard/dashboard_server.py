from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()


HTML = """
<html>
<head>
<title>CyberDudeBivash Recon Dashboard</title>
</head>

<body>

<h1>CyberDudeBivash Recon Platform</h1>

<p>Attack Surface Monitoring Dashboard</p>

<ul>
<li>Subdomains</li>
<li>Endpoints</li>
<li>JS Assets</li>
<li>Risk Scores</li>
</ul>

</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def dashboard():
    return HTML