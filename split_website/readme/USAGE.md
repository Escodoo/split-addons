After installing the module, browse to the website front end:

- `/` home with the featured productions carousel, work galleries, services
  and client testimonials
- `/reel` studio showreel
- `/our-work` client productions
- `/split-originals` in-house intellectual properties
- `/about` studio story and founders
- `/contactus` contact form

Every page is a regular website builder page, so the content can be edited from
the front end with **Edit**.

The contact form creates a `crm.lead` assigned to the **Intake** sales team when
that team exists, tagged with the `Website` medium. The subject, field of work
and portfolio link answers are appended to the lead description.

To refresh the images from the live site, run `tools/download_assets.sh` from the
module directory. It downloads and optimises every picture into
`static/src/binary/ir_attachment/`, which is what `data/ir_attachment_pre.xml`
loads.
