# INTENT2-Web

This project is a flask-based web demo for illustrating the enrichment process of [INTENT2](https://github.com/rgeorgi/INTENT2), a tool to automatically enrich [Interlinear Glossed Text (IGT)](https://en.wikipedia.org/wiki/Interlinear_gloss) instances, including:

* Alignment between language line and translation line via the gloss
* Part-of-Speech tags via
  * Projection utilizing alignment from above
  * Classification on gloss-line tokens directly
* Dependency Parses via projection 

A demonstration server can be found running at [intent.xigt.org](http://intent.xigt.org).

## Setup

To run this service, minimally `flask` and `intent` must be installed. The module may use flask's built-in development server to run.

I usually deploy my web apps using [`mod_wsgi`](https://pypi.org/project/mod_wsgi/) and Apache. Instructions can be found on flask's website [here](http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/)