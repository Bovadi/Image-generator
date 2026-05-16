module Characters
  PLACEHOLDER_LORA = nil # set to real URL during development if needed

  SOUTH_ASIAN_GIRL_CHILD_LORA = "https://v3b.fal.media/files/b/0a94ce41/4o-h-nA8AJA25YJcqjVTx_pytorch_lora_weights.safetensors"

  REGISTRY = {
    # ── Child characters ────────────────────────────────────────────────────
    "asian_boy_child" => {
      label:       "Asian Boy (Child)",
      gender:      "boy",
      age:         "child",
      trigger:     "BIPCHAR_asian_boy",
      description: "young Asian boy, short black hair, light blue hoodie, navy blue shorts, gray sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "asian_girl_child" => {
      label:       "Asian Girl (Child)",
      gender:      "girl",
      age:         "child",
      trigger:     "BIPCHAR_asian_girl",
      description: "young Asian girl, black hair in pigtails, pink t-shirt, purple leggings, white sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "black_boy_child" => {
      label:       "Black Boy (Child)",
      gender:      "boy",
      age:         "child",
      trigger:     "BIPCHAR_black_boy",
      description: "young Black boy, short curly black hair, yellow t-shirt, green shorts, white sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "black_girl_child" => {
      label:       "Black Girl (Child)",
      gender:      "girl",
      age:         "child",
      trigger:     "BIPCHAR_black_girl",
      description: "young Black girl, natural curly black hair, orange dress, white sandals",
      lora_url:    PLACEHOLDER_LORA,
    },
    "hispanic_boy_child" => {
      label:       "Hispanic Boy (Child)",
      gender:      "boy",
      age:         "child",
      trigger:     "BIPCHAR_hispanic_boy",
      description: "young Hispanic boy, dark brown hair, teal shirt, khaki shorts, brown sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "hispanic_girl_child" => {
      label:       "Hispanic Girl (Child)",
      gender:      "girl",
      age:         "child",
      trigger:     "BIPCHAR_hispanic_girl",
      description: "young Hispanic girl, long dark brown hair, red top, blue jeans, red sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "white_boy_child" => {
      label:       "White Boy (Child)",
      gender:      "boy",
      age:         "child",
      trigger:     "BIPCHAR_white_boy",
      description: "young white boy, blond hair, green t-shirt, blue jeans, green sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "white_girl_child" => {
      label:       "White Girl (Child)",
      gender:      "girl",
      age:         "child",
      trigger:     "BIPCHAR_white_girl",
      description: "young white girl, wavy red hair, lavender dress, purple sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "south_asian_boy_child" => {
      label:       "South Asian Boy (Child)",
      gender:      "boy",
      age:         "child",
      trigger:     "BIPCHAR_south_asian_boy",
      description: "young South Asian boy, straight black hair, blue striped shirt, gray pants, blue sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "south_asian_girl_child" => {
      label:       "South Asian Girl (Child)",
      gender:      "girl",
      age:         "child",
      trigger:     "BIPCHAR_south_asian_girl",
      description: "young South Asian girl, long black hair, peach t-shirt, khaki shorts, white sneakers",
      lora_url:    SOUTH_ASIAN_GIRL_CHILD_LORA,
    },
    "middle_eastern_boy_child" => {
      label:       "Middle Eastern Boy (Child)",
      gender:      "boy",
      age:         "child",
      trigger:     "BIPCHAR_middle_eastern_boy",
      description: "young Middle Eastern boy, dark wavy hair, white shirt, olive pants, brown shoes",
      lora_url:    PLACEHOLDER_LORA,
    },
    "middle_eastern_girl_child" => {
      label:       "Middle Eastern Girl (Child)",
      gender:      "girl",
      age:         "child",
      trigger:     "BIPCHAR_middle_eastern_girl",
      description: "young Middle Eastern girl, dark hair with light blue hijab, teal top, dark pants, white sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    # ── Teen characters ─────────────────────────────────────────────────────
    "asian_boy_teen" => {
      label:       "Asian Boy (Teen)",
      gender:      "boy",
      age:         "teen",
      trigger:     "BIPCHAR_asian_teen_boy",
      description: "teenage Asian boy, short black hair, dark blue hoodie, black jeans, white sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "asian_girl_teen" => {
      label:       "Asian Girl (Teen)",
      gender:      "girl",
      age:         "teen",
      trigger:     "BIPCHAR_asian_teen_girl",
      description: "teenage Asian girl, black hair in a ponytail, pink hoodie, light jeans, white sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "black_boy_teen" => {
      label:       "Black Boy (Teen)",
      gender:      "boy",
      age:         "teen",
      trigger:     "BIPCHAR_black_teen_boy",
      description: "teenage Black boy, short fade haircut, gray hoodie, dark jeans, red sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "black_girl_teen" => {
      label:       "Black Girl (Teen)",
      gender:      "girl",
      age:         "teen",
      trigger:     "BIPCHAR_black_teen_girl",
      description: "teenage Black girl, natural afro, purple jacket, black leggings, white sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "hispanic_boy_teen" => {
      label:       "Hispanic Boy (Teen)",
      gender:      "boy",
      age:         "teen",
      trigger:     "BIPCHAR_hispanic_teen_boy",
      description: "teenage Hispanic boy, medium-length dark hair, green bomber jacket, dark jeans, black shoes",
      lora_url:    PLACEHOLDER_LORA,
    },
    "hispanic_girl_teen" => {
      label:       "Hispanic Girl (Teen)",
      gender:      "girl",
      age:         "teen",
      trigger:     "BIPCHAR_hispanic_teen_girl",
      description: "teenage Hispanic girl, long dark wavy hair, orange sweater, blue jeans, white sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "white_boy_teen" => {
      label:       "White Boy (Teen)",
      gender:      "boy",
      age:         "teen",
      trigger:     "BIPCHAR_white_teen_boy",
      description: "teenage white boy, light brown hair, navy t-shirt, khaki pants, gray sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "white_girl_teen" => {
      label:       "White Girl (Teen)",
      gender:      "girl",
      age:         "teen",
      trigger:     "BIPCHAR_white_teen_girl",
      description: "teenage white girl, straight blond hair, light pink cardigan, white shirt, blue jeans, tan boots",
      lora_url:    PLACEHOLDER_LORA,
    },
    "south_asian_boy_teen" => {
      label:       "South Asian Boy (Teen)",
      gender:      "boy",
      age:         "teen",
      trigger:     "BIPCHAR_south_asian_teen_boy",
      description: "teenage South Asian boy, dark hair, teal hoodie, black jeans, white sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "south_asian_girl_teen" => {
      label:       "South Asian Girl (Teen)",
      gender:      "girl",
      age:         "teen",
      trigger:     "BIPCHAR_south_asian_teen_girl",
      description: "teenage South Asian girl, long black hair, purple hoodie, dark jeans, purple sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
    "middle_eastern_boy_teen" => {
      label:       "Middle Eastern Boy (Teen)",
      gender:      "boy",
      age:         "teen",
      trigger:     "BIPCHAR_middle_eastern_teen_boy",
      description: "teenage Middle Eastern boy, short dark hair, olive jacket, dark pants, brown boots",
      lora_url:    PLACEHOLDER_LORA,
    },
    "middle_eastern_girl_teen" => {
      label:       "Middle Eastern Girl (Teen)",
      gender:      "girl",
      age:         "teen",
      trigger:     "BIPCHAR_middle_eastern_teen_girl",
      description: "teenage Middle Eastern girl, dark hair with navy blue hijab, teal jacket, dark jeans, white sneakers",
      lora_url:    PLACEHOLDER_LORA,
    },
  }.freeze

  def self.exists?(id)
    REGISTRY.key?(id)
  end

  def self.find!(id)
    REGISTRY.fetch(id) { raise KeyError, "Unknown character_id: '#{id}'" }
  end

  def self.all
    REGISTRY
  end
end
