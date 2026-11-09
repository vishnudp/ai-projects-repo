from pathlib import Path

from moviepy import *

from moviepy.video.fx.CrossFadeIn import CrossFadeIn
from moviepy.video.fx.Resize import Resize

from services.subtitle_generator import (
    build_word_subtitles
)

from services.subtitle_styler import (
    create_subtitle
)

from services.motion_graphics import (
    create_kinetic_title,
    create_progress_bar
)

from services.music_selector import (
    load_background_music
)

from services.broll_engine import (
    create_broll_clip
)

from services.cover_generator import (
    create_cover_clip
)

from services.social_overlay import (
    create_social_overlay
)

from services.cta_generator import (
    create_cta_clip
)

from services.intro import (
    create_intro
)

from services.course_broll_engine import (
    create_course_clip
)

from services.ui.title_block import *
from services.ui.purpose_block import *
from services.ui.key_idea_card import *
from services.ui.number_card import *
from services.ui.insight_card import *
from services.ui.quote_card import *
from services.ui.outcome_card import *
from services.ui.footer_bar import *
from services.ui.bottom_gradient import *
from services.ui.card_helper import create_card

def fit_background(clip):

    TARGET_W = 1080
    TARGET_H = 1920

    scale = min(
        TARGET_W / clip.w,
        TARGET_H / clip.h
    )

    foreground = clip.resized(scale)

    blurred_bg = (
        clip
        .resized(height=1920)
        .with_opacity(0.35)
    )

    return CompositeVideoClip(
        [
            blurred_bg.with_position(
                ("center","center")
            ),
            foreground.with_position(
                ("center","center")
            )
        ],
        size=(1080,1920)
    )

def create_rating_overlay(score, duration):

    assets = Path(
        "generated/assets/icons"
    )

    # badge_bg = (

    #     ColorClip(
    #         size=(180,100),
    #         color=(15,15,15)
    #     )

    #     .with_opacity(0.8)

    #     .with_duration(duration)

    #     .with_position((20,30))

    # )

    badge_bg = create_card(
        width=180,
        height=100,
        color=(15,15,15),
        radius=25,
        duration=duration,
        border_color=(0,0,0,255),
        border_width=3
    ).with_opacity(0.8).with_position((20,30))

    star = (

        ImageClip(
            str(assets / "star.png")
        )

        .resized(height=45)

        .with_duration(duration)

        .with_position((40,60))

    )

    score_txt = (

        TextClip(
            text=str(score),
            font_size=48,
            color="white",
            stroke_color="black",
            stroke_width=2,
            size=(90, 60),     # important
        )

        .with_duration(duration)

        .with_position((90,40))

    )

    return [

        badge_bg,

        star,

        score_txt

    ]




def render_reel(
    scenes,
    output_path
):

    clips = []

    intro = create_intro()

    # ---------------------------------
    # COVER SCREEN
    # ---------------------------------

   
    # score_clip = TextClip(
    #     text=f"Score {score}",
    #     font_size=50,
    #     color="#E50914"
    # ).with_position(
    #     ("center",1500)
    # ).with_duration(2)

    cover = CompositeVideoClip(
        [
            create_cover_clip(
                scenes[0]["title"]
            )
        ],
        size=(1080,1920)
    )

    clips.append(
        intro
    )

    clips.append(
        cover
    )

    # ---------------------------------
    # THUMBNAIL
    # ---------------------------------

    thumbnails_dir = Path(
        "generated/thumbnails"
    )

    thumbnails_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    thumbnail_path = (
        thumbnails_dir
        /
        (
            Path(output_path).stem
            + ".png"
        )
    )

    cover.save_frame(
        str(thumbnail_path),
        t=0
    )

    print(
        f"Thumbnail saved: {thumbnail_path}"
    )

    # ---------------------------------
    # SCENES
    # ---------------------------------

    for scene in scenes:

        narration = AudioFileClip(
            scene["audio_path"]
        )

        print(
            "\nRENDERING:",
            scene["title"]
        )

        print(
            "Purpose:",
            scene.get(
                "purpose"
            )
        )

        print(
            "Key Ideas:",
            scene.get(
                "key_ideas"
            )
        )

        print(
            "Numbers:",
            scene.get(
                "important_numbers"
            )
        )

        print(
            "Insights:",
            scene.get(
                "key_insights"
            )
        )

        print(
            "Quotes:",
            scene.get(
                "important_quotes"
            )
        )

        print(
            "Learning Outcome:",
            scene.get(
                "learning_outcome"
            )
        )

        duration = narration.duration

        rating_overlay = create_rating_overlay(
            scene["rating"],
            duration
        )

        # ---------------------------------
        # BROLL / IMAGE
        # ---------------------------------

        background = create_course_clip(
            scene,
            duration
        )

        if not background:

            background = create_broll_clip(
                scene,
                duration
            )

        if background:

            background = background.with_duration(
                duration
            )

        else:

            background = (
                ImageClip(
                    scene["image_path"]
                )
                .with_duration(duration)
            )

        # ---------------------------------
        # BLURRED FULLSCREEN BACKGROUND
        # ---------------------------------

        blur_bg = (
            background
            .resized(height=1920)
        )

        # if width still smaller than screen
        if blur_bg.w < 1080:

            blur_bg = blur_bg.resized(width=1080)

        blur_bg = blur_bg.with_position(
            ("center", "center")
        )

        # ---------------------------------
        # TITLE
        # ---------------------------------

        title_clip = create_kinetic_title(
            scene["title"],
            duration
        )

        # purpose_clip = TextClip(
        #     text=scene.get(
        #         "purpose",
        #         ""
        #     ),
        #     font_size=32,
        #     color="#FFD700",
        #     method="caption",
        #     size=(900, None)
        # ).with_position(
        #     ("center", 260)
        # ).with_duration(
        #     duration
        # )

        
        social_overlay = create_social_overlay(
            duration
        )

        # ---------------------------------
        # SUBTITLES
        # ---------------------------------

        subtitles = build_word_subtitles(
            scene["voiceover"],
            duration
        )

        subtitle_clips = []

        for subtitle in subtitles:

            subtitle_clips.append(

                create_subtitle(
                    subtitle["text"],
                    subtitle["start"],
                    subtitle["end"]
                )

            )

        # ---------------------------------
        # PROGRESS BAR
        # ---------------------------------

        progress_bar = create_progress_bar(
            duration
        )

        # ---------------------------------
        # SCENE COMPOSITE
        # ---------------------------------
        dark_overlay = (

            ColorClip(
                size=(1080,1920),
                color=(0,0,0)
            )

            .with_opacity(0.28)

            .with_duration(duration)

        )

        content_panel = (

            ColorClip(
                size=(1000, 750),
                color=(0,0,0)
            )

            .with_opacity(0.65)

            .with_duration(duration)

            .with_position(
                (
                    40,
                    950
                )
            )

        )

        purpose_clip = TextClip(

            text=scene.get(
                "purpose",
                ""
            ),

            font_size=38,

            color="#FFD700",

            method="caption",

            size=(920, None)

        ).with_duration(duration)

        purpose_clip = purpose_clip.with_position(
            (
                80,
                980
            )
        )

        title_block = create_title_block(
            scene["title"],
            duration
        )

        purpose_block = create_purpose_block(
            scene["purpose"],
            duration
        )

        idea_card = create_key_idea_card(
            scene["key_ideas"],
            duration
        )

        number_card = create_number_card(
            str(scene["important_numbers"]),
            duration
        )

        insight_card = create_insight_card(
            scene["key_insights"],
            duration
        )

        quote_card = create_quote_card(
            scene["important_quotes"],
            duration
        )

        outcome_card = create_outcome_card(
            scene["learning_outcome"],
            duration
        )

        footer_bar = create_footer_bar(
           scene["search_keywords"],
            duration
            
        )

        bottom_gradient = create_bottom_gradient(
            duration
        )

        ui_clips = [
            title_block,
            purpose_block,
            idea_card,
            number_card,
            insight_card,
            quote_card,
            outcome_card,
            footer_bar
        ]

        content_bg = (
            ColorClip(
                size=(1080, 1020),
                color=(0,0,0)
            )
            .with_duration(duration)
            .with_position((0,900))
        )

        for clip in ui_clips:

            print(
                type(clip).__name__,
                clip.duration
            )

        scene_clip = (

            CompositeVideoClip(

                [
                    content_bg,
                    background,
                    dark_overlay,
                    # bottom_gradient,
                    *rating_overlay,                  

                    title_block,
                    purpose_block,
                    idea_card,
                    number_card,
                    insight_card,
                    quote_card,
                    outcome_card,
                    
                    footer_bar,
                    *subtitle_clips,

                    progress_bar,

                    social_overlay,

                    
                ],

                size=(1080, 1920)

            )

            .with_audio(
                narration
            )

        )

        clips.append(
            scene_clip
        )

    

    # ---------------------------------
    # CTA END SCREEN
    # ---------------------------------

    cta_clip = create_cta_clip()

    clips.append(
        cta_clip
    )

    # ---------------------------------
    # CROSSFADE
    # ---------------------------------

    processed = []

    for idx, clip in enumerate(
        clips
    ):

        if idx > 0:

            clip = clip.with_effects([
                CrossFadeIn(0.5)
            ])

        processed.append(
            clip
        )

    final = concatenate_videoclips(
        processed,
        method="compose",
        padding=-0.4
    )

    # ---------------------------------
    # BACKGROUND MUSIC
    # ---------------------------------

    try:

        bg_music = (
            load_background_music()
            .subclipped(
                0,
                final.duration
            )
            .with_volume_scaled(
                0.10
            )
        )

        final_audio = CompositeAudioClip(
            [
                final.audio,
                bg_music
            ]
        )

        final = final.with_audio(
            final_audio
        )

    except Exception as e:

        print(
            "Music skipped:",
            e
        )

    # ---------------------------------
    # EXPORT
    # ---------------------------------

    final.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        threads=4
    )

    return {

        "video": output_path,

        "thumbnail": str(
            thumbnail_path
        )

    }