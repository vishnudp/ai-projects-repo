import cv2
import os


def add_score_overlay(
    image_path,
    score
):

    img = cv2.imread(
        image_path
    )

    if img is None:

        return image_path

    # -------------------------
    # Star Icon
    # -------------------------

    star_path = (
        "generated/assets/icons/star.png"
    )

    if os.path.exists(
        star_path
    ):

        star = cv2.imread(
            star_path,
            cv2.IMREAD_UNCHANGED
        )

        if star is not None:

            star = cv2.resize(
                star,
                (70, 70)
            )

            y1 = 50
            y2 = y1 + 70

            x1 = 50
            x2 = x1 + 70

            if star.shape[2] == 4:

                alpha = (
                    star[:, :, 3] / 255.0
                )

                for c in range(3):

                    img[
                        y1:y2,
                        x1:x2,
                        c
                    ] = (

                        alpha
                        * star[:, :, c]

                        +

                        (
                            1 - alpha
                        )
                        * img[
                            y1:y2,
                            x1:x2,
                            c
                        ]

                    )

            else:

                img[
                    y1:y2,
                    x1:x2
                ] = star[:, :, :3]

    # -------------------------
    # Score Box
    # -------------------------

    cv2.rectangle(

        img,

        (130, 40),

        (300, 120),

        (0, 0, 0),

        -1

    )

    cv2.putText(

        img,

        str(score),

        (145, 98),

        cv2.FONT_HERSHEY_DUPLEX,

        1.8,

        (255, 255, 255),

        3,

        cv2.LINE_AA

    )

    # -------------------------
    # Save
    # -------------------------

    cv2.imwrite(
        image_path,
        img
    )

    return image_path