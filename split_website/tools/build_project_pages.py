# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Generate project pages and wrap gallery cards with their URLs."""
# pylint: disable=print-used
# ruff: noqa: E501

import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

MODULE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = MODULE_DIR / "data"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from work_catalog import FILTERS, NEW_PROJECTS, WORK_CARDS  # noqa: E402

PROJECTS = (
    {
        "xml_id": "project_rick_and_morty",
        "url": "/work/rick-and-morty",
        "title": "Rick and Morty",
        "client": "Bardel",
        "kind": "Animated episodes",
        "image": "work_rick_and_morty",
        "banner": "banner_rick_and_morty",
        "back_url": "/our-work",
        "back_label": "Our Work",
        "video": "https://player.vimeo.com/video/727502245?h=ace901b1c8",
        "facts": (
            ("Client", "Bardel"),
            ("Format", "Season 5 episodes"),
            ("Services", "2D Animation"),
        ),
        "summary": (
            "Animated episodes produced for the fifth season of Rick and Morty, "
            "one of the studio's international service titles."
        ),
        "synopsis": (
            "Split joined Bardel on season 5 of Rick and Morty, delivering 2D "
            "animation for one of Adult Swim's flagship comedies. The episodes "
            "sit in the studio's international service slate, next to other "
            "long-running series produced for US networks."
        ),
    },
    {
        "xml_id": "project_hello_kitty",
        "url": "/work/hello-kitty-supercute",
        "title": "Hello Kitty and Friends Supercute Adventures",
        "client": "Sanrio",
        "kind": "Web series",
        "image": "work_hello_kitty_supercute",
        "banner": "banner_hello_kitty",
        "back_url": "/our-work",
        "back_label": "Our Work",
        "video": "https://www.youtube.com/embed/BbCefdlDDTU",
        "facts": (
            ("Client", "Sanrio Brazil"),
            ("Format", "75 x 3′"),
            (
                "Services",
                "Direction, Storyboard & Animatic, Character Design, Props, "
                "Backgrounds, Builds, 2D Animation, Editing, Composition, "
                "Sound FX, Songs, Mix",
            ),
        ),
        "summary": (
            "New episodes produced for the Hello Kitty Brazil, Mexico and "
            "Latin America channels, published on YouTube every Wednesday."
        ),
        "synopsis": (
            "Split directs and produces new episodes of Hello Kitty and Friends "
            "Supercute Adventures for Sanrio Brazil, covering the full 2D "
            "pipeline from storyboard to mix. Fresh episodes land on the Hello "
            "Kitty Brazil, Mexico and Latin America YouTube channels every "
            "Wednesday."
        ),
    },
    {
        "xml_id": "project_tito_and_the_birds",
        "url": "/work/tito-and-the-birds",
        "title": "Tito and the Birds",
        "client": "Bit Productions",
        "kind": "Feature film",
        "image": "work_tito_and_the_birds",
        "banner": "work_tito_and_the_birds",
        "back_url": "/our-work",
        "back_label": "Our Work",
        "video": "https://player.vimeo.com/video/286577783",
        "facts": (
            ("Client", "Bit Productions"),
            ("Release year", "2018"),
            (
                "Services",
                "Storyboard & Animatic, Character Design, Props, "
                "Backgrounds, Builds, 2D Animation",
            ),
        ),
        "summary": (
            "Feature film animation produced with Bit Productions. Split "
            "raised the quality of the conception, animation and art."
        ),
        "synopsis": (
            "Feature-length animation produced with Bit Productions. Split "
            "joined for storyboard, design, backgrounds, builds and 2D "
            "animation, raising the quality of the conception, animation and "
            "art that took Tito to festivals around the world."
        ),
    },
    {
        "xml_id": "project_my_life_is_worth_living",
        "url": "/work/my-life-is-worth-living",
        "title": "My Life Is Worth Living",
        "client": "Wonder Media",
        "kind": "Animated series",
        "image": "work_my_life_is_worth_living",
        "banner": "work_my_life_is_worth_living",
        "back_url": "/our-work",
        "back_label": "Our Work",
        "video": "https://www.youtube.com/embed/rx3X1VJqEq4",
        "facts": (
            ("Client", "Wonder Media"),
            ("Format", "20 x 5 min"),
            (
                "Services",
                "Storyboard & Animatic, Character Designs, Props, "
                "Backgrounds, Builds, 2D Animation, Editing, Compositing",
            ),
        ),
        "summary": (
            "Animated series produced with Wonder Media, part of a slate of "
            "stories designed to communicate through social causes."
        ),
        "synopsis": (
            "A 20 x 5 minute series produced with Wonder Media. The stories "
            "were designed to communicate through social causes, and Split "
            "handled the 2D pipeline from storyboard and character design "
            "through animation, editing and compositing."
        ),
    },
    {
        "xml_id": "project_monica_and_friends",
        "url": "/work/monica-and-friends",
        "title": "Monica and Friends",
        "client": "Mauricio de Sousa Produções",
        "kind": "TV series",
        "image": "work_monica_and_friends",
        "banner": "banner_monica_and_friends",
        "back_url": "/our-work",
        "back_label": "Our Work",
        "video": "https://player.vimeo.com/video/217550961",
        "facts": (
            ("Client", "Cartoon Network"),
            ("Format", "52 x 7′"),
            (
                "Services",
                "Direction, Script, Storyboard & Animatic, Character Design, "
                "Props, Backgrounds, Builds, 2D Animation, Editing, Composition",
            ),
        ),
        "summary": (
            "Classic Monica and Friends episodes produced for Cartoon Network, "
            "one of the most watched Brazilian shows on the channel."
        ),
        "synopsis": (
            "Classic Monica and Friends episodes produced for Cartoon Network: "
            "52 x 7 minutes, from direction and script through the full 2D "
            "pipeline. The series is one of the most watched Brazilian shows "
            "on the channel."
        ),
    },
    {
        "xml_id": "project_fit_ufc",
        "url": "/work/fit-ufc-true-myth",
        "title": "Fit UFC | True Myth",
        "client": "UFC",
        "kind": "Branded series",
        "image": "work_fit_ufc",
        "banner": "work_fit_ufc",
        "back_url": "/our-work",
        "back_label": "Our Work",
        "video": "https://player.vimeo.com/video/655025664?h=9226e530e7",
        "facts": (
            ("Client", "UFC"),
            ("Format", "Branded series"),
            (
                "Services",
                "Direction, Script, Storyboard & Animatic, Voices, "
                "Character Design, Props, Backgrounds, Builds, 2D Animation, "
                "Editing, Composition, Sound FX, Songs, Mix",
            ),
        ),
        "summary": (
            "Branded series produced for UFC, mixing fight mythology with "
            "Split's 2D animation pipeline."
        ),
        "synopsis": (
            "Branded shorts produced for UFC, mixing fight mythology with "
            "Split's 2D pipeline. The studio covered the show from direction "
            "and script through voices, animation, sound and mix."
        ),
    },
    {
        "xml_id": "project_are_you_okay",
        "url": "/work/are-you-okay",
        "title": "Are You Okay?",
        "client": "Wonder Media",
        "kind": "Animated series",
        "image": "work_are_you_okay",
        "banner": "work_are_you_okay",
        "back_url": "/our-work",
        "back_label": "Our Work",
        "video": "https://www.youtube.com/embed/tJsGGsPNakw",
        "facts": (
            ("Client", "Wonder Media"),
            ("Release year", "2021"),
            (
                "Services",
                "Props, Backgrounds, Builds, 2D Animation, Composition",
            ),
        ),
        "summary": (
            "Animated series produced with Wonder Media in 2021, part of the "
            "studio's slate of stories built around social causes."
        ),
        "synopsis": (
            "Produced with Wonder Media in 2021, Are You Okay? uses animation "
            "to open a conversation about mental health. Split delivered "
            "props, backgrounds, builds, 2D animation and composition."
        ),
    },
    {
        "xml_id": "project_is_anybody_out_there",
        "url": "/work/is-anybody-out-there",
        "title": "Is Anybody Out There?",
        "client": "Wonder Media",
        "kind": "Animated series",
        "image": "work_is_anybody_out_there",
        "banner": "work_is_anybody_out_there",
        "back_url": "/our-work",
        "back_label": "Our Work",
        "video": "https://www.youtube.com/embed/xgKdiPFrdl0",
        "facts": (
            ("Client", "Wonder Media"),
            ("Release year", "2022"),
            (
                "Services",
                "Direction, Storyboard & Animatic, Props, Backgrounds, "
                "Builds, 2D Animation, Editing, Composition",
            ),
        ),
        "summary": (
            "Animated series produced with Wonder Media in 2022, directed "
            "in house and delivered through the full 2D pipeline."
        ),
        "synopsis": (
            "The second series Split produced with Wonder Media, this time "
            "with the studio also on direction. The team carried the show "
            "from storyboard and animatic through animation, editing and "
            "composition."
        ),
    },
    {
        "xml_id": "project_bit_wars",
        "url": "/work/bit-wars",
        "title": "Bit Wars",
        "client": "NuBoom",
        "kind": "Promo",
        "image": "work_bit_wars",
        "banner": "banner_bit_wars",
        "back_url": "/our-work",
        "back_label": "Our Work",
        "video": "https://www.youtube.com/embed/z7qujaY59wc",
        "facts": (
            ("Client", "NuBoom"),
            ("Format", "Promo"),
            ("Services", "Layout, Animation"),
        ),
        "summary": ("Promo produced for NuBoom, with Split on layout and animation."),
        "synopsis": (
            "A promo produced for NuBoom. Split handled layout and animation, "
            "turning a retro gaming pitch into a fast, readable piece."
        ),
    },
    {
        "xml_id": "project_mr_men_little_miss",
        "url": "/work/mr-men-little-miss",
        "title": "Mr Men Little Miss",
        "client": "Sanrio Brazil",
        "kind": "Promo",
        "image": "work_mr_men_little_miss",
        "banner": "work_mr_men_little_miss",
        "back_url": "/our-work",
        "back_label": "Our Work",
        "video": "https://player.vimeo.com/video/731166549?h=0f8b2fd4a8",
        "video_ratio": "1x1",
        "facts": (
            ("Client", "Sanrio Brazil"),
            (
                "Services",
                "Direction, Storyboard & Animatic, Voices, Props, "
                "Backgrounds, Builds, 2D Animation, Composition, Sound FX, "
                "Songs, Mix",
            ),
        ),
        "summary": (
            "Promo produced for Sanrio Brazil, covering the full 2D pipeline "
            "from direction to mix."
        ),
        "synopsis": (
            "A promo for Sanrio Brazil's Mr Men Little Miss. Split directed "
            "the piece and covered everything from storyboard and voices to "
            "animation, sound effects, songs and mix."
        ),
    },
    {
        "xml_id": "project_bubu_and_the_little_owls",
        "url": "/work/bubu-and-the-little-owls",
        "title": "Bubu and the Little Owls",
        "client": "Up Content",
        "kind": "Preschool series",
        "image": "work_bubu_and_the_little_owls",
        "banner": "work_bubu_and_the_little_owls",
        "back_url": "/our-work",
        "back_label": "Our Work",
        "video": "https://player.vimeo.com/video/727504876?h=ef9b70da52",
        "facts": (
            ("Client", "Up Content"),
            ("Format", "Preschool series"),
            ("Services", "2D Animation"),
        ),
        "summary": (
            "Preschool series produced with Up Content, with Split on 2D " "animation."
        ),
        "synopsis": (
            "A preschool series produced with Up Content. Split contributed "
            "2D animation to the show that follows Bubu and his owl friends."
        ),
    },
    {
        "xml_id": "project_the_boy_and_the_world",
        "url": "/work/the-boy-and-the-world",
        "title": "The Boy and the World",
        "client": "Paper Films",
        "kind": "Feature film",
        "image": "work_the_boy_and_the_world",
        "banner": "work_the_boy_and_the_world",
        "back_url": "/our-work",
        "back_label": "Our Work",
        "video": "https://www.youtube.com/embed/eqdrwu0NvY8",
        "facts": (
            ("Client", "Paper Films"),
            ("Format", "Feature film"),
            ("Services", "2D Animation"),
        ),
        "summary": (
            "Oscar-nominated feature film produced with Paper Films, with "
            "Split on 2D animation."
        ),
        "synopsis": (
            "Feature film produced with Paper Films. Split contributed 2D "
            "animation to a film that travelled the festival circuit and "
            "reached an Academy Award nomination."
        ),
    },
    {
        "xml_id": "project_weeboom",
        "url": "/originals/weeboom",
        "title": "WeeBoom",
        "client": "Split Studio",
        "kind": "Preschool series",
        "image": "original_weeboom",
        "banner": "original_weeboom",
        "back_url": "/split-originals",
        "back_label": "Split Originals",
        "layout": "weeboom",
        "facts": (
            ("Format", "26 x 7′ | 4 to 7 years old"),
            ("Genres", "Comedy | Adventure | Travel"),
        ),
        "summary": (
            "Original preschool series created inside the studio. The first "
            "season is available in multiple territories."
        ),
        "synopsis": (
            "WEE is an adventurous, smart and strong-willed rabbit. BOOM is a "
            "goofy mythical creature full of special powers. Together, they "
            "travel through cities around the world in search of capturing "
            "the BOOMIES, fun little magical creatures that are spreading "
            "chaos everywhere!"
        ),
    },
    {
        "xml_id": "project_among_the_stars",
        "url": "/originals/among-the-stars",
        "title": "Among the Stars",
        "client": "Split Studio",
        "kind": "Game",
        "image": "banner_among_the_stars",
        "banner": "banner_among_the_stars",
        "back_url": "/split-originals",
        "back_label": "Split Originals",
        "facts": (
            ("Client", "Split Studio"),
            ("Format", "Game"),
            ("Status", "In development"),
        ),
        "summary": (
            "Split original game. Help make this project a reality on Catarse."
        ),
        "synopsis": (
            "Among the Stars is an original game created inside Split. The "
            "studio is developing the world, characters and animation in "
            "house and inviting the audience to help make the project a "
            "reality on Catarse."
        ),
        "cta_label": "Support on Catarse",
        "cta_href": "https://www.catarse.com.br/entreasestrelas-original",
    },
    {
        "xml_id": "project_whats_up_bud",
        "url": "/originals/whats-up-bud",
        "title": "What's Up, Bud?",
        "client": "Split Studio",
        "kind": "Comedy series",
        "image": "original_whats_up_bud",
        "banner": "original_whats_up_bud",
        "back_url": "/split-originals",
        "back_label": "Split Originals",
        "video": "https://player.vimeo.com/video/642375897?h=118e81dc08",
        "facts": (
            ("Created by", "Michele Massagli"),
            (
                "Services",
                "Direction, Script, Storyboard & Animatic, Voices, "
                "Character Design, Props, Backgrounds, Builds, 2D Animation, "
                "Editing, Composition, Sound FX, Songs, Mix",
            ),
        ),
        "summary": (
            "Original comedy series created by Michele Massagli and produced "
            "inside Split."
        ),
        "synopsis": (
            "An original comedy series created by Michele Massagli. Split "
            "covers the full 2D pipeline, from direction and script through "
            "voices, animation, sound and mix."
        ),
        "cta_label": "Co-produce with us",
    },
    {
        "xml_id": "project_charcoal_swordsman",
        "url": "/originals/the-charcoal-swordsman",
        "title": "The Charcoal Swordsman",
        "client": "Split Studio",
        "kind": "Series in development",
        "image": "original_charcoal_swordsman",
        "banner": "charcoal_cover",
        "back_url": "/split-originals",
        "back_label": "Split Originals",
        "layout": "ip",
        "hero_image": "charcoal_cover",
        "logo": "charcoal_logo",
        "seal": "charcoal_seal",
        "format": "10 x 22′ | 12+ years old",
        "genres": "Adventure | Fantasy | Drama",
        "highlights": (
            "Based on Affonso Solano's work",
            "Produced by Split Studio",
            "Teaser project released in CCXP19",
        ),
        "tagline": "A divided world. A unique journey.",
        "video": "https://www.youtube.com/embed/Y4jV4n_K7mc",
        "characters": (
            {
                "image": "charcoal_character_adapak",
                "name": "Adapak",
                "role": "",
                "bio": (
                    "A kind and altruistic youth with white eyes and dark "
                    "skin. Adapak wanders the world of Kurgala, searching "
                    "for a meaning to his own existence and unraveling the "
                    "mysteries that The Four That Are One hide from mortals. "
                    "He is a master of the Tibaul Circles, a martial art "
                    "that lets him defend himself from multiple opponents at "
                    "once. Despite being extremely cultured and skilled in "
                    "combat, his innocence and inexperience in the mortal "
                    "world involuntarily involve him in conflict."
                ),
            },
            {
                "image": "charcoal_character_sirara",
                "name": "Sirara",
                "role": "Loyal Companion",
                "bio": (
                    "A human of nearly 25 cycles. She is the captain of a "
                    "ship she inherited from her deceased uncle and shelters "
                    "Adapak at the beginning of his journey, helping him "
                    "travel to the island of Caspama. A woman of strong "
                    "personality, she uses it to disguise her own "
                    "insecurities. Sirara is one of the only mortals to "
                    "know Adapak's origin."
                ),
            },
        ),
        "gallery": (
            "charcoal_still_01",
            "charcoal_still_02",
            "charcoal_still_03",
            "charcoal_still_04",
        ),
        "facts": (
            ("Format", "10 x 22′ | 12+ years old"),
            ("Genres", "Adventure | Fantasy | Drama"),
        ),
        "summary": (
            "Original adventure series based on Affonso Solano's work. The "
            "teaser was released at CCXP19."
        ),
        "synopsis": (
            "Welcome to a world divided between the wild and the civilized, "
            "the mundane and the sacred, where forests and deserts hide "
            "ruins of once-forgotten gods and the seas shelter monsters "
            "capable of swallowing ships; where bone blades keep the law in "
            "cities of rock and wood, and a plurality of species must live "
            "together — in harmony or not."
        ),
        "cta_label": "Co-produce with us",
    },
    {
        "xml_id": "project_sun_boy",
        "url": "/originals/sun-boy-and-friends",
        "title": "Sun Boy and Friends",
        "client": "Midas Productions",
        "kind": "Music videos",
        "image": "original_sun_boy",
        "banner": "original_sun_boy",
        "back_url": "/split-originals",
        "back_label": "Split Originals",
        "video": "https://www.youtube.com/embed/dfgleWIL04s",
        "facts": (
            ("Client", "Midas Productions"),
            (
                "Services",
                "Direction, Storyboard & Animatic, Character Design, Props, "
                "Backgrounds, Builds, 2D Animation, Editing, Composition",
            ),
        ),
        "summary": ("Music videos for Sun Boy and Friends, with songs by Vitor Kley."),
        "synopsis": (
            "Animated music videos for Sun Boy and Friends, produced with "
            "Midas Productions and scored with Vitor Kley's songs. Split "
            "directed the pieces and carried them through the 2D pipeline."
        ),
        "cta_label": "Co-produce with us",
    },
    {
        "xml_id": "project_que_corpo_e_esse",
        "url": "/originals/que-corpo-e-esse",
        "title": "Que Corpo é Esse?",
        "client": "Canal Futura",
        "kind": "Original series",
        "image": "original_que_corpo_e_esse",
        "banner": "original_que_corpo_e_esse",
        "back_url": "/split-originals",
        "back_label": "Split Originals",
        "video": "https://player.vimeo.com/video/235423978?h=92bcd23f38",
        "facts": (
            ("Client", "Canal Futura"),
            (
                "Services",
                "Direction, Script, Storyboard & Animatic, Voices, "
                "Character Design, Props, Backgrounds, Builds, 2D Animation, "
                "Editing, Composition, Sound FX, Songs, Mix",
            ),
        ),
        "summary": (
            "Original series produced with Canal Futura, covering the full "
            "2D pipeline."
        ),
        "synopsis": (
            "An original series produced with Canal Futura. Split directed "
            "the show and covered everything from script and voices to "
            "animation, sound and mix."
        ),
        "cta_label": "Co-produce with us",
    },
    {
        "xml_id": "project_wizavior",
        "url": "/originals/wizavior",
        "title": "Wizavior",
        "client": "Split Studio",
        "kind": "Game",
        "image": "original_wizavior",
        "banner": "original_wizavior",
        "back_url": "/split-originals",
        "back_label": "Split Originals",
        "video": "https://www.youtube.com/embed/iGOUS0az-54",
        "facts": (
            ("Client", "Split Studio"),
            ("Status", "In development"),
            (
                "Services",
                "Direction, Script, Storyboard & Animatic, Voices, "
                "Character Design, Props, Backgrounds, Builds, 2D Animation, "
                "Editing, Composition, Sound FX, Songs, Mix, 3D Animation",
            ),
        ),
        "summary": ("Split original game in development, mixing 2D and 3D animation."),
        "synopsis": (
            "Wizavior is an original game created inside Split. The studio "
            "is developing the world, characters and animation in house, "
            "mixing the 2D pipeline with 3D animation."
        ),
        "cta_label": "Co-produce with us",
    },
    {
        "xml_id": "project_egregora",
        "url": "/originals/egregore",
        "title": "Egregore",
        "client": "Split Studio",
        "kind": "Short film",
        "image": "original_egregora",
        "banner": "original_egregora",
        "back_url": "/split-originals",
        "back_label": "Split Originals",
        "video": "https://player.vimeo.com/video/313229925?h=b1753368c2",
        "facts": (
            ("Client", "Split Studio"),
            ("Format", "Short film"),
            (
                "Services",
                "Direction, Script, Storyboard & Animatic, Voices, "
                "Character Design, Props, Backgrounds, Builds, 2D Animation, "
                "Editing, Composition, Sound FX, Songs, Mix",
            ),
        ),
        "summary": "Original animated short created and produced by Split.",
        "synopsis": (
            "An original animated short created inside Split. The studio "
            "covered the film from direction and script through animation, "
            "sound and mix."
        ),
        "cta_label": "Co-produce with us",
    },
    {
        "xml_id": "project_children_of_the_world",
        "url": "/originals/children-of-the-world",
        "title": "Children of the World",
        "client": "Split Studio",
        "kind": "Series",
        "image": "original_children_of_the_world",
        "banner": "original_children_of_the_world",
        "back_url": "/split-originals",
        "back_label": "Split Originals",
        "layout": "ip",
        "hero_image": "original_children_of_the_world",
        "logo": "children_of_the_world_logo",
        "format": "TV series & Digital Game",
        "genres": "Adventure | Fantasy | Drama",
        "video": "https://player.vimeo.com/video/435369576",
        "extra": (
            "Children of the World is a 2D adventure indie game displayed "
            "in a 3D world, with puzzle, platform, music and minigame "
            "elements.",
            "The game tells a universal and contemporary story, which "
            "could be the story of many children from different "
            "nationalities.",
            "It continues the world of The Boy and the World, the 2016 "
            "Academy Award-nominated animated feature, as a crossmedia "
            "proposal pairing a TV series with a digital game.",
        ),
        "facts": (
            ("Format", "TV series & Digital Game"),
            ("Genres", "Adventure | Fantasy | Drama"),
        ),
        "summary": (
            "Crossmedia original pairing a TV series with a digital game, "
            "continuing the world of The Boy and the World."
        ),
        "synopsis": (
            "Children of the World gives players a poetic art direction "
            "filled with grace and bittersweet optimism, broadening the "
            "narrative of a film that travelled the festival circuit and "
            "reached an Academy Award nomination."
        ),
        "cta_label": "Co-produce with us",
    },
    {
        "xml_id": "project_blue_butterflies",
        "url": "/originals/blue-butterflies",
        "title": "On the Trail of the Blue Butterflies",
        "client": "Split Studio",
        "kind": "Series",
        "image": "original_blue_butterflies",
        "banner": "original_blue_butterflies",
        "back_url": "/split-originals",
        "back_label": "Split Originals",
        "video": "https://player.vimeo.com/video/377842284",
        "facts": (
            ("Client", "Split Studio"),
            (
                "Services",
                "Direction, Script, Storyboard & Animatic, Voices, "
                "Character Design, Props, Backgrounds, Builds, 2D Animation, "
                "Editing, Composition, Sound FX, Songs, Mix",
            ),
        ),
        "summary": (
            "Original series created inside Split, covering the full 2D " "pipeline."
        ),
        "synopsis": (
            "An original series created inside Split. The studio covers the "
            "full 2D pipeline, from direction and script through animation, "
            "sound and mix."
        ),
        "cta_label": "Co-produce with us",
    },
    {
        "xml_id": "project_howdy_harrdy",
        "url": "/originals/howdy-harrdy",
        "title": "Howdy Harrdy",
        "client": "Nick Jr. US",
        "kind": "Series in development",
        "image": "original_howdy_harrdy",
        "banner": "original_howdy_harrdy",
        "back_url": "/split-originals",
        "back_label": "Split Originals",
        "video": "https://player.vimeo.com/video/118581932",
        "facts": (
            ("Client", "Nick Jr. US"),
            ("Release year", "2015"),
            ("Created by", "Henrique Lira"),
        ),
        "extra": (
            "Howdy Harrdy is a preschool cartoon created by Henrique Lira "
            "and produced by Split Studio in partnership with Animact! for "
            "Nick Jr. US through the Nickelodeon Animated Shorts Program.",
        ),
        "summary": (
            "Preschool cartoon created by Henrique Lira for Nick Jr. US "
            "through the Nickelodeon Animated Shorts Program."
        ),
        "synopsis": (
            "A preschool short produced with Animact! for Nickelodeon's "
            "Animated Shorts Program. Henrique Lira created the series and "
            "Split produced it for Nick Jr. US."
        ),
        "cta_label": "Co-produce with us",
    },
    {
        "xml_id": "project_miss_and_grubs",
        "url": "/originals/miss-and-grubs",
        "title": "Miss & Grubs",
        "client": "Split Studio",
        "kind": "Series in development",
        "image": "original_miss_and_grubs",
        "banner": "original_miss_and_grubs",
        "back_url": "/split-originals",
        "back_label": "Split Originals",
        "video": "https://player.vimeo.com/video/120198390",
        "facts": (
            ("Format", "Animated short"),
            ("Release year", "2015"),
            ("Created by", "Camila Kamimura and Victor Canela"),
        ),
        "extra": (
            "Once upon a time, in a Dark Forest where no ray of light or "
            "love could get in, a perfect and tiny rodent lives alone in a "
            "perfect egg house, where everything works and fits perfectly. "
            "One day her power goes out, and Miss has to face the wild "
            "dangers of the darkness to find what she is looking for.",
        ),
        "summary": (
            "Animated short created by Camila Kamimura and Victor Canela "
            "and produced by Split with support from the São Paulo "
            "government."
        ),
        "synopsis": (
            "An animated short originally created by Camila Kamimura and "
            "Victor Canela and produced by Split with the support of the "
            "São Paulo government Culture Secretary through the Programa de "
            "Ação Cultural in 2013."
        ),
        "cta_label": "Co-produce with us",
    },
    {
        "xml_id": "project_to_reach_the_moon",
        "url": "/originals/to-reach-the-moon",
        "title": "To Reach the Moon",
        "client": "Split Studio",
        "kind": "Short film",
        "image": "original_to_reach_the_moon",
        "banner": "original_to_reach_the_moon",
        "back_url": "/split-originals",
        "back_label": "Split Originals",
        "video": "https://player.vimeo.com/video/7721831?h=63cd34166f",
        "facts": (
            ("Client", "Split Studio"),
            ("Format", "Short film"),
            (
                "Services",
                "Direction, Script, Storyboard & Animatic, Voices, "
                "Character Design, Props, Backgrounds, Builds, 2D Animation, "
                "Editing, Composition, Songs, Mix",
            ),
        ),
        "summary": "Original animated short created and produced by Split.",
        "synopsis": (
            "An original animated short created inside Split. The studio "
            "covered the film from direction and script through animation "
            "and mix."
        ),
        "cta_label": "Co-produce with us",
    },
)
PROJECTS = PROJECTS + NEW_PROJECTS

CARD_LINKS = {
    "work_rick_and_morty": "/work/rick-and-morty",
    "work_hello_kitty_supercute": "/work/hello-kitty-supercute",
    "work_tito_and_the_birds": "/work/tito-and-the-birds",
    "work_my_life_is_worth_living": "/work/my-life-is-worth-living",
    "work_monica_and_friends": "/work/monica-and-friends",
    "work_fit_ufc": "/work/fit-ufc-true-myth",
    "work_are_you_okay": "/work/are-you-okay",
    "work_is_anybody_out_there": "/work/is-anybody-out-there",
    "work_bit_wars": "/work/bit-wars",
    "work_mr_men_little_miss": "/work/mr-men-little-miss",
    "work_bubu_and_the_little_owls": "/work/bubu-and-the-little-owls",
    "work_the_boy_and_the_world": "/work/the-boy-and-the-world",
    "original_weeboom": "/originals/weeboom",
    "original_whats_up_bud": "/originals/whats-up-bud",
    "original_charcoal_swordsman": "/originals/the-charcoal-swordsman",
    "original_sun_boy": "/originals/sun-boy-and-friends",
    "original_que_corpo_e_esse": "/originals/que-corpo-e-esse",
    "original_wizavior": "/originals/wizavior",
    "original_egregora": "/originals/egregore",
    "original_children_of_the_world": "/originals/children-of-the-world",
    "original_blue_butterflies": "/originals/blue-butterflies",
    "original_howdy_harrdy": "/originals/howdy-harrdy",
    "original_miss_and_grubs": "/originals/miss-and-grubs",
    "original_to_reach_the_moon": "/originals/to-reach-the-moon",
}

# Captions that drifted from the official credits.
CARD_CAPTIONS = {
    "work_bubu_and_the_little_owls": "Up Content · Preschool series",
    "work_the_boy_and_the_world": "Paper Films · Feature film",
    "work_bit_wars": "NuBoom · Promo",
    "work_mr_men_little_miss": "Sanrio Brazil · Promo",
}

CARD_LINKS.update({card["image"]: card["url"] for card in WORK_CARDS})
WORK_CATEGORIES = {card["image"]: card["category"] for card in WORK_CARDS}

VIEW_TEMPLATE = """    <record id="{xml_id}" model="ir.ui.view">
        <field name="name">Split Studio - {title}</field>
        <field name="key">split_website.{xml_id}</field>
        <field name="type">qweb</field>
        <field name="website_id" ref="website.default_website" />
        <field name="active" eval="True" />
        <field name="arch" type="xml">
            <t name="{title}" t-name="split_website.{xml_id}">
                <t t-call="website.layout">
                    <div id="wrap">
                        <div
                            id="oe_structure_split_website_{xml_id}"
                            class="oe_structure"
                        >
                            <section
                                class="s_cover parallax s_parallax_is_fixed split-hero o_cc o_cc5"
                                data-vcss="001"
                                data-snippet="s_cover"
                                data-name="Cover"
                                data-scroll-background-ratio="1"
                            >
                                <span
                                    class="s_parallax_bg oe_img_bg o_bg_img_center"
                                    style="background-image: url('/web/image/split_website.{banner}');"
                                />
                                <div class="o_we_bg_filter bg-black-50" />
                                <div class="container">
                                    <div class="row">
                                        <div class="col-lg-8">
                                            <p class="mb-2">
                                                <a href="{back_url}">{back_label}</a>
                                            </p>
                                            <h1 class="display-2-fs">{title}</h1>
                                            <p class="lead mb-0">{client} · {kind}</p>
                                        </div>
                                    </div>
                                </div>
                            </section>
{video}                            <section
                                class="s_text_block pt64 pb32 o_cc o_cc5"
                                data-snippet="s_text_block"
                                data-name="Credits"
                            >
                                <div class="container">
                                    <div class="row split-project-facts">
{facts}
                                    </div>
                                </div>
                            </section>
                            <section
                                class="s_text_block pt16 pb64 o_cc o_cc5"
                                data-snippet="s_text_block"
                                data-name="Project"
                            >
                                <div class="container">
                                    <div class="row align-items-center">
                                        <div class="col-lg-7">
                                            <img
                                                src="/web/image/split_website.{image}"
                                                class="img img-fluid w-100"
                                                style="aspect-ratio: 16 / 9; object-fit: cover;"
                                                alt="{title}"
                                            />
                                        </div>
                                        <div class="col-lg-5 mt-4 mt-lg-0">
                                            <p class="lead">{synopsis}</p>
{extra}                                            <p>
                                                <a
                                                    href="{cta_href}"
                                                    class="btn btn-primary"
                                                >{cta_label}</a>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </section>
                        </div>
                    </div>
                </t>
            </t>
        </field>
    </record>
"""

VIDEO_SECTION = """                            <section
                                class="s_embed_code pt64 pb0 o_cc o_cc5"
                                data-snippet="s_embed_code"
                                data-name="Video"
                            >
                                <div class="container">
                                    <div class="row justify-content-center">
                                        <div class="{column}">
                                            <div
                                                class="s_embed_code_embedded ratio ratio-{ratio}"
                                            >
                                                <iframe
                                                    src="{video}"
                                                    title="{title}"
                                                    frameborder="0"
                                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                                    allowfullscreen="allowfullscreen"
                                                    loading="lazy"
                                                />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </section>
"""

PAGE_RECORD = """    <record id="page_{xml_id}" model="website.page">
        <field name="view_id" ref="{xml_id}" />
        <field name="url">{url}</field>
        <field name="website_id" ref="website.default_website" />
        <field name="is_published" eval="True" />
        <field name="header_overlay" eval="True" />
        <field name="track" eval="True" />
        <field name="website_meta_description">{summary}</field>
    </record>
"""


def _paragraphs_xml(paragraphs):
    return "".join(
        f"""                                            <p>{escape(paragraph)}</p>
"""
        for paragraph in paragraphs
    )


def _facts_xml(facts):
    chunks = []
    for label, value in facts:
        width = "col-lg-8" if label == "Services" else "col-lg-4 col-md-6"
        chunks.append(
            f"""                                        <div class="{width} pt8 pb16">
                                            <p class="o_small text-uppercase mb-1">{escape(label)}</p>
                                            <p class="mb-0">{escape(value)}</p>
                                        </div>"""
        )
    return "\n".join(chunks)


def _video_xml(project):
    video = project.get("video")
    if not video:
        return ""
    ratio = project.get("video_ratio", "16x9")
    return VIDEO_SECTION.format(
        video=escape(video),
        title=escape(project["title"]),
        ratio=ratio,
        column="col-12" if ratio == "16x9" else "col-lg-7",
    )


def _service_view(project):
    values = {
        "xml_id": project["xml_id"],
        "title": escape(project["title"]),
        "banner": project["banner"],
        "image": project["image"],
        "back_url": escape(project["back_url"]),
        "back_label": escape(project["back_label"]),
        "client": escape(project["client"]),
        "kind": escape(project["kind"]),
        "synopsis": escape(project["synopsis"]),
        "cta_label": escape(project.get("cta_label", "Start a project")),
        "cta_href": escape(project.get("cta_href", "/contactus")),
        "facts": _facts_xml(project["facts"]),
        "video": _video_xml(project),
        "extra": _paragraphs_xml(project.get("extra", ())),
    }
    return VIEW_TEMPLATE.format(**values)


def _ip_hero_xml(project):
    if project.get("hero_video"):
        media = f"""                                <video
                                    class="split-ip-hero-video"
                                    src="{escape(project["hero_video"])}"
                                    autoplay="autoplay"
                                    muted="muted"
                                    loop="loop"
                                    playsinline="playsinline"
                                    preload="metadata"
                                />"""
    else:
        media = f"""                                <img
                                    class="split-ip-hero-video"
                                    src="/web/image/split_website.{project["hero_image"]}"
                                    alt=""
                                />"""
    mark = ""
    if project.get("logo"):
        mark = f"""
                                <div class="split-ip-hero-mark">
                                    <img
                                        src="/web/image/split_website.{project["logo"]}"
                                        class="img img-fluid"
                                        alt="{escape(project["title"])}"
                                    />
                                </div>"""
    return f"""                            <section
                                class="split-ip-hero"
                                data-name="Cover"
                            >
{media}{mark}
                            </section>
"""


def _ip_about_xml(project):
    seal = ""
    if project.get("seal"):
        seal = f"""                                        <div class="col-lg-2 col-md-3 text-center pb32">
                                            <img
                                                src="/web/image/split_website.{project["seal"]}"
                                                class="img img-fluid split-ip-seal"
                                                alt=""
                                            />
                                        </div>
"""
    title_width = "col-lg-10" if project.get("seal") else "col-12"
    highlights = ""
    if project.get("highlights"):
        items = "\n".join(
            f"                                                <li>{escape(item)}</li>"
            for item in project["highlights"]
        )
        highlights = f"""                                        <div class="col-lg-5">
                                            <ul class="mb-4">
{items}
                                            </ul>
                                        </div>
"""
    copy_width = "col-lg-7" if project.get("highlights") else "col-lg-10"
    extra = "".join(
        f"""                                            <p>{escape(paragraph)}</p>
"""
        for paragraph in project.get("extra", ())
    )
    tagline = ""
    if project.get("tagline"):
        tagline = f"""                                            <p class="h3-fs mb-3">{escape(project["tagline"])}</p>
"""
    return f"""                            <section
                                class="s_text_block pt64 pb64 o_cc o_cc5"
                                data-snippet="s_text_block"
                                data-name="About"
                            >
                                <div class="container">
                                    <div class="row align-items-start">
{seal}                                        <div class="{title_width}">
                                            <p class="mb-2">
                                                <a href="/split-originals">Split Originals</a>
                                            </p>
                                            <h1 class="display-2-fs mb-3">{escape(project["title"])}</h1>
                                            <p class="h3-fs mb-2">{escape(project["format"])}</p>
                                            <p class="h3-fs mb-4">{escape(project["genres"])}</p>
                                        </div>
                                    </div>
                                    <div class="row">
{highlights}                                        <div class="{copy_width}">
{tagline}                                            <p class="lead">{escape(project["synopsis"])}</p>
{extra}                                        </div>
                                    </div>
                                </div>
                            </section>
"""


def _ip_characters_xml(project):
    characters = project.get("characters")
    if not characters:
        return ""
    cards = []
    width = "col-lg-6" if len(characters) == 2 else "col-lg-4"
    for character in characters:
        role = ""
        if character.get("role"):
            role = f"""                                            <p class="text-uppercase o_small mb-2">{escape(character["role"])}</p>
"""
        cards.append(
            f"""                                        <div class="{width} pt16 pb32 split-character">
                                            <img
                                                src="/web/image/split_website.{character["image"]}"
                                                class="img img-fluid w-100 mb-3"
                                                alt="{escape(character["name"])}"
                                            />
                                            <h3>{escape(character["name"])}</h3>
{role}                                            <p>{escape(character["bio"])}</p>
                                        </div>"""
        )
    body = "\n".join(cards)
    return f"""                            <section
                                class="s_text_block pt64 pb64 o_cc o_cc5"
                                data-snippet="s_text_block"
                                data-name="Characters"
                            >
                                <div class="container">
                                    <h2 class="text-center mb-5">Characters</h2>
                                    <div class="row">
{body}
                                    </div>
                                </div>
                            </section>
"""


def _ip_gallery_xml(project):
    gallery = project.get("gallery")
    if not gallery:
        return ""
    tiles = []
    for index, xml_id in enumerate(gallery):
        width = "col-12" if index == 0 else "col-lg-4"
        tiles.append(
            f"""                                        <div class="{width}">
                                            <img
                                                class="img img-fluid d-block w-100"
                                                src="/web/image/split_website.{xml_id}"
                                                data-index="{index}"
                                                data-name="Image"
                                                alt="{escape(project["title"])} still"
                                            />
                                        </div>"""
        )
    body = "\n".join(tiles)
    return f"""                            <section
                                class="s_image_gallery o_spc-none o_grid pt0 pb0 o_cc o_cc5 split-gallery"
                                data-snippet="s_images_wall"
                                data-name="Gallery"
                                data-vcss="002"
                                data-columns="3"
                            >
                                <div class="container-fluid px-0">
                                    <div class="row s_nb_column_fixed g-0">
{body}
                                    </div>
                                </div>
                            </section>
"""


def _ip_cta_xml(project):
    return f"""                            <section
                                class="s_text_block pt64 pb64 o_cc o_cc5"
                                data-snippet="s_text_block"
                                data-name="Call to action"
                            >
                                <div class="container text-center">
                                    <a
                                        href="/contactus"
                                        class="btn btn-primary"
                                    >{escape(project.get("cta_label", "Co-produce with us"))}</a>
                                </div>
                            </section>
"""


def _ip_view(project):
    """Data-driven IP bible: hero, credits, teaser, characters, gallery."""
    return f"""    <record id="{project["xml_id"]}" model="ir.ui.view">
        <field name="name">Split Studio - {escape(project["title"])}</field>
        <field name="key">split_website.{project["xml_id"]}</field>
        <field name="type">qweb</field>
        <field name="website_id" ref="website.default_website" />
        <field name="active" eval="True" />
        <field name="arch" type="xml">
            <t name="{escape(project["title"])}" t-name="split_website.{project["xml_id"]}">
                <t t-call="website.layout">
                    <div id="wrap">
                        <div
                            id="oe_structure_split_website_{project["xml_id"]}"
                            class="oe_structure"
                        >
{_ip_hero_xml(project)}{_ip_about_xml(project)}{_video_xml(project)}{_ip_characters_xml(project)}{_ip_gallery_xml(project)}{_ip_cta_xml(project)}                        </div>
                    </div>
                </t>
            </t>
        </field>
    </record>
"""


def _weeboom_view(project):
    """WeeBoom is an original IP bible, not a service credit sheet."""
    return f"""    <record id="{project["xml_id"]}" model="ir.ui.view">
        <field name="name">Split Studio - {escape(project["title"])}</field>
        <field name="key">split_website.{project["xml_id"]}</field>
        <field name="type">qweb</field>
        <field name="website_id" ref="website.default_website" />
        <field name="active" eval="True" />
        <field name="arch" type="xml">
            <t name="{escape(project["title"])}" t-name="split_website.{project["xml_id"]}">
                <t t-call="website.layout">
                    <div id="wrap">
                        <div
                            id="oe_structure_split_website_{project["xml_id"]}"
                            class="oe_structure"
                        >
                            <section
                                class="split-ip-hero"
                                data-name="Cover"
                            >
                                <video
                                    class="split-ip-hero-video"
                                    src="/split_website/static/src/video/weeboom_hero.mp4"
                                    autoplay="autoplay"
                                    muted="muted"
                                    loop="loop"
                                    playsinline="playsinline"
                                    preload="metadata"
                                />
                                <div class="split-ip-hero-mark">
                                    <img
                                        src="/web/image/split_website.weeboom_logo"
                                        class="img img-fluid"
                                        alt="WeeBoom"
                                    />
                                </div>
                            </section>
                            <section
                                class="s_text_block pt64 pb64 o_cc o_cc5"
                                data-snippet="s_text_block"
                                data-name="About"
                            >
                                <div class="container">
                                    <div class="row align-items-start">
                                        <div class="col-lg-2 col-md-3 text-center pb32">
                                            <img
                                                src="/web/image/split_website.weeboom_seal"
                                                class="img img-fluid split-ip-seal"
                                                alt=""
                                            />
                                        </div>
                                        <div class="col-lg-10">
                                            <p class="mb-2">
                                                <a href="/split-originals">Split Originals</a>
                                            </p>
                                            <h1 class="display-2-fs mb-3">WeeBoom</h1>
                                            <p class="h3-fs mb-2">26 x 7′ | 4 to 7 years old</p>
                                            <p class="h3-fs mb-4">Comedy | Adventure | Travel</p>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-lg-5">
                                            <ul class="mb-4">
                                                <li>Season 1 available in Portuguese and Spanish, in multiple territories. Sample English episodes available.</li>
                                            </ul>
                                        </div>
                                        <div class="col-lg-7">
                                            <p class="lead">{escape(project["synopsis"])}</p>
                                            <p>Wee and Boom are two friends who travel the world to capture some fun and magical creatures, the Boomies.</p>
                                        </div>
                                    </div>
                                </div>
                            </section>
                            <section
                                class="s_text_block pt64 pb64 o_cc o_cc5"
                                data-snippet="s_text_block"
                                data-name="Characters"
                            >
                                <div class="container">
                                    <h2 class="text-center mb-5">Characters</h2>
                                    <div class="row">
                                        <div class="col-lg-4 pt16 pb32 split-character">
                                            <img
                                                src="/web/image/split_website.weeboom_character_wee"
                                                class="img img-fluid w-100 mb-3"
                                                alt="Wee"
                                            />
                                            <h3>Wee</h3>
                                            <p class="text-uppercase o_small mb-2">The Adventure</p>
                                            <p>Wee lives for adventures. In one of them, she accidentally woke Boom from centuries of slumber. By doing so, she also accidentally brought the Boomies into the world. Now they are lost and out there. Wee is a caring, athletic and competitive friend, and capturing Boomies has become her mission.</p>
                                        </div>
                                        <div class="col-lg-4 pt16 pb32 split-character">
                                            <img
                                                src="/web/image/split_website.weeboom_character_boom"
                                                class="img img-fluid w-100 mb-3"
                                                alt="Boom"
                                            />
                                            <h3>Boom</h3>
                                            <p class="text-uppercase o_small mb-2">The Mythological Giant</p>
                                            <p>Boom is silly, sweet and is also the guardian of all the sounds in the universe. Inside his body one will find a library of sounds, managed by the Boomies. Boom is always looking for fun, and despite his naivety and lack of attention, he is Wee's best friend and greatest ally.</p>
                                        </div>
                                        <div class="col-lg-4 pt16 pb32 split-character">
                                            <img
                                                src="/web/image/split_website.weeboom_character_boomies"
                                                class="img img-fluid w-100 mb-3"
                                                alt="Boomies"
                                            />
                                            <h3>Boomies</h3>
                                            <p class="text-uppercase o_small mb-2">Run Away from Them!</p>
                                            <p>Boomies are cute yellow creatures that live inside Boom, where they take care of all the sounds of the universe. They are now lost to the world and go crazy listening to music. When that happens, they use their magical powers to set wherever they are on chaos. Watch out!</p>
                                        </div>
                                    </div>
                                </div>
                            </section>
                            <section
                                class="s_image_gallery o_spc-none o_grid pt0 pb0 o_cc o_cc5 split-gallery"
                                data-snippet="s_images_wall"
                                data-name="Gallery"
                                data-vcss="002"
                                data-columns="3"
                            >
                                <div class="container-fluid px-0">
                                    <div class="row s_nb_column_fixed g-0">
                                        <div class="col-12">
                                            <img
                                                class="img img-fluid d-block w-100"
                                                src="/web/image/split_website.weeboom_still_01"
                                                data-index="0"
                                                data-name="Image"
                                                alt="WeeBoom still"
                                            />
                                        </div>
                                        <div class="col-lg-4">
                                            <img
                                                class="img img-fluid d-block w-100"
                                                src="/web/image/split_website.weeboom_still_02"
                                                data-index="1"
                                                data-name="Image"
                                                alt="WeeBoom still"
                                            />
                                        </div>
                                        <div class="col-lg-4">
                                            <img
                                                class="img img-fluid d-block w-100"
                                                src="/web/image/split_website.weeboom_still_03"
                                                data-index="2"
                                                data-name="Image"
                                                alt="WeeBoom still"
                                            />
                                        </div>
                                        <div class="col-lg-4">
                                            <img
                                                class="img img-fluid d-block w-100"
                                                src="/web/image/split_website.weeboom_still_04"
                                                data-index="3"
                                                data-name="Image"
                                                alt="WeeBoom still"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </section>
                            <section
                                class="s_text_block pt64 pb64 o_cc o_cc5"
                                data-snippet="s_text_block"
                                data-name="Episodes"
                            >
                                <div class="container">
                                    <h2 class="text-center mb-5">Check out some episode synopses</h2>
                                    <div class="row">
                                        <div class="col-lg-6 pt16 pb32 split-episode">
                                            <img
                                                src="/web/image/split_website.weeboom_episode_01"
                                                class="img img-fluid w-100 mb-3"
                                                alt="Episode 01"
                                            />
                                            <h3>Ep 01 – Mamma Mia!</h3>
                                            <p class="text-uppercase o_small mb-2">Palermo, Italy</p>
                                            <p>Hmmm, I'm so hungry! Wee and Boom look for a Boomie in the city of Palermo, Italy, famous for its tarantella and pasta. A very hungry Wee and Boom stumble upon a restaurant whose boss seems to be crazy, turning the place and customers upside down. That smells like Boomie!</p>
                                        </div>
                                        <div class="col-lg-6 pt16 pb32 split-episode">
                                            <img
                                                src="/web/image/split_website.weeboom_episode_02"
                                                class="img img-fluid w-100 mb-3"
                                                alt="Episode 02"
                                            />
                                            <h3>Ep 02 – Ah, I'amour…</h3>
                                            <p class="text-uppercase o_small mb-2">Paris, France</p>
                                            <p>Ah, Paris, the city of love! Wee and Boom are looking for a Boomie in this très magnifique city, whose inhabitants seem to be more in love than usual. The contagious love will even hit Wee, who gets extremely in love with Boom. Now Boom will have to find a way to capture the Boomie so that Wee and the city return to normal.</p>
                                        </div>
                                    </div>
                                    <p class="text-center pt16 mb-0">
                                        <a
                                            href="/contactus"
                                            class="btn btn-primary"
                                        >Co-produce with us</a>
                                    </p>
                                </div>
                            </section>
                        </div>
                    </div>
                </t>
            </t>
        </field>
    </record>
"""


def _project_view(project):
    if project.get("layout") == "weeboom":
        return _weeboom_view(project)
    if project.get("layout") == "ip":
        return _ip_view(project)
    return _service_view(project)


def _work_card_xml(card):
    title = escape(card["title"])
    return f"""                                        <div
                                            class="col-lg-4 col-md-6 pt16 pb16 split-work-item"
                                            data-category="{escape(card["category"])}"
                                        >
                                            <a
                                                href="{escape(card["url"])}"
                                                class="text-reset split-project-card"
                                            >
                                                <figure class="mb-0">
                                                    <img
                                                        src="/web/image/split_website.{card["image"]}"
                                                        class="img img-fluid w-100"
                                                        style="aspect-ratio: 16 / 9; object-fit: cover;"
                                                        alt="{title}"
                                                        loading="lazy"
                                                    />
                                                    <figcaption class="pt-2">
                                                        <h4 class="mb-0">{title}</h4>
                                                        <p
                                                            class="o_small mb-0"
                                                        >{escape(card["caption"])}</p>
                                                    </figcaption>
                                                </figure>
                                            </a>
                                        </div>
"""


def _work_filter_xml():
    chunks = []
    for key, label in FILTERS:
        checked = ' checked="checked"' if key == "all" else ""
        chunks.append(
            f"""                                    <input
                                        type="radio"
                                        name="split_work_cat"
                                        id="split_work_{key}"{checked}
                                    />
                                    <label for="split_work_{key}">{escape(label)}</label>
"""
        )
    return "".join(chunks)


def write_our_work_grid():
    """Replace the productions section with the official catalog."""
    path = DATA_DIR / "website_view_our_work.xml"
    text = path.read_text(encoding="utf-8")
    start = text.find(
        '<section\n                                class="s_text_block pt64 pb64'
    )
    end = text.rfind("                            </section>")
    if start < 0 or end < 0:
        raise SystemExit("could not find the Our Work productions section")
    end += len("                            </section>")
    cards = "".join(_work_card_xml(card) for card in WORK_CARDS)
    replacement = f"""                            <section
                                class="s_text_block pt64 pb64 o_cc o_cc5"
                                data-snippet="s_text_block"
                                data-name="Client productions"
                            >
                                <div class="container split-work-filter">
                                    <div class="row">
                                        <div
                                            class="col-lg-12 pb16 d-flex flex-wrap align-items-baseline justify-content-between"
                                        >
                                            <div>
                                                <h2 class="mb-0">Client productions</h2>
                                                <p
                                                    class="lead mb-0"
                                                >Series, films, promos and branded content.</p>
                                            </div>
                                            <p class="mb-0">
                                                <a href="/contactus">Start a project <i
                                                    class="fa fa-long-arrow-right ms-2"
                                                /></a>
                                            </p>
                                        </div>
                                    </div>
{_work_filter_xml()}                                    <div class="row">
{cards}                                    </div>
                                </div>
                            </section>"""
    path.write_text(text[:start] + replacement + text[end:], encoding="utf-8")
    print(f"wrote {len(WORK_CARDS)} work cards in {path.name}")


def write_project_views():
    chunks = [
        '<?xml version="1.0" encoding="utf-8" ?>\n',
        "<odoo>\n",
    ]
    for project in PROJECTS:
        chunks.append(_project_view(project))
    chunks.append("</odoo>\n")
    target = DATA_DIR / "website_view_projects.xml"
    target.write_text("".join(chunks), encoding="utf-8")
    print(f"wrote {target.name} ({len(PROJECTS)} pages)")


def append_project_pages():
    target = DATA_DIR / "website_page.xml"
    text = target.read_text(encoding="utf-8")
    if "page_project_rick_and_morty" in text:
        text = text.split('    <record id="page_project_')[0].rstrip() + "\n</odoo>\n"
    if '<field name="header_overlay"' not in text:
        text = text.replace(
            '<field name="is_published" eval="True" />',
            '<field name="is_published" eval="True" />\n'
            '        <field name="header_overlay" eval="True" />',
        )
    pages = "".join(PAGE_RECORD.format(**project) for project in PROJECTS)
    if not text.endswith("</odoo>\n"):
        raise SystemExit("unexpected website_page.xml footer")
    text = text[: -len("</odoo>\n")] + pages + "</odoo>\n"
    target.write_text(text, encoding="utf-8")
    print(f"updated {target.name}")


def wrap_cards(path):
    text = path.read_text(encoding="utf-8")
    for xml_id, url in CARD_LINKS.items():
        needle = f'src="/web/image/split_website.{xml_id}"'
        if needle not in text:
            continue
        # Wrap each unwrapped figure that uses this image.
        start = 0
        while True:
            idx = text.find(needle, start)
            if idx < 0:
                break
            fig = text.rfind("<figure", 0, idx)
            fig_end = text.find("</figure>", idx)
            if fig < 0 or fig_end < 0:
                break
            fig_end += len("</figure>")
            block = text[fig:fig_end]
            # The anchor, when present, sits between the column div and the
            # figure. Anything wider matches the previous card once prettier
            # has reflowed the attributes onto their own lines.
            col = max(text.rfind("<div", 0, fig), 0)
            if "split-project-card" in text[col:fig]:
                start = fig_end
                continue
            indent = " " * (fig - text.rfind("\n", 0, fig) - 1)
            inner = block.replace("\n", f"\n{' ' * 4}")
            wrapped = (
                f"<a\n"
                f'{indent}    href="{url}"\n'
                f'{indent}    class="text-reset split-project-card"\n'
                f"{indent}>\n"
                f"{indent}    {inner}\n"
                f"{indent}</a>"
            )
            text = text[:fig] + wrapped + text[fig_end:]
            start = fig + len(wrapped)
    path.write_text(text, encoding="utf-8")
    print(f"wrapped cards in {path.name}")


def fix_captions(path):
    text = path.read_text(encoding="utf-8")
    for xml_id, caption in CARD_CAPTIONS.items():
        idx = text.find(f'src="/web/image/split_website.{xml_id}"')
        if idx < 0:
            continue
        end = text.find("</figcaption>", idx)
        block = text[idx:end]
        old = re.search(
            r'<p\s+class="o_small mb-0"\s*>([^<]+)</p>', block
        ) or re.search(r'<p\n\s+class="o_small mb-0"\n\s+>([^<]+)</p>', block)
        if not old or old.group(1) == caption:
            continue
        start = idx + old.start(1)
        text = text[:start] + caption + text[idx + old.end(1) :]
    path.write_text(text, encoding="utf-8")
    print(f"fixed captions in {path.name}")


def add_work_filter():
    path = DATA_DIR / "website_view_our_work.xml"
    text = path.read_text(encoding="utf-8")
    for xml_id, category in WORK_CATEGORIES.items():
        old = (
            f'<div class="col-lg-4 col-md-6 pt16 pb16">\n'
            f'                                            <figure class="mb-0">\n'
            f"                                                <img\n"
            f'                                                    src="/web/image/split_website.{xml_id}"'
        )
        new = (
            f'<div class="col-lg-4 col-md-6 pt16 pb16 split-work-item" '
            f'data-category="{category}">\n'
            f'                                            <figure class="mb-0">\n'
            f"                                                <img\n"
            f'                                                    src="/web/image/split_website.{xml_id}"'
        )
        if f'data-category="{category}"' in text and xml_id in text:
            continue
        if old in text:
            text = text.replace(old, new, 1)
            continue
        # Generic: add class on the column that contains this image.
        marker = f'src="/web/image/split_website.{xml_id}"'
        idx = text.find(marker)
        if idx < 0:
            continue
        col = text.rfind('<div class="col-lg-4 col-md-6 pt16 pb16"', 0, idx)
        if col < 0:
            continue
        text = (
            text[:col] + f'<div class="col-lg-4 col-md-6 pt16 pb16 split-work-item" '
            f'data-category="{category}"'
            + text[col + len('<div class="col-lg-4 col-md-6 pt16 pb16"') :]
        )
    if 'class="row split-work-filter"' not in text:
        # The productions grid is the only row that already has project columns.
        text = text.replace(
            '<div class="row">\n'
            "                                    <div\n"
            '                                        class="col-lg-12 pb16 d-flex flex-wrap'
            ' align-items-baseline justify-content-between"',
            '<div class="row split-work-filter">\n'
            "                                    <div\n"
            '                                        class="col-lg-12 pb16 d-flex flex-wrap'
            ' align-items-baseline justify-content-between"',
            1,
        )
    filter_bar = """                                            <div class="col-12 pt8 pb8">
                                                <input
                                                    type="radio"
                                                    name="split_work_cat"
                                                    id="split_work_all"
                                                    checked="checked"
                                                />
                                                <label for="split_work_all">All</label>
                                                <input
                                                    type="radio"
                                                    name="split_work_cat"
                                                    id="split_work_shows"
                                                />
                                                <label for="split_work_shows">Shows</label>
                                                <input
                                                    type="radio"
                                                    name="split_work_cat"
                                                    id="split_work_features"
                                                />
                                                <label
                                                    for="split_work_features"
                                                >Feature films</label>
                                                <input
                                                    type="radio"
                                                    name="split_work_cat"
                                                    id="split_work_branded"
                                                />
                                                <label
                                                    for="split_work_branded"
                                                >Ads and branded</label>
                                                <input
                                                    type="radio"
                                                    name="split_work_cat"
                                                    id="split_work_promos"
                                                />
                                                <label
                                                    for="split_work_promos"
                                                >Pilots and promos</label>
                                            </div>
"""
    if 'id="split_work_all"' not in text:
        row = text.find('<div class="row">')
        # The productions section row is the second row in the file.
        row = text.find('<div class="row">', row + 1) if row >= 0 else -1
        # Safer: insert before the first split-work-item / first project column.
        insert_at = text.find('<div class="col-lg-4 col-md-6 pt16 pb16')
        if insert_at < 0:
            raise SystemExit("could not find work grid")
        text = text[:insert_at] + filter_bar + text[insert_at:]
        # The filter radios must be siblings of the row. Close the header
        # flex row first: move the filter to wrap the grid instead.
    path.write_text(text, encoding="utf-8")
    print(f"categorised {path.name}")


def link_carousel():
    path = DATA_DIR / "website_view_home.xml"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        'href="/split-originals"\n                                                                class="btn btn-primary"',
        'href="/originals/among-the-stars"\n                                                                class="btn btn-primary"',
        1,
    )
    replacements = (
        (
            "banner_rick_and_morty",
            "Animated episodes produced for the fifth season.",
            "/work/rick-and-morty",
        ),
        (
            "banner_hello_kitty",
            "New episodes on YouTube every Wednesday.",
            "/work/hello-kitty-supercute",
        ),
        (
            "banner_monica_and_friends",
            "The most watched Brazilian show on Cartoon Network.",
            "/work/monica-and-friends",
        ),
    )
    for banner, lead, url in replacements:
        lead_xml = f">{lead}</p>"
        idx = text.find(banner)
        if idx < 0:
            continue
        lead_idx = text.find(lead_xml, idx)
        if lead_idx < 0 or f'href="{url}"' in text[idx : lead_idx + 200]:
            continue
        insert = (
            f">{lead}</p>\n"
            f"                                                        <p>\n"
            f"                                                            <a\n"
            f'                                                                href="{url}"\n'
            f'                                                                class="btn btn-primary"\n'
            f"                                                            >Discover the project</a>\n"
            f"                                                        </p>"
        )
        text = text[:lead_idx] + insert + text[lead_idx + len(lead_xml) :]
    path.write_text(text, encoding="utf-8")
    print(f"linked carousel in {path.name}")


def complete_work_catalog():
    """Rebuild project sheets and the Our Work grid. Do not run add_work_filter()."""
    write_our_work_grid()
    write_project_views()
    append_project_pages()


def main():
    write_project_views()
    append_project_pages()
    wrap_cards(DATA_DIR / "website_view_home.xml")
    wrap_cards(DATA_DIR / "website_view_our_work.xml")
    wrap_cards(DATA_DIR / "website_view_originals.xml")
    fix_captions(DATA_DIR / "website_view_our_work.xml")
    fix_captions(DATA_DIR / "website_view_home.xml")
    add_work_filter()
    link_carousel()


if __name__ == "__main__":
    main()
