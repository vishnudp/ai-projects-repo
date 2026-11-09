# services/image_prompt_builder.py

def build_image_prompt(scene):

    visual = scene["visual"]

    return f"""
Netflix documentary style.

{visual}

Ultra realistic.
4K.
Cinematic lighting.
Volumetric light.
Professional photography.
Shallow depth of field.
Highly detailed.
Movie still.
"""