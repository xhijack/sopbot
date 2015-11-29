SopBot
------
Automatically fill forms and it can be BOT

Installation
---
```
#  git clone https://github.com/xhijack/sopbot
```

Usage
---
```
from form_faker import FormFactory

# if you know the form name
form_factory = FormFactory(url=URL,
                               form_url=FORM_URL,
                               form_name='register_form',

response = form_factory.process()


def select_form(form):
    return form.attrs.get('id', None) == 'mainForm'

# if you didn't know form name
form_factory = FormFactory(url=URL,
                               form_url=FORM_URL,
                               form_name='register_form',
                               select_form=select_form
                               )

form_factory = FormFactory(url=URL,
                               form_url=FORM_URL,
                               form_name='register_form',
                               select_form=select_form,
                               attrs={'email':EMAIL, 'password':PASSWORD, 'password_confirmation':PASSWORD}
                               )


response = form_factory.process()
```

====
Next To Do

Unit Testing

=======
