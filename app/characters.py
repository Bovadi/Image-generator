# Character registry: maps character_id to LoRA config and visual profile.
# lora_url will be replaced with real trained LoRA URLs once character sheets are finalized.
# trigger_word must match the token used during LoRA training.

PLACEHOLDER_LORA = "https://huggingface.co/alvdansen/frosting_lane_redux/resolve/main/fluxtest.safetensors"

CHARACTERS: dict[str, dict] = {
    # --- Child characters ---
    "asian_boy_child": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_asian_boy",
        "description": "young Asian boy, short black hair, light blue hoodie, navy blue shorts, gray sneakers",
    },
    "asian_girl_child": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_asian_girl",
        "description": "young Asian girl, black hair in pigtails, pink t-shirt, purple leggings, white sneakers",
    },
    "black_boy_child": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_black_boy",
        "description": "young Black boy, short curly black hair, yellow t-shirt, green shorts, white sneakers",
    },
    "black_girl_child": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_black_girl",
        "description": "young Black girl, natural curly black hair, orange dress, white sandals",
    },
    "hispanic_boy_child": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_hispanic_boy",
        "description": "young Hispanic boy, dark brown hair, teal shirt, khaki shorts, brown sneakers",
    },
    "hispanic_girl_child": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_hispanic_girl",
        "description": "young Hispanic girl, long dark brown hair, red top, blue jeans, red sneakers",
    },
    "white_boy_child": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_white_boy",
        "description": "young white boy, blond hair, green t-shirt, blue jeans, green sneakers",
    },
    "white_girl_child": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_white_girl",
        "description": "young white girl, wavy red hair, lavender dress, purple sneakers",
    },
    "south_asian_boy_child": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_south_asian_boy",
        "description": "young South Asian boy, straight black hair, blue striped shirt, gray pants, blue sneakers",
    },
    "south_asian_girl_child": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_south_asian_girl",
        "description": "young South Asian girl, long black hair, yellow kurta top, navy leggings, gold sandals",
    },
    "middle_eastern_boy_child": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_middle_eastern_boy",
        "description": "young Middle Eastern boy, dark wavy hair, white shirt, olive pants, brown shoes",
    },
    "middle_eastern_girl_child": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_middle_eastern_girl",
        "description": "young Middle Eastern girl, dark hair with light blue hijab, teal top, dark pants, white sneakers",
    },
    # --- Teen characters ---
    "asian_boy_teen": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_asian_teen_boy",
        "description": "teenage Asian boy, short black hair, dark blue hoodie, black jeans, white sneakers",
    },
    "asian_girl_teen": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_asian_teen_girl",
        "description": "teenage Asian girl, black hair in a ponytail, pink hoodie, light jeans, white sneakers",
    },
    "black_boy_teen": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_black_teen_boy",
        "description": "teenage Black boy, short fade haircut, gray hoodie, dark jeans, red sneakers",
    },
    "black_girl_teen": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_black_teen_girl",
        "description": "teenage Black girl, natural afro, purple jacket, black leggings, white sneakers",
    },
    "hispanic_boy_teen": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_hispanic_teen_boy",
        "description": "teenage Hispanic boy, medium-length dark hair, green bomber jacket, dark jeans, black shoes",
    },
    "hispanic_girl_teen": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_hispanic_teen_girl",
        "description": "teenage Hispanic girl, long dark wavy hair, orange sweater, blue jeans, white sneakers",
    },
    "white_boy_teen": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_white_teen_boy",
        "description": "teenage white boy, light brown hair, navy t-shirt, khaki pants, gray sneakers",
    },
    "white_girl_teen": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_white_teen_girl",
        "description": "teenage white girl, straight blond hair, light pink cardigan, white shirt, blue jeans, tan boots",
    },
    "south_asian_boy_teen": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_south_asian_teen_boy",
        "description": "teenage South Asian boy, dark hair, teal hoodie, black jeans, white sneakers",
    },
    "south_asian_girl_teen": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_south_asian_teen_girl",
        "description": "teenage South Asian girl, long black hair, purple hoodie, dark jeans, purple sneakers",
    },
    "middle_eastern_boy_teen": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_middle_eastern_teen_boy",
        "description": "teenage Middle Eastern boy, short dark hair, olive jacket, dark pants, brown boots",
    },
    "middle_eastern_girl_teen": {
        "lora_url": PLACEHOLDER_LORA,
        "trigger_word": "BIPCHAR_middle_eastern_teen_girl",
        "description": "teenage Middle Eastern girl, dark hair with navy blue hijab, teal jacket, dark jeans, white sneakers",
    },
}


def get_character(character_id: str) -> dict:
    character = CHARACTERS.get(character_id)
    if not character:
        raise ValueError(f"Unknown character_id: '{character_id}'. Valid IDs: {list(CHARACTERS.keys())}")
    return character
