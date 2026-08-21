# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestSplitElearningPages(HttpCase):
    def test_catalog_lists_academy_courses(self):
        names = (
            self.env["slide.channel"]
            .with_context(lang="en_US")
            .search(
                [
                    (
                        "id",
                        "in",
                        [
                            self.env.ref(
                                "split_elearning.slide_channel_backgrounds"
                            ).id,
                            self.env.ref(
                                "split_elearning.slide_channel_cutout_acting"
                            ).id,
                            self.env.ref(
                                "split_elearning.slide_channel_cutout_harmony"
                            ).id,
                            self.env.ref(
                                "split_elearning.slide_channel_rigs_harmony"
                            ).id,
                            self.env.ref(
                                "split_elearning.slide_channel_visual_development"
                            ).id,
                            self.env.ref(
                                "split_elearning.slide_channel_creative_writing"
                            ).id,
                        ],
                    )
                ]
            )
            .mapped("name")
        )
        self.assertEqual(len(names), 6)
        self.assertIn("The Art of Creating Backgrounds", names)
        self.assertIn("Cut-out Acting – Bringing Characters to Life", names)
        self.assertIn("Cut-out Animation in Toon Boom Harmony", names)
        self.assertIn("Creating Rigs in Toon Boom Harmony", names)
        self.assertIn("Visual Development – Building Worlds", names)
        self.assertIn("Creative Writing for Animation Projects", names)

    def test_courses_are_public_and_published(self):
        xmlids = (
            "slide_channel_backgrounds",
            "slide_channel_cutout_acting",
            "slide_channel_cutout_harmony",
            "slide_channel_rigs_harmony",
            "slide_channel_visual_development",
            "slide_channel_creative_writing",
        )
        channels = self.env["slide.channel"].browse(
            [self.env.ref(f"split_elearning.{xmlid}").id for xmlid in xmlids]
        )
        self.assertTrue(all(channel.is_published for channel in channels))
        self.assertTrue(all(channel.visibility == "public" for channel in channels))
        self.assertTrue(all(channel.enroll == "public" for channel in channels))
        featured = self.env.ref("split_elearning.slide_channel_backgrounds")
        self.assertTrue(featured.website_url)
        self.assertIn("/slides/", featured.website_url)

    def test_featured_course_shows_about_and_instructor(self):
        channel = self.env.ref(
            "split_elearning.slide_channel_backgrounds"
        ).with_context(lang="en_US")
        lesson_names = channel.slide_ids.mapped("name")
        self.assertIn("About the course", lesson_names)
        self.assertIn("Instructor", lesson_names)
        self.assertIn("Beatriz Gondim", lesson_names)
        self.assertIn("Build a production background", lesson_names)
        about = self.env.ref("split_elearning.slide_lesson_backgrounds_about")
        self.assertTrue(about.is_preview)
        practice = self.env.ref("split_elearning.slide_lesson_backgrounds_practice")
        self.assertFalse(practice.is_preview)

    def test_academy_crm_tag_exists(self):
        tag = self.env.ref("split_elearning.crm_tag_academy")
        self.assertEqual(tag.with_context(lang="en_US").name, "Academy")
        intake = self.env.ref("split_crm_custom.crm_team_intake")
        self.assertTrue(intake.exists())

    def test_courses_menu_points_to_slides(self):
        menu = self.env.ref("website_slides.website_menu_slides")
        self.assertEqual(menu.url, "/slides")
