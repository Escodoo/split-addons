Open **Website** and switch to **Split Academia**, or browse
``http://academia.localhost`` (add that host to ``/etc/hosts`` in
development). The homepage introduces the academy; **Courses** opens
the ``/slides`` catalog.

In production, set the Academia website domain to
``https://splitacademia.com.br``.

The public menu is Home, Courses, About, Educators and Contact. Visitors
see **Sign in** in the header; after login the user name replaces it.
The studio website does not show a **Courses** menu.

Open **eLearning** to edit the Academy courses, lessons and tags.
Every course includes an About lesson, a preview class, the official
instructor and a members-only practice brief.

The Contact form creates an Intake lead. In **CRM**, apply the
**Academy** tag on leads that come from course interest.

If this database still has the former ``split_elearning`` module
installed, install ``split_website_elearning`` (do not run ``-u all``
first). The pre-init hook reuses the existing course xmlids.
