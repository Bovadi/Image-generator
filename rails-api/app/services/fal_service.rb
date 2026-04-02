class FalService
  class GenerationError < StandardError; end

  FAL_MODEL     = "fal-ai/flux-lora"
  IMAGE_SIZE    = { width: 1024, height: 512 }.freeze
  MAX_ATTEMPTS  = 4
  BACKOFF       = [2, 4, 8].freeze

  STYLE_SUFFIX = "flat illustration style, clean lines, minimal shading, solid flat colors, " \
                 "educational illustration, child-friendly, friendly cartoon, " \
                 "full rectangular scene, edge to edge background, no text, no words"

  NEGATIVE_PROMPT = "realistic, photographic, 3D render, complex shading, dark, scary, violent, " \
                    "sexual, text, watermark, logo, holding hands, hand holding, " \
                    "vignette, oval mask, circular crop, blob background, faded edges, " \
                    "plain background, white background, gradient background"

  def self.generate(character_id, scenario, supporting = "")
    character = Characters.find!(character_id)
    prompt    = build_prompt(character, scenario, supporting)

    last_error = nil
    MAX_ATTEMPTS.times do |attempt|
      Rails.logger.info("fal.ai attempt #{attempt + 1} for character=#{character_id}")
      begin
        return call_fal(character, prompt)
      rescue => e
        last_error = e
        Rails.logger.warn("fal.ai attempt #{attempt + 1} failed: #{e.message}")
        sleep(BACKOFF[attempt]) if attempt < BACKOFF.length
      end
    end

    raise GenerationError, "All #{MAX_ATTEMPTS} attempts failed: #{last_error&.message}"
  end

  private

  def self.build_prompt(character, scenario, supporting)
    has_adult    = supporting.present? && !%w[none no n/a].include?(supporting.downcase.strip)
    adult_prefix = has_adult ? "scene includes a fully grown adult #{supporting}, adult body proportions, clearly taller than the child, mature facial features. " : ""
    solo_clause  = has_adult ? "" : ", only one child in the scene, no other people"

    "#{adult_prefix}#{character[:description]}, actively #{scenario}#{solo_clause}, " \
    "full body, dynamic action pose, full scene with walls floor and furniture visible. #{STYLE_SUFFIX}."
  end

  def self.call_fal(character, prompt)
    conn = Faraday.new("https://fal.run") do |f|
      f.request  :json
      f.response :json
      f.response :raise_error
    end

    body = {
      prompt:                prompt,
      negative_prompt:       NEGATIVE_PROMPT,
      image_size:            IMAGE_SIZE,
      num_inference_steps:   28,
      guidance_scale:        3.5,
      num_images:            1,
      enable_safety_checker: true
    }

    if character[:lora_url].present?
      body[:loras] = [{ path: character[:lora_url], scale: 1.0 }]
    end

    response = conn.post("/#{FAL_MODEL}", body) do |req|
      req.headers["Authorization"] = "Key #{ENV.fetch('FAL_KEY')}"
    end

    images = response.body.dig("images")
    raise GenerationError, "fal.ai returned no images" if images.blank?

    images.first["url"]
  end
end
