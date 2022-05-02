from .views import app
from .models import graph

graph.run("CREATE CONSTRAINT IF NOT EXISTS ON (n:User) ASSERT (n.username) IS UNIQUE").data()
graph.run("CREATE CONSTRAINT IF NOT EXISTS ON (n:Post) ASSERT (n.id) IS UNIQUE").data()
graph.run("CREATE CONSTRAINT IF NOT EXISTS ON (n:Tag) ASSERT (n.name) IS UNIQUE").data()
graph.run("CREATE INDEX IF NOT EXISTS FOR (n:Post) ON (n.date)").data()

