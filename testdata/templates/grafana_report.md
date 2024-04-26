# Hello, world!

{% for dashboard in dashboards %}
## Grafana dashboard - {{ dashboard.name }}
![{{ dashboard.name }}]({{ render_grafana_dashboard(dashboard.url, width=1024) }} "{{ dashboard.name }}")
{% endfor %}
