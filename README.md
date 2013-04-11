# Deform templates in Foundation

This is a python package to replace Deform's default templates with templates designed to use Foundation's nice features
(particularly with forms and form errors).

## Dependencies

1. [Zurb's Foundation 4.x](http://foundation.zurb.com/)
2. [Garlic.js](http://garlicjs.org/)

Garlic.js isn't *necessary* for operation, but it does provide nice functionality for your users by saving the form
state to localStorage in the event they accidentally hit the back button or their browser crashes. It's easy to include
on your site:

    <html lang="en">
      <head>
        <script src="//cdnjs.cloudflare.com/ajax/libs/garlic.js/1.2.0/garlic.min.js"></script>
      </head>
      <body>
      </body>
    </html>

## Installation

Inside your virtualenv run: `pip install deform-foundation`; this will install the templates. You now need to include
the "sub-app" into your primary load point for Pyramid. I do this inside of my project's `__init__.py` files towards the
bottom:

    config.include('deform_foundation')
    return config.make_wsgi_app()

## March 25th, 2013

Presently, I've only cleaned up the default form.pt template to remove unnecessary messages when the form is in an
exceptional state and to provide the inter-field form error messages better styled.

All form field error messages use Foundation's form error message styling.
