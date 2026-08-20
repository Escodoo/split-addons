# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Official Our Work catalog: cards, new project sheets and pt_BR titles."""

# Filter order matches https://splitstudio.tv/en/trabalhos/
FILTERS = (
    ("all", "All"),
    ("music", "Music videos"),
    ("branded", "Ads and branded"),
    ("shorts", "Short films"),
    ("games", "Games"),
    ("features", "Feature films"),
    ("promos", "Pilots and promos"),
    ("shows", "Shows"),
)


def _sheet(
    xml_id,
    url,
    title,
    client,
    kind,
    image,
    video,
    services,
    summary,
    synopsis,
    extra_facts=(),
):
    facts = [("Client", client)]
    facts.extend(extra_facts)
    facts.append(("Services", services))
    return {
        "xml_id": xml_id,
        "url": url,
        "title": title,
        "client": client,
        "kind": kind,
        "image": image,
        "banner": image,
        "back_url": "/our-work",
        "back_label": "Our Work",
        "video": video,
        "facts": tuple(facts),
        "summary": summary,
        "synopsis": synopsis,
    }


# Listing order matches the official Trabalhos archive.
WORK_CARDS = (
    {
        "image": "work_castanhari_2023",
        "url": "/work/castanhari-2023",
        "title": "Castanhari 2023 Recap",
        "caption": "Canal Nostalgia · Music video",
        "category": "music",
    },
    {
        "image": "work_castanhari_2022",
        "url": "/work/castanhari-2022",
        "title": "Castanhari 2022 Recap",
        "caption": "Canal Nostalgia · Music video",
        "category": "music",
    },
    {
        "image": "work_bit_wars",
        "url": "/work/bit-wars",
        "title": "Bit Wars",
        "caption": "NuBoom · Promo",
        "category": "promos",
    },
    {
        "image": "work_rick_and_morty",
        "url": "/work/rick-and-morty",
        "title": "Rick and Morty",
        "caption": "Adult Swim · Animated episodes",
        "category": "shows",
    },
    {
        "image": "work_my_life_is_worth_living",
        "url": "/work/my-life-is-worth-living",
        "title": "My Life Is Worth Living",
        "caption": "Wonder Media · Animated series",
        "category": "shows",
    },
    {
        "image": "work_monica_and_friends",
        "url": "/work/monica-and-friends",
        "title": "Monica and Friends",
        "caption": "Mauricio de Sousa Produções · TV series",
        "category": "shows",
    },
    {
        "image": "work_hello_kitty_supercute",
        "url": "/work/hello-kitty-supercute",
        "title": "Hello Kitty and Friends Supercute Adventures",
        "caption": "Sanrio · Web series",
        "category": "shows",
    },
    {
        "image": "work_mr_men_little_miss",
        "url": "/work/mr-men-little-miss",
        "title": "Mr Men Little Miss",
        "caption": "Sanrio Brazil · Promo",
        "category": "shows",
    },
    {
        "image": "work_bubu_and_the_little_owls",
        "url": "/work/bubu-and-the-little-owls",
        "title": "Bubu and the Little Owls",
        "caption": "Up Content · Preschool series",
        "category": "shows",
    },
    {
        "image": "original_sun_boy",
        "url": "/originals/sun-boy-and-friends",
        "title": "Sun Boy and Friends",
        "caption": "Split Studio · Music videos",
        "category": "music",
    },
    {
        "image": "work_the_boy_and_the_world",
        "url": "/work/the-boy-and-the-world",
        "title": "The Boy and the World",
        "caption": "Paper Films · Feature film",
        "category": "features",
    },
    {
        "image": "work_is_anybody_out_there",
        "url": "/work/is-anybody-out-there",
        "title": "Is Anybody Out There?",
        "caption": "Wonder Media · Animated series",
        "category": "shorts",
    },
    {
        "image": "original_whats_up_bud",
        "url": "/originals/whats-up-bud",
        "title": "What's Up, Bud?",
        "caption": "Split Studio · Promo",
        "category": "promos",
    },
    {
        "image": "work_tito_and_the_birds",
        "url": "/work/tito-and-the-birds",
        "title": "Tito and the Birds",
        "caption": "Bits Produções · Feature film",
        "category": "features",
    },
    {
        "image": "original_weeboom",
        "url": "/originals/weeboom",
        "title": "WeeBoom",
        "caption": "Split Studio · Comedy series",
        "category": "shows",
    },
    {
        "image": "original_wizavior",
        "url": "/originals/wizavior",
        "title": "Wizavior",
        "caption": "Split Studio · Game",
        "category": "games",
    },
    {
        "image": "work_fit_ufc",
        "url": "/work/fit-ufc-true-myth",
        "title": "Fit UFC | True Myth",
        "caption": "UFC · Branded series",
        "category": "branded",
    },
    {
        "image": "work_heart_of_darkness",
        "url": "/work/heart-of-darkness",
        "title": "Heart of Darkness",
        "caption": "Karmatique · Promo",
        "category": "promos",
    },
    {
        "image": "work_are_you_okay",
        "url": "/work/are-you-okay",
        "title": "Are You Okay?",
        "caption": "Wonder Media · Animated series",
        "category": "shorts",
    },
    {
        "image": "work_dc_fandome",
        "url": "/work/dc-fandome",
        "title": "DC Fandome",
        "caption": "Mauricio de Sousa Produções · Branded content",
        "category": "branded",
    },
    {
        "image": "original_miss_and_grubs",
        "url": "/originals/miss-and-grubs",
        "title": "Miss & Grubs",
        "caption": "Split Studio · Short film",
        "category": "shorts",
    },
    {
        "image": "original_charcoal_swordsman",
        "url": "/originals/the-charcoal-swordsman",
        "title": "The Charcoal Swordsman",
        "caption": "Split Studio · Promo",
        "category": "promos",
    },
    {
        "image": "original_howdy_harrdy",
        "url": "/originals/howdy-harrdy",
        "title": "Howdy Harrdy",
        "caption": "Nick Jr. US · Promo",
        "category": "promos",
    },
    {
        "image": "work_adventures_of_mike",
        "url": "/work/adventures-of-mike",
        "title": "The Adventures of Mike",
        "caption": "FalaíDearo · Animated series",
        "category": "shows",
    },
    {
        "image": "work_hello_kitty_chef_star",
        "url": "/work/hello-kitty-chef-star",
        "title": "Hello Kitty Chef Star",
        "caption": "Sanrio Brazil · Web series",
        "category": "shows",
    },
    {
        "image": "work_hello_kitty_fun",
        "url": "/work/hello-kitty-fun",
        "title": "Hello Kitty Fun",
        "caption": "Sanrio Brazil · Web series",
        "category": "shows",
    },
    {
        "image": "work_radio_bita",
        "url": "/work/radio-bita",
        "title": "Radio Bita",
        "caption": "Mr Plot · Music video",
        "category": "music",
    },
    {
        "image": "original_que_corpo_e_esse",
        "url": "/originals/que-corpo-e-esse",
        "title": "Que Corpo é Esse?",
        "caption": "Canal Futura · Original series",
        "category": "shows",
    },
    {
        "image": "work_league_of_legends",
        "url": "/work/league-of-legends",
        "title": "League of Legends | Project n.5",
        "caption": "Riot Games · Branded content",
        "category": "branded",
    },
    {
        "image": "work_senninha",
        "url": "/work/senninha",
        "title": "Senninha on the Crazy Track",
        "caption": "Instituto Ayrton Senna · Animated series",
        "category": "shows",
    },
    {
        "image": "work_betania_kids",
        "url": "/work/betania-kids",
        "title": "Betania Kids | Monica and Friends",
        "caption": "Mauricio de Sousa Produções · Branded content",
        "category": "branded",
    },
    {
        "image": "work_seara_monica",
        "url": "/work/seara-monica",
        "title": "Seara | Monica and Friends",
        "caption": "Mauricio de Sousa Produções · Branded content",
        "category": "branded",
    },
    {
        "image": "original_blue_butterflies",
        "url": "/originals/blue-butterflies",
        "title": "On the Trail of the Blue Butterflies",
        "caption": "Split Studio · Short film",
        "category": "shorts",
    },
    {
        "image": "work_cool_sneakers",
        "url": "/work/cool-sneakers",
        "title": "Cool Sneakers",
        "caption": "TV Escola · Short film",
        "category": "shorts",
    },
    {
        "image": "original_egregora",
        "url": "/originals/egregore",
        "title": "Egregore",
        "caption": "Split Studio · Short film",
        "category": "shorts",
    },
    {
        "image": "work_world_doesnt_know",
        "url": "/work/the-world-doesnt-know",
        "title": "The World Doesn't Know What It Lost",
        "caption": "Split Studio · Promo",
        "category": "promos",
    },
    {
        "image": "work_oglobo_media_day",
        "url": "/work/oglobo-media-day",
        "title": "O Globo | Media Day",
        "caption": "O Globo · Branded content",
        "category": "branded",
    },
    {
        "image": "work_studio_r",
        "url": "/work/studio-r",
        "title": "Studio R",
        "caption": "Studio R · Promo",
        "category": "promos",
    },
    {
        "image": "work_sesc",
        "url": "/work/sesc-what-is-it",
        "title": "SESC | What Is It?",
        "caption": "SESC · Branded content",
        "category": "branded",
    },
    {
        "image": "work_luan_santana",
        "url": "/work/luan-santana",
        "title": "Luan Santana | I Didn't Deserve This",
        "caption": "Luan Santana · Music video",
        "category": "music",
    },
    {
        "image": "work_cabrito_chewy",
        "url": "/work/cabrito-chewy",
        "title": "Cabrito & Chewy",
        "caption": "Kids Glove · Promo",
        "category": "promos",
    },
    {
        "image": "work_one_fm_giant_robot",
        "url": "/work/1-fm-giant-robot",
        "title": "1 FM | Giant Robot",
        "caption": "1 FM · Branded content",
        "category": "branded",
    },
    {
        "image": "work_monica_month",
        "url": "/work/monica-month",
        "title": "Cartoon Network | Monica Month",
        "caption": "Cartoon Network · Branded content",
        "category": "branded",
    },
    {
        "image": "work_zolkin",
        "url": "/work/zolkin",
        "title": "Zolkin",
        "caption": "Zolkin · Branded content",
        "category": "branded",
    },
    {
        "image": "work_parmalat",
        "url": "/work/parmalat-manifesto",
        "title": "Parmalat | Manifesto",
        "caption": "Parmalat · Branded content",
        "category": "branded",
    },
    {
        "image": "work_zis",
        "url": "/work/zis",
        "title": "Zis",
        "caption": "Hélio Ziskind · Music video",
        "category": "music",
    },
    {
        "image": "work_from_love_to_bingo",
        "url": "/work/from-love-to-bingo",
        "title": "Getty Images | From Love to Bingo",
        "caption": "Getty Images · Branded content",
        "category": "branded",
    },
    {
        "image": "work_under_undergrounds",
        "url": "/work/under-undergrounds",
        "title": "The Under-Undergrounds",
        "caption": "Tortuga Studios · Animated series",
        "category": "shows",
    },
    {
        "image": "work_nick_summer",
        "url": "/work/nick-summer",
        "title": "Nickelodeon | Nick Summer",
        "caption": "Nickelodeon · Branded content",
        "category": "branded",
    },
    {
        "image": "work_que_corpo_eca",
        "url": "/work/que-corpo-e-esse-eca",
        "title": "Que Corpo é Esse? | Eca 30 Years",
        "caption": "Canal Futura · Branded content",
        "category": "branded",
    },
    {
        "image": "work_pernambucanas",
        "url": "/work/pernambucanas-friozinho",
        "title": "Pernambucanas | A Little Cold",
        "caption": "Pernambucanas · Branded content",
        "category": "branded",
    },
    {
        "image": "work_lala",
        "url": "/work/lala",
        "title": "Lala",
        "caption": "Lala Produções · Animated series",
        "category": "shows",
    },
    {
        "image": "work_balacobaco",
        "url": "/work/balacobaco",
        "title": "Balacobaco",
        "caption": "Record · Branded content",
        "category": "branded",
    },
    {
        "image": "work_yellow_woodpecker",
        "url": "/work/yellow-woodpecker-farm",
        "title": "Yellow Woodpecker Farm",
        "caption": "Rede Globo · TV series",
        "category": "shows",
    },
    {
        "image": "work_elma_chips",
        "url": "/work/elma-chips",
        "title": "Elma Chips | Peanuts",
        "caption": "Elma Chips · Branded content",
        "category": "branded",
    },
    {
        "image": "work_a_common_place",
        "url": "/work/a-common-place",
        "title": "A Common Place",
        "caption": "Split Studio · Short film",
        "category": "shorts",
    },
    {
        "image": "work_iguatemi",
        "url": "/work/iguatemi-theater",
        "title": "Iguatemi Theater",
        "caption": "Teatro Iguatemi · Branded content",
        "category": "branded",
    },
    {
        "image": "original_to_reach_the_moon",
        "url": "/originals/to-reach-the-moon",
        "title": "To Reach the Moon",
        "caption": "Split Studio · Short film",
        "category": "shorts",
    },
)

NEW_ASSETS = (
    (
        "work_castanhari_2023",
        "https://splitstudio.tv/wp-content/uploads/2025/09/Castanhari_2023_Retrospectiva_Split_Studio_Animation.jpg",
    ),
    (
        "work_castanhari_2022",
        "https://splitstudio.tv/wp-content/uploads/2023/01/Split_Studio_Castanhari_Retrospectiva_animation.jpg",
    ),
    (
        "work_heart_of_darkness",
        "https://splitstudio.tv/wp-content/uploads/2021/02/Coracao_trevas-800x450-1.jpg",
    ),
    (
        "work_dc_fandome",
        "https://splitstudio.tv/wp-content/uploads/2022/06/Split_Studio_DC_fandome_turma_monica_animation.jpg",
    ),
    (
        "work_adventures_of_mike",
        "https://splitstudio.tv/wp-content/uploads/2022/06/Split_Studio_as_aventuras_de_mike_animation.jpg",
    ),
    (
        "work_hello_kitty_chef_star",
        "https://splitstudio.tv/wp-content/uploads/2022/06/Split_Studio_sanrio_hello_kitty_chef_star_animation.jpg",
    ),
    (
        "work_hello_kitty_fun",
        "https://splitstudio.tv/wp-content/uploads/2022/07/Split_Studio_Hello_Kitty_Fun_animation.jpg",
    ),
    (
        "work_radio_bita",
        "https://splitstudio.tv/wp-content/uploads/2022/05/Split_Studio_Mr-Plot_r%C3%A1dio_bita_aquarela_animation.jpg",
    ),
    (
        "work_league_of_legends",
        "https://splitstudio.tv/wp-content/uploads/2021/02/masteryi.png",
    ),
    (
        "work_senninha",
        "https://splitstudio.tv/wp-content/uploads/2021/06/Split_Studio_Senninha_Pista_Maluca_animation.jpg",
    ),
    (
        "work_betania_kids",
        "https://splitstudio.tv/wp-content/uploads/2021/06/Split_Studio_Turma_da_Monica_Betania_Kids_animation.jpg",
    ),
    (
        "work_seara_monica",
        "https://splitstudio.tv/wp-content/uploads/2022/06/Split_Studio_seara_turma_monica_animation.jpg",
    ),
    (
        "work_cool_sneakers",
        "https://splitstudio.tv/wp-content/uploads/2022/06/Split_Studio_TV_escola_tenis_da_hora_animation.jpg",
    ),
    (
        "work_world_doesnt_know",
        "https://splitstudio.tv/wp-content/uploads/2021/02/omundonaosabe.png",
    ),
    (
        "work_oglobo_media_day",
        "https://splitstudio.tv/wp-content/uploads/2021/02/Split_Studio_Globo_Dia_Midia_animation.jpg",
    ),
    (
        "work_studio_r",
        "https://splitstudio.tv/wp-content/uploads/2022/07/Split_Studio_Studio_R_animation.jpg",
    ),
    (
        "work_sesc",
        "https://splitstudio.tv/wp-content/uploads/2021/02/SESC-800x450-1.jpg",
    ),
    (
        "work_luan_santana",
        "https://splitstudio.tv/wp-content/uploads/2021/02/Split_Studio_luan_santana_eu_n%C3%A3o_merecia_isso_animation.jpg",
    ),
    (
        "work_cabrito_chewy",
        "https://splitstudio.tv/wp-content/uploads/2021/02/cabrito.png",
    ),
    (
        "work_one_fm_giant_robot",
        "https://splitstudio.tv/wp-content/uploads/2021/02/Split_Studio_1FM_robo_gigante_animation.jpg",
    ),
    (
        "work_monica_month",
        "https://splitstudio.tv/wp-content/uploads/2021/02/Split_Studio_mes_monica_como_voc%C3%AA_imagina_a_monica_mais_velha_animation.jpg",
    ),
    (
        "work_zolkin",
        "https://splitstudio.tv/wp-content/uploads/2021/02/Split_Studio_zolkin_estabelecimentos_animation.jpg",
    ),
    (
        "work_parmalat",
        "https://splitstudio.tv/wp-content/uploads/2021/02/Split_Studio_Manifesto_Parmalat_animation.jpg",
    ),
    (
        "work_zis",
        "https://splitstudio.tv/wp-content/uploads/2021/02/Split_Studio_zis_volta_ao_mundo_num_bal%C3%A3o_animation.jpg",
    ),
    (
        "work_from_love_to_bingo",
        "https://splitstudio.tv/wp-content/uploads/2022/07/Split_Studio_Getty_Images_From_Love_To_Bingo_animation.jpg",
    ),
    (
        "work_under_undergrounds",
        "https://splitstudio.tv/wp-content/uploads/2021/02/underg.png",
    ),
    (
        "work_nick_summer",
        "https://splitstudio.tv/wp-content/uploads/2021/02/Split_Studio_ver%C3%A3o_nick_2020_animation.jpg",
    ),
    (
        "work_que_corpo_eca",
        "https://splitstudio.tv/wp-content/uploads/2021/02/Split_Studio_eca_que_corpo_%C3%A9_esse_animation.jpg",
    ),
    (
        "work_pernambucanas",
        "https://splitstudio.tv/wp-content/uploads/2021/02/Split_Studio_lojas_pernambucanas_friozinho_animation.jpg",
    ),
    (
        "work_lala",
        "https://splitstudio.tv/wp-content/uploads/2021/02/lala-800x450-1.jpg",
    ),
    (
        "work_balacobaco",
        "https://splitstudio.tv/wp-content/uploads/2021/02/Split_Studio_balacobaco_TV_record_animation.jpg",
    ),
    (
        "work_yellow_woodpecker",
        "https://splitstudio.tv/wp-content/uploads/2021/02/SITIO-800x450-1.jpg",
    ),
    (
        "work_elma_chips",
        "https://splitstudio.tv/wp-content/uploads/2022/06/Split_Studio_elma_chips_amendoim_animation.jpg",
    ),
    (
        "work_a_common_place",
        "https://splitstudio.tv/wp-content/uploads/2020/08/a_common_place_um_lugar_comum_split-studio_animation.jpg",
    ),
    (
        "work_iguatemi",
        "https://splitstudio.tv/wp-content/uploads/2021/02/iguatemi-800x450-1.jpg",
    ),
)

NEW_PROJECTS = (
    _sheet(
        "project_castanhari_2023",
        "/work/castanhari-2023",
        "Castanhari 2023 Recap",
        "Canal Nostalgia",
        "Music video",
        "work_castanhari_2023",
        "https://www.youtube.com/embed/f-P5jNek2Eo",
        "Direction, Storyboard & Animatic, Character Design, Props, "
        "Backgrounds, 2D Animation, Editing, Composition",
        "Year-end recap produced for Felipe Castanhari's Canal Nostalgia.",
        "A 2023 recap produced by Split for Canal Nostalgia, mixing 2D "
        "animation with Castanhari's year on YouTube.",
    ),
    _sheet(
        "project_castanhari_2022",
        "/work/castanhari-2022",
        "Castanhari 2022 Recap",
        "Canal Nostalgia",
        "Music video",
        "work_castanhari_2022",
        "https://www.youtube.com/embed/6yzRr3SGuv0",
        "Direction, Storyboard & Animatic, Character Design, Props, "
        "Backgrounds, 2D Animation, Editing, Composition",
        "Year-end recap produced for Felipe Castanhari's Canal Nostalgia.",
        "A 2022 recap produced by Split for Canal Nostalgia, covering "
        "direction, design and 2D animation through the final mix of the cut.",
    ),
    _sheet(
        "project_heart_of_darkness",
        "/work/heart-of-darkness",
        "Heart of Darkness",
        "Karmatique",
        "Promo",
        "work_heart_of_darkness",
        "https://player.vimeo.com/video/174560242",
        "Props, Backgrounds, 2D Animation, Editing, Composition",
        "Promo produced with Karmatique, with Split on art and 2D animation.",
        "A promo produced with Karmatique. Split handled props, backgrounds, "
        "2D animation, editing and composition.",
    ),
    _sheet(
        "project_dc_fandome",
        "/work/dc-fandome",
        "DC Fandome",
        "Mauricio de Sousa Produções",
        "Branded content",
        "work_dc_fandome",
        "https://www.youtube.com/embed/IlqcFlxbU2w",
        "Direction, Script, Storyboard & Animatic, Character Design, Props, "
        "Backgrounds, Builds, 2D Animation, Editing, Composition",
        "Branded short produced with Mauricio de Sousa Produções for DC Fandome.",
        "A branded Monica and Friends short produced with Mauricio de Sousa "
        "Produções for DC Fandome, covering the full 2D pipeline from "
        "direction and script through composition.",
    ),
    _sheet(
        "project_adventures_of_mike",
        "/work/adventures-of-mike",
        "The Adventures of Mike",
        "FalaíDearo",
        "Animated series",
        "work_adventures_of_mike",
        "https://www.youtube.com/embed/YGPIRtcOqDI",
        "Direction, Storyboard & Animatic, Voices, Character Design, Props, "
        "Backgrounds, Builds, 2D Animation, Editing, Composition, Sound FX, "
        "Songs, Mix",
        "Animated series produced with FalaíDearo, covering Split's 2D pipeline.",
        "An animated series produced with FalaíDearo. Split covered direction, "
        "voices, design and 2D animation through sound and mix.",
    ),
    _sheet(
        "project_hello_kitty_chef_star",
        "/work/hello-kitty-chef-star",
        "Hello Kitty Chef Star",
        "Sanrio Brazil",
        "Web series",
        "work_hello_kitty_chef_star",
        "https://www.youtube.com/embed/ZJ3KUnHManE",
        "Direction, Script, Storyboard & Animatic, Voices, Character Design, "
        "Props, Backgrounds, Builds, 2D Animation, Editing, Composition, "
        "Sound FX, Songs, Mix",
        "Hello Kitty web episodes produced for Sanrio Brazil.",
        "Web episodes of Hello Kitty Chef Star produced for Sanrio Brazil, "
        "from direction and script through animation, songs and mix.",
    ),
    _sheet(
        "project_hello_kitty_fun",
        "/work/hello-kitty-fun",
        "Hello Kitty Fun",
        "Sanrio Brazil",
        "Web series",
        "work_hello_kitty_fun",
        "https://www.youtube.com/embed/ZDn81ZwLs4c",
        "Direction, Script, Storyboard & Animatic, Voices, Character Design, "
        "Props, Backgrounds, Builds, 2D Animation, Editing, Composition, "
        "Sound FX, Songs, Mix",
        "Hello Kitty web episodes produced for Sanrio Brazil.",
        "Web episodes of Hello Kitty Fun produced for Sanrio Brazil, covering "
        "the full 2D pipeline from storyboard to mix.",
    ),
    _sheet(
        "project_radio_bita",
        "/work/radio-bita",
        "Radio Bita",
        "Mr Plot",
        "Music video",
        "work_radio_bita",
        "https://www.youtube.com/embed/72DQARLcNaY",
        "Storyboard & Animatic, 2D Animation",
        "Music videos produced with Mr Plot for Radio Bita.",
        "Music videos produced with Mr Plot for Radio Bita. Split handled "
        "storyboard, animatic and 2D animation.",
    ),
    _sheet(
        "project_league_of_legends",
        "/work/league-of-legends",
        "League of Legends | Project n.5",
        "Riot Games",
        "Branded content",
        "work_league_of_legends",
        "https://player.vimeo.com/video/76361506?h=5bab1a1926",
        "Direction, Storyboard & Animatic, Voices, Character Design, Props, "
        "Backgrounds, Builds, 2D Animation, Editing, Composition, Sound FX, "
        "Songs, Mix",
        "Branded film produced for Riot Games' League of Legends.",
        "A branded film produced for Riot Games. Split covered direction, "
        "voices, design and 2D animation through sound and mix.",
    ),
    _sheet(
        "project_senninha",
        "/work/senninha",
        "Senninha on the Crazy Track",
        "Instituto Ayrton Senna",
        "Animated series",
        "work_senninha",
        "https://player.vimeo.com/video/727512295?h=db7dc24b6a",
        "Direction, Storyboard & Animatic, Character Design, Props, "
        "Backgrounds, Builds, 2D Animation, Editing, Composition",
        "Animated series produced with Instituto Ayrton Senna and Gullane.",
        "An animated series produced with Instituto Ayrton Senna and Gullane. "
        "Split handled direction, design and 2D animation through composition.",
    ),
    _sheet(
        "project_betania_kids",
        "/work/betania-kids",
        "Betania Kids | Monica and Friends",
        "Mauricio de Sousa Produções",
        "Branded content",
        "work_betania_kids",
        "https://player.vimeo.com/video/310353799?h=f60fe5aa26",
        "2D Animation",
        "Branded Monica and Friends spots produced for Betania Kids.",
        "Branded Monica and Friends spots produced with Mauricio de Sousa "
        "Produções for Betania Kids, with Split on 2D animation.",
    ),
    _sheet(
        "project_seara_monica",
        "/work/seara-monica",
        "Seara | Monica and Friends",
        "Mauricio de Sousa Produções",
        "Branded content",
        "work_seara_monica",
        "https://player.vimeo.com/video/597442233?h=a0a54360aa",
        "Storyboard & Animatic, Props, Backgrounds, Builds, 2D Animation, "
        "Editing, Composition",
        "Branded Monica and Friends spots produced for Seara.",
        "Branded Monica and Friends spots produced with Mauricio de Sousa "
        "Produções for Seara, from storyboard through 2D animation and "
        "composition.",
    ),
    _sheet(
        "project_cool_sneakers",
        "/work/cool-sneakers",
        "Cool Sneakers",
        "TV Escola",
        "Short film",
        "work_cool_sneakers",
        "https://player.vimeo.com/video/127165510?h=227b2fea7c",
        "Direction, Script, Storyboard & Animatic, Voices, Character Design, "
        "Props, Backgrounds, Builds, 2D Animation, Editing, Composition, "
        "Sound FX, Songs",
        "Animated short produced with TV Escola.",
        "An animated short produced with TV Escola. Split covered direction, "
        "script, voices and 2D animation through songs.",
    ),
    _sheet(
        "project_world_doesnt_know",
        "/work/the-world-doesnt-know",
        "The World Doesn't Know What It Lost",
        "Split Studio",
        "Promo",
        "work_world_doesnt_know",
        "https://player.vimeo.com/video/421343267",
        "Direction, Script, Storyboard & Animatic, Voices, Character Design, "
        "Props, Backgrounds, Builds, 2D Animation, Editing, Composition, "
        "Sound FX, Songs, Mix",
        "Original promo created and produced inside Split.",
        "An original promo created inside Split, covering the film from "
        "direction and script through animation, sound and mix.",
    ),
    _sheet(
        "project_oglobo_media_day",
        "/work/oglobo-media-day",
        "O Globo | Media Day",
        "O Globo",
        "Branded content",
        "work_oglobo_media_day",
        "https://player.vimeo.com/video/69272160",
        "Direction, Storyboard & Animatic, Character Design, Props, "
        "Backgrounds, Builds, 2D Animation, Editing, Composition, Sound FX, "
        "Songs, Mix",
        "Branded film produced for O Globo's Media Day.",
        "A branded film produced for O Globo. Split handled direction, design "
        "and 2D animation through sound and mix.",
    ),
    _sheet(
        "project_studio_r",
        "/work/studio-r",
        "Studio R",
        "Studio R",
        "Promo",
        "work_studio_r",
        "https://player.vimeo.com/video/394302745",
        "Direction, Script, Storyboard & Animatic, Character Design, Props, "
        "Backgrounds, Builds, 2D Animation, Editing, Composition",
        "Promo produced for Studio R, covering Split's 2D pipeline.",
        "A promo produced for Studio R, from direction and script through "
        "design, 2D animation and composition.",
    ),
    _sheet(
        "project_sesc",
        "/work/sesc-what-is-it",
        "SESC | What Is It?",
        "SESC",
        "Branded content",
        "work_sesc",
        "https://player.vimeo.com/video/76134552",
        "Direction, Script, Storyboard & Animatic, Props, Backgrounds, "
        "Builds, 2D Animation, Editing, Composition",
        "Branded film produced for SESC.",
        "A branded film produced for SESC. Split covered direction, script "
        "and 2D animation through composition.",
    ),
    _sheet(
        "project_luan_santana",
        "/work/luan-santana",
        "Luan Santana | I Didn't Deserve This",
        "Luan Santana",
        "Music video",
        "work_luan_santana",
        "https://player.vimeo.com/video/174703209",
        "Direction, Storyboard & Animatic, Character Design, Props, "
        "Backgrounds, Builds, 2D Animation, Editing, Composition",
        "Animated music video produced for Luan Santana.",
        "An animated music video produced for Luan Santana, from direction "
        "and storyboard through 2D animation and composition.",
    ),
    _sheet(
        "project_cabrito_chewy",
        "/work/cabrito-chewy",
        "Cabrito & Chewy",
        "Kids Glove",
        "Promo",
        "work_cabrito_chewy",
        "https://player.vimeo.com/video/293003920",
        "Props, Backgrounds, Builds, 2D Animation",
        "Promo produced with Kids Glove, with Split on art and 2D animation.",
        "A promo produced with Kids Glove. Split handled props, backgrounds, "
        "builds and 2D animation.",
    ),
    _sheet(
        "project_one_fm_giant_robot",
        "/work/1-fm-giant-robot",
        "1 FM | Giant Robot",
        "1 FM",
        "Branded content",
        "work_one_fm_giant_robot",
        "https://player.vimeo.com/video/97970395",
        "Direction, Script, Storyboard & Animatic, Voices, Character Design, "
        "Props, Backgrounds, Builds, 2D Animation, Editing, Composition, "
        "Sound FX, Songs, Mix",
        "Branded film produced for 1 FM.",
        "A branded film produced for 1 FM. Split covered direction, voices "
        "and 2D animation through sound and mix.",
    ),
    _sheet(
        "project_monica_month",
        "/work/monica-month",
        "Cartoon Network | Monica Month",
        "Cartoon Network",
        "Branded content",
        "work_monica_month",
        "https://www.youtube.com/embed/YCD1sUe4gUU",
        "Direction, Script, Storyboard & Animatic, Character Design, Props, "
        "Backgrounds, Builds, 2D Animation, Editing, Composition",
        "Branded campaign produced for Cartoon Network's Monica Month.",
        "A branded campaign produced for Cartoon Network's Monica Month, "
        "from direction and script through 2D animation and composition.",
    ),
    _sheet(
        "project_zolkin",
        "/work/zolkin",
        "Zolkin",
        "Zolkin",
        "Branded content",
        "work_zolkin",
        "https://player.vimeo.com/video/234067873",
        "Direction, Storyboard & Animatic, Voices, Character Design, Props, "
        "Backgrounds, Builds, 2D Animation, Editing, Composition, Sound FX, "
        "Songs, Mix",
        "Branded film produced for Zolkin.",
        "A branded film produced for Zolkin, covering direction, voices and "
        "2D animation through sound and mix.",
    ),
    _sheet(
        "project_parmalat",
        "/work/parmalat-manifesto",
        "Parmalat | Manifesto",
        "Parmalat",
        "Branded content",
        "work_parmalat",
        "https://player.vimeo.com/video/50889510",
        "Storyboard & Animatic, Character Designs, Props, Backgrounds, "
        "Builds, 2D Animation, Editing, Compositing",
        "Branded manifesto produced for Parmalat.",
        "A branded manifesto produced for Parmalat. Split handled storyboard, "
        "design and 2D animation through compositing.",
    ),
    _sheet(
        "project_zis",
        "/work/zis",
        "Zis",
        "Hélio Ziskind",
        "Music video",
        "work_zis",
        "https://player.vimeo.com/video/121944857",
        "Direction, Script, Storyboard & Animatic, Character Design, Props, "
        "Backgrounds, Builds, 2D Animation, Editing, Composition",
        "Animated music video produced with Hélio Ziskind.",
        "An animated music video produced with Hélio Ziskind, from direction "
        "and script through 2D animation and composition.",
    ),
    _sheet(
        "project_from_love_to_bingo",
        "/work/from-love-to-bingo",
        "Getty Images | From Love to Bingo",
        "Getty Images",
        "Branded content",
        "work_from_love_to_bingo",
        "https://player.vimeo.com/video/42153891",
        "Editing, Composition",
        "Branded film produced for Getty Images.",
        "A branded film produced for Getty Images, with Split on editing and "
        "composition.",
    ),
    _sheet(
        "project_under_undergrounds",
        "/work/under-undergrounds",
        "The Under-Undergrounds",
        "Tortuga Studios",
        "Animated series",
        "work_under_undergrounds",
        "https://player.vimeo.com/video/238816077",
        "Storyboard & Animatic, Builds, 2D Animation",
        "Animated series produced with Tortuga Studios.",
        "An animated series produced with Tortuga Studios. Split handled "
        "storyboard, builds and 2D animation.",
    ),
    _sheet(
        "project_nick_summer",
        "/work/nick-summer",
        "Nickelodeon | Nick Summer",
        "Nickelodeon",
        "Branded content",
        "work_nick_summer",
        "https://player.vimeo.com/video/386018977",
        "Direction, Storyboard & Animatic, Voices, Character Design, Props, "
        "Backgrounds, Builds, 2D Animation, Editing, Composition",
        "Branded campaign produced for Nickelodeon's Nick Summer.",
        "A branded campaign produced for Nickelodeon. Split covered direction, "
        "voices, design and 2D animation through composition.",
    ),
    _sheet(
        "project_que_corpo_eca",
        "/work/que-corpo-e-esse-eca",
        "Que Corpo é Esse? | Eca 30 Years",
        "Canal Futura",
        "Branded content",
        "work_que_corpo_eca",
        "https://player.vimeo.com/video/507737822",
        "Direction, Script, Voices, Storyboard & Animatic, Character Design, "
        "Props, Backgrounds, Builds, 2D Animation, Editing, Composition, "
        "Sound FX, Songs, Mix",
        "Branded film produced with Canal Futura for Eca's 30th anniversary.",
        "A branded Que Corpo é Esse? film produced with Canal Futura for "
        "Eca's 30th anniversary, covering the full 2D pipeline.",
    ),
    _sheet(
        "project_pernambucanas",
        "/work/pernambucanas-friozinho",
        "Pernambucanas | A Little Cold",
        "Pernambucanas",
        "Branded content",
        "work_pernambucanas",
        "https://player.vimeo.com/video/378914575",
        "2D Animation",
        "Branded spot produced for Pernambucanas.",
        "A branded spot produced for Pernambucanas, with Split on 2D "
        "animation.",
    ),
    _sheet(
        "project_lala",
        "/work/lala",
        "Lala",
        "Lala Produções",
        "Animated series",
        "work_lala",
        "https://player.vimeo.com/video/323883479",
        "Character Design, Props, Backgrounds, Builds, 2D Animation",
        "Animated series produced with Lala Produções.",
        "An animated series produced with Lala Produções. Split handled "
        "character design, props, backgrounds, builds and 2D animation.",
    ),
    _sheet(
        "project_balacobaco",
        "/work/balacobaco",
        "Balacobaco",
        "Record",
        "Branded content",
        "work_balacobaco",
        "https://player.vimeo.com/video/53354419",
        "2D Animation",
        "Branded content produced for Record.",
        "Branded content produced for Record, with Split on 2D animation.",
    ),
    _sheet(
        "project_yellow_woodpecker",
        "/work/yellow-woodpecker-farm",
        "Yellow Woodpecker Farm",
        "Rede Globo",
        "TV series",
        "work_yellow_woodpecker",
        "https://player.vimeo.com/video/238807979",
        "2D Animation",
        "TV series animation produced for Rede Globo.",
        "Animation produced for Rede Globo's Yellow Woodpecker Farm. The "
        "series ran 26 episodes of 11 minutes, with Split on 2D animation.",
        extra_facts=(("Format", "26 x 11 min"),),
    ),
    _sheet(
        "project_elma_chips",
        "/work/elma-chips",
        "Elma Chips | Peanuts",
        "Elma Chips",
        "Branded content",
        "work_elma_chips",
        "https://player.vimeo.com/video/36199978?h=e785e7870c",
        "Direction, Script, Storyboard & Animatic, Voices, Character Design, "
        "Props, Backgrounds, Builds, 2D Animation, Editing, Composition, "
        "Sound FX, Songs, Mix",
        "Branded film produced for Elma Chips.",
        "A branded film produced for Elma Chips. Split covered direction, "
        "voices and 2D animation through sound and mix.",
    ),
    _sheet(
        "project_a_common_place",
        "/work/a-common-place",
        "A Common Place",
        "Split Studio",
        "Short film",
        "work_a_common_place",
        "https://player.vimeo.com/video/7727630?h=deb532ce96",
        "Direction, Script, Storyboard & Animatic, Voices, Character Design, "
        "Props, Backgrounds, Builds, 2D Animation, Editing, Composition, "
        "Songs, Mix",
        "Original animated short created and produced by Split.",
        "An original animated short created inside Split, from direction and "
        "script through animation, songs and mix.",
    ),
    _sheet(
        "project_iguatemi",
        "/work/iguatemi-theater",
        "Iguatemi Theater",
        "Teatro Iguatemi",
        "Branded content",
        "work_iguatemi",
        "https://player.vimeo.com/video/61545340",
        "Direction, Script, Storyboard & Animatic, Voices, Character Design, "
        "Props, Backgrounds, Builds, 2D Animation, Editing, Composition, "
        "Sound FX, Songs, Mix",
        "Branded film produced for Teatro Iguatemi.",
        "A branded film produced for Teatro Iguatemi, covering direction, "
        "voices and 2D animation through sound and mix.",
    ),
)

TITLE_TRANSLATIONS = {
    "Castanhari 2023 Recap": "Retrospectiva Castanhari 2023",
    "Castanhari 2022 Recap": "Retrospectiva Castanhari 2022",
    "The Adventures of Mike": "As Aventuras de Mike",
    "Radio Bita": "Rádio Bita",
    "Senninha on the Crazy Track": "Senninha na Pista Maluca",
    "Betania Kids | Monica and Friends": "Betânia Kids | Turma da Mônica",
    "Seara | Monica and Friends": "Seara | Turma da Mônica",
    "Cool Sneakers": "Tênis da Hora",
    "The World Doesn't Know What It Lost": "O Mundo Não Sabe o que Perdeu",
    "O Globo | Media Day": "O Globo | Dia do Mídia",
    "SESC | What Is It?": "SESC | O Que é o Que é?",
    "Luan Santana | I Didn't Deserve This": "Luan Santana | Eu Não Merecia Isso",
    "1 FM | Giant Robot": "1 FM | Robô Gigante",
    "Cartoon Network | Monica Month": "Cartoon Network | Mês da Mônica",
    "The Under-Undergrounds": "Os Under-Undergrounds",
    "Nickelodeon | Nick Summer": "Nickelodeon | Verão Nick",
    "Que Corpo é Esse? | Eca 30 Years": "Que Corpo é Esse? | Eca 30 Anos",
    "Pernambucanas | A Little Cold": "Lojas Pernambucanas | Friozinho",
    "Yellow Woodpecker Farm": "Sítio do Picapau Amarelo",
    "Elma Chips | Peanuts": "Elma Chips | Amendoim",
    "A Common Place": "Um Lugar Comum",
    "Iguatemi Theater": "Teatro Iguatemi",
    "Music videos": "Clipes musicais",
    "Short films": "Curtas-metragens",
    "Games": "Games",
    "Music video": "Clipe musical",
    "Branded content": "Branded content",
    "Canal Nostalgia · Music video": "Canal Nostalgia · Clipe musical",
    "FalaíDearo · Animated series": "FalaíDearo · Série animada",
    "Sanrio Brazil · Web series": "Sanrio Brasil · Websérie",
    "Mr Plot · Music video": "Mr Plot · Clipe musical",
    "Riot Games · Branded content": "Riot Games · Branded content",
    "Instituto Ayrton Senna · Animated series": (
        "Instituto Ayrton Senna · Série animada"
    ),
    "Mauricio de Sousa Produções · Branded content": (
        "Mauricio de Sousa Produções · Branded content"
    ),
    "TV Escola · Short film": "TV Escola · Curta-metragem",
    "Split Studio · Promo": "Split Studio · Promo",
    "Split Studio · Music videos": "Split Studio · Clipes musicais",
    "Split Studio · Short film": "Split Studio · Curta-metragem",
    "O Globo · Branded content": "O Globo · Branded content",
    "Studio R · Promo": "Studio R · Promo",
    "SESC · Branded content": "SESC · Branded content",
    "Luan Santana · Music video": "Luan Santana · Clipe musical",
    "Kids Glove · Promo": "Kids Glove · Promo",
    "1 FM · Branded content": "1 FM · Branded content",
    "Cartoon Network · Branded content": "Cartoon Network · Branded content",
    "Zolkin · Branded content": "Zolkin · Branded content",
    "Parmalat · Branded content": "Parmalat · Branded content",
    "Hélio Ziskind · Music video": "Hélio Ziskind · Clipe musical",
    "Getty Images · Branded content": "Getty Images · Branded content",
    "Tortuga Studios · Animated series": "Tortuga Studios · Série animada",
    "Nickelodeon · Branded content": "Nickelodeon · Branded content",
    "Canal Futura · Branded content": "Canal Futura · Branded content",
    "Pernambucanas · Branded content": "Pernambucanas · Branded content",
    "Lala Produções · Animated series": "Lala Produções · Série animada",
    "Record · Branded content": "Record · Branded content",
    "Rede Globo · TV series": "Rede Globo · Série de TV",
    "Elma Chips · Branded content": "Elma Chips · Branded content",
    "Teatro Iguatemi · Branded content": "Teatro Iguatemi · Branded content",
    "Karmatique · Promo": "Karmatique · Promo",
    "Nick Jr. US · Promo": "Nick Jr. US · Promo",
    "26 x 11 min": "26 x 11 min",
    "Year-end recap produced for Felipe Castanhari's Canal Nostalgia.": (
        "Retrospectiva produzida para o Canal Nostalgia de Felipe Castanhari."
    ),
    "A 2023 recap produced by Split for Canal Nostalgia, mixing 2D "
    "animation with Castanhari's year on YouTube.": (
        "Retrospectiva de 2023 produzida pela Split para o Canal Nostalgia, "
        "misturando animação 2D com o ano do Castanhari no YouTube."
    ),
    "A 2022 recap produced by Split for Canal Nostalgia, covering "
    "direction, design and 2D animation through the final mix of the cut.": (
        "Retrospectiva de 2022 produzida pela Split para o Canal Nostalgia, "
        "da direção e do design à animação 2D e à mixagem final."
    ),
    "Branded film produced for Riot Games' League of Legends.": (
        "Filme branded produzido para o League of Legends da Riot Games."
    ),
    "A branded film produced for Riot Games. Split covered direction, "
    "voices, design and 2D animation through sound and mix.": (
        "Filme branded produzido para a Riot Games. A Split cobriu direção, "
        "vozes, design e animação 2D até o som e a mixagem."
    ),
    "Animated series produced with Instituto Ayrton Senna and Gullane.": (
        "Série animada produzida com o Instituto Ayrton Senna e a Gullane."
    ),
    "An animated series produced with Instituto Ayrton Senna and Gullane. "
    "Split handled direction, design and 2D animation through composition.": (
        "Série animada produzida com o Instituto Ayrton Senna e a Gullane. "
        "A Split fez direção, design e animação 2D até a composição."
    ),
    "Promo produced with Karmatique, with Split on art and 2D animation.": (
        "Promo produzida com a Karmatique, com a Split na arte e na animação 2D."
    ),
    "A promo produced with Karmatique. Split handled props, backgrounds, "
    "2D animation, editing and composition.": (
        "Promo produzida com a Karmatique. A Split fez props, cenários, "
        "animação 2D, edição e composição."
    ),
    "Branded short produced with Mauricio de Sousa Produções for DC Fandome.": (
        "Curta branded produzido com a Mauricio de Sousa Produções para o DC Fandome."
    ),
    "A branded Monica and Friends short produced with Mauricio de Sousa "
    "Produções for DC Fandome, covering the full 2D pipeline from "
    "direction and script through composition.": (
        "Curta branded da Turma da Mônica produzido com a Mauricio de Sousa "
        "Produções para o DC Fandome, cobrindo o pipeline 2D da direção e "
        "do roteiro até a composição."
    ),
    "Animated series produced with FalaíDearo, covering Split's 2D pipeline.": (
        "Série animada produzida com a FalaíDearo, cobrindo o pipeline 2D da Split."
    ),
    "An animated series produced with FalaíDearo. Split covered direction, "
    "voices, design and 2D animation through sound and mix.": (
        "Série animada produzida com a FalaíDearo. A Split cobriu direção, "
        "vozes, design e animação 2D até o som e a mixagem."
    ),
    "Hello Kitty web episodes produced for Sanrio Brazil.": (
        "Episódios web da Hello Kitty produzidos para a Sanrio Brasil."
    ),
    "Web episodes of Hello Kitty Chef Star produced for Sanrio Brazil, "
    "from direction and script through animation, songs and mix.": (
        "Episódios web de Hello Kitty Chef Star produzidos para a Sanrio "
        "Brasil, da direção e do roteiro à animação, às músicas e à mixagem."
    ),
    "Web episodes of Hello Kitty Fun produced for Sanrio Brazil, covering "
    "the full 2D pipeline from storyboard to mix.": (
        "Episódios web de Hello Kitty Fun produzidos para a Sanrio Brasil, "
        "cobrindo o pipeline 2D do storyboard à mixagem."
    ),
    "Music videos produced with Mr Plot for Radio Bita.": (
        "Clipes produzidos com a Mr Plot para o Rádio Bita."
    ),
    "Music videos produced with Mr Plot for Radio Bita. Split handled "
    "storyboard, animatic and 2D animation.": (
        "Clipes produzidos com a Mr Plot para o Rádio Bita. A Split fez "
        "storyboard, animatic e animação 2D."
    ),
    "Branded Monica and Friends spots produced for Betania Kids.": (
        "Spots branded da Turma da Mônica produzidos para a Betânia Kids."
    ),
    "Branded Monica and Friends spots produced with Mauricio de Sousa "
    "Produções for Betania Kids, with Split on 2D animation.": (
        "Spots branded da Turma da Mônica produzidos com a Mauricio de Sousa "
        "Produções para a Betânia Kids, com a Split na animação 2D."
    ),
    "Branded Monica and Friends spots produced for Seara.": (
        "Spots branded da Turma da Mônica produzidos para a Seara."
    ),
    "Branded Monica and Friends spots produced with Mauricio de Sousa "
    "Produções for Seara, from storyboard through 2D animation and "
    "composition.": (
        "Spots branded da Turma da Mônica produzidos com a Mauricio de Sousa "
        "Produções para a Seara, do storyboard à animação 2D e à composição."
    ),
    "Animated short produced with TV Escola.": (
        "Curta animado produzido com a TV Escola."
    ),
    "An animated short produced with TV Escola. Split covered direction, "
    "script, voices and 2D animation through songs.": (
        "Curta animado produzido com a TV Escola. A Split cobriu direção, "
        "roteiro, vozes e animação 2D até as músicas."
    ),
    "Original promo created and produced inside Split.": (
        "Promo original criada e produzida dentro da Split."
    ),
    "An original promo created inside Split, covering the film from "
    "direction and script through animation, sound and mix.": (
        "Promo original criada dentro da Split, cobrindo o filme da direção "
        "e do roteiro à animação, ao som e à mixagem."
    ),
    "Branded film produced for O Globo's Media Day.": (
        "Filme branded produzido para o Dia do Mídia do O Globo."
    ),
    "A branded film produced for O Globo. Split handled direction, design "
    "and 2D animation through sound and mix.": (
        "Filme branded produzido para O Globo. A Split fez direção, design "
        "e animação 2D até o som e a mixagem."
    ),
    "Promo produced for Studio R, covering Split's 2D pipeline.": (
        "Promo produzida para o Studio R, cobrindo o pipeline 2D da Split."
    ),
    "A promo produced for Studio R, from direction and script through "
    "design, 2D animation and composition.": (
        "Promo produzida para o Studio R, da direção e do roteiro ao design, "
        "à animação 2D e à composição."
    ),
    "Branded film produced for SESC.": "Filme branded produzido para o SESC.",
    "A branded film produced for SESC. Split covered direction, script "
    "and 2D animation through composition.": (
        "Filme branded produzido para o SESC. A Split cobriu direção, roteiro "
        "e animação 2D até a composição."
    ),
    "Animated music video produced for Luan Santana.": (
        "Clipe animado produzido para Luan Santana."
    ),
    "An animated music video produced for Luan Santana, from direction "
    "and storyboard through 2D animation and composition.": (
        "Clipe animado produzido para Luan Santana, da direção e do "
        "storyboard à animação 2D e à composição."
    ),
    "Promo produced with Kids Glove, with Split on art and 2D animation.": (
        "Promo produzida com a Kids Glove, com a Split na arte e na animação 2D."
    ),
    "A promo produced with Kids Glove. Split handled props, backgrounds, "
    "builds and 2D animation.": (
        "Promo produzida com a Kids Glove. A Split fez props, cenários, "
        "rigs e animação 2D."
    ),
    "Branded film produced for 1 FM.": "Filme branded produzido para a 1 FM.",
    "A branded film produced for 1 FM. Split covered direction, voices "
    "and 2D animation through sound and mix.": (
        "Filme branded produzido para a 1 FM. A Split cobriu direção, vozes "
        "e animação 2D até o som e a mixagem."
    ),
    "Branded campaign produced for Cartoon Network's Monica Month.": (
        "Campanha branded produzida para o Mês da Mônica do Cartoon Network."
    ),
    "A branded campaign produced for Cartoon Network's Monica Month, "
    "from direction and script through 2D animation and composition.": (
        "Campanha branded produzida para o Mês da Mônica do Cartoon Network, "
        "da direção e do roteiro à animação 2D e à composição."
    ),
    "Branded film produced for Zolkin.": "Filme branded produzido para a Zolkin.",
    "A branded film produced for Zolkin, covering direction, voices and "
    "2D animation through sound and mix.": (
        "Filme branded produzido para a Zolkin, cobrindo direção, vozes e "
        "animação 2D até o som e a mixagem."
    ),
    "Branded manifesto produced for Parmalat.": (
        "Manifesto branded produzido para a Parmalat."
    ),
    "A branded manifesto produced for Parmalat. Split handled storyboard, "
    "design and 2D animation through compositing.": (
        "Manifesto branded produzido para a Parmalat. A Split fez storyboard, "
        "design e animação 2D até a composição."
    ),
    "Animated music video produced with Hélio Ziskind.": (
        "Clipe animado produzido com Hélio Ziskind."
    ),
    "An animated music video produced with Hélio Ziskind, from direction "
    "and script through 2D animation and composition.": (
        "Clipe animado produzido com Hélio Ziskind, da direção e do roteiro "
        "à animação 2D e à composição."
    ),
    "Branded film produced for Getty Images.": (
        "Filme branded produzido para a Getty Images."
    ),
    "A branded film produced for Getty Images, with Split on editing and "
    "composition.": (
        "Filme branded produzido para a Getty Images, com a Split na edição "
        "e na composição."
    ),
    "Animated series produced with Tortuga Studios.": (
        "Série animada produzida com a Tortuga Studios."
    ),
    "An animated series produced with Tortuga Studios. Split handled "
    "storyboard, builds and 2D animation.": (
        "Série animada produzida com a Tortuga Studios. A Split fez "
        "storyboard, rigs e animação 2D."
    ),
    "Branded campaign produced for Nickelodeon's Nick Summer.": (
        "Campanha branded produzida para o Verão Nick da Nickelodeon."
    ),
    "A branded campaign produced for Nickelodeon. Split covered direction, "
    "voices, design and 2D animation through composition.": (
        "Campanha branded produzida para a Nickelodeon. A Split cobriu "
        "direção, vozes, design e animação 2D até a composição."
    ),
    "Branded film produced with Canal Futura for Eca's 30th anniversary.": (
        "Filme branded produzido com o Canal Futura para os 30 anos da Eca."
    ),
    "A branded Que Corpo é Esse? film produced with Canal Futura for "
    "Eca's 30th anniversary, covering the full 2D pipeline.": (
        "Filme branded de Que Corpo é Esse? produzido com o Canal Futura "
        "para os 30 anos da Eca, cobrindo o pipeline 2D completo."
    ),
    "Branded spot produced for Pernambucanas.": (
        "Spot branded produzido para as Pernambucanas."
    ),
    "A branded spot produced for Pernambucanas, with Split on 2D "
    "animation.": (
        "Spot branded produzido para as Pernambucanas, com a Split na "
        "animação 2D."
    ),
    "Animated series produced with Lala Produções.": (
        "Série animada produzida com a Lala Produções."
    ),
    "An animated series produced with Lala Produções. Split handled "
    "character design, props, backgrounds, builds and 2D animation.": (
        "Série animada produzida com a Lala Produções. A Split fez design "
        "de personagens, props, cenários, rigs e animação 2D."
    ),
    "Branded content produced for Record.": (
        "Branded content produzido para a Record."
    ),
    "Branded content produced for Record, with Split on 2D animation.": (
        "Branded content produzido para a Record, com a Split na animação 2D."
    ),
    "TV series animation produced for Rede Globo.": (
        "Animação de série produzida para a Rede Globo."
    ),
    "Animation produced for Rede Globo's Yellow Woodpecker Farm. The "
    "series ran 26 episodes of 11 minutes, with Split on 2D animation.": (
        "Animação produzida para o Sítio do Picapau Amarelo da Rede Globo. "
        "A série teve 26 episódios de 11 minutos, com a Split na animação 2D."
    ),
    "Branded film produced for Elma Chips.": (
        "Filme branded produzido para a Elma Chips."
    ),
    "A branded film produced for Elma Chips. Split covered direction, "
    "voices and 2D animation through sound and mix.": (
        "Filme branded produzido para a Elma Chips. A Split cobriu direção, "
        "vozes e animação 2D até o som e a mixagem."
    ),
    "Original animated short created and produced by Split.": (
        "Curta original criado e produzido pela Split."
    ),
    "An original animated short created inside Split, from direction and "
    "script through animation, songs and mix.": (
        "Curta original criado dentro da Split, da direção e do roteiro à "
        "animação, às músicas e à mixagem."
    ),
    "Branded film produced for Teatro Iguatemi.": (
        "Filme branded produzido para o Teatro Iguatemi."
    ),
    "A branded film produced for Teatro Iguatemi, covering direction, "
    "voices and 2D animation through sound and mix.": (
        "Filme branded produzido para o Teatro Iguatemi, cobrindo direção, "
        "vozes e animação 2D até o som e a mixagem."
    ),
    "Cabrito & Chewy": "Cabrito & Chewy",
    "Cabrito &amp; Chewy": "Cabrito &amp; Chewy",
    "Hélio Ziskind": "Hélio Ziskind",
    "Luan Santana": "Luan Santana",
    "Rede Globo": "Rede Globo",
    "TV Escola": "TV Escola",
}
