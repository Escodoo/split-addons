# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Merge an Odoo-exported POT with Brazilian Portuguese translations."""
# pylint: disable=print-used

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent.parent
I18N_DIR = MODULE_DIR / "i18n"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from work_catalog import TITLE_TRANSLATIONS  # noqa: E402
DEFAULT_EXPORT = Path("/opt/odoo/auto/split_website.export.pot")
LOCAL_EXPORT = MODULE_DIR.parents[4] / "auto" / "split_website.export.pot"

HEADER = '''# Translation of Odoo Server.
# This file contains the translation of the following modules:
# \t* split_website
#
msgid ""
msgstr ""
"Project-Id-Version: Odoo Server 18.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2026-08-19 19:30+0000\\n"
"PO-Revision-Date: 2026-08-19 19:30+0000\\n"
"Last-Translator: Escodoo <https://www.escodoo.com.br>\\n"
"Language-Team: Portuguese (Brazil)\\n"
"Language: pt_BR\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: \\n"
"Plural-Forms: nplurals=2; plural=(n > 1);\\n"
'''


def normalize(text: str) -> str:
    return " ".join(text.replace("\xa0", " ").split())


def parse_po(path: Path) -> list[dict]:
    entries: list[dict] = []
    msgid = None
    msgstr = None
    comments: list[str] = []
    mode = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal msgid, msgstr, comments
        if msgid is not None:
            entries.append(
                {"comments": comments, "msgid": msgid, "msgstr": msgstr or ""}
            )
        comments = []
        msgid = None
        msgstr = None

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            if mode in {"msgid", "msgstr"}:
                if mode == "msgid":
                    msgid = "".join(buf)
                else:
                    msgstr = "".join(buf)
                mode = None
                buf = []
            comments.append(line)
        elif line.startswith("msgid "):
            if mode == "msgstr":
                msgstr = "".join(buf)
                flush()
            mode = "msgid"
            buf = [json.loads(line[6:])]
        elif line.startswith("msgstr "):
            if mode == "msgid":
                msgid = "".join(buf)
            mode = "msgstr"
            buf = [json.loads(line[7:])]
        elif line.startswith('"') and mode:
            buf.append(json.loads(line))
        elif not line.strip():
            if mode == "msgstr":
                msgstr = "".join(buf)
                flush()
            mode = None
            buf = []
    if mode == "msgstr":
        msgstr = "".join(buf)
        flush()
    return entries


def encode_po_string(value: str) -> str:
    escaped = json.dumps(value, ensure_ascii=False)
    if "\n" not in value and len(escaped) <= 76:
        return escaped
    parts = ['""']
    if "\n" in value:
        chunks = value.split("\n")
        for index, chunk in enumerate(chunks):
            suffix = "\n" if index < len(chunks) - 1 else ""
            parts.append(json.dumps(chunk + suffix, ensure_ascii=False))
        return "\n".join(parts)
    words = value.split(" ")
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if current and len(json.dumps(candidate, ensure_ascii=False)) > 76:
            parts.append(json.dumps(current + " ", ensure_ascii=False))
            current = word
        else:
            current = candidate
    if current:
        parts.append(json.dumps(current, ensure_ascii=False))
    return "\n".join(parts)


def expand_copied_view_comments(comments: list[str]) -> list[str]:
    """Home and contact replace core website views on every module update."""
    blob = "\n".join(comments)
    extra = []
    if (
        "split_website.homepage" in blob
        and "arch_db:website.homepage" not in blob
    ):
        extra.append("#: model_terms:ir.ui.view,arch_db:website.homepage")
    if (
        "split_website.contactus" in blob
        and "arch_db:website.contactus" not in blob
    ):
        extra.append("#: model_terms:ir.ui.view,arch_db:website.contactus")
    return comments + extra


def write_po(path: Path, entries: list[dict], *, pot: bool) -> None:
    chunks = [HEADER if not pot else HEADER.replace("Language: pt_BR\\n", "")]
    for entry in entries:
        if not entry["msgid"]:
            continue
        if entry["comments"]:
            chunks.append("\n".join(entry["comments"]))
        chunks.append(f"msgid {encode_po_string(entry['msgid'])}")
        chunks.append(
            f"msgstr {encode_po_string('' if pot else entry['msgstr'])}"
        )
        chunks.append("")
    path.write_text("\n".join(chunks) + "\n", encoding="utf-8")


# Normalized English -> Portuguese. Official Split copy is preferred.
TRANSLATIONS = {
    **TITLE_TRANSLATIONS,
    "10 x 22′ | 12+ years old": "10 x 22′ | 12+ anos",
    "20 x 5 min": "20 x 5 min",
    "26 x 7′ | 4 to 7 years old": "26 x 7′ | 4 a 7 anos",
    "2D Animation": "Animação 2D",
    "52 x 7′": "52 x 7′",
    "75 x 3′": "75 x 3′",
    "A divided world. A unique journey.": "Um mundo dividido. Uma jornada única.",
    "A few minutes through ten years of animation.": (
        "Alguns minutos por dez anos de animação."
    ),
    "A full 2D pipeline, from the first idea to the final render.": (
        "Um pipeline 2D completo, da primeira ideia ao render final."
    ),
    "About": "Sobre",
    "Contact": "Contato",
    "Ads and branded": "Publicidade e branded",
    "Adult Swim · Animated episodes": "Adult Swim · Episódios animados",
    "Adventure | Fantasy | Drama": "Aventura | Fantasia | Drama",
    "All": "Todos",
    "Among the Stars": "Entre as Estrelas",
    "Animated episodes produced for the fifth season.": (
        "Episódios animados para a 5ª temporada."
    ),
    "Animated series, films, promos and branded content produced by Split Studio.": (
        "Séries, filmes, promos e branded content produzidos pela Split Studio."
    ),
    "Animated short": "Curta animado",
    "Animation & Games": "Animação e games",
    "Animation &amp; Games": "Animação e games",
    "Bardel · Animated episodes": "Bardel · Episódios animados",
    "Based on Affonso Solano's work": "Baseado na obra de Affonso Solano",
    "Bit Productions": "Bits Produções",
    "Bit Productions · Feature film": "Bits Produções · Longa-metragem",
    "Bits Produções · Feature film": "Bits Produções · Longa-metragem",
    "Branded series": "Série branded",
    "Brazil": "Brasil",
    "<span> | Brazil | São Paulo – SP &amp; Rio de Janeiro – RJ</span>": (
        "<span> | Brasil | São Paulo – SP &amp; Rio de Janeiro – RJ</span>"
    ),
    "<span> | USA | Dallas – TX</span>": "<span> | EUA | Dallas – TX</span>",
    "Bubu and the Little Owls": "Bubu e as Corujinhas",
    "Canal Futura · Original series": "Canal Futura · Série original",
    "Carousel indicator": "Indicador do carrossel",
    "Character Design & Backgrounds": "Design de personagens e cenários",
    "Character Design &amp; Backgrounds": "Design de personagens e cenários",
    "Characters": "Personagens",
    "Check out some episode synopses": "Confira algumas sinopses de episódios",
    "Childhood": "Infância",
    "Children of the World": "Crianças do Mundo",
    "Client": "Cliente",
    "Client productions": "Produções para clientes",
    "Co-produce with us": "Coproduza conosco",
    "Co-produce with us <i class=\"fa fa-long-arrow-right ms-2\"/>": (
        'Coproduza conosco <i class="fa fa-long-arrow-right ms-2"/>'
    ),
    "Come along with us": "Venha com a gente",
    "Comedy | Adventure | Travel": "Comédia | Aventura | Viagem",
    "Contact form": "Formulário de contato",
    "Created by": "Criação",
    "Creation & Development": "Criação e desenvolvimento",
    "Creation &amp; Development": "Criação e desenvolvimento",
    "Cut Out & Traditional Animation": "Animação cut out e tradicional",
    "Cut Out &amp; Traditional Animation": "Animação cut out e tradicional",
    "Discover the project": "Conheça o projeto",
    "Egregore": "Egrégora",
    "Ep 01 – Mamma Mia!": "Ep 01 – Mamma mia!",
    "Ep 02 – Ah, I'amour…": "Ep 02 – Ah, I'amour…",
    "Episode 01": "Episódio 01",
    "Episode 02": "Episódio 02",
    "Executive Producer & Animation Director": (
        "Produtor executivo e diretor de animação"
    ),
    "Executive Producer &amp; Animation Director": (
        "Produtor executivo e diretor de animação"
    ),
    "FX & Motion Animation": "FX e motion animation",
    "FX &amp; Motion Animation": "FX e motion animation",
    "Feature film": "Longa-metragem",
    "Feature films": "Longas",
    "Film Editing": "Edição de vídeo",
    "Fit UFC | True Myth": "Fit UFC | Mito de Verdade",
    "Format": "Formato",
    "Founder & CEO": "Fundador e CEO",
    "Founder &amp; CEO": "Fundador e CEO",
    "Founder, Director & Writer": "Fundador, diretor e roteirista",
    "Founder, Director &amp; Writer": "Fundador, diretor e roteirista",
    "Game": "Game",
    "Hello Kitty Supercute Adventures": "Hello Kitty Supercute Adventures",
    "Hello Kitty and Friends Supercute Adventures": (
        "Hello Kitty and Friends Supercute Adventures"
    ),
    "How Split Studio uses the information you send through the website.": (
        "Como a Split Studio usa as informações que você envia pelo site."
    ),
    "How Split uses the information you send us.": (
        "Como a Split usa as informações que você envia."
    ),
    "How long we keep it": "Por quanto tempo guardamos",
    "I agree to the": "Concordo com a",
    "IPs Creation": "Criação de IPs",
    "If there's 2D animation, Split can do it.": "Se tem animação, a Split faz.",
    "In development": "Em desenvolvimento",
    "Intellectual properties created and developed inside Split Studio.": (
        "Propriedades intelectuais criadas e desenvolvidas no Split Studio."
    ),
    "Intellectual properties created inside the studio.": (
        "Propriedades intelectuais criadas no estúdio."
    ),
    "Layout, Animation": "Layout, animação",
    "Loyal Companion": "Fiel companheira",
    "Mauricio de Sousa Produções · TV series": (
        "Mauricio de Sousa Produções · Série de TV"
    ),
    "Midas Productions · Music videos": "Midas Productions · Clipes musicais",
    "Miss & Grubs": "Miss & Grubs",
    "Miss &amp; Grubs": "Miss &amp; Grubs",
    "Monica and Friends": "Turma da Mônica",
    "More of our work lives on Vimeo and YouTube.": (
        "Tem mais trabalho no Vimeo e no YouTube."
    ),
    "Music videos for Sun Boy and Friends, with songs by Vitor Kley.": (
        "Clipes da Turma do Menino Sol, com as músicas de Vitor Kley."
    ),
    "New episodes on YouTube every Wednesday.": (
        "Episódios novos no YouTube toda quarta-feira."
    ),
    "Newsletter": "Newsletter",
    "Next": "Próximo",
    "Nick Jr. US · Series in development": (
        "Nick Jr. US · Série em desenvolvimento"
    ),
    "NuBoom · Promo": "NuBoom · Promo",
    "On the Trail of the Blue Butterflies": (
        "Na Trilha das Borboletas Azuis"
    ),
    "Original IP · Comedy series": "IP original · Série de comédia",
    "Original IP · Game": "IP original · Game",
    "Original IP · Music videos": "IP original · Clipes musicais",
    "Original IP · Preschool series": "IP original · Série preschool",
    "Original IP · Series": "IP original · Série",
    "Original IP · Series in development": (
        "IP original · Série em desenvolvimento"
    ),
    "Original IP · Short film": "IP original · Curta",
    "Original IP · Promo": "IP original · Promo",
    "Original animated short created and produced by Split.": (
        "Curta original criado e produzido pela Split."
    ),
    "Original comedy series created by Michele Massagli and produced inside Split.": (
        "Série de comédia original criada por Michele Massagli e produzida na Split."
    ),
    "Original intellectual properties": "Propriedades intelectuais originais",
    "Original series created inside Split, covering the full 2D pipeline.": (
        "Série original criada na Split, cobrindo o pipeline 2D completo."
    ),
    "Original series produced with Canal Futura, covering the full 2D pipeline.": (
        "Série original produzida com o Canal Futura, cobrindo o pipeline 2D completo."
    ),
    "Our Work": "Nossos trabalhos",
    "Palermo, Italy": "Palermo, Itália",
    "Paper Films · Feature film": "Paper Films · Longa-metragem",
    "Paris, France": "Paris, França",
    "Pilots and promos": "Pilotos e promos",
    "Post-Production": "Pós-produção",
    "Pre-Production": "Pré-produção",
    "Preschool series": "Série preschool",
    "Preschool series produced with Up Content, with Split on 2D animation.": (
        "Série preschool produzida com a Up Content, com a Split na animação 2D."
    ),
    "Previous": "Anterior",
    "Privacy": "Privacidade",
    "Produced by Split Studio": "Produzido pelo Split Studio",
    "Productions created and animated with channels, studios and brands.": (
        "Produções criadas e animadas com canais, estúdios e marcas."
    ),
    "Project Development": "Desenvolvimento de projetos",
    "Promo": "Promo",
    "Promo produced for NuBoom, with Split on layout and animation.": (
        "Promo produzido para a NuBoom, com a Split no layout e na animação."
    ),
    "Props, Backgrounds, Builds, 2D Animation, Composition": (
        "Props, cenários, builds, animação 2D, composição"
    ),
    "Questions:": "Dúvidas:",
    "Reel": "Reel",
    "Release year": "Ano de lançamento",
    "Rendering": "Rendering",
    "Run Away from Them!": "Fuja deles!",
    "Sanrio Brazil": "Sanrio Brasil",
    "Sanrio Brazil · Promo": "Sanrio Brasil · Promo",
    "Sanrio · Web series": "Sanrio · Websérie",
    "Scene Composition": "Composição de cena",
    "Script Writing": "Roteiro",
    "Season 5 episodes": "Episódios da 5ª temporada",
    'See them all <i class="fa fa-long-arrow-right ms-2"/>': (
        'Ver todos <i class="fa fa-long-arrow-right ms-2"/>'
    ),
    "Send": "Enviar",
    "Series promo on air.": "Tem promo da série no ar.",
    "Series, films, promos and branded content.": (
        "Séries, filmes, promos e branded content."
    ),
    "Services": "Serviços",
    "Setup & Rigging": "Setup e rigging",
    "Setup &amp; Rigging": "Setup e rigging",
    "Short film": "Curta-metragem",
    "Shows": "Séries",
    "Sign up for our newsletter": "Inscreva-se na newsletter",
    "Split Academy": "Split Academia",
    "Split Originals": "Originais Split",
    "Split Studio Reel": "Reel da Split Studio",
    "Split Studio characters": "Personagens da Split Studio",
    "Split Studio · Comedy series": "Split Studio · Série de comédia",
    "Split Studio · Game": "Split Studio · Game",
    "Split Studio · Series": "Split Studio · Série",
    "Split Studio · Series in development": (
        "Split Studio · Série em desenvolvimento"
    ),
    "Split Studio · Short film": "Split Studio · Curta",
    "Split brand character": "Personagem da marca Split",
    "Split original game in development, mixing 2D and 3D animation.": (
        "Game original da Split em desenvolvimento, misturando animação 2D e 3D."
    ),
    "Split original game. Help make this project a reality on Catarse.": (
        "Game original da Split. Ajude a tornar este projeto realidade no Catarse."
    ),
    "Split original — help make this game a reality at Catarse.": (
        "Ajude a transformar esse game em realidade no Catarse."
    ),
    "Split's animation school, built on more than ten years of studio practice.": (
        "A nova escola de animação da Split."
    ),
    "Staging & Blocking": "Staging e blocking",
    "Staging &amp; Blocking": "Staging e blocking",
    "Start a project": "Comece um projeto",
    'Start a project <i class="fa fa-long-arrow-right ms-2"/>': (
        'Comece um projeto <i class="fa fa-long-arrow-right ms-2"/>'
    ),
    "Status": "Status",
    "Stories we create, develop and produce ourselves.": (
        "Histórias que criamos, desenvolvemos e produzimos."
    ),
    "Storyboard & Animatic": "Storyboard e animatic",
    "Storyboard &amp; Animatic": "Storyboard e animatic",
    "Subscribe": "Assinar",
    "Sun Boy and Friends": "Turma do Menino Sol",
    "Support on Catarse": "Apoie no Catarse",
    "TV and YouTube channels, film companies, ad agencies and big corporations.": (
        "Canais de TV e YouTube, produtoras de filmes, agências e grandes empresas."
    ),
    "TV series & Digital Game": "Série de TV e jogo digital",
    "TV series &amp; Digital Game": "Série de TV e jogo digital",
    "Talk to us": "Fale conosco",
    "Teaser project released in CCXP19": "Teaser do projeto lançado na CCXP19",
    "Tell us about your project, your studio or the story you want to animate.": (
        "Conte sobre o seu projeto, o seu estúdio ou a história que você quer animar."
    ),
    "The Adventure": "Aventureira",
    "The Boy and the World": "O Menino e o Mundo",
    "The Charcoal Swordsman": "O Espadachim de Carvão",
    "The Charcoal Swordsman still": "Still de O Espadachim de Carvão",
    "The Mythological Giant": "Gigante mitológico",
    "The most watched Brazilian show on Cartoon Network.": (
        "Série brasileira mais assistida no Cartoon Network."
    ),
    "Tito and the Birds": "Tito e os Pássaros",
    "To Reach the Moon": "Para Chegar à Lua",
    "UFC · Branded series": "UFC · Série branded",
    "USA": "EUA",
    "Up Content · Preschool series": "Up Content · Série preschool",
    "Vimeo channel": "Canal no Vimeo",
    "Watch Split's Reel": "Assista ao reel da Split",
    "Watch the Split Studio showreel.": "Assista ao showreel da Split Studio.",
    "We are Split.<br/>We love telling stories.": (
        "Somos a Split.<br/>Adoramos contar histórias."
    ),
    "WeeBoom still": "Still do WeeBoom",
    "What Split does": "O que a Split faz",
    "What's Up, Bud?": "Qual é, Broto?",
    "Who leads the studio": "Quem lidera o estúdio",
    "Who we are and what Split Studio does.": (
        "Quem somos e o que a Split Studio faz."
    ),
    "Who we create with": "Com quem criamos",
    "Wonder Media · Animated series": "Wonder Media · Série animada",
    "YouTube channel": "Canal no YouTube",
    "Your name": "Seu nome",
    "privacy policy": "política de privacidade",
    "you@example.com": "voce@exemplo.com",
    "A 20 x 5 minute series produced with Wonder Media. The stories were designed to communicate through social causes, and Split handled the 2D pipeline from storyboard and character design through animation, editing and compositing.": (
        "Uma série de 20 x 5 minutos produzida com a Wonder Media. As histórias "
        "foram pensadas para comunicar a partir de causas, e a Split tocou o "
        "pipeline 2D do storyboard e do design de personagens até a animação, "
        "a edição e a composição."
    ),
    "A human of nearly 25 cycles. She is the captain of a ship she inherited from her deceased uncle and shelters Adapak at the beginning of his journey, helping him travel to the island of Caspama. A woman of strong personality, she uses it to disguise her own insecurities. Sirara is one of the only mortals to know Adapak's origin.": (
        "Uma humana de aproximadamente 25 ciclos de idade. Ela é capitã de um "
        "navio que herdou de seu falecido tio e abriga Adapak no início de sua "
        "jornada, ajudando-o a viajar até a ilha de Caspama. Uma mulher de "
        "personalidade forte, e usa isso para disfarçar suas próprias "
        "inseguranças. Sirara é uma das únicas mortais a saber a origem de Adapak."
    ),
    "A kind and altruistic youth with white eyes and dark skin. Adapak wanders the world of Kurgala, searching for a meaning to his own existence and unraveling the mysteries that The Four That Are One hide from mortals. He is a master of the Tibaul Circles, a martial art that lets him defend himself from multiple opponents at once. Despite being extremely cultured and skilled in combat, his innocence and inexperience in the mortal world involuntarily involve him in conflict.": (
        "Um jovem bondoso e altruísta, de olhos brancos e pele negra. Adapak "
        "vaga pelo mundo de Kurgala, em busca de um significado para sua "
        "própria existência e desvendando os mistérios que Os Quatro Que São "
        "Um escondem dos mortais. Adapak é um mestre dos Círculos Tibaul: arte "
        "marcial que o permite se defender de múltiplos oponentes "
        "simultaneamente. Apesar de extremamente culto e hábil em combate, a "
        "inocência e a inexperiência de Adapak perante o mundo dos mortais "
        "fazem com que ele se envolva de forma involuntária em conflitos."
    ),
    "A preschool series produced with Up Content. Split contributed 2D animation to the show that follows Bubu and his owl friends.": (
        "Série preschool produzida com a Up Content. A Split contribuiu com a "
        "animação 2D do programa que acompanha Bubu e seus amigos corujas."
    ),
    "A preschool short produced with Animact! for Nickelodeon's Animated Shorts Program. Henrique Lira created the series and Split produced it for Nick Jr. US.": (
        "Curta preschool produzido com a Animact! para o Nickelodeon Animated "
        "Shorts Program. Henrique Lira criou a série e a Split produziu para "
        "o Nick Jr. US."
    ),
    "A promo for Sanrio Brazil's Mr Men Little Miss. Split directed the piece and covered everything from storyboard and voices to animation, sound effects, songs and mix.": (
        "Promo de Mr Men Little Miss para a Sanrio Brasil. A Split dirigiu a "
        "peça e cobriu tudo, do storyboard e das vozes à animação, aos efeitos "
        "sonoros, às músicas e à mixagem."
    ),
    "A promo produced for NuBoom. Split handled layout and animation, turning a retro gaming pitch into a fast, readable piece.": (
        "Promo produzido para a NuBoom. A Split ficou com layout e animação, "
        "transformando um pitch de game retrô numa peça rápida e legível."
    ),
    "Ah, Paris, the city of love! Wee and Boom are looking for a Boomie in this très magnifique city, whose inhabitants seem to be more in love than usual. The contagious love will even hit Wee, who gets extremely in love with Boom. Now Boom will have to find a way to capture the Boomie so that Wee and the city return to normal.": (
        "Ah, Paris, a cidade do amor! Wee e Boom procuram por um Boomie nesta "
        "cidade très magnifique, cujos habitantes parecem estar mais… bem… "
        "apaixonados do que o normal. O contagiante amor (vulgo poder do "
        "Boomie) inclusive acerta Wee, que fica extremamente apaixonada por "
        "Boom. Agora Boom terá que dar um jeito de capturar o Boomie para que "
        "Wee e a cidade voltem ao normal."
    ),
    "Among the Stars is an original game created inside Split. The studio is developing the world, characters and animation in house and inviting the audience to help make the project a reality on Catarse.": (
        "Entre as Estrelas é um game original criado na Split. O estúdio "
        "desenvolve o mundo, os personagens e a animação internamente e "
        "convida o público a ajudar a tornar o projeto realidade no Catarse."
    ),
    "An animated short originally created by Camila Kamimura and Victor Canela and produced by Split with the support of the São Paulo government Culture Secretary through the Programa de Ação Cultural in 2013.": (
        "Curta originalmente criado por Camila Kamimura e Victor Canela e "
        "produzido pela Split com o apoio da Secretaria de Cultura do Governo "
        "do Estado de São Paulo, por meio do Programa de Ação Cultural em 2013."
    ),
    "An original animated short created inside Split. The studio covered the film from direction and script through animation and mix.": (
        "Curta original criado na Split. O estúdio cobriu o filme da direção "
        "e do roteiro até a animação e a mixagem."
    ),
    "An original animated short created inside Split. The studio covered the film from direction and script through animation, sound and mix.": (
        "Curta original criado na Split. O estúdio cobriu o filme da direção "
        "e do roteiro até a animação, o som e a mixagem."
    ),
    "An original comedy series created by Michele Massagli. Split covers the full 2D pipeline, from direction and script through voices, animation, sound and mix.": (
        "Série de comédia original criada por Michele Massagli. A Split cobre "
        "o pipeline 2D completo, da direção e do roteiro às vozes, à animação, "
        "ao som e à mixagem."
    ),
    "An original series created inside Split. The studio covers the full 2D pipeline, from direction and script through animation, sound and mix.": (
        "Série original criada na Split. O estúdio cobre o pipeline 2D "
        "completo, da direção e do roteiro à animação, ao som e à mixagem."
    ),
    "An original series produced with Canal Futura. Split directed the show and covered everything from script and voices to animation, sound and mix.": (
        "Série original produzida com o Canal Futura. A Split dirigiu o "
        "programa e cobriu tudo, do roteiro e das vozes à animação, ao som e "
        "à mixagem."
    ),
    "Animated episodes produced for the fifth season of Rick and Morty, one of the studio's international service titles.": (
        "Episódios animados da quinta temporada de Rick and Morty, um dos "
        "títulos internacionais de serviço do estúdio."
    ),
    "Animated music videos for Sun Boy and Friends, produced with Midas Productions and scored with Vitor Kley's songs. Split directed the pieces and carried them through the 2D pipeline.": (
        "Clipes animados da Turma do Menino Sol, produzidos com a Midas "
        "Productions e com as músicas de Vitor Kley. A Split dirigiu as peças "
        "e as levou pelo pipeline 2D."
    ),
    "Animated series produced with Wonder Media in 2021, part of the studio's slate of stories built around social causes.": (
        "Série animada produzida com a Wonder Media em 2021, parte do slate "
        "de histórias construídas em torno de causas."
    ),
    "Animated series produced with Wonder Media in 2022, directed in house and delivered through the full 2D pipeline.": (
        "Série animada produzida com a Wonder Media em 2022, dirigida em casa "
        "e entregue pelo pipeline 2D completo."
    ),
    "Animated series produced with Wonder Media, part of a slate of stories designed to communicate through social causes.": (
        "Série animada produzida com a Wonder Media, parte de um slate de "
        "histórias pensadas para comunicar a partir de causas."
    ),
    "Animated short created by Camila Kamimura and Victor Canela and produced by Split with support from the São Paulo government.": (
        "Curta criado por Camila Kamimura e Victor Canela e produzido pela "
        "Split com apoio do Governo de São Paulo."
    ),
    "Boom is silly, sweet and is also the guardian of all the sounds in the universe. Inside his body one will find a library of sounds, managed by the Boomies. Boom is always looking for fun, and despite his naivety and lack of attention, he is Wee's best friend and greatest ally.": (
        "Boom é bobo, doce e também é o guardião de todos os sons do universo. "
        "Dentro do seu corpo vive uma biblioteca de sons, cuidados por Boomies. "
        "Sempre em busca de diversão, e apesar de sua ingenuidade e falta de "
        "atenção, Boom é o melhor amigo e maior aliado de Wee."
    ),
    "Boomies are cute yellow creatures that live inside Boom, where they take care of all the sounds of the universe. They are now lost to the world and go crazy listening to music. When that happens, they use their magical powers to set wherever they are on chaos. Watch out!": (
        "Os Boomies são criaturas amarelas fofas que vivem dentro de Boom, onde "
        "cuidam de todos os sons do universo. No entanto, eles agora estão "
        "perdidos pelo mundo e enlouquecem ao ouvir música. Quando isso "
        "acontece, eles usam seus poderes mágicos para espalhar caos por onde "
        "estão. Cuidado!"
    ),
    "Branded series produced for UFC, mixing fight mythology with Split's 2D animation pipeline.": (
        "Série branded produzida para o UFC, misturando a mitologia da luta "
        "com o pipeline 2D da Split."
    ),
    "Branded shorts produced for UFC, mixing fight mythology with Split's 2D pipeline. The studio covered the show from direction and script through voices, animation, sound and mix.": (
        "Curtas branded produzidos para o UFC, misturando a mitologia da luta "
        "com o pipeline 2D da Split. O estúdio cobriu o programa da direção e "
        "do roteiro às vozes, à animação, ao som e à mixagem."
    ),
    "Children of the World gives players a poetic art direction filled with grace and bittersweet optimism, broadening the narrative of a film that travelled the festival circuit and reached an Academy Award nomination.": (
        "Crianças do Mundo oferece aos jogadores uma direção de arte poética, "
        "repleta de graça e um otimismo agridoce, ampliando a narrativa de um "
        "filme que percorreu o circuito de festivais e chegou a uma indicação "
        "ao Oscar."
    ),
    "Children of the World is a 2D adventure indie game displayed in a 3D world, with puzzle, platform, music and minigame elements.": (
        "Crianças do Mundo é um jogo de aventura 2D indie que se passa em um "
        "mundo 3D, com quebra-cabeças, plataformas, músicas e elementos de "
        "minijogos."
    ),
    "Cid is an Executive Producer and Animation Director with more than 15 years of experience across TV series, feature films, short films and other formats. At Split, he carries the production torch and leads the teams toward innovation, quality and top-notch delivery.": (
        "Cid é produtor executivo e diretor de animação com mais de 15 anos de "
        "experiência. Ao longo desse tempo, trabalhou em séries de TV, "
        "longas-metragens, curtas e outros formatos. Na Split, ele carrega a "
        "tocha da produção e lidera as equipes na busca de inovação, qualidade "
        "e entrega de alto nível."
    ),
    "Classic Monica and Friends episodes produced for Cartoon Network, one of the most watched Brazilian shows on the channel.": (
        "Episódios clássicos da Turma da Mônica produzidos para o Cartoon "
        "Network, uma das séries brasileiras mais assistidas no canal."
    ),
    "Classic Monica and Friends episodes produced for Cartoon Network: 52 x 7 minutes, from direction and script through the full 2D pipeline. The series is one of the most watched Brazilian shows on the channel.": (
        "Episódios clássicos da Turma da Mônica produzidos para o Cartoon "
        "Network: 52 x 7 minutos, da direção e do roteiro ao pipeline 2D "
        "completo. A série é uma das mais assistidas do Brasil no canal."
    ),
    "Creating and producing animated stories for some of the biggest brands in the world for more than 10 years": (
        "Há mais de 10 anos criamos e produzimos histórias para as maiores "
        "marcas do Brasil."
    ),
    "Crossmedia original pairing a TV series with a digital game, continuing the world of The Boy and the World.": (
        "Original transmídia que une série de TV e jogo digital, dando "
        "continuidade ao mundo de O Menino e o Mundo."
    ),
    "Direction, Script, Storyboard & Animatic, Character Design, Props, Backgrounds, Builds, 2D Animation, Editing, Composition": (
        "Direção, roteiro, storyboard e animatic, design de personagens, "
        "props, cenários, builds, animação 2D, edição, composição"
    ),
    "Direction, Script, Storyboard &amp; Animatic, Character Design, Props, Backgrounds, Builds, 2D Animation, Editing, Composition": (
        "Direção, roteiro, storyboard e animatic, design de personagens, "
        "props, cenários, builds, animação 2D, edição, composição"
    ),
    "Direction, Script, Storyboard & Animatic, Voices, Character Design, Props, Backgrounds, Builds, 2D Animation, Editing, Composition, Songs, Mix": (
        "Direção, roteiro, storyboard e animatic, vozes, design de "
        "personagens, props, cenários, builds, animação 2D, edição, "
        "composição, músicas, mixagem"
    ),
    "Direction, Script, Storyboard &amp; Animatic, Voices, Character Design, Props, Backgrounds, Builds, 2D Animation, Editing, Composition, Songs, Mix": (
        "Direção, roteiro, storyboard e animatic, vozes, design de "
        "personagens, props, cenários, builds, animação 2D, edição, "
        "composição, músicas, mixagem"
    ),
    "Direction, Script, Storyboard & Animatic, Voices, Character Design, Props, Backgrounds, Builds, 2D Animation, Editing, Composition, Sound FX, Songs, Mix": (
        "Direção, roteiro, storyboard e animatic, vozes, design de "
        "personagens, props, cenários, builds, animação 2D, edição, "
        "composição, efeitos sonoros, músicas, mixagem"
    ),
    "Direction, Script, Storyboard &amp; Animatic, Voices, Character Design, Props, Backgrounds, Builds, 2D Animation, Editing, Composition, Sound FX, Songs, Mix": (
        "Direção, roteiro, storyboard e animatic, vozes, design de "
        "personagens, props, cenários, builds, animação 2D, edição, "
        "composição, efeitos sonoros, músicas, mixagem"
    ),
    "Direction, Script, Storyboard & Animatic, Voices, Character Design, Props, Backgrounds, Builds, 2D Animation, Editing, Composition, Sound FX, Songs, Mix, 3D Animation": (
        "Direção, roteiro, storyboard e animatic, vozes, design de "
        "personagens, props, cenários, builds, animação 2D, edição, "
        "composição, efeitos sonoros, músicas, mixagem, animação 3D"
    ),
    "Direction, Script, Storyboard &amp; Animatic, Voices, Character Design, Props, Backgrounds, Builds, 2D Animation, Editing, Composition, Sound FX, Songs, Mix, 3D Animation": (
        "Direção, roteiro, storyboard e animatic, vozes, design de "
        "personagens, props, cenários, builds, animação 2D, edição, "
        "composição, efeitos sonoros, músicas, mixagem, animação 3D"
    ),
    "Direction, Storyboard & Animatic, Character Design, Props, Backgrounds, Builds, 2D Animation, Editing, Composition": (
        "Direção, storyboard e animatic, design de personagens, props, "
        "cenários, builds, animação 2D, edição, composição"
    ),
    "Direction, Storyboard &amp; Animatic, Character Design, Props, Backgrounds, Builds, 2D Animation, Editing, Composition": (
        "Direção, storyboard e animatic, design de personagens, props, "
        "cenários, builds, animação 2D, edição, composição"
    ),
    "Direction, Storyboard & Animatic, Character Design, Props, Backgrounds, Builds, 2D Animation, Editing, Composition, Sound FX, Songs, Mix": (
        "Direção, storyboard e animatic, design de personagens, props, "
        "cenários, builds, animação 2D, edição, composição, efeitos sonoros, "
        "músicas, mixagem"
    ),
    "Direction, Storyboard &amp; Animatic, Character Design, Props, Backgrounds, Builds, 2D Animation, Editing, Composition, Sound FX, Songs, Mix": (
        "Direção, storyboard e animatic, design de personagens, props, "
        "cenários, builds, animação 2D, edição, composição, efeitos sonoros, "
        "músicas, mixagem"
    ),
    "Direction, Storyboard & Animatic, Props, Backgrounds, Builds, 2D Animation, Editing, Composition": (
        "Direção, storyboard e animatic, props, cenários, builds, animação "
        "2D, edição, composição"
    ),
    "Direction, Storyboard &amp; Animatic, Props, Backgrounds, Builds, 2D Animation, Editing, Composition": (
        "Direção, storyboard e animatic, props, cenários, builds, animação "
        "2D, edição, composição"
    ),
    "Direction, Storyboard & Animatic, Voices, Props, Backgrounds, Builds, 2D Animation, Composition, Sound FX, Songs, Mix": (
        "Direção, storyboard e animatic, vozes, props, cenários, builds, "
        "animação 2D, composição, efeitos sonoros, músicas, mixagem"
    ),
    "Direction, Storyboard &amp; Animatic, Voices, Props, Backgrounds, Builds, 2D Animation, Composition, Sound FX, Songs, Mix": (
        "Direção, storyboard e animatic, vozes, props, cenários, builds, "
        "animação 2D, composição, efeitos sonoros, músicas, mixagem"
    ),
    "Feature film animation produced with Bits Produções. Split raised the quality of the conception, animation and art.": (
        "Longa animado produzido com a Bits Produções. A Split elevou a "
        "qualidade da concepção, da animação e da arte."
    ),
    "Feature film produced with Paper Films. Split contributed 2D animation to a film that travelled the festival circuit and reached an Academy Award nomination.": (
        "Longa produzido com a Paper Films. A Split contribuiu com a animação "
        "2D de um filme que percorreu o circuito de festivais e chegou a uma "
        "indicação ao Oscar."
    ),
    "Feature-length animation produced with Bit Productions. Split joined for storyboard, design, backgrounds, builds and 2D animation, raising the quality of the conception, animation and art that took Tito to festivals around the world.": (
        "Longa produzido com a Bits Produções. A Split entrou no storyboard, "
        "no design, nos cenários, nos builds e na animação 2D, elevando a "
        "qualidade da concepção, da animação e da arte que levou Tito aos "
        "festivais do mundo."
    ),
    "Guille is a producer, director, editor, screenwriter and animator, with a degree in Image and Sound from UFSCar. One of the founders of Split and its current CEO, he has produced dozens of films, series, games and comics, and created the studio's Games Center and special projects.": (
        "Guille é produtor, diretor, editor, roteirista e animador. Bacharel "
        "em Imagem e Som pela UFSCar, é um dos fundadores do Split Studio e "
        "atualmente seu CEO. Pela Split, produziu dezenas de filmes, séries, "
        "games e quadrinhos, e criou o Núcleo de Games e os projetos especiais."
    ),
    "Have you noticed that the character of our brand is splitting? It's because Split works daily to create and produce top-quality animation and games.": (
        "Já percebeu que a personagem da nossa marca está se dividindo? É "
        "porque a Split se desdobra todos os dias para criar e produzir "
        "animações e games de primeira qualidade."
    ),
    "Hmmm, I'm so hungry! Wee and Boom look for a Boomie in the city of Palermo, Italy, famous for its tarantella and pasta. A very hungry Wee and Boom stumble upon a restaurant whose boss seems to be crazy, turning the place and customers upside down. That smells like Boomie!": (
        "Hmmm, que fome! Wee e Boom procuram por um Boomie na cidade de "
        "Palermo, Itália, famosa por suas tarantelas e massas. Famintos, Wee "
        "e Boom dão de encontro com uma cantina cujo chefe parece estar "
        "malucão, deixando o lugar e os clientes de cabeça pra baixo. Isso "
        "cheira a Boomie!"
    ),
    "Howdy Harrdy is a preschool cartoon created by Henrique Lira and produced by Split Studio in partnership with Animact! for Nick Jr. US through the Nickelodeon Animated Shorts Program.": (
        "Howdy Harrdy é um cartoon preschool criado por Henrique Lira e "
        "produzido pelo Split Studio em parceria com a Animact! para o Nick "
        "Jr. US, pelo Nickelodeon Animated Shorts Program."
    ),
    "If you subscribe to the newsletter, we keep the e-mail address you gave us in order to send studio news. You can unsubscribe from any message.": (
        "Se você assina a newsletter, guardamos o e-mail informado para "
        "enviar as novidades do estúdio. Dá para cancelar a inscrição em "
        "qualquer mensagem."
    ),
    "In order to find <strong>a new path within this huge adventure that is storytelling through animation</strong>, Split cannot be one; it needs to be many. With each new journey, with each new partner, with each new initiative, our studio divides and multiplies. Each new version can fully understand the objectives of the content to deliver the best result. That is, Split will always find a way to fit perfectly into your project.": (
        "E, para encontrar <strong>todos os novos caminhos dentro dessa enorme "
        "aventura que é contar histórias animadas</strong>, a Split não pode "
        "ser uma, precisa ser várias. A cada nova jornada, a cada novo "
        "parceiro, a cada nova iniciativa, nosso estúdio se divide e se "
        "multiplica; e cada nova versão é capaz de entender direitinho os "
        "objetivos do conteúdo para entregar o melhor resultado. Ou seja: "
        "sempre vai ter uma Split que se encaixa perfeitamente no seu projeto."
    ),
    "Intellectual properties created inside the studio, from preschool series to games.": (
        "Propriedades intelectuais criadas no estúdio, de séries preschool a games."
    ),
    "It continues the world of The Boy and the World, the 2016 Academy Award-nominated animated feature, as a crossmedia proposal pairing a TV series with a digital game.": (
        "Dá continuidade ao mundo de O Menino e o Mundo, longa indicado ao "
        "Oscar em 2016, numa proposta transmídia que une série de TV e jogo "
        "digital."
    ),
    "Jonas is a director, producer, writer and animator, with a degree in Image and Sound from UFSCar and a fellowship at the National Film Board of Canada. He has always been involved with the creative side of Split and now produces the studio's international projects from the US office.": (
        "Jonas é diretor, produtor, escritor e animador, e um dos fundadores "
        "da Split. Formado em Imagem e Som pela UFSCar e com passagem pelo "
        "National Film Board of Canada, sempre esteve no lado criativo, "
        "dirigindo e escrevendo produções da Split. Hoje também produz os "
        "projetos internacionais no escritório dos EUA."
    ),
    "New episodes produced for the Hello Kitty Brazil, Mexico and Latin America channels, published on YouTube every Wednesday.": (
        "Novos episódios para os canais da Hello Kitty Brasil, México e "
        "Latinoamérica, publicados no YouTube toda quarta-feira."
    ),
    "Once upon a time, in a Dark Forest where no ray of light or love could get in, a perfect and tiny rodent lives alone in a perfect egg house, where everything works and fits perfectly. One day her power goes out, and Miss has to face the wild dangers of the darkness to find what she is looking for.": (
        "Era uma vez, numa Floresta Escura onde nenhum raio de luz ou de amor "
        "entrava, uma roedora perfeita e minúscula que vivia sozinha numa casa "
        "ovo, onde tudo funcionava e se encaixava perfeitamente. Um dia a "
        "energia acaba, e Miss precisa enfrentar os perigos selvagens da "
        "escuridão para encontrar o que procura."
    ),
    "Original adventure series based on Affonso Solano's work. The teaser was released at CCXP19.": (
        "Série de aventura original baseada na obra de Affonso Solano. O "
        "teaser foi lançado na CCXP19."
    ),
    "Original preschool series created inside the studio. The first season is available in multiple territories.": (
        "Série preschool original criada no estúdio. A primeira temporada "
        "está disponível em vários territórios."
    ),
    "Oscar-nominated feature film produced with Paper Films, with Split on 2D animation.": (
        "Longa indicado ao Oscar, produzido com a Paper Films, com a Split na "
        "animação 2D."
    ),
    "Preschool cartoon created by Henrique Lira for Nick Jr. US through the Nickelodeon Animated Shorts Program.": (
        "Cartoon preschool criado por Henrique Lira para o Nick Jr. US pelo "
        "Nickelodeon Animated Shorts Program."
    ),
    "Produced with Wonder Media in 2021, Are You Okay? uses animation to open a conversation about mental health. Split delivered props, backgrounds, builds, 2D animation and composition.": (
        "Produzida com a Wonder Media em 2021, Are You Okay? usa a animação "
        "para abrir uma conversa sobre saúde mental. A Split entregou props, "
        "cenários, builds, animação 2D e composição."
    ),
    "Productions created and animated for channels, studios, agencies and brands around the world.": (
        "Produções criadas e animadas para canais, estúdios, agências e marcas "
        "no mundo todo."
    ),
    "Productions, original IPs and studio news, straight to your inbox.": (
        "Produções, IPs originais e novidades do estúdio, direto no seu e-mail."
    ),
    "Promo produced for Sanrio Brazil, covering the full 2D pipeline from direction to mix.": (
        "Promo produzido para a Sanrio Brasil, cobrindo o pipeline 2D "
        "completo da direção à mixagem."
    ),
    "Season 1 available in Portuguese and Spanish, in multiple territories. Sample English episodes available.": (
        "1ª Temporada disponível em Português e Espanhol, em múltiplos "
        "territórios. Episódios em Inglês disponíveis para amostra."
    ),
    "Since 2009, we have been producing a world of animation. Not one, actually, but many. To be honest, entire universes! Today we create entertainment content for <strong>Cartoon Network, Cartoonito, Comedy Central, Canal Futura, Sanrio, Disney Jr., Instituto Ayrton Senna, Mauricio de Sousa Produções, Wonder Media, Midas Music</strong> and <strong>Future Channel</strong>, among others. We're constantly adapting our pipelines to deliver the best-animated story yet.": (
        "Desde 2009, nós produzimos um mundo de animação. Um não, vários. "
        "Universos inteiros. Hoje, criamos conteúdo de entretenimento para "
        "<strong>Cartoon Network, Cartoonito, Comedy Central, Canal Futura, "
        "Sanrio, Disney Jr., Instituto Ayrton Senna, Mauricio de Sousa "
        "Produções, Wonder Media, Midas Music</strong> e <strong>Canal "
        "Futura</strong>, entre outros, sempre adaptando nossos pipelines "
        "para entregar a melhor história animada."
    ),
    "Split directs and produces new episodes of Hello Kitty and Friends Supercute Adventures for Sanrio Brazil, covering the full 2D pipeline from storyboard to mix. Fresh episodes land on the Hello Kitty Brazil, Mexico and Latin America YouTube channels every Wednesday.": (
        "A Split dirige e produz novos episódios de Hello Kitty and Friends "
        "Supercute Adventures para a Sanrio Brasil, cobrindo o pipeline 2D "
        "completo do storyboard à mixagem. Episódios novos sobem nos canais "
        "da Hello Kitty Brasil, México e Latinoamérica no YouTube toda "
        "quarta-feira."
    ),
    "Split joined Bardel on season 5 of Rick and Morty, delivering 2D animation for one of Adult Swim's flagship comedies. The episodes sit in the studio's international service slate, next to other long-running series produced for US networks.": (
        "A Split entrou com a Bardel na 5ª temporada de Rick and Morty, "
        "entregando animação 2D para uma das principais comédias do Adult "
        "Swim. Os episódios fazem parte do slate internacional de serviço do "
        "estúdio, ao lado de outras séries longas para redes dos EUA."
    ),
    "Storyboard & Animatic, Character Design, Props, Backgrounds, Builds, 2D Animation": (
        "Storyboard e animatic, design de personagens, props, cenários, "
        "builds, animação 2D"
    ),
    "Storyboard &amp; Animatic, Character Design, Props, Backgrounds, Builds, 2D Animation": (
        "Storyboard e animatic, design de personagens, props, cenários, "
        "builds, animação 2D"
    ),
    "Storyboard & Animatic, Character Designs, Props, Backgrounds, Builds, 2D Animation, Editing, Compositing": (
        "Storyboard e animatic, design de personagens, props, cenários, "
        "builds, animação 2D, edição, composição"
    ),
    "Storyboard &amp; Animatic, Character Designs, Props, Backgrounds, Builds, 2D Animation, Editing, Compositing": (
        "Storyboard e animatic, design de personagens, props, cenários, "
        "builds, animação 2D, edição, composição"
    ),
    "TV & YouTube channels, film companies, ad agencies and big corporations.": (
        "Canais de TV e YouTube, produtoras de filmes, agências e grandes empresas."
    ),
    "TV &amp; YouTube channels, film companies, ad agencies and big corporations.": (
        "Canais de TV e YouTube, produtoras de filmes, agências e grandes empresas."
    ),
    "The game tells a universal and contemporary story, which could be the story of many children from different nationalities.": (
        "O jogo conta uma história universal e contemporânea, que pode ser a "
        "história de muitas crianças de nacionalidades diferentes."
    ),
    "The second series Split produced with Wonder Media, this time with the studio also on direction. The team carried the show from storyboard and animatic through animation, editing and composition.": (
        "A segunda série que a Split produziu com a Wonder Media, desta vez "
        "também na direção. O time levou o programa do storyboard e do "
        "animatic à animação, à edição e à composição."
    ),
    "Therefore, <strong>if there is animation, Split has the solution.</strong> From branded content to feature films, TV shows to streaming mini-series, web series to games, promos, commercials and music videos, we'll be there for you every step of the way.": (
        "É por isso que, <strong>se tem animação, a Split tem solução.</strong> "
        "De branded content a longas-metragens, de séries de TV a minisséries "
        "de streaming, de webséries a games, passando por promos, comerciais "
        "e clipes musicais, a gente está com você em cada etapa."
    ),
    "WEE is an adventurous, smart and strong-willed rabbit. BOOM is a goofy mythical creature full of special powers. Together, they travel through cities around the world in search of capturing the BOOMIES, fun little magical creatures that are spreading chaos everywhere!": (
        "WEEBOOM é uma série de humor em animação 2D para crianças de 4 a 7 "
        "anos sobre dois amigos – WEE, uma coelha aventureira, esperta e de "
        "gênio forte, e BOOM, uma criatura mítica e abobalhada cheia de "
        "poderes especiais. Juntos eles viajam, por cidades do mundo em busca "
        "de capturar os BOOMIES, divertidas criaturinhas mágicas que, ao "
        "ouvirem música, ficam louquinhas e espalham caos em todo lugar!"
    ),
    "We keep contact and newsletter records for as long as we need them to answer you or run the list, and we do not sell that data.": (
        "Guardamos os registros de contato e da newsletter pelo tempo "
        "necessário para responder ou manter a lista, e não vendemos esses dados."
    ),
    "Wee and Boom are two friends who travel the world to capture some fun and magical creatures, the Boomies.": (
        "Wee e Boom são dois amigos que viajam o mundo em busca de capturar "
        "criaturinhas mágicas e divertidas, os Boomies."
    ),
    "Wee lives for adventures. In one of them, she accidentally woke Boom from centuries of slumber. By doing so, she also accidentally brought the Boomies into the world. Now they are lost and out there. Wee is a caring, athletic and competitive friend, and capturing Boomies has become her mission.": (
        "Wee vive pra aventuras, e em uma delas acidentalmente acordou Boom de "
        "seus séculos de sono. Ela também acidentalmente trouxe Boomies pro "
        "mundo. Agora eles estão perdidos e aprontando por aí. Wee é uma amiga "
        "carinhosa, atlética e competitiva, e capturar Boomies tornou-se sua "
        "grande missão."
    ),
    "Welcome to a world divided between the wild and the civilized, the mundane and the sacred, where forests and deserts hide ruins of once-forgotten gods and the seas shelter monsters capable of swallowing ships; where bone blades keep the law in cities of rock and wood, and a plurality of species must live together — in harmony or not.": (
        "Bem-vindo a um mundo dividido entre o selvagem e o civilizado, o "
        "mundano e o sagrado, onde as florestas e desertos escondem ruínas "
        "esquecidas pelos deuses de outrora e os mares abrigam monstros "
        "capazes de engolir navios; onde lâminas de osso mantêm a lei em "
        "cidades de rocha e madeira e a pluralidade de espécies é obrigada a "
        "conviver junta – em harmonia ou não."
    ),
    "When you write to us through the website, we store your name, e-mail, company, phone, the subject of the message, your field of work and portfolio link, and the message itself. That information becomes a lead in our studio CRM so the right person can reply.": (
        "Quando você escreve pelo site, guardamos nome, e-mail, empresa, "
        "telefone, o assunto da mensagem, a área de atuação, o link do "
        "portfólio e a mensagem. Essas informações viram um lead no CRM do "
        "estúdio para a pessoa certa responder."
    ),
    "Wizavior is an original game created inside Split. The studio is developing the world, characters and animation in house, mixing the 2D pipeline with 3D animation.": (
        "Wizavior é um game original criado na Split. O estúdio desenvolve o "
        "mundo, os personagens e a animação internamente, misturando o "
        "pipeline 2D com animação 3D."
    ),
    "“For us at Cartoon Network, working with Split is a real gift. It's the guarantee of excellent creative and technical quality, within the agreed deadline. After so many projects, Split is like an extension of our internal team.”": (
        "“Para nós do Cartoon Network, trabalhar com a Split é um verdadeiro "
        "presente. A garantia de excelente qualidade criativa e técnica, "
        "dentro do prazo acordado, passando pelos processos com muito amor. "
        "Depois de tantos projetos, a Split é como uma extensão do nosso time "
        "interno.”"
    ),
    "“For us at Sanrio Brazil it is a pleasure to work with Split in the development of our content for our Hello Kitty Brazil, Mexico and Latin America channels. All the projects have greatly met our expectations.”": (
        "“Para nós da Sanrio Brasil é um prazer trabalhar com a Split no "
        "desenvolvimento de nossos conteúdos para os canais da Hello Kitty "
        "Brasil, México e Latinoamérica. Os projetos desenvolvidos até o "
        "momento atenderam muito às nossas expectativas.”"
    ),
    "“I have had the joy and the privilege of working with the talent, quality and commitment of the Split team since the production of Sítio do Picapau Amarelo. Long live Split.”": (
        "“Tenho a alegria (e o privilégio!) de trabalhar e conviver com o "
        "talento, a qualidade e o comprometimento da equipe da Split desde a "
        "produção de Sítio do Picapau Amarelo. Viva a Split.”"
    ),
    "“My relationship with Split is intertwined with my start in animation. Since then, I've been more and more attracted by Split's enormous capacity to invest affection in all projects.”": (
        "“Meu relacionamento com a Split se confunde com meu começo na "
        "animação. Desde lá, fico cada vez mais atraído pela enorme "
        "capacidade da Split de investir carinho em todos os projetos.”"
    ),
    "“Split Studio has become an MSP extension, where the relationship between both teams goes beyond the partnership in projects, becoming a friendship relationship. We've always been able to count on their high production capacity, agility and fidelity to our ideology.”": (
        "“A Split é um estúdio que se tornou uma extensão da MSP, onde a "
        "relação entre as equipes vai além da parceria nos projetos e chega "
        "a uma relação de amizade. Sempre pudemos contar com alta capacidade "
        "de produção, agilidade e fidelidade na nossa ideologia.”"
    ),
    "“Split managed to greatly improve the quality of the project, both in terms of conception, animation and art. Without Split, we would never have gotten where we are with Tito and the Birds.”": (
        "“A Split conseguiu elevar muito a qualidade do projeto, tanto na "
        "concepção, quanto na animação e na arte. Sem a Split, nunca "
        "teríamos chegado onde chegamos com o Tito e os Pássaros.”"
    ),
    "“The work coming out of Split Studio is exceptional, and the entire team is extremely competent and super talented. Every project we have collaborated on with them has been easy and seamless.”": (
        "“O trabalho do Split Studio é excepcional, e o time todo é "
        "extremamente competente e super talentoso. Todo projeto em que nós "
        "trabalhamos juntos foi tranquilo e sem dificuldades.”"
    ),
    "“We are with Split in projects designed to communicate based on social causes. The studio and its team always surprise us, for the quality of what they do, and for living in the team's practice the diversity and mutual respect that we want to see on all screens.”": (
        "“Estamos com a Split em projetos que pensam a comunicação a partir "
        "de causas. O estúdio e sua equipe sempre nos surpreendem, pela "
        "qualidade do que realizam, e por viverem na prática da equipe a "
        "diversidade e o respeito mútuo que queremos ver em todas as telas.”"
    ),
    "“We were right in looking for Split to contribute to the production of the Rádio Bita show. We are very happy with the care, result and way of conducting the work by their team. At Split we found great partners and friends.”": (
        "“Acertamos em procurar a Split para contribuir na produção da série "
        "Rádio Bita. Ficamos muito felizes com o cuidado, o resultado e a "
        "forma de condução do trabalho pela equipe. Na Split encontramos "
        "ótimos parceiros e amigos.”"
    ),
    "“Working with Split on the development of the Senninha na Pista Maluca second season was a wonderful experience. A very committed, professional, flexible, creative and partner team. They're A+.”": (
        "“Trabalhar com a Split no desenvolvimento da segunda temporada do "
        "Senninha na Pista Maluca foi uma experiência maravilhosa. Uma equipe "
        "muito comprometida, profissional, flexível, criativa e parceira. "
        "Nota 10!”"
    ),
    "<strong>Come along and enjoy this journey with us.</strong>": (
        "<strong>Vem curtir essa jornada com a gente.</strong>"
    ),
}

IDENTITY = {
    "Adapak",
    "Adriana Alcântara",
    "Are You Okay?",
    "Bardel",
    "Bianca Senna",
    "Bit Wars",
    "Boom",
    "Boomerang",
    "Boomies",
    "Bruno Honda",
    "Camila Kamimura and Victor Canela",
    "Canal Futura",
    "Cartoon Network",
    "Cartoonito",
    "Cid Makino",
    "Comedy Central",
    "Disney Jr.",
    "Egrégora",
    "Felipe Almeida",
    "Globo",
    "Gloobinho",
    "Guille Hiertz",
    "Gullane",
    "Gustav Steinberg",
    "Henrique Lira",
    "Howdy Harrdy",
    "Instituto Ayrton Senna",
    "Is Anybody Out There?",
    "Jonas Brandão",
    "João Alegria",
    "Mauricio de Sousa",
    "Mauricio de Sousa Produções",
    "Michele Massagli",
    "Midas Productions",
    "Mixer Films",
    "Mr Men Little Miss",
    "Mr Plot",
    "My Life Is Worth Living",
    "Nick Jr. US",
    "Nickelodeon",
    "NuBoom",
    "Paper Films",
    "Paranoid",
    "Que Corpo é Esse?",
    "Record",
    "Renata Pereto",
    "René Veilleux",
    "Reynaldo Marchesini",
    "Rick and Morty",
    "Riot Games",
    "Sanrio",
    "Sirara",
    "Split Studio",
    "Split Studio Newsletter",
    "UFC",
    "Unicef",
    "Up Content",
    "Vimeo",
    "Website",
    "Wee",
    "WeeBoom",
    "Wizavior",
    "Wonder Media",
    "Canal Nostalgia",
    "FalaíDearo",
    "Karmatique",
    "Kids Glove",
    "Teatro Iguatemi",
    "Lala Produções",
    "Tortuga Studios",
    "DC Fandome",
    "Heart of Darkness",
    "Hello Kitty Chef Star",
    "Hello Kitty Fun",
    "Studio R",
    "Zolkin",
    "Zis",
    "Balacobaco",
    "Lala",
    "Getty Images",
    "Parmalat",
    "SESC",
    "1 FM",
    "Elma Chips",
    "Pernambucanas",
    "O Globo",
    "Cabrito & Chewy",
    "League of Legends | Project n.5",
    "Parmalat | Manifesto",
    "Getty Images | From Love to Bingo",
    "Hélio Ziskind",
    "Luan Santana",
    "Rede Globo",
    "TV Escola",
    "Cabrito & Chewy",
    "YouTube",
    "@splitstudiobr",
    "contato@splitstudio.tv",
    "vimeo.com/splitstudio",
}

HTML_REPLACEMENTS = (
    (">Select the subject<", ">Selecione o assunto<"),
    (">Select your field of work<", ">Selecione o campo de atuação<"),
    (">Link to portfolio<", ">Link para portfólio<"),
    (">Sales Team<", ">Equipe comercial<"),
    (">Field of work<", ">Área de atuação<"),
    (">Script Writing<", ">Roteiro<"),
    (">Work with Split<", ">Trabalhe na Split<"),
    (">Illustration<", ">Ilustração<"),
    (">Animation<", ">Animação<"),
    (">Production<", ">Produção<"),
    (">Storyboard<", ">Storyboard<"),
    (">Bids<", ">Orçamento<"),
    (">Press<", ">Imprensa<"),
    (">Other<", ">Outro<"),
    (">Company<", ">Empresa<"),
    (">E-mail<", ">E-mail<"),
    (">Message<", ">Mensagem<"),
    (">Medium<", ">Mídia<"),
    (">Phone<", ">Telefone<"),
    (">Name<", ">Nome<"),
    (">Next<", ">Próximo<"),
    (">Previous<", ">Anterior<"),
    (" | Brazil | ", " | Brasil | "),
    (" | USA | ", " | EUA | "),
    (">Sanrio Brazil<", ">Sanrio Brasil<"),
    (">Bit Productions<", ">Bits Produções<"),
    (">Verite Entertainment<", ">Verité Entertainment<"),
)


SERVICE_TOKENS = {
    "Direction": "Direção",
    "Script": "Roteiro",
    "Storyboard & Animatic": "Storyboard & Animatic",
    "Storyboard &amp; Animatic": "Storyboard &amp; Animatic",
    "Voices": "Vozes",
    "Character Design": "Design de personagens",
    "Character Designs": "Design de personagens",
    "Props": "Props",
    "Backgrounds": "Cenários",
    "Builds": "Rigs",
    "2D Animation": "Animação 2D",
    "Editing": "Edição",
    "Composition": "Composição",
    "Compositing": "Composição",
    "Sound FX": "Efeitos sonoros",
    "Songs": "Músicas",
    "Mix": "Mixagem",
}


def translate_services(msgid: str) -> str | None:
    if (
        "2D Animation" not in msgid
        and "Storyboard" not in msgid
        and "Editing" not in msgid
    ):
        return None
    if msgid.startswith("A ") or msgid.startswith("An ") or msgid.startswith("Branded"):
        return None
    parts = [part.strip() for part in msgid.split(",")]
    if len(parts) < 2:
        return None
    translated = [SERVICE_TOKENS.get(part, part) for part in parts]
    if translated == parts:
        return None
    return ", ".join(translated)


def translate_html(msgid: str) -> str | None:
    if "<" not in msgid:
        return None
    result = msgid
    changed = False
    for source, target in HTML_REPLACEMENTS:
        if source in result:
            result = result.replace(source, target)
            changed = True
    return result if changed else None


def translate(msgid: str, existing: dict[str, str]) -> str:
    if msgid in existing and existing[msgid]:
        return existing[msgid]
    key = normalize(msgid)
    if key in existing and existing[key]:
        return existing[key]
    if key in TRANSLATIONS:
        return TRANSLATIONS[key]
    if key in IDENTITY:
        return msgid
    html = translate_html(msgid)
    if html:
        return html
    services = translate_services(key)
    if services:
        return services
    # Keep phone, address and empty-option markup as-is.
    if msgid.startswith("<i class=") or msgid.startswith("<span class="):
        return msgid
    return ""


def main() -> int:
    export = Path(sys.argv[1]) if len(sys.argv) > 1 else LOCAL_EXPORT
    if not export.exists() and DEFAULT_EXPORT.exists():
        export = DEFAULT_EXPORT
    if not export.exists():
        raise SystemExit(f"Exported POT not found: {export}")

    exported = parse_po(export)
    existing_entries = parse_po(I18N_DIR / "pt_BR.po")
    existing = {}
    for entry in existing_entries:
        if entry["msgid"] and entry["msgstr"]:
            existing[entry["msgid"]] = entry["msgstr"]
            existing[normalize(entry["msgid"])] = entry["msgstr"]

    missing = []
    for entry in exported:
        if not entry["msgid"]:
            continue
        entry["comments"] = expand_copied_view_comments(entry["comments"])
        entry["msgstr"] = translate(entry["msgid"], existing)
        if not entry["msgstr"]:
            missing.append(normalize(entry["msgid"])[:160])

    write_po(I18N_DIR / "split_website.pot", exported, pot=True)
    write_po(I18N_DIR / "pt_BR.po", exported, pot=False)
    print(f"Wrote {len(exported) - 1} terms")
    if missing:
        print(f"UNTRANSLATED ({len(missing)}):")
        for item in missing:
            print(f" - {item}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
