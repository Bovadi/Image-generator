class GenerationJob < ApplicationJob
  queue_as :default

  # Returns { image_url: } on success or { error: } on failure.
  # When callback_url is present, POSTs result there instead of returning.
  def perform(character_id, scenario, supporting, callback_url)
    fal_url   = FalService.generate(character_id, scenario, supporting)
    image_url = ENV["AWS_BUCKET_NAME"].present? ? S3Service.upload_from_url(fal_url) : fal_url
    result    = { status: "success", image_url: image_url }

    if callback_url.present?
      post_callback(callback_url, result)
    else
      result
    end
  rescue FalService::GenerationError => e
    Rails.logger.error("Generation failed for #{character_id}: #{e.message}")
    result = { status: "error", message: e.message }
    post_callback(callback_url, result) if callback_url.present?
    { error: e.message }
  rescue => e
    Rails.logger.error("Unexpected error for #{character_id}: #{e.message}")
    result = { status: "error", message: "Unexpected server error" }
    post_callback(callback_url, result) if callback_url.present?
    { error: e.message }
  end

  private

  def post_callback(url, payload)
    conn = Faraday.new do |f|
      f.request :json
      f.response :raise_error
    end
    conn.post(url, payload) do |req|
      req.headers["Authorization"] = "Bearer #{ENV.fetch('CALLBACK_BEARER_TOKEN')}"
      req.headers["Content-Type"]  = "application/json"
    end
  rescue => e
    Rails.logger.error("Callback POST to #{url} failed: #{e.message}")
  end
end
